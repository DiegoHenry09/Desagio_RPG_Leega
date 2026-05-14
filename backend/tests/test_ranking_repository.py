"""
Testes de RankingRepository — Sprint 2.0.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from repositories import (
    player_repository,
    ranking_repository,
    session_repository,
)


def _session_id(db: Session, name: str = "Hugo") -> int:
    player = player_repository.create(db, name=name)
    return session_repository.create(db, player_id=player.id).id


def test_add_entry_persists_full_payload(db: Session) -> None:
    sid = _session_id(db)

    entry = ranking_repository.add(
        db,
        player_name="Hugo",
        score=551,
        ending_id="trainee_lenda",
        session_id=sid,
    )

    assert entry.id is not None
    assert entry.player_name == "Hugo"
    assert entry.score == 551
    assert entry.ending_id == "trainee_lenda"
    assert entry.session_id == sid


def test_top_n_orders_by_score_desc(db: Session) -> None:
    sid_a = _session_id(db, name="Ana")
    sid_b = _session_id(db, name="Bruno")
    sid_c = _session_id(db, name="Cris")

    ranking_repository.add(db, "Ana", 100, "sobrevivente", sid_a)
    ranking_repository.add(db, "Bruno", 551, "trainee_lenda", sid_b)
    ranking_repository.add(db, "Cris", 280, "sobrevivente", sid_c)

    top = ranking_repository.top_n(db, n=10)

    assert [e.score for e in top] == [551, 280, 100]
    assert [e.player_name for e in top] == ["Bruno", "Cris", "Ana"]


def test_top_n_limits_result(db: Session) -> None:
    base = _session_id(db, name="Base")
    for i in range(5):
        ranking_repository.add(db, f"P{i}", i * 10, "sobrevivente", base)

    top = ranking_repository.top_n(db, n=3)

    assert len(top) == 3
    assert [e.score for e in top] == [40, 30, 20]
