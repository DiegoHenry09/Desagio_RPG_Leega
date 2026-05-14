"""
Handlers globais de erro — Corporate Survivor backend.

Padroniza payloads de erro:
  {
    "error": {
      "code": "<error_code>",
      "message": "<mensagem segura>",
      "details": { ... opcional, sem stack ... }
    }
  }

Regras de segurança (alinhadas com `docs/02-product/architecture.md`):
  - Erros 500 NUNCA expõem stack trace ao cliente.
  - O log do servidor pode (e deve) registrar o stack — não é responsabilidade
    deste módulo configurar logging.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# HTTP status codes (literais) — evita acoplar à constante do Starlette,
# que está em meio à migração `HTTP_422_UNPROCESSABLE_ENTITY` →
# `HTTP_422_UNPROCESSABLE_CONTENT` (DeprecationWarning recente).
_HTTP_422 = 422
_HTTP_500 = 500

from .exceptions import (
    ConflictError,
    DomainError,
    DomainValidationError,
    NotFoundError,
)

if TYPE_CHECKING:
    from fastapi import FastAPI


def _payload(code: str, message: str, details: dict | None = None) -> dict:
    body: dict = {"error": {"code": code, "message": message}}
    if details:
        body["error"]["details"] = details
    return body


async def domain_error_handler(_: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_payload(exc.error_code, exc.message, exc.details or None),
    )


async def request_validation_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    # Pydantic v2 errors: lista de dicts com loc/msg/type. Sanitizamos para
    # não vazar objetos complexos.
    sanitized = [
        {
            "loc": list(err.get("loc", [])),
            "msg": err.get("msg", ""),
            "type": err.get("type", ""),
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=_HTTP_422,
        content=_payload(
            "validation_error",
            "Payload inválido.",
            {"errors": sanitized},
        ),
    )


async def unhandled_exception_handler(_: Request, __: Exception) -> JSONResponse:
    # 500 genérico sem stack. Detalhes vão para o log do servidor (quem
    # configura o logger é a aplicação, não o handler).
    return JSONResponse(
        status_code=_HTTP_500,
        content=_payload("internal_error", "Erro interno do servidor."),
    )


def register_error_handlers(app: "FastAPI") -> None:
    """Registra todos os handlers globais do backend na FastAPI app."""
    app.add_exception_handler(NotFoundError, domain_error_handler)
    app.add_exception_handler(ConflictError, domain_error_handler)
    app.add_exception_handler(DomainValidationError, domain_error_handler)
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
