"""
Schemas HTTP — perfil público do jogador (histórico + agregados).

Somente leitura de dados já persistidos (ranking + decisões). Não importa engine.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PlayerProfileStats(BaseModel):
    """Agregados sobre partidas que geraram entrada no ranking (finalizadas)."""

    model_config = ConfigDict(from_attributes=False)

    games_played: int
    best_score: int | None
    avg_score: float | None


class PlayerRunItem(BaseModel):
    """Uma partida concluída (espelha uma linha de ranking)."""

    model_config = ConfigDict(from_attributes=False)

    ranking_entry_id: int
    score: int
    ending_id: str
    created_at: datetime
    choices_count: int


class PlayerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=False)

    player_id: int
    player_name: str
    stats: PlayerProfileStats
    ending_counts: dict[str, int]
    runs: list[PlayerRunItem]


class PlayerRunChoiceItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_id: str
    option_id: str
    day: int
    sequence: int
    created_at: datetime


class PlayerRunChoicesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=False)

    ranking_entry_id: int
    choices: list[PlayerRunChoiceItem]
