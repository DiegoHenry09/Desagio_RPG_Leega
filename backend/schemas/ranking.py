"""
Schemas Pydantic v2 para Ranking — API HTTP (Sprint 2.3).

Decisões de exposição:
  - `RankingEntryResponse` expõe `id`, `player_name`, `score`, `ending_id`,
    `created_at`. **NÃO** expõe `session_id` — é chave estrangeira interna
    e revelaria informação operacional (quantas sessões um jogador teve)
    sem necessidade para o produto público.
  - `RankingListResponse` é envelope `{ items, limit, count }`. Não usa
    cursor/offset (Sprint 2.3 implementa só limite, conforme escopo).
    Envelope é compatível com paginação futura sem quebrar o contrato.

NÃO importar `engine` — schemas são contrato HTTP, não estado do jogo.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RankingEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    player_name: str
    score: int
    ending_id: str
    created_at: datetime


class RankingListResponse(BaseModel):
    """Envelope de leitura do ranking global."""

    model_config = ConfigDict(from_attributes=False)

    items: list[RankingEntryResponse]
    limit: int
    count: int
