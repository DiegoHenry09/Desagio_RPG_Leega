"""
Engine SQLAlchemy + SessionLocal + get_db — Corporate Survivor.

DATABASE_URL é lido de env. Padrão dev: SQLite em arquivo dentro de
`backend/data/`. Para SQLite, `check_same_thread=False` é necessário pois
o FastAPI/uvicorn alterna threads em I/O bloqueante.

Esta camada NÃO conhece regra de jogo. Apenas conexão e ciclo de vida de sessão.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

DEFAULT_DB_URL = "sqlite:///./data/corporate_survivor.db"

DATABASE_URL: str = os.environ.get("DATABASE_URL", DEFAULT_DB_URL)


def _ensure_sqlite_parent_dir(url: str) -> None:
    """Garante que o diretório-pai do arquivo SQLite exista.

    Útil para o caso de dev em que o backend sobe e a pasta `backend/data/`
    foi removida acidentalmente. Não faz nada para URLs não-SQLite-file.
    """
    if not url.startswith("sqlite:///"):
        return
    path_part = url.replace("sqlite:///", "", 1)
    if path_part.startswith(":memory:") or path_part == "":
        return
    parent = Path(path_part).parent
    if parent and not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)


def _build_engine(url: str) -> Engine:
    _ensure_sqlite_parent_dir(url)
    connect_args: dict[str, object] = {}
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(url, connect_args=connect_args, future=True)


engine: Engine = _build_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
    future=True,
)


def get_db() -> Iterator[Session]:
    """Generator para uso em dependency injection (FastAPI futuro).

    Garante fechamento da sessão. Use:
        with next(get_db()) as db: ...
    ou via `Depends(get_db)` quando os routers existirem.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
