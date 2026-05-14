"""
Schemas Pydantic v2 do backend Corporate Survivor.

Cada módulo expõe os DTOs (request/response) de uma área da API.
NÃO importar `engine` (schemas são contrato HTTP, não estado da engine).
"""

from .errors import ErrorBody, ErrorResponse
from .players import PlayerCreate, PlayerResponse
from .ranking import RankingEntryResponse, RankingListResponse
from .sessions import (
    AttributesPayload,
    ChoiceCreate,
    EventPayload,
    OptionPayload,
    SessionCreate,
    SessionResponse,
)

__all__ = [
    "AttributesPayload",
    "ChoiceCreate",
    "ErrorBody",
    "ErrorResponse",
    "EventPayload",
    "OptionPayload",
    "PlayerCreate",
    "PlayerResponse",
    "RankingEntryResponse",
    "RankingListResponse",
    "SessionCreate",
    "SessionResponse",
]
