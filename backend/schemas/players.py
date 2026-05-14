"""
Schemas Pydantic v2 para Player — API HTTP.

Validações:
  - `name`: 1..64 caracteres, regex permissiva (letras/dígitos/espaços e
    pontuação leve `-_.'`). Trim de bordas. Não aceita string vazia
    após o trim.

Decisão da Sprint 2.1: nome NÃO é único — múltiplos jogadores podem ter o
mesmo nome humano (alinhado com ranking global descrito em
`docs/02-product/game-rules.md`).
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

# Regex permissiva: letras (qualquer Unicode), dígitos, espaços e pontuação leve.
# Evita XSS-like tokens (`<`, `>`, `"`, `'` excluídos exceto apóstrofo padrão).
PlayerName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=64,
        pattern=r"^[\w\s\-_.'À-ÿ]+$",
    ),
]


class PlayerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: PlayerName

    @field_validator("name")
    @classmethod
    def _no_only_whitespace(cls, v: str) -> str:
        # StringConstraints já trim+min_length=1, mas garantimos defesa em
        # profundidade contra entradas que escapem do regex.
        if not v.strip():
            raise ValueError("name não pode ser vazio.")
        return v


class PlayerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime
