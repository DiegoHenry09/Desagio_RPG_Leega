"""
Registry de finais — Corporate Survivor.

Finais de fim de semana: avaliados ao fim do dia 5, em ordem de prioridade decrescente.
Finais antecipados: avaliados pela engine após cada clamp (ver engine.py _check_early_ending).

Nenhum import de FastAPI, SQLAlchemy ou frontend.
"""

from __future__ import annotations

from typing import Callable

from .types import Attributes, EndingResult, State

# ---------------------------------------------------------------------------
# Tipos
# ---------------------------------------------------------------------------

PredicateFn = Callable[[Attributes], bool]


# ---------------------------------------------------------------------------
# Score
# ---------------------------------------------------------------------------

ATTR_WEIGHTS: dict[str, int] = {
    "reputacao": 12,
    "produtividade": 10,
    "aprendizado": 9,
    "networking": 8,
    "energia": 5,
    "ansiedade": -7,  # penaliza
}

ENDING_BONUS: dict[str, int] = {
    "trainee_lenda": 200,
    "promessa": 120,
    "sobrevivente": 60,
    "invisivel": 20,
    "risco_op": 0,
    "burnout": -50,
    "demitido": -100,
}


def compute_score(state: State, ending_id: str) -> int:
    attrs = state.attributes
    base = (
        attrs.reputacao * ATTR_WEIGHTS["reputacao"]
        + attrs.produtividade * ATTR_WEIGHTS["produtividade"]
        + attrs.aprendizado * ATTR_WEIGHTS["aprendizado"]
        + attrs.networking * ATTR_WEIGHTS["networking"]
        + attrs.energia * ATTR_WEIGHTS["energia"]
        + attrs.ansiedade * ATTR_WEIGHTS["ansiedade"]
    )
    bonus = ENDING_BONUS.get(ending_id, 0)
    completion = state.days_completed * 5
    return max(0, base + bonus + completion)


# ---------------------------------------------------------------------------
# Registry de finais de fim de semana
# ---------------------------------------------------------------------------

_ENDING_REGISTRY: list[tuple[str, int, PredicateFn]] = []


def register_ending(
    ending_id: str, priority: int
) -> Callable[[PredicateFn], PredicateFn]:
    """Decorator que registra um predicado de final avaliado ao fim do dia 5."""

    def decorator(fn: PredicateFn) -> PredicateFn:
        _ENDING_REGISTRY.append((ending_id, priority, fn))
        _ENDING_REGISTRY.sort(key=lambda t: t[1], reverse=True)
        return fn

    return decorator


def resolve_ending_from_registry(state: State) -> EndingResult:
    """
    Avalia os predicados em ordem de prioridade decrescente.
    Retorna o primeiro que retorna True.
    Sempre retorna algo (o fallback 'sobrevivente' tem predicado lambda: True).
    """
    attrs = state.attributes
    for ending_id, _priority, predicate in _ENDING_REGISTRY:
        if predicate(attrs):
            score = compute_score(state, ending_id)
            return EndingResult(ending_id=ending_id, score=score)
    # nunca deve chegar aqui se 'sobrevivente' estiver registrado
    score = compute_score(state, "sobrevivente")
    return EndingResult(ending_id="sobrevivente", score=score)


# ---------------------------------------------------------------------------
# Predicados dos 7 finais de fim de semana (ADR-010, game-rules.md §3)
# Avaliados APENAS ao fim do dia 5 — não são gatilhos antecipados.
# ---------------------------------------------------------------------------

@register_ending("demitido", priority=100)
def _demitido(attrs: Attributes) -> bool:
    return attrs.reputacao <= 1


@register_ending("burnout", priority=95)
def _burnout(attrs: Attributes) -> bool:
    return attrs.energia <= 1 and attrs.ansiedade >= 8


@register_ending("risco_op", priority=80)
def _risco_op(attrs: Attributes) -> bool:
    return attrs.produtividade <= 2 and attrs.reputacao <= 3


@register_ending("invisivel", priority=60)
def _invisivel(attrs: Attributes) -> bool:
    return attrs.networking <= 2 and attrs.reputacao <= 4 and attrs.aprendizado <= 4


@register_ending("trainee_lenda", priority=50)
def _trainee_lenda(attrs: Attributes) -> bool:
    return (
        attrs.reputacao >= 8
        and attrs.networking >= 7
        and attrs.aprendizado >= 7
        and attrs.produtividade >= 7
    )


@register_ending("promessa", priority=40)
def _promessa(attrs: Attributes) -> bool:
    return attrs.reputacao >= 6 and (attrs.aprendizado >= 6 or attrs.produtividade >= 7)


@register_ending("sobrevivente", priority=0)
def _sobrevivente(attrs: Attributes) -> bool:  # noqa: ARG001
    return True  # fallback


# ---------------------------------------------------------------------------
# Mapeamento de gatilhos antecipados → final (ADR-010)
# Ordem de prioridade: reputacao > energia > ansiedade
# ---------------------------------------------------------------------------

EARLY_TRIGGER_ENDINGS: dict[str, str] = {
    "reputation_zero": "demitido",
    "energy_zero": "burnout",
    "anxiety_max": "burnout",
}
