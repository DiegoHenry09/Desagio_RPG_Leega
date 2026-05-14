"""
Use cases de escolhas — Sprint 2.2.

Orquestra `engine.apply_choice` e persiste resultado via
`session_repository.persist_apply_choice_turn` (uma transação por escolha).

Não replica regra de jogo da engine — apenas delega validação + transição.

Validações nesta camada:
  - sessão existe e está `active`;
  - `event_id` confere com `session.current_event_id`;
  - opção processável pela engine (ValueError da engine → erro HTTP coerente).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session as OrmSession

from core.exceptions import ConflictError, DomainValidationError, NotFoundError
from engine import Catalog, Event, State, apply_choice
from models.game_session import SESSION_STATUS_ACTIVE
from repositories import attributes_repository
from repositories import decision_repository as dec_repo
from repositories import player_repository as player_repo
from repositories import session_repository as session_repo

from .catalog_loader import get_catalog
from .session_state import hydrate_engine_state
from .session_use_cases import SessionSnapshot


@dataclass(frozen=True)
class ChoiceOutcome:
    snapshot: SessionSnapshot
    inject_secret_event: Optional[Event]


def _snapshot_after_persist(db: OrmSession, catalog: Catalog, session_id: int) -> SessionSnapshot:
    sess_row = session_repo.get(db, session_id)
    if sess_row is None:
        raise NotFoundError(
            "Sessão desapareceu após persistência (BUG).",
            details={"session_id": session_id},
        )
    attrs_row = attributes_repository.get(db, session_id)
    if attrs_row is None:
        raise NotFoundError(
            f"SessionAttributes ausente para session {session_id}.",
            details={"session_id": session_id},
        )

    if sess_row.status == SESSION_STATUS_ACTIVE:
        ce = catalog.get_main(sess_row.current_day, sess_row.current_sequence)
    else:
        ce = None

    return SessionSnapshot(
        session=sess_row,
        attributes=attrs_row,
        current_event=ce,
    )


def apply_session_choice(
    db: OrmSession,
    session_id: int,
    *,
    event_id: str,
    option_id: str,
) -> ChoiceOutcome:
    catalog = get_catalog()

    sess_row = session_repo.get(db, session_id)
    if sess_row is None:
        raise NotFoundError(
            f"Session {session_id} não encontrada.",
            details={"session_id": session_id},
        )

    if sess_row.status != SESSION_STATUS_ACTIVE:
        raise ConflictError(
            "Sessão não está ativa.",
            details={"session_id": session_id, "status": sess_row.status},
        )

    attrs_row = attributes_repository.get(db, session_id)
    if attrs_row is None:
        raise NotFoundError(
            f"SessionAttributes ausente para session {session_id}.",
            details={"session_id": session_id},
        )

    if sess_row.current_event_id != event_id:
        raise ConflictError(
            "`event_id` não corresponde ao evento atual da sessão.",
            details={
                "session_id": session_id,
                "expected_event_id": sess_row.current_event_id,
                "received_event_id": event_id,
            },
        )

    decisions = dec_repo.list_by_session(db, session_id)
    state = hydrate_engine_state(sess_row, attrs_row, ordered_decisions=decisions)

    if state.is_finished:
        raise ConflictError(
            "Estado interno inconsistênte: sessão marcada active mas.engine finished.",
            details={"session_id": session_id},
        )

    # Coordenadas do evento sendo respondido (antes da engine avançar)
    recorded_day = sess_row.current_day
    recorded_seq = sess_row.current_sequence

    try:
        result = apply_choice(state, catalog, option_id.strip())
    except ValueError as exc:
        msg = str(exc)
        raise DomainValidationError(
            msg,
            details={"session_id": session_id, "event_id": event_id},
        ) from exc

    new_state: State = result.state
    finished = result.ending is not None

    ranking_payload: tuple[str, int, str] | None = None
    if finished:
        ending = result.ending
        assert ending is not None
        player = player_repo.get(db, sess_row.player_id)
        if player is None:
            raise NotFoundError(
                f"Player {sess_row.player_id} não encontrado.",
                details={"player_id": sess_row.player_id},
            )
        ranking_payload = (player.name, ending.score, ending.ending_id)

    current_event_id: str | None
    if finished:
        main_at_cursor = catalog.get_main(new_state.current_day, new_state.current_sequence)
        current_event_id = main_at_cursor.id if main_at_cursor is not None else event_id
        next_day = new_state.current_day
        next_seq = new_state.current_sequence
        ending_id_fin = result.ending.ending_id if result.ending else None
        score_fin = result.ending.score if result.ending else None
        assert ending_id_fin is not None and score_fin is not None
    else:
        main_next = catalog.get_main(new_state.current_day, new_state.current_sequence)
        current_event_id = main_next.id if main_next is not None else None
        next_day = new_state.current_day
        next_seq = new_state.current_sequence
        ending_id_fin = None
        score_fin = None

    updated = session_repo.persist_apply_choice_turn(
        db,
        session_id=session_id,
        recorded_event_id=event_id,
        option_id=option_id.strip(),
        recorded_day=recorded_day,
        recorded_sequence=recorded_seq,
        attrs=new_state.attributes.to_dict(),
        secret_ids_seen=new_state.secret_ids_seen,
        finished=finished,
        current_day=next_day,
        current_sequence=next_seq,
        current_event_id=current_event_id,
        ending_id=ending_id_fin,
        score=score_fin,
        ranking_payload=ranking_payload,
    )
    if updated is None:
        raise NotFoundError(
            "Falha inesperada ao persistir a sessão após aplicar escolha.",
            details={"session_id": session_id},
        )

    snap = _snapshot_after_persist(db, catalog, session_id)
    return ChoiceOutcome(
        snapshot=snap,
        inject_secret_event=None if finished else result.secret_event,
    )
