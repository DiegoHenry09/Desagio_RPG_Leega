"""
Testes de SessionRepository — Sprint 2.0.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from models.game_session import SESSION_STATUS_ACTIVE, SESSION_STATUS_FINISHED
from repositories import player_repository, session_repository


def _player(db: Session, name: str = "Eve") -> int:
    return player_repository.create(db, name=name).id


def test_create_session_creates_attributes_with_defaults(db: Session) -> None:
    player_id = _player(db)

    session = session_repository.create(db, player_id=player_id)

    assert session.id is not None
    assert session.player_id == player_id
    assert session.status == SESSION_STATUS_ACTIVE
    assert session.current_day == 1
    assert session.current_sequence == 1
    assert session.ending_id is None
    assert session.score is None
    assert session.finished_at is None
    assert session.attributes is not None
    assert session.attributes.energia == 7
    assert session.attributes.reputacao == 5
    assert session.attributes.networking == 3
    assert session.attributes.ansiedade == 2
    assert session.attributes.produtividade == 5
    assert session.attributes.aprendizado == 4


def test_update_progress_persists_day_sequence_and_event(db: Session) -> None:
    session = session_repository.create(db, player_id=_player(db))

    updated = session_repository.update_progress(
        db,
        session_id=session.id,
        current_day=2,
        current_sequence=3,
        current_event_id="ev_day2_003",
    )

    assert updated is not None
    assert updated.current_day == 2
    assert updated.current_sequence == 3
    assert updated.current_event_id == "ev_day2_003"


def test_finish_marks_session_with_ending_and_score(db: Session) -> None:
    session = session_repository.create(db, player_id=_player(db))

    finished = session_repository.finish(
        db, session_id=session.id, ending_id="trainee_lenda", score=551
    )

    assert finished is not None
    assert finished.status == SESSION_STATUS_FINISHED
    assert finished.ending_id == "trainee_lenda"
    assert finished.score == 551
    assert finished.finished_at is not None


def test_update_progress_missing_session_returns_none(db: Session) -> None:
    result = session_repository.update_progress(
        db, session_id=999, current_day=1, current_sequence=1, current_event_id=None
    )
    assert result is None
