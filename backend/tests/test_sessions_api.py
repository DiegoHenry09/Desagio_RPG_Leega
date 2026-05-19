"""
Testes dos endpoints de Session — Sprint 2.1.

POST /api/sessions: cria sessão para player existente, popula current_event_id.
GET  /api/sessions/{id}: retorna snapshot completo com atributos + evento atual.

`POST /choices` é coberto por `tests/test_choices_api.py` (Sprint 2.2).
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create_player(client: TestClient, name: str = "Eve") -> int:
    response = client.post("/api/players", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]


def test_create_session_returns_201_with_initial_state(client: TestClient) -> None:
    player_id = _create_player(client)

    response = client.post("/api/sessions", json={"player_id": player_id})

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["player_id"] == player_id
    assert body["player_name"] == "Eve"
    assert body["status"] == "active"
    assert body["current_day"] == 1
    assert body["current_sequence"] == 1
    assert body["current_event_id"] == "ev_day1_001"
    assert body["ending_id"] is None
    assert body["score"] is None
    assert body["finished_at"] is None

    attrs = body["attributes"]
    assert attrs == {
        "energia": 7,
        "reputacao": 5,
        "networking": 3,
        "ansiedade": 2,
        "produtividade": 5,
        "aprendizado": 4,
    }

    event = body["current_event"]
    assert event is not None
    assert event["id"] == "ev_day1_001"
    assert event["is_main"] is True
    assert event["day"] == 1
    assert event["sequence"] == 1
    assert event["title"]
    assert event["scene"]
    assert len(event["options"]) >= 2
    for opt in event["options"]:
        assert opt["id"] in {"A", "B", "C", "D"}
        assert opt["label"]


def test_create_session_returns_404_for_missing_player(client: TestClient) -> None:
    response = client.post("/api/sessions", json={"player_id": 99999})

    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "not_found"


def test_create_session_rejects_invalid_payload(client: TestClient) -> None:
    bad_player = client.post("/api/sessions", json={"player_id": 0})
    assert bad_player.status_code == 422

    no_body = client.post("/api/sessions", json={})
    assert no_body.status_code == 422

    extra_field = client.post(
        "/api/sessions", json={"player_id": 1, "current_day": 5}
    )
    assert extra_field.status_code == 422


def test_get_session_returns_snapshot(client: TestClient) -> None:
    player_id = _create_player(client, name="Fabio")
    created = client.post("/api/sessions", json={"player_id": player_id}).json()
    session_id = created["id"]

    response = client.get(f"/api/sessions/{session_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == session_id
    assert body["player_id"] == player_id
    assert body["player_name"] == "Fabio"
    assert body["current_event"]["id"] == "ev_day1_001"
    assert body["attributes"]["energia"] == 7


def test_get_session_includes_null_inject_secret_field(client: TestClient) -> None:
    """Campo sempre presente (null) garante contrato para clientes antes de POST choices."""
    player_id = _create_player(client)
    sid = (
        client.post("/api/sessions", json={"player_id": player_id}).json()["id"]
    )
    body = client.get(f"/api/sessions/{sid}").json()
    assert body.get("inject_secret_event") is None


def test_get_session_returns_404_when_missing(client: TestClient) -> None:
    response = client.get("/api/sessions/99999")

    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "not_found"
    assert "details" in body["error"]
    assert body["error"]["details"]["session_id"] == 99999


def test_get_session_returns_422_for_non_integer_id(client: TestClient) -> None:
    response = client.get("/api/sessions/abc")

    assert response.status_code == 422
