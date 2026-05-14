"""
Fixtures de teste — Corporate Survivor backend.

Estratégia: SQLite in-memory por TESTE, com StaticPool para garantir que
todas as sessões usem a MESMA conexão (caso contrário cada conexão tem
seu próprio "database" no SQLite in-memory e o schema some).

Por que não compartilhar engine entre testes: isolamento total — cada
teste recria as tabelas, evita poluição cruzada e reproduz o cenário
"banco vazio" do ambiente de produção em cada execução.

Para testes de API (Sprint 2.1+), a fixture `client` instancia um
`TestClient` SEM disparar o lifespan (para não criar o banco de
produção em disco) e sobrescreve `get_db` via `app.dependency_overrides`.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from db.base import Base

# Import for side-effect: registra todos os modelos no metadata da Base
# antes do create_all() rodar nas fixtures abaixo.
import models  # noqa: F401


@pytest.fixture()
def engine_test() -> Iterator[Engine]:
    eng = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=eng)
    try:
        yield eng
    finally:
        Base.metadata.drop_all(bind=eng)
        eng.dispose()


@pytest.fixture()
def db(engine_test: Engine) -> Iterator[Session]:
    TestSessionLocal = sessionmaker(
        bind=engine_test,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=Session,
        future=True,
    )
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(engine_test: Engine) -> Iterator[TestClient]:
    """TestClient com `get_db` apontando para o banco in-memory.

    Não dispara lifespan — não chama `init_db()` em disco. O schema
    do banco de teste já foi criado pela fixture `engine_test`.
    """
    from app import app
    from db import get_db

    TestSessionLocal = sessionmaker(
        bind=engine_test,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=Session,
        future=True,
    )

    def _override_get_db() -> Iterator[Session]:
        session = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = _override_get_db
    # IMPORTANTE: NÃO usar `with TestClient(app)` aqui — `with` dispara o
    # lifespan da aplicação, que chama `init_db()` no engine de produção
    # (sqlite em disco). Em testes queremos isolamento total no in-memory.
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
