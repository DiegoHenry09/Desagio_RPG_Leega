"""
RankingRepository — CRUD puro para RankingEntry.

Contrato: NÃO calcula score. O score recebido aqui é o já calculado pela
engine (`compute_score` em `backend/engine/endings.py`).
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.ranking_entry import RankingEntry


def add(
    db: Session,
    player_name: str,
    score: int,
    ending_id: str,
    session_id: int,
) -> RankingEntry:
    entry = RankingEntry(
        player_name=player_name,
        score=score,
        ending_id=ending_id,
        session_id=session_id,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def top_n(db: Session, n: int = 10) -> list[RankingEntry]:
    """Top-N ordenado por score desc, desempate por created_at asc, id asc."""
    stmt = (
        select(RankingEntry)
        .order_by(
            RankingEntry.score.desc(),
            RankingEntry.created_at.asc(),
            RankingEntry.id.asc(),
        )
        .limit(n)
    )
    return list(db.execute(stmt).scalars().all())
