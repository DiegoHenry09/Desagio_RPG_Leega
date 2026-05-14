"""
Carregador do `events.json` — Corporate Survivor backend.

Consome APENAS a API pública da engine via `from engine import ...`,
conforme `.cursor/rules/backend.mdc`. Não toca em internals da engine
e não duplica regra de jogo.

Comportamento:
  - `load_events_dict()` lê o arquivo de catálogo do disco como dict bruto.
  - `validate_or_raise()` roda `engine.validate_events()` e propaga ValueError.
  - `get_catalog()` parseia o dict em `engine.Catalog` (singleton lazy).
  - `reset_catalog_cache()` é exposto para uso em testes.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from engine import Catalog, validate_events

# Caminho do catálogo. Pode ser sobrescrito via env (útil para testes).
_DEFAULT_EVENTS_PATH = Path(__file__).resolve().parent.parent / "engine" / "data" / "events.json"


def _events_path() -> Path:
    override = os.environ.get("EVENTS_JSON_PATH")
    return Path(override) if override else _DEFAULT_EVENTS_PATH


def load_events_dict(path: Optional[Path] = None) -> dict:
    """Carrega o JSON do catálogo como dict bruto, sem validar."""
    target = path if path is not None else _events_path()
    with target.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_or_raise(data: Optional[dict] = None) -> dict:
    """Valida via engine.validate_events. Retorna o dict carregado."""
    payload = data if data is not None else load_events_dict()
    validate_events(payload)
    return payload


@lru_cache(maxsize=1)
def get_catalog() -> Catalog:
    """Singleton lazy do catálogo já validado.

    Em testes, chame `get_catalog.cache_clear()` antes de trocar o env
    `EVENTS_JSON_PATH`.
    """
    data = validate_or_raise()
    return Catalog.from_dict(data)


def reset_catalog_cache() -> None:
    """Helper para testes: descarta o singleton para próxima chamada recarregar."""
    get_catalog.cache_clear()
