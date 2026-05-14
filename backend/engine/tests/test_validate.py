"""
Testes do validate_events — invariantes 1-11 (game-rules.md §4.3).
"""

from __future__ import annotations

import copy
import json
import pathlib

import pytest

from engine.engine import validate_events

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


def _load_placeholder() -> dict:
    with open(_DATA_DIR / "events.json", encoding="utf-8") as f:
        data = json.load(f)
    # Remove a chave "_comment" que não faz parte do schema real
    data.pop("_comment", None)
    return data


def _minimal_option(opt_id: str = "A") -> dict:
    return {"id": opt_id, "label": f"Opção {opt_id}", "consequences": {}}


def _make_main(ev_id: str, day: int, seq: int) -> dict:
    return {
        "id": ev_id,
        "isMain": True,
        "day": day,
        "sequence": seq,
        "title": f"Evento {ev_id}",
        "scene": "Cena.",
        "tags": [],
        "options": [_minimal_option("A"), _minimal_option("B")],
    }


def _make_secret(ev_id: str, unlock: dict) -> dict:
    return {
        "id": ev_id,
        "isMain": False,
        "day": None,
        "sequence": None,
        "title": f"Secreto {ev_id}",
        "scene": "Cena secreta.",
        "tags": [],
        "unlock": unlock,
        "options": [_minimal_option("A"), _minimal_option("B")],
    }


def _catalog_15_mains() -> dict:
    """Catálogo mínimo válido: 15 principais, sem secretos."""
    events = []
    for day in range(1, 6):
        for seq in range(1, 4):
            events.append(_make_main(f"ev_day{day}_00{seq}", day, seq))
    return {"schemaVersion": "1.0", "events": events}


# ---------------------------------------------------------------------------
# Invariante 1 — schemaVersion
# ---------------------------------------------------------------------------

class TestSchemaVersion:
    def test_valid_version(self):
        validate_events(_catalog_15_mains())

    def test_wrong_version(self):
        data = _catalog_15_mains()
        data["schemaVersion"] = "2.0"
        with pytest.raises(ValueError, match="schemaVersion"):
            validate_events(data)

    def test_missing_version(self):
        data = _catalog_15_mains()
        del data["schemaVersion"]
        with pytest.raises(ValueError, match="schemaVersion"):
            validate_events(data)


# ---------------------------------------------------------------------------
# Invariante 2 — 3 principais por dia × 5 dias
# ---------------------------------------------------------------------------

class TestMainEventsCount:
    def test_missing_one_event_in_day(self):
        data = _catalog_15_mains()
        data["events"] = [e for e in data["events"] if not (e["day"] == 3 and e["sequence"] == 2)]
        with pytest.raises(ValueError, match="Dia 3"):
            validate_events(data)

    def test_extra_event_in_day(self):
        data = _catalog_15_mains()
        extra = _make_main("ev_day2_extra", day=2, seq=2)
        extra["sequence"] = 2
        extra["id"] = "ev_day2_extra"
        data["events"].append(extra)
        with pytest.raises(ValueError, match="Dia 2"):
            validate_events(data)


# ---------------------------------------------------------------------------
# Invariante 3 — sequence cobre {1, 2, 3} sem repetição por dia
# ---------------------------------------------------------------------------

class TestSequences:
    def test_duplicate_sequence(self):
        data = _catalog_15_mains()
        # Troca o sequence=3 do dia 1 por sequence=1 (duplicado)
        for ev in data["events"]:
            if ev["day"] == 1 and ev["sequence"] == 3:
                ev["sequence"] = 1
                break
        with pytest.raises(ValueError, match="Dia 1"):
            validate_events(data)


# ---------------------------------------------------------------------------
# Invariante 4 — secretos: isMain=False, day=null, unlock presente
# ---------------------------------------------------------------------------

class TestSecrets:
    def _catalog_with_secret(self, secret_override: dict | None = None) -> dict:
        data = _catalog_15_mains()
        secret = _make_secret("ev_secret_001", {"min_attrs": {"reputacao": 7}})
        if secret_override:
            secret.update(secret_override)
        data["events"].append(secret)
        return data

    def test_valid_secret(self):
        validate_events(self._catalog_with_secret())

    def test_secret_with_day_not_null(self):
        data = self._catalog_with_secret({"day": 3})
        with pytest.raises(ValueError, match="day.*deve ser null"):
            validate_events(data)

    def test_secret_without_unlock(self):
        data = self._catalog_with_secret({"unlock": None})
        with pytest.raises(ValueError, match="unlock.*ausente"):
            validate_events(data)

    def test_secret_with_empty_unlock(self):
        data = self._catalog_with_secret({"unlock": {}})
        with pytest.raises(ValueError, match="nenhuma condição"):
            validate_events(data)


# ---------------------------------------------------------------------------
# Invariante 5 — referências de ID existem
# ---------------------------------------------------------------------------

class TestCrossReferences:
    def test_unlocks_nonexistent_id(self):
        data = _catalog_15_mains()
        data["events"][0]["options"][0]["unlocks"] = ["id_que_nao_existe"]
        with pytest.raises(ValueError, match="id_que_nao_existe"):
            validate_events(data)

    def test_blocks_nonexistent_id(self):
        data = _catalog_15_mains()
        data["events"][0]["options"][0]["blocks"] = ["outro_id_falso"]
        with pytest.raises(ValueError, match="outro_id_falso"):
            validate_events(data)


# ---------------------------------------------------------------------------
# Invariante 6 — 1-4 opções com IDs únicos em {A,B,C,D}
# ---------------------------------------------------------------------------

class TestOptions:
    def test_no_options(self):
        data = _catalog_15_mains()
        data["events"][0]["options"] = []
        with pytest.raises(ValueError, match="entre 1 e 4"):
            validate_events(data)

    def test_five_options(self):
        data = _catalog_15_mains()
        data["events"][0]["options"] = [_minimal_option(x) for x in ["A", "B", "C", "D", "A"]]
        with pytest.raises(ValueError):
            validate_events(data)

    def test_invalid_option_id(self):
        data = _catalog_15_mains()
        data["events"][0]["options"] = [{"id": "E", "label": "Opção E", "consequences": {}}]
        with pytest.raises(ValueError, match="IDs de opção inválidos"):
            validate_events(data)

    def test_duplicate_option_id(self):
        data = _catalog_15_mains()
        data["events"][0]["options"] = [_minimal_option("A"), _minimal_option("A")]
        with pytest.raises(ValueError, match="duplicados"):
            validate_events(data)


# ---------------------------------------------------------------------------
# Invariante 7 — soma absoluta dos deltas ≤ 7
# ---------------------------------------------------------------------------

class TestDeltaSum:
    def test_delta_sum_exactly_7(self):
        data = _catalog_15_mains()
        data["events"][0]["options"][0]["consequences"] = {"reputacao": 4, "aprendizado": 3}
        validate_events(data)  # 4+3 = 7, ok

    def test_delta_sum_8_fails(self):
        data = _catalog_15_mains()
        data["events"][0]["options"][0]["consequences"] = {"reputacao": 4, "aprendizado": 4}
        with pytest.raises(ValueError, match="soma absoluta"):
            validate_events(data)


# ---------------------------------------------------------------------------
# Invariante 8 — atributos válidos
# ---------------------------------------------------------------------------

class TestAttributeNames:
    def test_unknown_attribute(self):
        data = _catalog_15_mains()
        data["events"][0]["options"][0]["consequences"] = {"coragem": 2}
        with pytest.raises(ValueError, match="atributo desconhecido"):
            validate_events(data)


# ---------------------------------------------------------------------------
# Invariante 9 — sem auto-referência
# ---------------------------------------------------------------------------

class TestSelfReference:
    def test_event_unlocks_itself(self):
        data = _catalog_15_mains()
        ev = data["events"][0]
        ev["options"][0]["unlocks"] = [ev["id"]]
        with pytest.raises(ValueError, match="auto-referência"):
            validate_events(data)


# ---------------------------------------------------------------------------
# Invariante 10 — label não-vazio
# ---------------------------------------------------------------------------

class TestLabel:
    def test_empty_label(self):
        data = _catalog_15_mains()
        data["events"][0]["options"][0]["label"] = ""
        with pytest.raises(ValueError, match="label.*vazio"):
            validate_events(data)

    def test_whitespace_label(self):
        data = _catalog_15_mains()
        data["events"][0]["options"][0]["label"] = "   "
        with pytest.raises(ValueError, match="label.*vazio"):
            validate_events(data)


# ---------------------------------------------------------------------------
# Invariante 11 — IDs de finais antecipados no registry
# ---------------------------------------------------------------------------

class TestEarlyEndingIds:
    def test_registry_contains_demitido_and_burnout(self):
        """validate_events não deve lançar erro: demitido e burnout estão no registry."""
        validate_events(_catalog_15_mains())


# ---------------------------------------------------------------------------
# Placeholder real
# ---------------------------------------------------------------------------

class TestPlaceholderFile:
    def test_placeholder_passes_validation(self):
        """O events.json placeholder de Sprint 1.1 deve passar na validação."""
        data = _load_placeholder()
        validate_events(data)
