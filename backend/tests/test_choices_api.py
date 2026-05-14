"""Testes de POST /api/sessions/{id}/choices — Sprint 2.2 (+2.2-B QA)."""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.decision import Decision
from models.ranking_entry import RankingEntry


def _mk_player_session(client: TestClient) -> tuple[int, int]:
    p = client.post("/api/players", json={"name": "RankingBot"})
    assert p.status_code == 201
    pid = p.json()["id"]
    s = client.post("/api/sessions", json={"player_id": pid})
    assert s.status_code == 201
    return pid, s.json()["id"]


def _post_choice(
    client: TestClient, session_id: int, event_id: str, opt: str
) -> tuple[int, dict]:
    r = client.post(
        f"/api/sessions/{session_id}/choices",
        json={"event_id": event_id, "option_id": opt},
    )
    return r.status_code, r.json()


def test_submit_choice_wrong_event_returns_409(client: TestClient) -> None:
    _, sid = _mk_player_session(client)
    code, body = _post_choice(
        client,
        sid,
        event_id="ev_day2_999",
        opt="A",
    )
    assert code == 409
    assert body["error"]["code"] == "conflict"


def test_submit_choice_invalid_option_returns_422(client: TestClient) -> None:
    _, sid = _mk_player_session(client)
    bad = client.post(
        f"/api/sessions/{sid}/choices",
        json={"event_id": "ev_day1_001", "option_id": "Z"},
    )
    assert bad.status_code == 422


def test_submit_choice_engine_rejects_returns_422(client: TestClient) -> None:
    """Opção ausente no evento atual → ValueError na engine."""
    _, sid = _mk_player_session(client)
    bogus = client.post(
        f"/api/sessions/{sid}/choices",
        json={"event_id": "ev_day1_001", "option_id": "D"},
    )
    assert bogus.status_code == 422
    body = bogus.json()
    assert body["error"]["code"] == "validation_error"


def test_submit_choice_advances_primary_events(client: TestClient) -> None:
    _, sid = _mk_player_session(client)
    code1, b1 = _post_choice(client, sid, "ev_day1_001", "A")
    assert code1 == 200
    assert b1["status"] == "active"
    assert b1["current_event_id"] == "ev_day1_002"
    assert b1["current_day"] == 1
    assert b1["current_sequence"] == 2
    assert b1["attributes"]["reputacao"] == 5
    opts = b1["current_event"]["options"]
    assert len(opts) >= 2
    for o in opts:
        assert set(o.keys()) <= {"id", "label"}


_GREEDY_PATH = [
    ("ev_day1_001", "A"),
    ("ev_day1_002", "A"),
    ("ev_day1_003", "C"),
    ("ev_day2_001", "C"),
    ("ev_day2_002", "C"),
    ("ev_day2_003", "C"),
    ("ev_day3_001", "C"),
]


def test_full_path_early_ending_creates_ranking_and_blocks_new_choices(
    client: TestClient, db: Session
) -> None:
    _, sid = _mk_player_session(client)

    prev_eid = client.get(f"/api/sessions/{sid}").json()["current_event_id"]
    for ev_id, opt in _GREEDY_PATH:
        assert prev_eid == ev_id
        code, row = _post_choice(client, sid, ev_id, opt)
        assert code == 200, row
        prev_eid = row.get("current_event_id")

    final = client.get(f"/api/sessions/{sid}").json()
    assert final["status"] == "finished"
    assert final["ending_id"] == "demitido"
    assert final["score"] == 49
    assert final["current_event"] is None

    count = db.execute(
        select(func.count()).select_from(RankingEntry).where(RankingEntry.session_id == sid)
    ).scalar_one()
    assert count == 1

    stale = client.post(
        f"/api/sessions/{sid}/choices",
        json={
            # body ignorado antes do 409, mas válido sintaticamente
            "event_id": "ev_day1_001",
            "option_id": "A",
        },
    )
    assert stale.status_code == 409


# ---------------------------------------------------------------------------
# Sprint 2.2-B — Correções QA (auditoria read-only da 2.2)
# ---------------------------------------------------------------------------


def test_submit_choice_session_not_found_returns_404(client: TestClient) -> None:
    """Ressalva QA #1 — POST /choices em session_id inexistente deve dar 404
    com envelope de erro padronizado (`error.code = "not_found"`)."""
    bogus_id = 99999  # nenhum Player/Sessão criado
    r = client.post(
        f"/api/sessions/{bogus_id}/choices",
        json={"event_id": "ev_day1_001", "option_id": "A"},
    )
    assert r.status_code == 404
    body = r.json()
    assert body["error"]["code"] == "not_found"
    assert body["error"]["details"]["session_id"] == bogus_id


def test_submit_choice_persists_decision_row(
    client: TestClient, db: Session
) -> None:
    """Ressalva QA #2 — após escolha válida, deve existir EXATAMENTE 1
    Decision gravada com session_id, event_id, option_id, day, sequence
    coerentes (coordenadas do evento RESPONDIDO, antes da engine avançar)."""
    _, sid = _mk_player_session(client)

    code, _ = _post_choice(client, sid, "ev_day1_001", "A")
    assert code == 200

    decisions = list(
        db.execute(
            select(Decision).where(Decision.session_id == sid).order_by(Decision.id.asc())
        )
        .scalars()
        .all()
    )
    assert len(decisions) == 1
    rec = decisions[0]
    assert rec.session_id == sid
    assert rec.event_id == "ev_day1_001"
    assert rec.option_id == "A"
    # Day/sequence persistidos = coordenadas do evento RESPONDIDO
    # (recorded_day/recorded_seq), conforme choice_use_cases.py linhas 116-117.
    assert rec.day == 1
    assert rec.sequence == 1


def test_ranking_count_zero_before_session_finishes(
    client: TestClient, db: Session
) -> None:
    """Ressalva QA #3 — RankingEntry SÓ é criada quando a sessão termina.
    Antes do final (durante turnos válidos numa sessão active), a contagem
    permanece 0."""
    _, sid = _mk_player_session(client)

    pre_count = db.execute(
        select(func.count())
        .select_from(RankingEntry)
        .where(RankingEntry.session_id == sid)
    ).scalar_one()
    assert pre_count == 0

    code, body = _post_choice(client, sid, "ev_day1_001", "A")
    assert code == 200
    assert body["status"] == "active"  # sessão ainda viva

    mid_count = db.execute(
        select(func.count())
        .select_from(RankingEntry)
        .where(RankingEntry.session_id == sid)
    ).scalar_one()
    assert mid_count == 0


def test_submit_choice_existing_event_but_not_current_returns_409(
    client: TestClient,
) -> None:
    """Ressalva QA #4 — `event_id` que existe no catálogo mas é diferente do
    `current_event_id` da sessão deve retornar 409 (mismatch). Distingue do
    teste pré-existente (`test_submit_choice_wrong_event_returns_409`) que
    usa um ID inexistente — aqui o ID é VÁLIDO no catálogo, só está fora de
    posição na progressão da sessão."""
    _, sid = _mk_player_session(client)

    # Sessão recém-criada está em ev_day1_001. Usamos ev_day1_002, que existe
    # no catálogo (próximo evento principal) mas ainda não é o atual.
    code, body = _post_choice(client, sid, "ev_day1_002", "A")
    assert code == 409
    assert body["error"]["code"] == "conflict"
    details = body["error"]["details"]
    assert details["session_id"] == sid
    assert details["expected_event_id"] == "ev_day1_001"
    assert details["received_event_id"] == "ev_day1_002"
