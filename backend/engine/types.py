"""
Tipos imutáveis da game engine — Corporate Survivor.

Nenhum import de FastAPI, SQLAlchemy, Pydantic (API) ou bibliotecas de I/O de rede.
Todos os dataclasses são frozen (imutáveis) para garantir que o estado da sessão
seja tratado como valor, nunca como objeto mutável compartilhado.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Optional


# ---------------------------------------------------------------------------
# Atributos do personagem
# ---------------------------------------------------------------------------

VALID_ATTRIBUTES = frozenset(
    {"energia", "reputacao", "networking", "ansiedade", "produtividade", "aprendizado"}
)

ATTR_MIN = 0
ATTR_MAX = 10


@dataclass(frozen=True)
class Attributes:
    energia: int = 7
    reputacao: int = 5
    networking: int = 3
    ansiedade: int = 2
    produtividade: int = 5
    aprendizado: int = 4

    def clamp(self) -> "Attributes":
        """Retorna nova instância com todos os atributos dentro de [ATTR_MIN, ATTR_MAX]."""
        return Attributes(
            energia=max(ATTR_MIN, min(ATTR_MAX, self.energia)),
            reputacao=max(ATTR_MIN, min(ATTR_MAX, self.reputacao)),
            networking=max(ATTR_MIN, min(ATTR_MAX, self.networking)),
            ansiedade=max(ATTR_MIN, min(ATTR_MAX, self.ansiedade)),
            produtividade=max(ATTR_MIN, min(ATTR_MAX, self.produtividade)),
            aprendizado=max(ATTR_MIN, min(ATTR_MAX, self.aprendizado)),
        )

    def apply(self, delta: "Consequences") -> "Attributes":
        """Aplica consequência e retorna nova instância (sem clamp — clamp é responsabilidade do chamador)."""
        return Attributes(
            energia=self.energia + delta.energia,
            reputacao=self.reputacao + delta.reputacao,
            networking=self.networking + delta.networking,
            ansiedade=self.ansiedade + delta.ansiedade,
            produtividade=self.produtividade + delta.produtividade,
            aprendizado=self.aprendizado + delta.aprendizado,
        )

    def to_dict(self) -> dict[str, int]:
        return {
            "energia": self.energia,
            "reputacao": self.reputacao,
            "networking": self.networking,
            "ansiedade": self.ansiedade,
            "produtividade": self.produtividade,
            "aprendizado": self.aprendizado,
        }


# ---------------------------------------------------------------------------
# Consequências de uma opção
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Consequences:
    energia: int = 0
    reputacao: int = 0
    networking: int = 0
    ansiedade: int = 0
    produtividade: int = 0
    aprendizado: int = 0

    @property
    def abs_sum(self) -> int:
        """Soma absoluta dos deltas — usada pela validação (≤ 7 por opção)."""
        return (
            abs(self.energia)
            + abs(self.reputacao)
            + abs(self.networking)
            + abs(self.ansiedade)
            + abs(self.produtividade)
            + abs(self.aprendizado)
        )

    @classmethod
    def from_dict(cls, data: dict[str, int]) -> "Consequences":
        return cls(
            energia=data.get("energia", 0),
            reputacao=data.get("reputacao", 0),
            networking=data.get("networking", 0),
            ansiedade=data.get("ansiedade", 0),
            produtividade=data.get("produtividade", 0),
            aprendizado=data.get("aprendizado", 0),
        )


# ---------------------------------------------------------------------------
# Condições de unlock/requisito
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class UnlockCondition:
    requires_all: tuple[str, ...] = field(default_factory=tuple)
    requires_any: tuple[str, ...] = field(default_factory=tuple)
    blocked_by: tuple[str, ...] = field(default_factory=tuple)
    min_attrs: dict[str, int] = field(default_factory=dict)
    max_attrs: dict[str, int] = field(default_factory=dict)
    after_day: Optional[int] = None
    before_day: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "UnlockCondition":
        return cls(
            requires_all=tuple(data.get("requires_all", [])),
            requires_any=tuple(data.get("requires_any", [])),
            blocked_by=tuple(data.get("blocked_by", [])),
            min_attrs=dict(data.get("min_attrs", {})),
            max_attrs=dict(data.get("max_attrs", {})),
            after_day=data.get("after_day"),
            before_day=data.get("before_day"),
        )

    def has_at_least_one_condition(self) -> bool:
        return bool(
            self.requires_all
            or self.requires_any
            or self.blocked_by
            or self.min_attrs
            or self.max_attrs
            or self.after_day is not None
            or self.before_day is not None
        )


# ---------------------------------------------------------------------------
# Opção de um evento
# ---------------------------------------------------------------------------

VALID_OPTION_IDS = frozenset({"A", "B", "C", "D"})


@dataclass(frozen=True)
class Option:
    id: str  # "A" | "B" | "C" | "D"
    label: str
    consequences: Consequences
    requires: Optional[UnlockCondition] = None
    unlocks: tuple[str, ...] = field(default_factory=tuple)
    blocks: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_dict(cls, data: dict) -> "Option":
        return cls(
            id=data["id"],
            label=data["label"],
            consequences=Consequences.from_dict(data.get("consequences", {})),
            requires=(
                UnlockCondition.from_dict(data["requires"])
                if data.get("requires")
                else None
            ),
            unlocks=tuple(data.get("unlocks", [])),
            blocks=tuple(data.get("blocks", [])),
        )


# ---------------------------------------------------------------------------
# Evento principal ou secreto
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Event:
    id: str
    is_main: bool
    title: str
    scene: str
    options: tuple[Option, ...]
    tags: tuple[str, ...] = field(default_factory=tuple)
    feedback: Optional[str] = None
    day: Optional[int] = None       # obrigatório se is_main=True
    sequence: Optional[int] = None  # obrigatório se is_main=True (1|2|3)
    unlock: Optional[UnlockCondition] = None  # obrigatório se is_main=False

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        return cls(
            id=data["id"],
            is_main=data["isMain"],
            title=data["title"],
            scene=data["scene"],
            options=tuple(Option.from_dict(o) for o in data["options"]),
            tags=tuple(data.get("tags", [])),
            feedback=data.get("feedback"),
            day=data.get("day"),
            sequence=data.get("sequence"),
            unlock=(
                UnlockCondition.from_dict(data["unlock"])
                if data.get("unlock")
                else None
            ),
        )

    def get_option(self, option_id: str) -> Optional[Option]:
        for opt in self.options:
            if opt.id == option_id:
                return opt
        return None


# ---------------------------------------------------------------------------
# Catálogo completo (events.json carregado e parseado)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Catalog:
    schema_version: str
    events: tuple[Event, ...]

    def main_events(self) -> tuple[Event, ...]:
        return tuple(e for e in self.events if e.is_main)

    def secret_events(self) -> tuple[Event, ...]:
        return tuple(e for e in self.events if not e.is_main)

    def get_main(self, day: int, sequence: int) -> Optional[Event]:
        for e in self.events:
            if e.is_main and e.day == day and e.sequence == sequence:
                return e
        return None

    def all_event_ids(self) -> frozenset[str]:
        return frozenset(e.id for e in self.events)

    @classmethod
    def from_dict(cls, data: dict) -> "Catalog":
        return cls(
            schema_version=data["schemaVersion"],
            events=tuple(Event.from_dict(e) for e in data.get("events", [])),
        )


# ---------------------------------------------------------------------------
# Estado imutável da sessão
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ChoiceRecord:
    event_id: str
    option_id: str


@dataclass(frozen=True)
class State:
    """Estado completo de uma sessão de jogo — imutável."""

    current_day: int = 1
    current_sequence: int = 1
    attributes: Attributes = field(default_factory=Attributes)
    choices_log: tuple[ChoiceRecord, ...] = field(default_factory=tuple)
    secret_ids_seen: tuple[str, ...] = field(default_factory=tuple)
    is_finished: bool = False
    ending_id: Optional[str] = None
    score: Optional[int] = None

    @property
    def days_completed(self) -> int:
        """Dias com todos os 3 eventos principais consumidos."""
        if self.current_sequence == 1:
            return self.current_day - 1
        return self.current_day - 1

    def with_choice(self, record: ChoiceRecord) -> "State":
        return replace(self, choices_log=self.choices_log + (record,))

    def with_secret_seen(self, secret_id: str) -> "State":
        return replace(self, secret_ids_seen=self.secret_ids_seen + (secret_id,))

    def with_attributes(self, attrs: Attributes) -> "State":
        return replace(self, attributes=attrs)

    def finished(self, ending_id: str, score: int) -> "State":
        return replace(self, is_finished=True, ending_id=ending_id, score=score)

    def has_seen_event(self, event_id: str) -> bool:
        if any(r.event_id == event_id for r in self.choices_log):
            return True
        return event_id in self.secret_ids_seen

    def advance(self) -> "State":
        """Retorna novo estado com sequence/day avançado (chamado pela engine após processar uma escolha)."""
        if self.current_sequence < 3:
            return replace(self, current_sequence=self.current_sequence + 1)
        if self.current_day < 5:
            return replace(self, current_day=self.current_day + 1, current_sequence=1)
        return self


# ---------------------------------------------------------------------------
# Gatilho de final antecipado (ADR-010)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EarlyTrigger:
    """Resultado da checagem de gatilho antecipado."""
    triggered: bool
    ending_id: str = ""        # "demitido" ou "burnout"
    trigger_name: str = ""     # "reputation_zero" | "energy_zero" | "anxiety_max"


# ---------------------------------------------------------------------------
# Resultado de resolução de final
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EndingResult:
    ending_id: str
    score: int
    trigger_name: str = ""  # vazio = fim de semana normal; preenchido = antecipado
