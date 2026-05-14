"""
Decision — histórico de cada escolha do jogador numa sessão.

Campos definidos pelo enunciado da Sprint 2.0:
    - id
    - session_id
    - event_id
    - option_id
    - day
    - sequence
    - created_at
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from .game_session import GameSession


class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("game_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    event_id: Mapped[str] = mapped_column(String(64), nullable=False)
    option_id: Mapped[str] = mapped_column(String(1), nullable=False)
    day: Mapped[int] = mapped_column(Integer, nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )

    session: Mapped["GameSession"] = relationship(back_populates="decisions")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<Decision id={self.id} session_id={self.session_id} "
            f"event_id={self.event_id} option={self.option_id} "
            f"day={self.day} seq={self.sequence}>"
        )
