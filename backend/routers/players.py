"""
Router: /api/players — Corporate Survivor.

Router FINO. Apenas:
  - depende da sessão de DB,
  - delega ao use case,
  - serializa response.

NÃO contém regra de jogo. NÃO acessa repository diretamente.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from schemas.player_profile import PlayerProfileResponse, PlayerRunChoicesResponse
from schemas.players import PlayerCreate, PlayerResponse
from use_cases.player_profile_use_cases import build_player_profile, build_player_run_choices
from use_cases.player_use_cases import create_player

router = APIRouter(prefix="/api/players", tags=["players"])


@router.post(
    "",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_player_endpoint(
    payload: PlayerCreate,
    db: Session = Depends(get_db),
) -> PlayerResponse:
    player = create_player(db, payload)
    return PlayerResponse.model_validate(player)


@router.get(
    "/{player_id}/profile",
    response_model=PlayerProfileResponse,
)
def get_player_profile_endpoint(
    player_id: int,
    db: Session = Depends(get_db),
) -> PlayerProfileResponse:
    return build_player_profile(db, player_id)


@router.get(
    "/{player_id}/runs/{ranking_entry_id}/choices",
    response_model=PlayerRunChoicesResponse,
)
def get_player_run_choices_endpoint(
    player_id: int,
    ranking_entry_id: int,
    db: Session = Depends(get_db),
) -> PlayerRunChoicesResponse:
    return build_player_run_choices(db, player_id, ranking_entry_id)
