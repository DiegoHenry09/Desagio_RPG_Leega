"""Testes de GET /api/players/{id}/profile e timeline de escolhas."""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.ranking_entry import RankingEntry
from repositories import (
    decision_repository,
    player_repository,
    ranking_repository,
    session_repository,
)


def test_player_profile_unknown_player_returns_404(client: TestClient) -> None:
    r = client.get("/api/players/999999/profile")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"


def test_player_profile_no_ranking_returns_empty_runs(
    client: TestClient, db: Session
) -> None:
    player = player_repository.create(db, name="SemHistorico")
    r = client.get(f"/api/players/{player.id}/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["player_id"] == player.id
    assert body["player_name"] == "SemHistorico"
    assert body["stats"] == {"games_played": 0, "best_score": None, "avg_score": None}
    assert body["ending_counts"] == {}
    assert body["runs"] == []


def test_player_profile_aggregates_two_runs(client: TestClient, db: Session) -> None:
    player = player_repository.create(db, name="DuasPartidas")
    s1 = session_repository.create(db, player_id=player.id)
    s2 = session_repository.create(db, player_id=player.id)
    ranking_repository.add(
        db,
        player_name=player.name,
        score=100,
        ending_id="sobrevivente",
        session_id=s1.id,
    )
    ranking_repository.add(
        db,
        player_name=player.name,
        score=250,
        ending_id="burnout",
        session_id=s2.id,
    )

    r = client.get(f"/api/players/{player.id}/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["stats"]["games_played"] == 2
    assert body["stats"]["best_score"] == 250
    assert body["stats"]["avg_score"] == 175.0
    assert body["ending_counts"] == {"burnout": 1, "sobrevivente": 1}
    assert len(body["runs"]) == 2
    scores = [run["score"] for run in body["runs"]]
    assert scores == [250, 100]


def test_player_run_choices_returns_timeline(client: TestClient, db: Session) -> None:
    player = player_repository.create(db, name="ComEscolhas")
    sess = session_repository.create(db, player_id=player.id)
    decision_repository.record(db, sess.id, "ev_day1_001", "A", 1, 1)
    decision_repository.record(db, sess.id, "ev_day1_002", "C", 1, 2)
    ranking_repository.add(
        db,
        player_name=player.name,
        score=99,
        ending_id="demitido",
        session_id=sess.id,
    )
    rid = db.execute(
        select(RankingEntry.id).where(RankingEntry.session_id == sess.id)
    ).scalar_one()

    r = client.get(f"/api/players/{player.id}/runs/{rid}/choices")
    assert r.status_code == 200
    payload = r.json()
    assert payload["ranking_entry_id"] == rid
    assert len(payload["choices"]) == 2
    assert payload["choices"][0]["event_id"] == "ev_day1_001"
    assert payload["choices"][0]["option_id"] == "A"
    assert payload["choices"][1]["event_id"] == "ev_day1_002"


def test_player_run_choices_wrong_player_returns_404(
    client: TestClient, db: Session
) -> None:
    p1 = player_repository.create(db, name="Dono")
    p2 = player_repository.create(db, name="Outro")
    sess = session_repository.create(db, player_id=p1.id)
    ranking_repository.add(
        db,
        player_name=p1.name,
        score=10,
        ending_id="demitido",
        session_id=sess.id,
    )
    rid = db.execute(
        select(RankingEntry.id).where(RankingEntry.session_id == sess.id)
    ).scalar_one()

    r = client.get(f"/api/players/{p2.id}/runs/{rid}/choices")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "not_found"
