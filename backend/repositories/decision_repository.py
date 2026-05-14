"""
DecisionRepository — CRUD puro para Decision (histórico de escolhas).
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.decision import Decision


def record(
    db: Session,
    session_id: int,
    event_id: str,
    option_id: str,
    day: int,
    sequence: int,
) -> Decision:
    """Grava uma decisão. Não valida coerência com o estado da sessão —
    isso é responsabilidade do use case que orquestra a engine.
    """
    decision = Decision(
        session_id=session_id,
        event_id=event_id,
        option_id=option_id,
        day=day,
        sequence=sequence,
    )
    db.add(decision)
    db.commit()
    db.refresh(decision)
    return decision


def list_by_session(db: Session, session_id: int) -> list[Decision]:
    """Lista decisões em ordem de inserção (id ASC)."""
    stmt = (
        select(Decision)
        .where(Decision.session_id == session_id)
        .order_by(Decision.id.asc())
    )
    return list(db.execute(stmt).scalars().all())
