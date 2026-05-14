"""
SessionAttributes — atributos persistidos de uma sessão (1:1 com GameSession).

Defaults espelham os valores iniciais do jogo definidos em
`docs/02-product/game-rules.md` §1. ATENÇÃO: os defaults aqui são apenas
para o caso de criação manual da row sem passar valores; a engine continua
sendo a fonte da verdade sobre o estado oficial. Nada de clamp/regra aqui.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from .game_session import GameSession


class SessionAttributes(Base):
    __tablename__ = "session_attributes"

    session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("game_sessions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    energia: Mapped[int] = mapped_column(Integer, nullable=False, default=7)
    reputacao: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    networking: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    ansiedade: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    produtividade: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    aprendizado: Mapped[int] = mapped_column(Integer, nullable=False, default=4)

    session: Mapped["GameSession"] = relationship(back_populates="attributes")

    def to_dict(self) -> dict[str, int]:
        return {
            "energia": self.energia,
            "reputacao": self.reputacao,
            "networking": self.networking,
            "ansiedade": self.ansiedade,
            "produtividade": self.produtividade,
            "aprendizado": self.aprendizado,
        }

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"<SessionAttributes session_id={self.session_id} "
            f"e={self.energia} r={self.reputacao} n={self.networking} "
            f"ans={self.ansiedade} p={self.produtividade} a={self.aprendizado}>"
        )
