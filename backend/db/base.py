"""
Base declarativa SQLAlchemy 2.0 — Corporate Survivor.

Todos os modelos (`backend/models/*`) herdam desta classe. Nenhum import de
engine, FastAPI, ou frontend. Camada exclusivamente de persistência (Agent
Backend, contrato em `docs/02-product/architecture.md`).
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarativa única do projeto.

    Centraliza o metadata. Importada por `init_db()` para criar/dropar tabelas.
    """

    pass
