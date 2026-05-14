"""
PlayerRepository — CRUD puro para Player.

Contrato: NÃO valida regex de nome (Sprint 2.1), NÃO normaliza, NÃO
implementa regra de jogo. Só persiste e lê.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.player import Player


def create(db: Session, name: str) -> Player:
    """Cria um novo Player e faz commit. Retorna a entidade com id preenchido."""
    player = Player(name=name)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def get(db: Session, player_id: int) -> Player | None:
    return db.get(Player, player_id)


def get_by_name(db: Session, name: str) -> Player | None:
    """Retorna o primeiro Player com este nome ou None.

    Não trata case/whitespace — quem chama decide a política. Backend
    "policy layer" (sprint futura) cuidará de normalização.
    """
    stmt = select(Player).where(Player.name == name).limit(1)
    return db.execute(stmt).scalar_one_or_none()
