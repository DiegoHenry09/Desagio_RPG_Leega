"""
Schemas Pydantic v2 para Session — API HTTP.

Decisão Sprint 2.1: GET /api/sessions/{id} retorna estado COMPLETO da
sessão: progresso (day/sequence/event_id), status, atributos correntes
e o **evento atual carregado do catálogo** (cena, opções) — conforme
`docs/02-product/api.md` que descreve "estado atual da sessão (dia,
sequência, evento atual, atributos)".

O backend NÃO calcula score nem ending aqui; só lê estado já persistido.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# IDs de opção permitidos pela engine (§4 engine / game-rules).


class ChoiceCreate(BaseModel):
    """Corpo POST /api/sessions/{id}/choices — Sprint 2.2."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    event_id: str = Field(min_length=1, max_length=64)
    option_id: str = Field(
        min_length=1,
        max_length=1,
        pattern=r"^[ABCD]$",
    )


class SessionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    player_id: int = Field(gt=0)


class AttributesPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    energia: int
    reputacao: int
    networking: int
    ansiedade: int
    produtividade: int
    aprendizado: int


class OptionPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    label: str


class EventPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    scene: str
    day: Optional[int] = None
    sequence: Optional[int] = None
    is_main: bool
    options: list[OptionPayload]


class SessionResponse(BaseModel):
    """Snapshot completo da sessão para o frontend."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    player_id: int
    status: str  # "active" | "finished"
    current_day: int
    current_sequence: int
    current_event_id: Optional[str] = None
    ending_id: Optional[str] = None
    score: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    finished_at: Optional[datetime] = None
    attributes: AttributesPayload
    #: Evento atual (principal) onde o jogador está; `null` se sessão já finalizada.
    current_event: Optional[EventPayload] = None
    #: Presente apenas após POST /choices: secreto disparado pela engine neste turno,
    #: sem leak de `consequences` nas options (mesmo mapeamento fino dos principais).
    inject_secret_event: Optional[EventPayload] = Field(
        None,
        description="Opcional — evento secreto injetado no turno atual para UX.",
    )
