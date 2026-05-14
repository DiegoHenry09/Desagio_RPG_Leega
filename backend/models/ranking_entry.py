"""
RankingEntry — entrada do ranking global persistido.

Campos definidos pelo enunciado da Sprint 2.0:
    - id
    - player_name
    - score
    - ending_id
    - session_id
    - created_at

NOTA DE GOVERNANÇA: o score gravado aqui é o calculado pela engine
(`compute_score` em `backend/engine/endings.py`). Esta tabela só persiste
o valor recebido — não recalcula.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from .game_session import GameSession


class RankingEntry(Base):
    __tablename__ = "ranking_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_name: Mapped[str] = mapped_column(String(64), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    ending_id: Mapped[str] = mapped_column(String(32), nullable=False)
    session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("game_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )

    session: Mapped["GameSession"] = relationship()

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<RankingEntry id={self.id} player={self.player_name!r} "
            f"score={self.score} ending={self.ending_id}>"
        )
