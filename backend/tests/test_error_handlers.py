"""
Testes dos handlers globais de erro — Sprint 2.1.

Os 422 (validação) e 404 (not_found) já são exercitados pelos testes
de players/sessions. Aqui cobrimos o shape geral do payload e o 500
genérico (sem stack).
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.error_handlers import register_error_handlers
from core.exceptions import ConflictError, DomainError, NotFoundError


def _isolated_app() -> FastAPI:
    """Mini-app só para exercitar os handlers fora do app principal."""
    app = FastAPI()
    register_error_handlers(app)

    @app.get("/boom/not_found")
    def boom_not_found() -> None:
        raise NotFoundError("alvo não existe", details={"id": 42})

    @app.get("/boom/conflict")
    def boom_conflict() -> None:
        raise ConflictError("estado inconsistente", details={"why": "current_event_id mismatch"})

    @app.get("/boom/domain_default")
    def boom_domain() -> None:
        raise DomainError("erro de domínio genérico")

    @app.get("/boom/unhandled")
    def boom_unhandled() -> None:
        raise RuntimeError("segredo do servidor que não deve vazar")

    return app


def test_not_found_handler_returns_404_payload() -> None:
    client = TestClient(_isolated_app(), raise_server_exceptions=False)

    response = client.get("/boom/not_found")

    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "not_found"
    assert body["error"]["message"] == "alvo não existe"
    assert body["error"]["details"] == {"id": 42}


def test_conflict_handler_returns_409_payload() -> None:
    client = TestClient(_isolated_app(), raise_server_exceptions=False)

    response = client.get("/boom/conflict")

    assert response.status_code == 409
    body = response.json()
    assert body["error"]["code"] == "conflict"


def test_domain_default_falls_to_500() -> None:
    client = TestClient(_isolated_app(), raise_server_exceptions=False)

    response = client.get("/boom/domain_default")

    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "internal_error"


def test_unhandled_exception_does_not_leak_stack() -> None:
    client = TestClient(_isolated_app(), raise_server_exceptions=False)

    response = client.get("/boom/unhandled")

    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "internal_error"
    assert body["error"]["message"] == "Erro interno do servidor."
    # Nada que mencione o segredo do servidor deve sair daqui.
    serialized = response.text
    assert "segredo do servidor" not in serialized
    assert "Traceback" not in serialized
