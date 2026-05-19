"""Testes de GET /api/ranking — Sprint 2.3.

Cobertura mínima exigida pela DoD da sprint:
  - ranking vazio devolve `{items:[], limit:10, count:0}`;
  - ordenação por score desc + tie-break determinístico;
  - default `limit=10`;
  - `limit` custom funciona;
  - `limit` fora dos bounds devolve 422 com envelope padrão;
  - resposta NÃO contém `session_id` (chave estrangeira interna);
  - smoke fim-a-fim: criar player → sessão → jogar caminho `demitido` via
    POST /choices → ranking expõe a entrada com `score=49`.
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from repositories import (
    player_repository,
    ranking_repository,
    session_repository,
)


# ---------------------------------------------------------------------------
# Helpers de setup
# ---------------------------------------------------------------------------


def _seed_ranking_via_repo(db: Session, entries: list[tuple[str, int, str]]) -> None:
    """Insere entradas de ranking diretamente via repository — útil para
    testes de leitura puros, sem precisar simular o jogo inteiro.

    `entries` é uma lista de `(player_name, score, ending_id)`. Cada entrada
    cria um Player + GameSession sintéticos (FK obrigatória em RankingEntry).
    """
    for name, score, ending_id in entries:
        player = player_repository.create(db, name=name)
        sess = session_repository.create(db, player_id=player.id)
        ranking_repository.add(
            db,
            player_name=name,
            score=score,
            ending_id=ending_id,
            session_id=sess.id,
        )


# ---------------------------------------------------------------------------
# Caminho feliz / leitura
# ---------------------------------------------------------------------------


def test_ranking_empty_returns_200_with_empty_envelope(client: TestClient) -> None:
    r = client.get("/api/ranking")
    assert r.status_code == 200
    body = r.json()
    assert body == {"items": [], "limit": 10, "count": 0}


def test_ranking_orders_by_score_desc(client: TestClient, db: Session) -> None:
    _seed_ranking_via_repo(
        db,
        [
            ("Ana", 100, "sobrevivente"),
            ("Bruno", 551, "trainee_lenda"),
            ("Cris", 280, "sobrevivente"),
        ],
    )

    body = client.get("/api/ranking").json()

    assert body["count"] == 3
    assert body["limit"] == 10
    scores = [item["score"] for item in body["items"]]
    names = [item["player_name"] for item in body["items"]]
    assert scores == [551, 280, 100]
    assert names == ["Bruno", "Cris", "Ana"]


def test_ranking_default_limit_is_ten(client: TestClient, db: Session) -> None:
    # Inserir 12 entradas — só as 10 maiores devem voltar
    entries = [(f"P{i:02d}", i * 10, "sobrevivente") for i in range(12)]
    _seed_ranking_via_repo(db, entries)

    body = client.get("/api/ranking").json()

    assert body["limit"] == 10
    assert body["count"] == 10
    assert len(body["items"]) == 10
    # Top scores: 110, 100, 90, ..., 20 (i=11 → 110, i=2 → 20)
    assert body["items"][0]["score"] == 110
    assert body["items"][-1]["score"] == 20


def test_ranking_respects_custom_limit(client: TestClient, db: Session) -> None:
    _seed_ranking_via_repo(
        db,
        [
            ("Ana", 100, "sobrevivente"),
            ("Bruno", 551, "trainee_lenda"),
            ("Cris", 280, "sobrevivente"),
        ],
    )

    body = client.get("/api/ranking?limit=2").json()

    assert body["limit"] == 2
    assert body["count"] == 2
    assert [item["score"] for item in body["items"]] == [551, 280]


def test_ranking_response_omits_session_id_field(
    client: TestClient, db: Session
) -> None:
    """RankingEntry tem `session_id` no banco mas o response público NÃO
    expõe — é chave estrangeira interna."""
    _seed_ranking_via_repo(db, [("Ana", 100, "sobrevivente")])

    body = client.get("/api/ranking").json()

    assert body["count"] == 1
    item = body["items"][0]
    assert set(item.keys()) == {
        "id",
        "player_id",
        "player_name",
        "score",
        "ending_id",
        "created_at",
    }
    assert "session_id" not in item


# ---------------------------------------------------------------------------
# Bounds / validação
# ---------------------------------------------------------------------------


def test_ranking_limit_zero_returns_422(client: TestClient) -> None:
    r = client.get("/api/ranking?limit=0")
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"


def test_ranking_limit_above_max_returns_422(client: TestClient) -> None:
    r = client.get("/api/ranking?limit=101")
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"


def test_ranking_limit_non_integer_returns_422(client: TestClient) -> None:
    r = client.get("/api/ranking?limit=abc")
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "validation_error"


# ---------------------------------------------------------------------------
# Smoke fim-a-fim: jogar até final antecipado e ver no ranking
# ---------------------------------------------------------------------------

# Caminho determinístico (replica `_GREEDY_PATH` de `test_choices_api.py`)
# até `demitido` com `score=49`, validado pela suíte da Sprint 2.2.
_GREEDY_PATH_TO_DEMITIDO = [
    ("ev_day1_001", "A"),
    ("ev_day1_002", "A"),
    ("ev_day1_003", "C"),
    ("ev_day2_001", "C"),
    ("ev_day2_002", "C"),
    ("ev_day2_003", "C"),
    ("ev_day3_001", "C"),
]


def test_ranking_smoke_end_to_end_finished_session_appears(
    client: TestClient,
) -> None:
    """Smoke: criar player → sessão → jogar até `demitido` → consultar ranking
    e verificar que a entrada aparece com `score=49`, `ending_id="demitido"`,
    `player_name` correto."""
    p = client.post("/api/players", json={"name": "SmokeRunner"})
    assert p.status_code == 201
    pid = p.json()["id"]

    s = client.post("/api/sessions", json={"player_id": pid})
    assert s.status_code == 201
    sid = s.json()["id"]

    for ev_id, opt in _GREEDY_PATH_TO_DEMITIDO:
        r = client.post(
            f"/api/sessions/{sid}/choices",
            json={"event_id": ev_id, "option_id": opt},
        )
        assert r.status_code == 200, r.json()

    final = client.get(f"/api/sessions/{sid}").json()
    assert final["status"] == "finished"
    assert final["ending_id"] == "demitido"
    assert final["score"] == 49

    body = client.get("/api/ranking").json()
    assert body["count"] == 1
    assert body["limit"] == 10

    item = body["items"][0]
    assert item["player_name"] == "SmokeRunner"
    assert item["score"] == 49
    assert item["ending_id"] == "demitido"
    assert isinstance(item["id"], int) and item["id"] > 0
    assert isinstance(item["created_at"], str)
    assert "session_id" not in item
