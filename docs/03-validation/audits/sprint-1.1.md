# Sprint 1.1 — Engine skeleton + schema `events.json` — Relatório de aceite

## 1. Resumo executivo

- Objetivo da sprint: criar a game engine em Python puro (`backend/engine/`) com tipos imutáveis, `validate_events()`, `apply_choice()`, `resolve_ending()`, `compute_score()`, `events.json` placeholder validável e testes unitários iniciais.
- Resultado: **FECHADA tecnicamente**, pendente de aceite humano formal.
- Decisão recomendada: aceitar a Sprint 1.1 após revisão; em seguida abrir a Sprint **1.2 — Catálogo completo dos 15 + 2 eventos** com Agent Engine/Content.

## 2. Escopo aprovado

- **`backend/engine/__init__.py`** — API pública exportada (consumida pelo backend via `from engine import ...`).
- **`backend/engine/types.py`** — dataclasses frozen: `Attributes`, `Consequences`, `UnlockCondition`, `Option`, `Event`, `Catalog`, `ChoiceRecord`, `State`, `EarlyTrigger`, `EndingResult`.
- **`backend/engine/endings.py`** — decorator `@register_ending`, registry dos 7 predicados de fim de semana, `compute_score()`, `EARLY_TRIGGER_ENDINGS` (mapeamento gatilho→final, ADR-010).
- **`backend/engine/engine.py`** — `validate_events()` (invariantes 1–11 de `game-rules.md` §4.3), `_check_early_ending()` (ADR-010 ordem de prioridade), `_find_eligible_secret()`, `apply_choice()`, `resolve_ending()`.
- **`backend/engine/data/events.json`** — placeholder mínimo com `schemaVersion: "1.0"`, 15 principais (5 dias × 3) e 2 secretos; deltas zerados; conteúdo narrativo real será adicionado na Sprint 1.2.
- **`backend/engine/tests/__init__.py`**, **`backend/engine/tests/test_validate.py`**, **`backend/engine/tests/test_apply_choice.py`** — 43 testes unitários iniciais cobrindo os 11 invariantes, os 3 gatilhos antecipados e a prioridade deles.

## 3. Fora de escopo

- API HTTP (`backend/app.py` não tocado — healthcheck preservado).
- Persistência SQLite, SQLAlchemy, routers, schemas Pydantic de API.
- Frontend (nenhum arquivo em `frontend/` tocado).
- Conteúdo narrativo real dos 15 + 2 eventos (Sprint 1.2).
- Ranking, sessões persistidas, score persistido.
- Rules `.cursor/rules/` e `scripts/` (não tocados).
- Skills formais do Cursor.

## 4. Agent / Rules / Skills

- **Agent usado:** Engine/Content.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](../../../.cursor/rules/_dispatcher.mdc), [`.cursor/rules/game-engine.mdc`](../../../.cursor/rules/game-engine.mdc).
- **Skills formais do Cursor:** **Skills formais não utilizadas nesta sprint**.
- **Como Agent/Rules ajudaram:**
  - `game-engine.mdc` proíbe import de FastAPI/SQLAlchemy/frontend na engine — verificado: nenhum desses imports existe nos módulos `engine/`.
  - `_dispatcher.mdc` exigiu checkpoint inicial (agent, sprint, arquivos, proibidos) antes de tocar código.
  - Domínio respeitado: `backend/app.py` e `backend/tests/test_health.py` não foram tocados.
  - API pública isolada em `backend/engine/__init__.py` — backend poderá consumir via `from engine import ...` quando implementado.

## 5. Evidências técnicas

### 5.1 pytest — todos os testes

Comando executado em **2026-05-14**, em `backend/`, com venv ativado:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ engine/tests/ -v
```

Saída:

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.3, pluggy-1.6.0
collected 44 items

tests/test_health.py::test_health_returns_ok PASSED                      [  2%]
engine/tests/test_apply_choice.py::TestEarlyEndingReputacao::test_reputacao_zero_triggers_demitido PASSED
engine/tests/test_apply_choice.py::TestEarlyEndingReputacao::test_reputacao_one_does_not_trigger PASSED
engine/tests/test_apply_choice.py::TestEarlyEndingReputacao::test_reputacao_already_zero_triggers PASSED
engine/tests/test_apply_choice.py::TestEarlyEndingEnergia::test_energia_zero_triggers_burnout PASSED
engine/tests/test_apply_choice.py::TestEarlyEndingEnergia::test_energia_one_does_not_trigger PASSED
engine/tests/test_apply_choice.py::TestEarlyEndingAnsiedade::test_ansiedade_max_triggers_burnout PASSED
engine/tests/test_apply_choice.py::TestEarlyEndingAnsiedade::test_ansiedade_nine_does_not_trigger PASSED
engine/tests/test_apply_choice.py::TestEarlyEndingAnsiedade::test_ansiedade_already_at_ten_triggers PASSED
engine/tests/test_apply_choice.py::TestEarlyEndingPriority::test_reputacao_beats_energia PASSED
engine/tests/test_apply_choice.py::TestEarlyEndingPriority::test_reputacao_beats_ansiedade PASSED
engine/tests/test_apply_choice.py::TestEarlyEndingPriority::test_energia_beats_ansiedade PASSED
engine/tests/test_apply_choice.py::TestEndOfWeek::test_last_choice_resolves_ending PASSED
engine/tests/test_apply_choice.py::TestEndOfWeek::test_game_continues_until_day5_seq3 PASSED
engine/tests/test_apply_choice.py::TestProgression::test_sequence_advances PASSED
engine/tests/test_apply_choice.py::TestProgression::test_day_advances_after_seq3 PASSED
engine/tests/test_apply_choice.py::TestClamp::test_attribute_clamped_to_zero PASSED
engine/tests/test_apply_choice.py::TestClamp::test_attribute_clamped_to_ten PASSED
engine/tests/test_apply_choice.py::TestClamp::test_ansiedade_clamped_to_ten PASSED
engine/tests/test_apply_choice.py::TestInvalidOption::test_nonexistent_option_raises PASSED
engine/tests/test_validate.py::TestSchemaVersion::test_valid_version PASSED
engine/tests/test_validate.py::TestSchemaVersion::test_wrong_version PASSED
engine/tests/test_validate.py::TestSchemaVersion::test_missing_version PASSED
engine/tests/test_validate.py::TestMainEventsCount::test_missing_one_event_in_day PASSED
engine/tests/test_validate.py::TestMainEventsCount::test_extra_event_in_day PASSED
engine/tests/test_validate.py::TestSequences::test_duplicate_sequence PASSED
engine/tests/test_validate.py::TestSecrets::test_valid_secret PASSED
engine/tests/test_validate.py::TestSecrets::test_secret_with_day_not_null PASSED
engine/tests/test_validate.py::TestSecrets::test_secret_without_unlock PASSED
engine/tests/test_validate.py::TestSecrets::test_secret_with_empty_unlock PASSED
engine/tests/test_validate.py::TestCrossReferences::test_unlocks_nonexistent_id PASSED
engine/tests/test_validate.py::TestCrossReferences::test_blocks_nonexistent_id PASSED
engine/tests/test_validate.py::TestOptions::test_no_options PASSED
engine/tests/test_validate.py::TestOptions::test_five_options PASSED
engine/tests/test_validate.py::TestOptions::test_invalid_option_id PASSED
engine/tests/test_validate.py::TestOptions::test_duplicate_option_id PASSED
engine/tests/test_validate.py::TestDeltaSum::test_delta_sum_exactly_7 PASSED
engine/tests/test_validate.py::TestDeltaSum::test_delta_sum_8_fails PASSED
engine/tests/test_validate.py::TestAttributeNames::test_unknown_attribute PASSED
engine/tests/test_validate.py::TestSelfReference::test_event_unlocks_itself PASSED
engine/tests/test_validate.py::TestLabel::test_empty_label PASSED
engine/tests/test_validate.py::TestLabel::test_whitespace_label PASSED
engine/tests/test_validate.py::TestEarlyEndingIds::test_registry_contains_demitido_and_burnout PASSED
engine/tests/test_validate.py::TestPlaceholderFile::test_placeholder_passes_validation PASSED

============================= 44 passed in 0.58s ==============================
```

Exit code: **0** — 44/44 (43 engine + 1 healthcheck pré-existente).

### 5.2 audit.ps1

```powershell
powershell -ExecutionPolicy Bypass -File scripts/audit.ps1
```

```
== Corporate Survivor - audit.ps1 (governance 0.1-D) ==
OK - governanca minima presente e raiz limpa.
Nota: backend/frontend ainda nao sao exigidos nesta auditoria.
```

Exit code: **0**.

### 5.3 Arquivos criados

| Arquivo | Responsabilidade |
|---|---|
| `backend/engine/__init__.py` | API pública exportada |
| `backend/engine/types.py` | Tipos imutáveis (dataclasses frozen) |
| `backend/engine/endings.py` | Registry endings + compute_score + EARLY_TRIGGER_ENDINGS |
| `backend/engine/engine.py` | validate_events, apply_choice, resolve_ending |
| `backend/engine/data/events.json` | Placeholder validável (Sprint 1.1) |
| `backend/engine/tests/__init__.py` | Pacote de testes |
| `backend/engine/tests/test_validate.py` | 24 testes do validate_events (invariantes 1–11) |
| `backend/engine/tests/test_apply_choice.py` | 19 testes de apply_choice (gatilhos, prioridade, progressão, clamp) |

### 5.4 Testes de prioridade de gatilhos (ADR-010)

Cobertura explícita da ordem `reputacao > energia > ansiedade`:
- `test_reputacao_beats_energia` — `rep=0 AND ene=0` → `demitido` (não `burnout`).
- `test_reputacao_beats_ansiedade` — `rep=0 AND ans=10` → `demitido`.
- `test_energia_beats_ansiedade` — `ene=0 AND ans=10` (sem `rep=0`) → `burnout` via `energy_zero`.

## 6. Limitações conhecidas

- `events.json` é placeholder com deltas zerados — todos os finais no placeholder caem em `sobrevivente` (atributos iniciais inalterados). Conteúdo narrativo real entra na Sprint 1.2.
- `apply_choice` tem esqueleto de secretos: detecta e marca secreto como "injetado" mas a chamada da opção do secreto (`apply_secret_choice`) é delegada a uma função futura. A orquestração completa (backend chama engine, recebe secreto, apresenta ao jogador, chama engine de novo) é implementada quando o Backend/API integrar a engine (sprint futura).
- `compute_score` não está sendo chamado no boot do FastAPI ainda; isso acontece quando o Backend integrar a engine.

## 7. Validação documental

- `game-rules.md` §4.4 e §11 já contemplavam o contrato implementado — sem divergências.
- `decisions.md` ADR-010 foi implementada fielmente (ordem de prioridade, mapeamento ending_id, trigger_name).
- `api.md` — sem alteração; a engine é independente da API.
- `sprint-plan.md` — Sprint 1.1 DoD verificado item a item (§8 abaixo).

## 8. Critério de aceite aplicado

- [x] Agent declarado (Engine/Content) com checkpoint no início.
- [x] Sprint declarada (1.1).
- [x] `backend/engine/` criado, em conformidade com `game-engine.mdc` (nenhum import de FastAPI/SQLAlchemy/frontend/Pydantic de API).
- [x] Tipos imutáveis (frozen dataclasses) para `State`, `Attributes`, `Event`, `Option`, `Consequences`, `EarlyTrigger`, `EndingResult`, `Catalog`.
- [x] `validate_events()` cobre invariantes 1–11 de `game-rules.md` §4.3.
- [x] `backend/engine/data/events.json` mínimo validável (15 principais + 2 secretos, `schemaVersion: "1.0"`).
- [x] `apply_choice()` com clamp + checagem de gatilho antecipado na ordem ADR-010.
- [x] 43 testes unitários: validador (catálogo válido/inválido) e 3 gatilhos antecipados (incluindo prioridade `reputacao > energia > ansiedade`).
- [x] `audit.ps1` passou (exit code 0).
- [x] `test_health` pré-existente continua passando — regressão zero.
- [x] Skills formais não declaradas falsamente (frase obrigatória registrada em §4).
- [x] `backend/app.py`, `backend/tests/`, `frontend/**`, `.cursor/rules/`, `scripts/` — não tocados.

## 9. Pendências

- Aceite humano desta sprint (campo na §10).
- `apply_secret_choice` (chamada da opção de secreto) — será implementada junto com a integração backend/engine (sprint de API ou sprint dedicada).
- Sprint 1.2 — catálogo completo dos 15 + 2 eventos com conteúdo narrativo real.
- Balanceamento (checklist `game-rules.md` §10) e playthroughs em `docs/03-validation/playthroughs/` (Sprint 4).

## 10. Decisão de aceite humano

- Aceite humano: **ACEITO — 2026-05-14**.
- Observações do aceite:
  - 44/44 testes pytest passaram (43 engine + 1 healthcheck pré-existente).
  - `audit.ps1` passou — exit code 0.
  - Engine não importa FastAPI, SQLAlchemy ou frontend — verificado.
  - `events.json` é placeholder validável (15 principais + 2 secretos, `schemaVersion: "1.0"`).
  - Conteúdo narrativo real dos eventos fica para Sprint 1.2 — aceito.
  - Próxima etapa autorizada: **Sprint 1.2 — Catálogo completo dos 15 + 2 eventos**.
