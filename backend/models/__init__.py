"""
Modelos SQLAlchemy do Corporate Survivor.

Importar este pacote registra todos os modelos no metadata da `Base` —
necessário antes de chamar `Base.metadata.create_all()`.

NÃO importar a engine aqui. Modelos são camada de persistência pura.
"""

from .decision import Decision
from .game_session import (
    SESSION_STATUS_ACTIVE,
    SESSION_STATUS_FINISHED,
    GameSession,
)
from .player import Player
from .ranking_entry import RankingEntry
from .session_attributes import SessionAttributes

__all__ = [
    "Decision",
    "GameSession",
    "Player",
    "RankingEntry",
    "SessionAttributes",
    "SESSION_STATUS_ACTIVE",
    "SESSION_STATUS_FINISHED",
]
