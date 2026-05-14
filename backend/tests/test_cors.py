"""
Teste do middleware CORS — Sprint 2.1.

Cobre o preflight `OPTIONS` com `Origin` permitido. Sem `Origin`, o
middleware não emite cabeçalho `Access-Control-Allow-Origin` — esse
caso é testado para garantir que não há vazamento permissivo.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_preflight_allows_configured_origin(client: TestClient) -> None:
    response = client.options(
        "/api/players",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )

    assert response.status_code in (200, 204)
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    allowed_methods = response.headers.get("access-control-allow-methods", "")
    assert "POST" in allowed_methods


def test_request_without_origin_has_no_cors_header(client: TestClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    # Sem header Origin, CORSMiddleware NÃO devolve allow-origin.
    assert "access-control-allow-origin" not in response.headers
