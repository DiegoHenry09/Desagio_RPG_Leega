"""
API pública da game engine — Corporate Survivor.

O backend (FastAPI) consome apenas os símbolos exportados aqui.
Nada além desta interface deve ser importado diretamente pelo backend.
"""

from .engine import ApplyResult, apply_choice, resolve_ending, validate_events
from .endings import compute_score
from .types import (
    Attributes,
    Catalog,
    ChoiceRecord,
    Consequences,
    EarlyTrigger,
    EndingResult,
    Event,
    Option,
    State,
    UnlockCondition,
)

__all__ = [
    # Engine functions
    "validate_events",
    "apply_choice",
    "resolve_ending",
    "compute_score",
    # Result types
    "ApplyResult",
    "EndingResult",
    "EarlyTrigger",
    # State / catalog
    "State",
    "Attributes",
    "Catalog",
    "ChoiceRecord",
    # Event model
    "Event",
    "Option",
    "Consequences",
    "UnlockCondition",
]
