"""
Testes de apply_choice — gatilhos antecipados, prioridade e fim de semana.
"""

from __future__ import annotations

from engine.engine import apply_choice
from engine.types import (
    Attributes,
    Catalog,
    Consequences,
    Event,
    Option,
    State,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _opt(opt_id: str, **deltas: int) -> Option:
    return Option(id=opt_id, label=f"Opção {opt_id}", consequences=Consequences(**deltas))


def _event(ev_id: str, day: int, seq: int, options: list[Option]) -> Event:
    return Event(
        id=ev_id,
        is_main=True,
        title=ev_id,
        scene="Cena.",
        options=tuple(options),
        day=day,
        sequence=seq,
    )


def _catalog_flat(attrs_per_option: dict[tuple[int, int], dict[str, int]] | None = None) -> Catalog:
    """
    Catálogo mínimo: 15 principais, sem secretos.
    attrs_per_option: {(day, seq): {atributo: delta}} para customizar consequências.
    """
    events = []
    for day in range(1, 6):
        for seq in range(1, 4):
            deltas = (attrs_per_option or {}).get((day, seq), {})
            events.append(
                _event(
                    f"ev_day{day}_00{seq}",
                    day,
                    seq,
                    [_opt("A", **deltas), _opt("B")],
                )
            )
    return Catalog(schema_version="1.0", events=tuple(events))


def _state(attrs: Attributes | None = None, day: int = 1, seq: int = 1) -> State:
    return State(
        current_day=day,
        current_sequence=seq,
        attributes=attrs or Attributes(),
    )


# ---------------------------------------------------------------------------
# Gatilho 1: reputacao <= 0 → demitido
# ---------------------------------------------------------------------------

class TestEarlyEndingReputacao:
    def test_reputacao_zero_triggers_demitido(self):
        catalog = _catalog_flat({(1, 1): {"reputacao": -5}})
        state = _state(Attributes(reputacao=5))
        result = apply_choice(state, catalog, "A")
        assert result.ending is not None
        assert result.ending.ending_id == "demitido"
        assert result.ending.trigger_name == "reputation_zero"
        assert result.state.is_finished

    def test_reputacao_one_does_not_trigger(self):
        catalog = _catalog_flat({(1, 1): {"reputacao": -4}})
        state = _state(Attributes(reputacao=5))
        result = apply_choice(state, catalog, "A")
        # reputacao = 5 - 4 = 1, ainda não disparou
        assert result.ending is None

    def test_reputacao_already_zero_triggers(self):
        catalog = _catalog_flat({(1, 1): {"reputacao": -1}})
        state = _state(Attributes(reputacao=1))
        result = apply_choice(state, catalog, "A")
        assert result.ending is not None
        assert result.ending.ending_id == "demitido"


# ---------------------------------------------------------------------------
# Gatilho 2: energia <= 0 → burnout
# ---------------------------------------------------------------------------

class TestEarlyEndingEnergia:
    def test_energia_zero_triggers_burnout(self):
        catalog = _catalog_flat({(1, 1): {"energia": -7}})
        state = _state(Attributes(energia=7))
        result = apply_choice(state, catalog, "A")
        assert result.ending is not None
        assert result.ending.ending_id == "burnout"
        assert result.ending.trigger_name == "energy_zero"

    def test_energia_one_does_not_trigger(self):
        catalog = _catalog_flat({(1, 1): {"energia": -6}})
        state = _state(Attributes(energia=7))
        result = apply_choice(state, catalog, "A")
        # energia = 7-6 = 1, não disparou
        assert result.ending is None


# ---------------------------------------------------------------------------
# Gatilho 3: ansiedade >= 10 → burnout
# ---------------------------------------------------------------------------

class TestEarlyEndingAnsiedade:
    def test_ansiedade_max_triggers_burnout(self):
        catalog = _catalog_flat({(1, 1): {"ansiedade": 7}})
        state = _state(Attributes(ansiedade=3))
        result = apply_choice(state, catalog, "A")
        assert result.ending is not None
        assert result.ending.ending_id == "burnout"
        assert result.ending.trigger_name == "anxiety_max"

    def test_ansiedade_nine_does_not_trigger(self):
        catalog = _catalog_flat({(1, 1): {"ansiedade": 6}})
        state = _state(Attributes(ansiedade=3))
        result = apply_choice(state, catalog, "A")
        # ansiedade = 3+6 = 9, não disparou
        assert result.ending is None

    def test_ansiedade_already_at_ten_triggers(self):
        # sem delta, mas ansiedade já está em 10
        catalog = _catalog_flat()
        state = _state(Attributes(ansiedade=10))
        result = apply_choice(state, catalog, "A")
        assert result.ending is not None
        assert result.ending.ending_id == "burnout"


# ---------------------------------------------------------------------------
# Prioridade dos gatilhos: reputacao > energia > ansiedade
# ---------------------------------------------------------------------------

class TestEarlyEndingPriority:
    def test_reputacao_beats_energia(self):
        """reputacao=0 E energia=0 ao mesmo tempo → deve registrar 'demitido', não 'burnout'."""
        catalog = _catalog_flat({(1, 1): {"reputacao": -5, "energia": -7}})
        state = _state(Attributes(reputacao=5, energia=7))
        result = apply_choice(state, catalog, "A")
        assert result.ending is not None
        assert result.ending.ending_id == "demitido"
        assert result.ending.trigger_name == "reputation_zero"

    def test_reputacao_beats_ansiedade(self):
        """reputacao=0 E ansiedade=10 → deve registrar 'demitido'."""
        catalog = _catalog_flat({(1, 1): {"reputacao": -5, "ansiedade": 7}})
        state = _state(Attributes(reputacao=5, ansiedade=3))
        result = apply_choice(state, catalog, "A")
        assert result.ending is not None
        assert result.ending.ending_id == "demitido"

    def test_energia_beats_ansiedade(self):
        """energia=0 E ansiedade=10 (sem reputacao=0) → deve registrar 'burnout' via 'energy_zero'."""
        # reputacao=5 (ok), energia=0, ansiedade=10
        catalog = _catalog_flat({(1, 1): {"energia": -7, "ansiedade": 7}})
        state = _state(Attributes(energia=7, ansiedade=3, reputacao=5))
        result = apply_choice(state, catalog, "A")
        assert result.ending is not None
        assert result.ending.ending_id == "burnout"
        assert result.ending.trigger_name == "energy_zero"


# ---------------------------------------------------------------------------
# Fim de semana normal
# ---------------------------------------------------------------------------

class TestEndOfWeek:
    def test_last_choice_resolves_ending(self):
        catalog = _catalog_flat()
        state = _state(day=5, seq=3)
        result = apply_choice(state, catalog, "A")
        assert result.ending is not None
        assert result.ending.trigger_name == ""  # fim de semana, não antecipado
        assert result.state.is_finished

    def test_game_continues_until_day5_seq3(self):
        catalog = _catalog_flat()
        state = _state(day=5, seq=2)
        result = apply_choice(state, catalog, "A")
        assert result.ending is None
        assert not result.state.is_finished


# ---------------------------------------------------------------------------
# Progressão de day/sequence
# ---------------------------------------------------------------------------

class TestProgression:
    def test_sequence_advances(self):
        catalog = _catalog_flat()
        state = _state(day=1, seq=1)
        result = apply_choice(state, catalog, "A")
        assert result.state.current_day == 1
        assert result.state.current_sequence == 2

    def test_day_advances_after_seq3(self):
        catalog = _catalog_flat()
        state = _state(day=2, seq=3)
        result = apply_choice(state, catalog, "A")
        assert result.state.current_day == 3
        assert result.state.current_sequence == 1


# ---------------------------------------------------------------------------
# Clamp
# ---------------------------------------------------------------------------

class TestClamp:
    def test_attribute_clamped_to_zero(self):
        catalog = _catalog_flat({(1, 1): {"energia": -10}})
        state = _state(Attributes(energia=3, reputacao=5))
        result = apply_choice(state, catalog, "A")
        # energia clampada a 0 → dispara burnout
        assert result.ending is not None
        assert result.ending.ending_id == "burnout"

    def test_attribute_clamped_to_ten(self):
        catalog = _catalog_flat({(1, 1): {"aprendizado": 10}})
        state = _state(Attributes(aprendizado=8))
        result = apply_choice(state, catalog, "A")
        assert result.state.attributes.aprendizado == 10

    def test_ansiedade_clamped_to_ten(self):
        catalog = _catalog_flat({(1, 1): {"ansiedade": 5}})
        state = _state(Attributes(ansiedade=9))
        result = apply_choice(state, catalog, "A")
        # ansiedade = 9+5 = 14 → clamp → 10 → dispara anxiety_max
        assert result.ending is not None
        assert result.ending.trigger_name == "anxiety_max"


# ---------------------------------------------------------------------------
# Opção inválida
# ---------------------------------------------------------------------------

class TestInvalidOption:
    def test_nonexistent_option_raises(self):
        import pytest
        catalog = _catalog_flat()
        state = _state()
        with pytest.raises(ValueError, match="Opção.*não existe"):
            apply_choice(state, catalog, "Z")
