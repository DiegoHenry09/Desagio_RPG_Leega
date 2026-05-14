"""
Testes do endpoint POST /api/players — Sprint 2.1.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_create_player_returns_201_and_body(client: TestClient) -> None:
    response = client.post("/api/players", json={"name": "Alice"})

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["name"] == "Alice"
    assert "created_at" in body


def test_create_player_trims_name(client: TestClient) -> None:
    response = client.post("/api/players", json={"name": "  Bruno  "})

    assert response.status_code == 201
    assert response.json()["name"] == "Bruno"


def test_create_player_rejects_empty_name(client: TestClient) -> None:
    response = client.post("/api/players", json={"name": ""})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "validation_error"


def test_create_player_rejects_too_long_name(client: TestClient) -> None:
    response = client.post("/api/players", json={"name": "x" * 65})

    assert response.status_code == 422


def test_create_player_rejects_invalid_chars(client: TestClient) -> None:
    response = client.post("/api/players", json={"name": "<script>"})

    assert response.status_code == 422


def test_create_player_rejects_extra_fields(client: TestClient) -> None:
    response = client.post(
        "/api/players", json={"name": "Carla", "id": 999}
    )

    assert response.status_code == 422


def test_create_player_allows_duplicate_names(client: TestClient) -> None:
    """Decisão Sprint 2.1: nome NÃO é único — sempre cria novo Player."""
    first = client.post("/api/players", json={"name": "Duplo"})
    second = client.post("/api/players", json={"name": "Duplo"})

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]
    assert first.json()["name"] == second.json()["name"] == "Duplo"
