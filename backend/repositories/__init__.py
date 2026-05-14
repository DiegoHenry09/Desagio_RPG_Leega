"""
Repositories — Corporate Survivor backend.

Cada submodule expõe funções module-style CRUD sobre SQLAlchemy.
"""

from . import attributes_repository
from . import decision_repository
from . import player_repository
from . import ranking_repository
from . import session_repository

__all__ = [
    "attributes_repository",
    "decision_repository",
    "player_repository",
    "ranking_repository",
    "session_repository",
]
