"""
Testes de PlayerRepository — Sprint 2.0.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from repositories import player_repository as repo


def test_create_player_persists_with_id_and_timestamp(db: Session) -> None:
    player = repo.create(db, name="Alice")

    assert player.id is not None
    assert player.name == "Alice"
    assert player.created_at is not None


def test_get_player_returns_persisted_entity(db: Session) -> None:
    created = repo.create(db, name="Bob")
    fetched = repo.get(db, created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == "Bob"


def test_get_player_missing_returns_none(db: Session) -> None:
    assert repo.get(db, 999) is None


def test_get_by_name_returns_match(db: Session) -> None:
    repo.create(db, name="Carla")
    repo.create(db, name="Daniel")

    found = repo.get_by_name(db, "Carla")
    assert found is not None
    assert found.name == "Carla"

    assert repo.get_by_name(db, "Inexistente") is None
