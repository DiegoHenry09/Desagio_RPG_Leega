"""
Routers HTTP — Corporate Survivor backend.

Routers são FINOS: apenas request/response e delegação a use cases.
Nada de regra de jogo, nada de acesso direto a repository.
"""

from . import players, ranking, sessions

__all__ = ["players", "ranking", "sessions"]
