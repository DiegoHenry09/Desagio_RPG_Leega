"""
Testes do setup do banco — Sprint 2.0.

Verifica que `init_db()` cria todas as 5 tabelas esperadas e que a base
declarativa enxerga os 5 modelos.
"""

from __future__ import annotations

from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from db.base import Base
from db.init_db import init_db


EXPECTED_TABLES = {
    "players",
    "game_sessions",
    "session_attributes",
    "decisions",
    "ranking_entries",
}


def test_metadata_contains_all_five_tables() -> None:
    assert EXPECTED_TABLES.issubset(set(Base.metadata.tables.keys()))


def test_init_db_creates_all_tables(engine_test: Engine) -> None:
    init_db(bind=engine_test)
    inspector = inspect(engine_test)
    assert EXPECTED_TABLES.issubset(set(inspector.get_table_names()))


def test_init_db_is_idempotent(engine_test: Engine) -> None:
    init_db(bind=engine_test)
    init_db(bind=engine_test)
    inspector = inspect(engine_test)
    assert EXPECTED_TABLES.issubset(set(inspector.get_table_names()))
