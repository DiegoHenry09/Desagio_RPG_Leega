"""
Router: /api/ranking — Corporate Survivor (Sprint 2.3).

Router FINO:
  - depende da sessão de DB,
  - delega ao use case `list_top_ranking`,
  - serializa via `RankingListResponse` (envelope `{items, limit, count}`).

NÃO contém regra de jogo. NÃO acessa repository diretamente.
NÃO calcula score (a engine já fez isso ao final da partida via
`compute_score` em `backend/engine/endings.py`).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db import get_db
from schemas.ranking import RankingEntryResponse, RankingListResponse
from use_cases.ranking_use_cases import list_top_ranking

router = APIRouter(prefix="/api/ranking", tags=["ranking"])

# Bounds explícitos: default 10, mínimo 1, máximo 100. Limite máximo evita
# resposta absurdamente grande sem necessidade. Valores fora dos bounds são
# rejeitados pelo Pydantic (RequestValidationError → handler global → 422
# com envelope `{"error": {"code": "validation_error", ...}}`).
_DEFAULT_LIMIT = 10
_MIN_LIMIT = 1
_MAX_LIMIT = 100


@router.get(
    "",
    response_model=RankingListResponse,
)
def list_ranking_endpoint(
    db: Session = Depends(get_db),
    limit: int = Query(
        _DEFAULT_LIMIT,
        ge=_MIN_LIMIT,
        le=_MAX_LIMIT,
        description="Número máximo de entradas retornadas (1..100, default 10).",
    ),
) -> RankingListResponse:
    rows = list_top_ranking(db, limit=limit)
    items = [RankingEntryResponse.model_validate(row) for row in rows]
    return RankingListResponse(
        items=items,
        limit=limit,
        count=len(items),
    )
