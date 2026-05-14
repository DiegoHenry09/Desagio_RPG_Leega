"""
API pública da camada de persistência — Corporate Survivor.

Consumida pelo backend (routers/use cases — quando existirem) e pelos
repositórios. NÃO consumida pela engine: a engine é Python puro.
"""

from .base import Base
from .init_db import init_db
from .session import DATABASE_URL, SessionLocal, engine, get_db

__all__ = [
    "Base",
    "DATABASE_URL",
    "SessionLocal",
    "engine",
    "get_db",
    "init_db",
]
