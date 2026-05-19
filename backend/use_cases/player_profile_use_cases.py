"""
Perfil do jogador — leitura agregada de ranking e timeline de escolhas.

NÃO recalcula score/ending. NÃO importa engine.
"""

from __future__ import annotations

from collections import Counter

from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from models.ranking_entry import RankingEntry
from repositories import ranking_repository
from schemas.player_profile import (
    PlayerProfileResponse,
    PlayerProfileStats,
    PlayerRunChoiceItem,
    PlayerRunChoicesResponse,
    PlayerRunItem,
)
from use_cases.player_use_cases import get_player


def build_player_profile(db: Session, player_id: int) -> PlayerProfileResponse:
    player = get_player(db, player_id)
    entries = ranking_repository.list_for_player_profile(db, player_id)
    if not entries:
        stats = PlayerProfileStats(games_played=0, best_score=None, avg_score=None)
        return PlayerProfileResponse(
            player_id=player.id,
            player_name=player.name,
            stats=stats,
            ending_counts={},
            runs=[],
        )

    scores = [e.score for e in entries]
    ending_counts = Counter(e.ending_id for e in entries)
    total = sum(scores)
    n = len(scores)
    stats = PlayerProfileStats(
        games_played=n,
        best_score=max(scores),
        avg_score=round(total / n, 1),
    )
    runs = [
        PlayerRunItem(
            ranking_entry_id=e.id,
            score=e.score,
            ending_id=e.ending_id,
            created_at=e.created_at,
            choices_count=len(e.session.decisions),
        )
        for e in entries
    ]
    return PlayerProfileResponse(
        player_id=player.id,
        player_name=player.name,
        stats=stats,
        ending_counts=dict(sorted(ending_counts.items())),
        runs=runs,
    )


def build_player_run_choices(
    db: Session, player_id: int, ranking_entry_id: int
) -> PlayerRunChoicesResponse:
    """Timeline de escolhas de uma partida listada no ranking.

    Usa apenas `ranking_entry_id` público; valida que a entrada pertence ao
    `player_id` para não vazar sessões de terceiros.
    """
    get_player(db, player_id)
    entry = db.get(RankingEntry, ranking_entry_id)
    if entry is None:
        raise NotFoundError(
            "Entrada de ranking não encontrada.",
            details={"ranking_entry_id": ranking_entry_id},
        )
    # session já veio com ranking insert — garantir player_id
    sess = entry.session
    if sess.player_id != player_id:
        raise NotFoundError(
            "Entrada de ranking não encontrada.",
            details={"ranking_entry_id": ranking_entry_id, "player_id": player_id},
        )
    decisions = sorted(sess.decisions, key=lambda d: d.id)
    choices = [PlayerRunChoiceItem.model_validate(d) for d in decisions]
    return PlayerRunChoicesResponse(ranking_entry_id=entry.id, choices=choices)
