"""
Testes dos schemas Pydantic v2 — Sprint 2.1.

Cobre apenas casos não exercitados pelos testes de API (que já testam
422 nos endpoints): tipos básicos e edge cases de validação.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from schemas.players import PlayerCreate
from schemas.sessions import SessionCreate


def test_player_create_accepts_unicode_name() -> None:
    parsed = PlayerCreate(name="Adriana Cárdenas")
    assert parsed.name == "Adriana Cárdenas"


def test_player_create_strips_whitespace() -> None:
    parsed = PlayerCreate(name="   José   ")
    assert parsed.name == "José"


def test_player_create_rejects_whitespace_only() -> None:
    with pytest.raises(ValidationError):
        PlayerCreate(name="   ")


def test_player_create_rejects_64_plus_one() -> None:
    with pytest.raises(ValidationError):
        PlayerCreate(name="a" * 65)


def test_player_create_accepts_64_chars() -> None:
    parsed = PlayerCreate(name="a" * 64)
    assert len(parsed.name) == 64


def test_session_create_requires_positive_player_id() -> None:
    with pytest.raises(ValidationError):
        SessionCreate(player_id=0)

    with pytest.raises(ValidationError):
        SessionCreate(player_id=-1)


def test_session_create_forbids_extra_fields() -> None:
    with pytest.raises(ValidationError):
        SessionCreate(player_id=1, status="active")  # type: ignore[call-arg]
