"""
Schemas de erro — Corporate Survivor backend.

Espelha o payload produzido por `core/error_handlers.py`. Útil para
documentação OpenAPI e para clients tipados (frontend) consumirem.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ErrorBody(BaseModel):
    code: str
    message: str
    details: Optional[dict] = None


class ErrorResponse(BaseModel):
    error: ErrorBody
