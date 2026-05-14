"""
Use cases de Session — orquestração entre router, repositórios e catálogo.

Operações desta Sprint 2.1:
  - `create_session(db, payload)` cria sessão+atributos iniciais e
    materializa `current_event_id` chamando o catálogo (`day=1, seq=1`).
  - `get_session_snapshot(db, session_id)` monta um snapshot completo
    com atributos + evento atual (cena/opções) lido do catálogo.

NÃO chama `apply_choice` (Sprint 2.2). NÃO calcula score/ending.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from engine import Catalog, Event
from models.game_session import GameSession
from models.session_attributes import SessionAttributes
from repositories import (
    attributes_repository,
    player_repository,
    session_repository,
)
from schemas.sessions import SessionCreate

from .catalog_loader import get_catalog


@dataclass(frozen=True)
class SessionSnapshot:
    """Agregado para serialização — sessão + atributos + evento atual.

    O router converte isto em `SessionResponse` via `from_attributes`/build.
    """

    session: GameSession
    attributes: SessionAttributes
    current_event: Optional[Event]


def _current_event(catalog: Catalog, session: GameSession) -> Optional[Event]:
    if session.status != "active":
        return None
    return catalog.get_main(session.current_day, session.current_sequence)


def create_session(db: Session, payload: SessionCreate) -> SessionSnapshot:
    """Cria sessão para um Player existente."""
    player = player_repository.get(db, payload.player_id)
    if player is None:
        raise NotFoundError(
            f"Player {payload.player_id} não encontrado.",
            details={"player_id": payload.player_id},
        )

    session = session_repository.create(db, player_id=player.id)

    catalog = get_catalog()
    first_event = catalog.get_main(1, 1)
    if first_event is not None:
        session = session_repository.update_progress(
            db,
            session_id=session.id,
            current_day=session.current_day,
            current_sequence=session.current_sequence,
            current_event_id=first_event.id,
        )
        # update_progress retornou; se o catálogo ficou sem ev_day1_seq1, é
        # bug de catálogo capturado por validate_events no boot.

    attrs = attributes_repository.get(db, session.id)
    if attrs is None:
        # session_repository.create já cria SessionAttributes na MESMA
        # transação; este branch só dispara em bug grave do repo.
        raise NotFoundError(
            f"SessionAttributes ausente para session {session.id}.",
            details={"session_id": session.id},
        )

    return SessionSnapshot(
        session=session,
        attributes=attrs,
        current_event=_current_event(catalog, session),
    )


def get_session_snapshot(db: Session, session_id: int) -> SessionSnapshot:
    """Lê snapshot completo. 404 se sessão não existe."""
    session = session_repository.get(db, session_id)
    if session is None:
        raise NotFoundError(
            f"Session {session_id} não encontrada.",
            details={"session_id": session_id},
        )
    attrs = attributes_repository.get(db, session_id)
    if attrs is None:
        raise NotFoundError(
            f"SessionAttributes ausente para session {session_id}.",
            details={"session_id": session_id},
        )
    return SessionSnapshot(
        session=session,
        attributes=attrs,
        current_event=_current_event(get_catalog(), session),
    )
