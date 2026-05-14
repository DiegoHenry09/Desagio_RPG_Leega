"""
Configuração centralizada — Corporate Survivor backend.

Lê variáveis de ambiente (com fallback) usando pydantic-settings.
Valores default mantêm o setup local funcionando sem `.env`.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação.

    O modo `APP_ENV` discrimina ambientes (development/test/production).
    Em testes, sobrescrevemos via dependency override quando necessário.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./data/corporate_survivor.db"

    # CSV de origens separadas por vírgula. Padrão cobre Vite dev local.
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton lazy. lru_cache garante reuso entre chamadas e simples
    invalidação em testes via `get_settings.cache_clear()`.
    """
    return Settings()
