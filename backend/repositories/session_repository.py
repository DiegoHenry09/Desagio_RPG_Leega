"""
SessionRepository — CRUD puro para GameSession.

Contrato: NÃO calcula score, NÃO decide final, NÃO avança day/sequence
por conta própria. Recebe valores prontos vindos da engine via use case.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models.decision import Decision
from models.game_session import (
    SESSION_STATUS_ACTIVE,
    SESSION_STATUS_FINISHED,
    GameSession,
)
from models.ranking_entry import RankingEntry
from models.session_attributes import SessionAttributes

_ATTR_KEYS = (
    "energia",
    "reputacao",
    "networking",
    "ansiedade",
    "produtividade",
    "aprendizado",
)


def create(db: Session, player_id: int) -> GameSession:
    """Cria GameSession ativa e SessionAttributes iniciais na MESMA transação.

    Os defaults dos atributos vêm dos defaults do modelo
    (`SessionAttributes`), que espelham os valores iniciais do jogo
    definidos em `docs/02-product/game-rules.md` §1.
    """
    session = GameSession(
        player_id=player_id,
        status=SESSION_STATUS_ACTIVE,
        current_day=1,
        current_sequence=1,
    )
    db.add(session)
    db.flush()  # garante session.id antes de criar attributes

    attrs = SessionAttributes(session_id=session.id)
    db.add(attrs)

    db.commit()
    db.refresh(session)
    return session


def get(db: Session, session_id: int) -> GameSession | None:
    return db.get(GameSession, session_id)


def update_progress(
    db: Session,
    session_id: int,
    current_day: int,
    current_sequence: int,
    current_event_id: str | None,
) -> GameSession | None:
    """Persiste avanço de dia/sequência informados pela engine.

    Não valida transição (engine já fez). Repositório é CRUD.
    """
    session = db.get(GameSession, session_id)
    if session is None:
        return None
    session.current_day = current_day
    session.current_sequence = current_sequence
    session.current_event_id = current_event_id
    db.commit()
    db.refresh(session)
    return session


def finish(
    db: Session,
    session_id: int,
    ending_id: str,
    score: int,
) -> GameSession | None:
    """Marca sessão como finished com ending_id/score vindos da engine."""
    session = db.get(GameSession, session_id)
    if session is None:
        return None
    session.status = SESSION_STATUS_FINISHED
    session.ending_id = ending_id
    session.score = score
    session.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    db.refresh(session)
    return session


def persist_apply_choice_turn(
    db: Session,
    *,
    session_id: int,
    recorded_event_id: str,
    option_id: str,
    recorded_day: int,
    recorded_sequence: int,
    attrs: dict[str, int],
    secret_ids_seen: tuple[str, ...],
    finished: bool,
    current_day: int,
    current_sequence: int,
    current_event_id: str | None,
    ending_id: str | None,
    score: int | None,
    ranking_payload: tuple[str, int, str] | None,
) -> GameSession | None:
    """Persiste o resultado COMPLETO de um `apply_choice` em UMA transação.

    Não delega decisão ao ORM nem recalcula score — apenas grava valores
    passados pelo use case (onde a engine já decidiu tudo).

    `ranking_payload` é `(player_name, score, ending_id)` quando a sessão
    termina; caso contrário `None`.
    """
    session_row = db.get(GameSession, session_id)
    if session_row is None:
        return None
    attrs_row = db.get(SessionAttributes, session_id)
    if attrs_row is None:
        return None

    decision = Decision(
        session_id=session_id,
        event_id=recorded_event_id,
        option_id=option_id,
        day=recorded_day,
        sequence=recorded_sequence,
    )
    db.add(decision)

    for k in _ATTR_KEYS:
        setattr(attrs_row, k, attrs[k])

    session_row.secrets_seen_json = json.dumps(list(secret_ids_seen))

    session_row.current_day = current_day
    session_row.current_sequence = current_sequence
    session_row.current_event_id = current_event_id

    if finished and ending_id is not None and score is not None:
        session_row.status = SESSION_STATUS_FINISHED
        session_row.ending_id = ending_id
        session_row.score = score
        session_row.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
        if ranking_payload is not None:
            name, rk_score, rk_ending = ranking_payload
            db.add(
                RankingEntry(
                    player_name=name,
                    score=rk_score,
                    ending_id=rk_ending,
                    session_id=session_id,
                )
            )
    else:
        session_row.status = SESSION_STATUS_ACTIVE
        # Garante que colunas de fim não ficam poluídas se houver reprocessamento
        # anômalo (fluxo normal: sessão ativa nunca teve ending preenchido).
        session_row.ending_id = None
        session_row.score = None
        session_row.finished_at = None

    db.commit()
    db.refresh(session_row)
    db.refresh(attrs_row)
    return session_row
