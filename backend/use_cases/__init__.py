"""
Use cases — orquestração de fluxos do backend Corporate Survivor.

Camada FINA entre routers e repositories. Pode consumir API pública da
engine (`from engine import ...`). NÃO contém regra de jogo nem cálculo
de score/final/consequência.
"""

from . import (
    catalog_loader,
    choice_use_cases,
    player_use_cases,
    ranking_use_cases,
    session_use_cases,
)

__all__ = [
    "catalog_loader",
    "choice_use_cases",
    "player_use_cases",
    "ranking_use_cases",
    "session_use_cases",
]
