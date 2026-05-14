"""
Testes de DecisionRepository — Sprint 2.0.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from repositories import (
    decision_repository,
    player_repository,
    session_repository,
)


def _session_id(db: Session) -> int:
    player = player_repository.create(db, name="Gabi")
    return session_repository.create(db, player_id=player.id).id


def test_record_persists_decision(db: Session) -> None:
    sid = _session_id(db)

    decision = decision_repository.record(
        db,
        session_id=sid,
        event_id="ev_day1_001",
        option_id="A",
        day=1,
        sequence=1,
    )

    assert decision.id is not None
    assert decision.session_id == sid
    assert decision.event_id == "ev_day1_001"
    assert decision.option_id == "A"
    assert decision.day == 1
    assert decision.sequence == 1
    assert decision.created_at is not None


def test_list_by_session_returns_in_insertion_order(db: Session) -> None:
    sid = _session_id(db)

    decision_repository.record(
        db, session_id=sid, event_id="ev_day1_001", option_id="A", day=1, sequence=1
    )
    decision_repository.record(
        db, session_id=sid, event_id="ev_day1_002", option_id="B", day=1, sequence=2
    )
    decision_repository.record(
        db, session_id=sid, event_id="ev_day1_003", option_id="C", day=1, sequence=3
    )

    history = decision_repository.list_by_session(db, sid)

    assert len(history) == 3
    assert [d.event_id for d in history] == [
        "ev_day1_001",
        "ev_day1_002",
        "ev_day1_003",
    ]
    assert [d.option_id for d in history] == ["A", "B", "C"]


def test_list_by_session_empty_returns_empty_list(db: Session) -> None:
    sid = _session_id(db)
    assert decision_repository.list_by_session(db, sid) == []
