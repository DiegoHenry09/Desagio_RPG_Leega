"""
Testes do catalog_loader — Sprint 2.1.

Valida que:
  - O catálogo padrão (`backend/engine/data/events.json`) é carregado
    e passa em `engine.validate_events`.
  - `get_catalog()` é singleton (cache_clear funciona).
  - Falha de validação propaga ValueError.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from engine import Catalog
from use_cases.catalog_loader import (
    get_catalog,
    load_events_dict,
    reset_catalog_cache,
    validate_or_raise,
)


def test_load_events_dict_returns_schema_v1() -> None:
    data = load_events_dict()
    assert data["schemaVersion"] == "1.0"
    assert "events" in data


def test_validate_or_raise_accepts_real_catalog() -> None:
    data = validate_or_raise()
    assert isinstance(data, dict)


def test_get_catalog_returns_catalog_instance() -> None:
    reset_catalog_cache()
    cat = get_catalog()
    assert isinstance(cat, Catalog)
    # 15 principais + 2 secretos = 17 eventos.
    assert len(cat.events) == 17
    assert cat.get_main(1, 1) is not None


def test_get_catalog_is_cached() -> None:
    reset_catalog_cache()
    first = get_catalog()
    second = get_catalog()
    assert first is second


def test_validate_or_raise_rejects_broken_dict() -> None:
    broken = {"schemaVersion": "9.9", "events": []}
    with pytest.raises(ValueError):
        validate_or_raise(broken)


def test_validate_or_raise_rejects_via_env_override(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Cria um events.json inválido e aponta EVENTS_JSON_PATH para ele.
    bad = tmp_path / "events.json"
    bad.write_text(json.dumps({"schemaVersion": "1.0", "events": []}))
    monkeypatch.setenv("EVENTS_JSON_PATH", str(bad))
    reset_catalog_cache()
    with pytest.raises(ValueError):
        validate_or_raise()
    reset_catalog_cache()  # limpa para próximos testes
