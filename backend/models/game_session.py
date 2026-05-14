"""
GameSession — modelo de uma sessão de jogo de um jogador.

Campos definidos pelo enunciado da Sprint 2.0:
    - id
    - player_id
    - status: active/finished
    - current_day
    - current_sequence
    - current_event_id
    - ending_id nullable
    - score nullable
    - created_at
    - updated_at
    - finished_at nullable

NOTA DE GOVERNANÇA: este modelo apenas **persiste** estado. A engine
(`backend/engine/`) é quem decide finais, score e progressão. O backend
chama a engine, recebe o novo estado e grava aqui. Esta camada não calcula.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from .decision import Decision
    from .player import Player
    from .session_attributes import SessionAttributes


SESSION_STATUS_ACTIVE = "active"
SESSION_STATUS_FINISHED = "finished"


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("players.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default=SESSION_STATUS_ACTIVE
    )
    current_day: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    current_sequence: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    current_event_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    #: JSON-serialização de lista de IDs de eventos secretos já marcados como
    #: vistos pela engine (`State.secret_ids_seen`). Necessário para reidratar
    #: estado entre requests — secreto pode ser marcado sem `Decision`.
    #: Sprint 2.2 — formato `["ev_secret_xyz", ...]`.
    secrets_seen_json: Mapped[str] = mapped_column(
        String(4096),
        nullable=False,
        default="[]",
        server_default="[]",
    )
    ending_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    player: Mapped["Player"] = relationship(back_populates="sessions")
    attributes: Mapped[Optional["SessionAttributes"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )
    decisions: Mapped[list["Decision"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="Decision.id",
        lazy="selectin",
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<GameSession id={self.id} player_id={self.player_id} "
            f"status={self.status} day={self.current_day} seq={self.current_sequence}>"
        )
