"""
Game engine — Corporate Survivor.

Funções puras sem efeitos colaterais externos.
Nenhum import de FastAPI, SQLAlchemy, Pydantic (API) ou frontend.

Contrato público (consumido pelo backend via __init__.py):
  - validate_events(catalog_dict) -> None  (lança ValueError em catálogo inválido)
  - apply_choice(state, catalog, option_id) -> ApplyResult
  - resolve_ending(state) -> EndingResult  (fim de semana)
  - compute_score(state, ending_id) -> int
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional

from .endings import (
    EARLY_TRIGGER_ENDINGS,
    compute_score,
    resolve_ending_from_registry,
)
from .types import (
    ATTR_MAX,
    ATTR_MIN,
    VALID_ATTRIBUTES,
    VALID_OPTION_IDS,
    Attributes,
    Catalog,
    ChoiceRecord,
    EarlyTrigger,
    EndingResult,
    Event,
    Option,
    State,
    UnlockCondition,
)


# ---------------------------------------------------------------------------
# Resultado de apply_choice
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ApplyResult:
    state: State
    ending: Optional[EndingResult]  # None = jogo continua; preenchido = sessão encerrada
    secret_event: Optional[Event]   # secreto injetado neste passo (se houver)


# ---------------------------------------------------------------------------
# validate_events (invariantes 1–11, game-rules.md §4.3)
# ---------------------------------------------------------------------------

def validate_events(catalog_dict: dict) -> None:
    """
    Valida o dicionário carregado de events.json.
    Lança ValueError com mensagem descritiva se qualquer invariante falhar.
    Em caso de sucesso, retorna None.
    """

    # 1 — schemaVersion
    if catalog_dict.get("schemaVersion") != "1.0":
        raise ValueError(
            f"schemaVersion deve ser '1.0', encontrado: {catalog_dict.get('schemaVersion')!r}"
        )

    raw_events: list[dict] = catalog_dict.get("events", [])

    # Indexar por id para checks de referência cruzada
    by_id: dict[str, dict] = {}
    for ev in raw_events:
        ev_id = ev.get("id", "")
        if not ev_id:
            raise ValueError("Evento sem 'id' encontrado.")
        if ev_id in by_id:
            raise ValueError(f"ID de evento duplicado: {ev_id!r}")
        by_id[ev_id] = ev

    all_ids = frozenset(by_id.keys())

    # Separar principais e secretos
    main_events = [ev for ev in raw_events if ev.get("isMain") is True]
    secret_events = [ev for ev in raw_events if ev.get("isMain") is False]

    # 2 — exatamente 3 principais por dia × 5 dias = 15
    for day in range(1, 6):
        mains_for_day = [ev for ev in main_events if ev.get("day") == day]
        if len(mains_for_day) != 3:
            raise ValueError(
                f"Dia {day}: esperado 3 eventos principais, encontrado {len(mains_for_day)}."
            )

        # 3 — sequence cobre {1, 2, 3} exatamente uma vez por dia
        seqs = sorted(ev.get("sequence") for ev in mains_for_day)
        if seqs != [1, 2, 3]:
            raise ValueError(
                f"Dia {day}: sequences devem ser [1, 2, 3] sem repetição, encontrado {seqs}."
            )

    # 4 — secretos: isMain=False, day=None, unlock presente com ao menos uma condição
    for ev in secret_events:
        ev_id = ev.get("id", "?")
        if ev.get("day") is not None:
            raise ValueError(f"Secreto {ev_id!r}: 'day' deve ser null.")
        if ev.get("sequence") is not None:
            raise ValueError(f"Secreto {ev_id!r}: 'sequence' deve ser null.")
        unlock = ev.get("unlock")
        if unlock is None:
            raise ValueError(
                f"Secreto {ev_id!r}: campo 'unlock' ausente ou vazio."
            )
        cond = UnlockCondition.from_dict(unlock)
        if not cond.has_at_least_one_condition():
            raise ValueError(
                f"Secreto {ev_id!r}: 'unlock' existe mas não tem nenhuma condição."
            )

    # 5 — toda referência de ID em unlocks/blocks/requires_* aponta para evento existente
    ref_fields = ("unlocks", "blocks", "requires_all", "requires_any", "blocked_by")
    for ev in raw_events:
        ev_id = ev.get("id", "?")
        for opt in ev.get("options", []):
            for fld in ("unlocks", "blocks"):
                for ref in opt.get(fld, []):
                    if ref not in all_ids:
                        raise ValueError(
                            f"Evento {ev_id!r}, opção {opt.get('id')!r}: referência {ref!r} em '{fld}' não existe."
                        )
            req = opt.get("requires", {})
            for sub in ("requires_all", "requires_any", "blocked_by"):
                for ref in req.get(sub, []):
                    if ref not in all_ids:
                        raise ValueError(
                            f"Evento {ev_id!r}, opção {opt.get('id')!r}: referência {ref!r} em 'requires.{sub}' não existe."
                        )
        # unlock pode ser None para eventos principais — usar {} como fallback
        unlock = ev.get("unlock") or {}
        for sub in ("requires_all", "requires_any", "blocked_by"):
            for ref in unlock.get(sub, []):
                if ref not in all_ids:
                    raise ValueError(
                        f"Evento {ev_id!r}: referência {ref!r} em 'unlock.{sub}' não existe."
                    )

    # 6 — cada evento tem 1–4 opções com IDs únicos em {A, B, C, D}
    for ev in raw_events:
        ev_id = ev.get("id", "?")
        opts: list[dict] = ev.get("options", [])
        if not (1 <= len(opts) <= 4):
            raise ValueError(
                f"Evento {ev_id!r}: deve ter entre 1 e 4 opções, encontrado {len(opts)}."
            )
        opt_ids = [o.get("id") for o in opts]
        if any(oid not in VALID_OPTION_IDS for oid in opt_ids):
            invalid = [oid for oid in opt_ids if oid not in VALID_OPTION_IDS]
            raise ValueError(
                f"Evento {ev_id!r}: IDs de opção inválidos {invalid}. Válidos: A B C D."
            )
        if len(opt_ids) != len(set(opt_ids)):
            raise ValueError(f"Evento {ev_id!r}: IDs de opção duplicados: {opt_ids}.")

    # 7 — soma absoluta dos deltas por opção ≤ 7
    for ev in raw_events:
        ev_id = ev.get("id", "?")
        for opt in ev.get("options", []):
            from .types import Consequences
            cons = Consequences.from_dict(opt.get("consequences", {}))
            if cons.abs_sum > 7:
                raise ValueError(
                    f"Evento {ev_id!r}, opção {opt.get('id')!r}: soma absoluta dos deltas "
                    f"é {cons.abs_sum}, máximo permitido é 7."
                )

    # 8 — atributos referenciados pertencem aos 6 válidos
    for ev in raw_events:
        ev_id = ev.get("id", "?")
        for opt in ev.get("options", []):
            for attr in opt.get("consequences", {}).keys():
                if attr not in VALID_ATTRIBUTES:
                    raise ValueError(
                        f"Evento {ev_id!r}, opção {opt.get('id')!r}: atributo desconhecido {attr!r}."
                    )
        for sub in ("min_attrs", "max_attrs"):
            for attr in ev.get("unlock", {}).get(sub, {}).keys():
                if attr not in VALID_ATTRIBUTES:
                    raise ValueError(
                        f"Evento {ev_id!r}: atributo desconhecido {attr!r} em 'unlock.{sub}'."
                    )

    # 9 — nenhum evento referencia a si mesmo
    for ev in raw_events:
        ev_id = ev.get("id", "?")
        for opt in ev.get("options", []):
            for fld in ("unlocks", "blocks"):
                if ev_id in opt.get(fld, []):
                    raise ValueError(
                        f"Evento {ev_id!r}: auto-referência em opção '{opt.get('id')}' campo '{fld}'."
                    )
        for sub in ("requires_all", "requires_any", "blocked_by"):
            if ev_id in ev.get("unlock", {}).get(sub, []):
                raise ValueError(
                    f"Evento {ev_id!r}: auto-referência em 'unlock.{sub}'."
                )

    # 10 — cada opção tem label não-vazio
    for ev in raw_events:
        ev_id = ev.get("id", "?")
        for opt in ev.get("options", []):
            if not opt.get("label", "").strip():
                raise ValueError(
                    f"Evento {ev_id!r}, opção {opt.get('id')!r}: 'label' vazio ou ausente."
                )

    # 11 — IDs de finais antecipados existem no registry de endings
    from .endings import EARLY_TRIGGER_ENDINGS, _ENDING_REGISTRY
    registry_ids = frozenset(t[0] for t in _ENDING_REGISTRY)
    for trigger_name, ending_id in EARLY_TRIGGER_ENDINGS.items():
        if ending_id not in registry_ids:
            raise ValueError(
                f"Gatilho antecipado '{trigger_name}' aponta para ending '{ending_id}' "
                f"que não está registrado no registry de finais."
            )


# ---------------------------------------------------------------------------
# Checagem de final antecipado (ADR-010, game-rules.md §4.4.2-3)
# Chamada após cada clamp: retorna o primeiro gatilho disparado na ordem de prioridade.
# ---------------------------------------------------------------------------

def _check_early_ending(attrs: Attributes) -> EarlyTrigger:
    """
    Avalia gatilhos antecipados na ordem de prioridade (ADR-010):
      1. reputacao <= 0  → demitido   (perda objetiva da posição)
      2. energia <= 0    → burnout     (esgotamento físico)
      3. ansiedade >= 10 → burnout     (esgotamento psicológico)
    """
    if attrs.reputacao <= 0:
        return EarlyTrigger(triggered=True, ending_id="demitido", trigger_name="reputation_zero")
    if attrs.energia <= 0:
        return EarlyTrigger(triggered=True, ending_id="burnout", trigger_name="energy_zero")
    if attrs.ansiedade >= ATTR_MAX:
        return EarlyTrigger(triggered=True, ending_id="burnout", trigger_name="anxiety_max")
    return EarlyTrigger(triggered=False)


# ---------------------------------------------------------------------------
# Elegibilidade de evento secreto (game-rules.md §4.2)
# ---------------------------------------------------------------------------

def _find_eligible_secret(state: State, catalog: Catalog) -> Optional[Event]:
    """
    Retorna o primeiro secreto elegível (menor ID lexicográfico) ou None.
    Um secreto é elegível se:
      - ainda não foi vivenciado;
      - sua UnlockCondition é satisfeita pelo estado atual.
    """
    candidates: list[Event] = []
    for secret in catalog.secret_events():
        if state.has_seen_event(secret.id):
            continue
        if secret.unlock is None:
            continue
        if _unlock_satisfied(secret.unlock, state):
            candidates.append(secret)
    if not candidates:
        return None
    return min(candidates, key=lambda e: e.id)


def _unlock_satisfied(cond: UnlockCondition, state: State) -> bool:
    attrs = state.attributes
    history_ids = frozenset(r.event_id for r in state.choices_log) | frozenset(state.secret_ids_seen)

    if cond.requires_all and not all(eid in history_ids for eid in cond.requires_all):
        return False
    if cond.requires_any and not any(eid in history_ids for eid in cond.requires_any):
        return False
    if cond.blocked_by and any(eid in history_ids for eid in cond.blocked_by):
        return False
    for attr, min_val in cond.min_attrs.items():
        if getattr(attrs, attr, 0) < min_val:
            return False
    for attr, max_val in cond.max_attrs.items():
        if getattr(attrs, attr, 0) > max_val:
            return False
    if cond.after_day is not None and state.current_day < cond.after_day:
        return False
    if cond.before_day is not None and state.current_day > cond.before_day:
        return False
    return True


# ---------------------------------------------------------------------------
# apply_choice — núcleo da engine
# ---------------------------------------------------------------------------

def apply_choice(state: State, catalog: Catalog, option_id: str) -> ApplyResult:
    """
    Aplica a escolha do jogador sobre o evento atual do estado.

    Fluxo (game-rules.md §4.1 + §4.4.3):
      1. Carrega evento atual via (current_day, current_sequence).
      2. Valida a opção (existe? requisitos atendidos?).
      3. Aplica consequências.
      4. Clamp.
      5. Checa gatilho antecipado — se disparou, encerra a sessão.
      6. Registra choice no log.
      7. Verifica secreto elegível — se houver, aplica-o e re-checa gatilho.
      8. Avança day/sequence.
      9. Se chegou ao fim do dia 5 (15 principais), resolve final de fim de semana.

    Retorna ApplyResult com estado final e, se sessão encerrada, EndingResult.
    """
    # 1 — carregar evento atual
    current_event = catalog.get_main(state.current_day, state.current_sequence)
    if current_event is None:
        raise ValueError(
            f"Evento principal não encontrado para day={state.current_day}, "
            f"sequence={state.current_sequence}."
        )

    # 2 — validar opção
    option = current_event.get_option(option_id)
    if option is None:
        raise ValueError(
            f"Opção {option_id!r} não existe no evento {current_event.id!r}."
        )
    if option.requires is not None and not _unlock_satisfied(option.requires, state):
        raise ValueError(
            f"Opção {option_id!r} do evento {current_event.id!r} não está disponível "
            f"para o estado atual."
        )

    # 3 — aplicar consequência + 4 — clamp
    new_attrs = state.attributes.apply(option.consequences).clamp()

    # 5 — checagem de gatilho antecipado (principal)
    early = _check_early_ending(new_attrs)

    # 6 — registrar choice
    state = state.with_choice(ChoiceRecord(event_id=current_event.id, option_id=option_id))
    state = state.with_attributes(new_attrs)

    if early.triggered:
        score = compute_score(state, early.ending_id)
        ending = EndingResult(
            ending_id=early.ending_id,
            score=score,
            trigger_name=early.trigger_name,
        )
        return ApplyResult(state=state.finished(early.ending_id, score), ending=ending, secret_event=None)

    # 7 — verificar secreto elegível
    secret_event: Optional[Event] = _find_eligible_secret(state, catalog)
    if secret_event is not None:
        # aplicar secreto (o jogador ainda vai escolher a opção do secreto numa
        # chamada separada; aqui apenas marcamos como "injetado neste passo")
        # NOTA: a opção do secreto chega numa chamada futura a apply_secret_choice.
        # Por enquanto o secreto é retornado para a camada de orquestração,
        # que deve apresentá-lo ao jogador antes de avançar.
        state = state.with_secret_seen(secret_event.id)

    # 8 — avançar day/sequence
    prev_day = state.current_day
    prev_seq = state.current_sequence
    state = state.advance()

    # 9 — verificar se chegou ao fim do dia 5 (sessão encerrada normalmente)
    end_of_week = prev_day == 5 and prev_seq == 3
    if end_of_week:
        ending = resolve_ending_from_registry(state)
        ending = EndingResult(
            ending_id=ending.ending_id,
            score=ending.score,
            trigger_name="",
        )
        return ApplyResult(
            state=state.finished(ending.ending_id, ending.score),
            ending=ending,
            secret_event=secret_event,
        )

    return ApplyResult(state=state, ending=None, secret_event=secret_event)


# ---------------------------------------------------------------------------
# resolve_ending — delegado ao registry (usado externamente se necessário)
# ---------------------------------------------------------------------------

def resolve_ending(state: State) -> EndingResult:
    """Resolve o final ao fim do dia 5 usando o registry de predicados."""
    return resolve_ending_from_registry(state)
