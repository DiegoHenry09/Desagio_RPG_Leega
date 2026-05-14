"""
Infra transversal do backend — settings, exceções e handlers.

Não conhece regra de jogo. Não importa engine.
"""

from .config import Settings, get_settings
from .error_handlers import register_error_handlers
from .exceptions import (
    ConflictError,
    DomainError,
    DomainValidationError,
    NotFoundError,
)

__all__ = [
    "ConflictError",
    "DomainError",
    "DomainValidationError",
    "NotFoundError",
    "Settings",
    "get_settings",
    "register_error_handlers",
]
