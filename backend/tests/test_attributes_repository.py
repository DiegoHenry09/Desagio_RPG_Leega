"""
Testes de AttributesRepository — Sprint 2.0.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from repositories import (
    attributes_repository,
    player_repository,
    session_repository,
)


def _session_id(db: Session) -> int:
    player = player_repository.create(db, name="Fabio")
    return session_repository.create(db, player_id=player.id).id


def test_get_attributes_returns_initial_state(db: Session) -> None:
    sid = _session_id(db)

    attrs = attributes_repository.get(db, sid)

    assert attrs is not None
    assert attrs.to_dict() == {
        "energia": 7,
        "reputacao": 5,
        "networking": 3,
        "ansiedade": 2,
        "produtividade": 5,
        "aprendizado": 4,
    }


def test_update_attributes_replaces_only_passed_keys(db: Session) -> None:
    sid = _session_id(db)

    updated = attributes_repository.update(
        db, sid, {"energia": 4, "ansiedade": 6}
    )

    assert updated is not None
    assert updated.energia == 4
    assert updated.ansiedade == 6
    # Outros atributos permanecem inalterados:
    assert updated.reputacao == 5
    assert updated.networking == 3
    assert updated.produtividade == 5
    assert updated.aprendizado == 4


def test_update_attributes_ignores_unknown_keys(db: Session) -> None:
    sid = _session_id(db)

    updated = attributes_repository.update(
        db, sid, {"energia": 9, "atributo_inexistente": 42}
    )

    assert updated is not None
    assert updated.energia == 9


def test_update_attributes_missing_session_returns_none(db: Session) -> None:
    assert attributes_repository.update(db, 999, {"energia": 1}) is None
