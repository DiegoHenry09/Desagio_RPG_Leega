"""
Montagem da `engine.State` a partir das linhas ORM persistidas — Sprint 2.2.

A engine trabalha apenas com valores puros (`State`, `Attributes`,
`ChoiceRecord`). Este módulo **não decide** jogada; apenas copia campo a
campo das tabelas `game_sessions`, `session_attributes` e histórico
`decisions` + `secrets_seen_json` (JSON array de IDs dos secretos que a
engine marcou como vistos — não geram Decision).
"""

from __future__ import annotations

import json

from engine import Attributes, ChoiceRecord, State
from models.decision import Decision
from models.game_session import SESSION_STATUS_FINISHED, GameSession
from models.session_attributes import SessionAttributes


def hydrate_engine_state(
    session_row: GameSession,
    attrs_row: SessionAttributes,
    *,
    ordered_decisions: list[Decision],
) -> State:
    """Reidratação fiel ao contrato SQLAlchemy → engine.State.

    `ordered_decisions` deve estar ordenado cronologicamente (id ASC —
    garantido pelo repositório `list_by_session`).
    """
    try:
        raw = json.loads(session_row.secrets_seen_json or "[]")
        if isinstance(raw, list):
            secrets_seen = tuple(str(x) for x in raw)
        else:
            secrets_seen = ()
    except json.JSONDecodeError:
        secrets_seen = ()

    choices_log = tuple(
        ChoiceRecord(event_id=d.event_id, option_id=d.option_id)
        for d in ordered_decisions
    )

    attrs_engine = Attributes(
        energia=attrs_row.energia,
        reputacao=attrs_row.reputacao,
        networking=attrs_row.networking,
        ansiedade=attrs_row.ansiedade,
        produtividade=attrs_row.produtividade,
        aprendizado=attrs_row.aprendizado,
    )

    finished = session_row.status == SESSION_STATUS_FINISHED

    return State(
        current_day=session_row.current_day,
        current_sequence=session_row.current_sequence,
        attributes=attrs_engine,
        choices_log=choices_log,
        secret_ids_seen=secrets_seen,
        is_finished=finished,
        ending_id=session_row.ending_id,
        score=session_row.score,
    )
