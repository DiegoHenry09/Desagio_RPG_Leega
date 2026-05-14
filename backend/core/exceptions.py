"""
Exceções de domínio — Corporate Survivor backend.

Camadas (use_cases, repositories) lançam estas; handlers em
`core/error_handlers.py` convertem em HTTPException com payload uniforme.

NÃO importar fastapi aqui — exceções são domínio puro do backend.
"""

from __future__ import annotations


class DomainError(Exception):
    """Base de erros previsíveis do domínio do backend.

    Subclasses devem mapear naturalmente para códigos HTTP via handlers.
    """

    status_code: int = 500
    error_code: str = "internal_error"

    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotFoundError(DomainError):
    status_code = 404
    error_code = "not_found"


class ConflictError(DomainError):
    """Estado inconsistente — ex.: `event_id` enviado não bate com `current_event_id`."""

    status_code = 409
    error_code = "conflict"


class DomainValidationError(DomainError):
    """Validação que escapa do Pydantic (ex.: campo válido mas semanticamente errado)."""

    status_code = 422
    error_code = "validation_error"
