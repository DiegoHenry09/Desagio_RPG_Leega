"""
Use cases de Ranking — Sprint 2.3.

Camada FINA entre router e repository:
  - `list_top_ranking(db, limit)` lê as top-N entradas via
    `ranking_repository.top_n` (ordenação `score desc, created_at asc, id asc`
    já garantida pelo repository — Sprint 2.0).

NÃO calcula score, NÃO recalcula ordenação, NÃO importa engine.
NÃO contém regra de jogo. Apenas leitura.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from models.ranking_entry import RankingEntry
from repositories import ranking_repository


def list_top_ranking(db: Session, *, limit: int) -> list[RankingEntry]:
    """Retorna as top-`limit` entradas do ranking global.

    Bounds de `limit` são responsabilidade da camada de transporte (Query
    do FastAPI). Aqui assumimos `limit` já validado.
    """
    return ranking_repository.top_n(db, n=limit)
