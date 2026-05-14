"""
Router: /api/sessions — Corporate Survivor.

Sprint 2.1+: criação, leitura e escolhas (2.2) integradas à engine.
Router **fino**: delegação total aos use cases.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from engine import Event
from schemas.sessions import (
    AttributesPayload,
    ChoiceCreate,
    EventPayload,
    OptionPayload,
    SessionCreate,
    SessionResponse,
)
from use_cases.choice_use_cases import apply_session_choice
from use_cases.session_use_cases import (
    SessionSnapshot,
    create_session,
    get_session_snapshot,
)

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


def _event_to_payload(event: Event | None) -> EventPayload | None:
    if event is None:
        return None
    return EventPayload(
        id=event.id,
        title=event.title,
        scene=event.scene,
        day=event.day,
        sequence=event.sequence,
        is_main=event.is_main,
        options=[OptionPayload(id=o.id, label=o.label) for o in event.options],
    )


def _snapshot_to_response(
    snapshot: SessionSnapshot,
    *,
    inject_secret: Event | None = None,
) -> SessionResponse:
    session = snapshot.session
    response = SessionResponse(
        id=session.id,
        player_id=session.player_id,
        status=session.status,
        current_day=session.current_day,
        current_sequence=session.current_sequence,
        current_event_id=session.current_event_id,
        ending_id=session.ending_id,
        score=session.score,
        created_at=session.created_at,
        updated_at=session.updated_at,
        finished_at=session.finished_at,
        attributes=AttributesPayload.model_validate(snapshot.attributes),
        current_event=_event_to_payload(snapshot.current_event),
        inject_secret_event=_event_to_payload(inject_secret),
    )
    return response


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_session_endpoint(
    payload: SessionCreate,
    db: Session = Depends(get_db),
) -> SessionResponse:
    snapshot = create_session(db, payload)
    return _snapshot_to_response(snapshot)


@router.post(
    "/{session_id}/choices",
    response_model=SessionResponse,
)
def submit_choice_endpoint(
    session_id: int,
    payload: ChoiceCreate,
    db: Session = Depends(get_db),
) -> SessionResponse:
    outcome = apply_session_choice(
        db,
        session_id,
        event_id=payload.event_id,
        option_id=payload.option_id,
    )
    return _snapshot_to_response(
        outcome.snapshot,
        inject_secret=outcome.inject_secret_event,
    )


@router.get(
    "/{session_id}",
    response_model=SessionResponse,
)
def get_session_endpoint(
    session_id: int,
    db: Session = Depends(get_db),
) -> SessionResponse:
    snapshot = get_session_snapshot(db, session_id)
    return _snapshot_to_response(snapshot)

