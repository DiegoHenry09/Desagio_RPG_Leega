"""
Corporate Survivor — FastAPI app entrypoint.

Mantém-se FINO (sem regra de jogo). Responsabilidades aqui:
  - Boot: init_db() + validate_events() do catálogo (falha cedo).
  - CORS para dev local (Vite em http://localhost:5173 por padrão).
  - Handlers globais de erro padronizados (422/404/409/500).
  - Include routers de players e sessions (Sprint 2.1) + ranking (Sprint 2.3).

POST /api/sessions/{session_id}/choices integrado à engine (Sprint 2.2).
GET /api/ranking lista o leaderboard global (Sprint 2.3).
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from core.error_handlers import register_error_handlers
from db import init_db
from routers.players import router as players_router
from routers.ranking import router as ranking_router
from routers.sessions import router as sessions_router
from use_cases.catalog_loader import get_catalog, validate_or_raise


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # 1) Schema: Sprint 2.0 + ADR-006 — create_all() idempotente.
    init_db()

    # 2) Catálogo: roda engine.validate_events sobre o arquivo no disco;
    #    aquece o singleton de Catalog. Falha aqui = boot falha
    #    (game-rules.md §4.3 + §9).
    validate_or_raise()
    get_catalog()

    yield


settings = get_settings()

app = FastAPI(title="Corporate Survivor API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    # Evita "*" em cabeçalhos sensíveis: fetch JSON do frontend só precisa
    # declarar Content-Type + Accept nos preflight.
    allow_headers=["Content-Type", "Accept"],
)

register_error_handlers(app)

app.include_router(players_router)
app.include_router(sessions_router)
app.include_router(ranking_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
