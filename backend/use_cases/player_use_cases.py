"""
Use cases de Player — orquestração fina entre router e repositório.

NÃO contém regra de jogo. Validação semântica (nome, tamanho, regex)
acontece nos schemas Pydantic; aqui resolvemos lookups e mapeamentos.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from models.player import Player
from repositories import player_repository
from schemas.players import PlayerCreate


def create_player(db: Session, payload: PlayerCreate) -> Player:
    """Cria um Player sempre novo.

    Decisão Sprint 2.1: nome NÃO é único — múltiplos Players podem ter
    o mesmo nome humano. Idempotência por nome NÃO é garantida nem
    pretendida (alinhado com ranking global que comporta entradas
    repetidas).
    """
    return player_repository.create(db, name=payload.name)


def get_player(db: Session, player_id: int) -> Player:
    """Retorna Player ou lança NotFoundError."""
    player = player_repository.get(db, player_id)
    if player is None:
        raise NotFoundError(
            f"Player {player_id} não encontrado.",
            details={"player_id": player_id},
        )
    return player
