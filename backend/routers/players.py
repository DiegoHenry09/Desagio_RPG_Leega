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
from schemas.players import PlayerCreate, PlayerResponse
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
