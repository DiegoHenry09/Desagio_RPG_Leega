"""
Inicialização de schema — Corporate Survivor.

Estratégia decidida em ADR-006: usar `Base.metadata.create_all()` no startup
do FastAPI (sem Alembic nesta sprint). Importa `models` para registrar as
tabelas no metadata antes do create_all.
"""

from __future__ import annotations

from sqlalchemy.engine import Engine

from .base import Base
from .session import engine as default_engine


def init_db(bind: Engine | None = None) -> None:
    """Cria todas as tabelas do metadata caso não existam.

    Idempotente: rodar várias vezes não causa erro nem reset.
    O parâmetro `bind` permite reuso em testes (engine in-memory).
    """
    # Import lazy: força registro dos modelos no metadata da Base ANTES do
    # create_all. Não há side-effect além desse registro.
    import models  # noqa: F401  (import-for-side-effect)

    target = bind if bind is not None else default_engine
    Base.metadata.create_all(bind=target)
