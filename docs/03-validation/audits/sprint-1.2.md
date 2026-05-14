# Sprint 1.2 — Catálogo completo dos 15 + 2 eventos — Relatório de aceite

## 1. Resumo executivo

- Objetivo da sprint: substituir o `events.json` placeholder (Sprint 1.1) pelo catálogo narrativo real com 15 eventos principais (5 dias × 3) e 2 eventos secretos; executar checklist de balanceamento (§10); documentar 3 playthroughs.
- Resultado: **FECHADA tecnicamente**, pendente de aceite humano formal.
- Decisão recomendada: aceitar a Sprint 1.2 após revisão; em seguida abrir a Sprint **2 — Robustez API** com Agent Backend ou outro agente conforme `sprint-plan.md`.

---

## 2. Escopo executado

- **`backend/engine/data/events.json`** — conteúdo narrativo real: 15 eventos principais + 2 secretos, todos com cenas em português, opções com labels não-vazios, consequências reais e condições de desbloqueio/requisito.
- **`docs/02-product/game-rules.md`** — ajuste de 2 deltas que excediam a invariante 7 (soma ≤ 7):
  - `ev_day5_001 A`: produtividade +2, ansiedade +2 → +1, +1 (soma 9 → 7)
  - `ev_day5_003 A`: energia -3 → -2 (soma 8 → 7)
- **`docs/03-validation/playthroughs/run_optimista.md`** — 15 eventos + 2 secretos; final `trainee_lenda`; score 551.
- **`docs/03-validation/playthroughs/run_demitido.md`** — final antecipado `demitido` em ev_day3_001 C; score 49.
- **`docs/03-validation/playthroughs/run_medio.md`** — 15 eventos; final `sobrevivente`; score 280.
- **`docs/03-validation/audits/sprint-1.2.md`** (este arquivo).
- **`docs/03-validation/sprint-history.md`**, **`PROJECT_STATUS.md`**, **`HANDOFF.md`**.

---

## 3. Fora de escopo

- API HTTP (`backend/app.py` não tocado — healthcheck preservado).
- Persistência SQLite, SQLAlchemy, routers, schemas Pydantic de API.
- Frontend (nenhum arquivo em `frontend/` tocado).
- Ranking, sessões persistidas, score persistido.
- `apply_secret_choice` (integração backend/engine — sprint futura).
- Rules `.cursor/rules/` e `scripts/` (não tocados).
- Skills formais do Cursor.

---

## 4. Agent / Rules / Skills

- **Agent usado:** Engine/Content.
- **Rules consultadas:** `.cursor/rules/_dispatcher.mdc`, `.cursor/rules/game-engine.mdc`, `.cursor/rules/events-json.mdc`.
- **Skills formais do Cursor:** **Skills formais não utilizadas nesta sprint**.
- **Como Agent/Rules ajudaram:**
  - `game-engine.mdc` proíbe import de FastAPI/SQLAlchemy/frontend na engine — sem violações.
  - `events-json.mdc` exigiu respeito a todas as invariantes de `game-rules.md` — catálogo passou `validate_events()`.
  - `_dispatcher.mdc` exigiu checkpoint inicial com escopo, proibidos e riscos declarados.
  - Domínio respeitado: `backend/app.py`, `frontend/`, `.cursor/rules/`, `scripts/` não foram tocados.

---

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

============================= 44 passed in 0.60s ==============================
```

Exit code: **0** — 44/44 — regressão zero.

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

### 5.3 Arquivos alterados/criados

| Arquivo | Ação | Responsabilidade |
|---------|------|------------------|
| `backend/engine/data/events.json` | Alterado | Catálogo narrativo real (15 + 2 eventos) |
| `docs/02-product/game-rules.md` | Alterado | Ajuste de 2 deltas (balanceamento §10) |
| `docs/03-validation/playthroughs/run_optimista.md` | Criado | Playthrough trainee_lenda (score 551) |
| `docs/03-validation/playthroughs/run_demitido.md` | Criado | Playthrough demitido antecipado (score 49) |
| `docs/03-validation/playthroughs/run_medio.md` | Criado | Playthrough sobrevivente (score 280) |
| `docs/03-validation/audits/sprint-1.2.md` | Criado | Este relatório |
| `docs/03-validation/sprint-history.md` | Alterado | Linha da Sprint 1.2 |
| `PROJECT_STATUS.md` | Alterado | Sprint atual e próximo passo |
| `HANDOFF.md` | Alterado | Entrada desta sessão |

---

## 6. Checklist de balanceamento (game-rules.md §10)

- [x] **Final `trainee_lenda` alcançável:** confirmado em `run_optimista.md` (15 eventos + 2 secretos).
- [x] **Final `demitido` alcançável:** confirmado em `run_demitido.md` (final antecipado no ev_day3_001).
- [x] **Final `sobrevivente` alcançável:** confirmado em `run_medio.md` (15 eventos, sem predicate positivo).
- [x] **Nenhuma opção dominante:** cada opção penaliza pelo menos um atributo ou tem custo de oportunidade.
- [x] **Soma absoluta dos deltas ≤ 7:** validado por `validate_events()` e confirmado evento a evento.
- [x] **Variedade por dia:** dias 1–5 tocam atributos diferentes (tabela §7 de `game-rules.md`).
- [x] **Secretos não-óbvios:** `ev_secret_001` requer rep≥7 e net≥5 a partir do dia 3 (atingível apenas em run específico); `ev_secret_002` requer ansiedade≥7 (estado de pressão acumulada, não trivial).
- [ ] **Finais `burnout`, `risco_op`, `invisivel`, `promessa` não foram playthroughados** — alcançáveis dado o espaço de estados, mas playthroughs completos ficam para sprint futura (Sprint 4 de qualidade narrativa).

> Nota de balanceamento: `trainee_lenda` exige cuidado extremo com energia em Day 3–4 e requer desbloqueio de `ev_secret_001` para compensar a perda de reputação em ev_day5_001 C. Não é trivial — design intencional.

---

## 7. Ajustes de balanceamento documentados

Dois deltas do spec original (`game-rules.md §5`) excediam o limite de soma ≤ 7:

| Evento | Opção | Original | Ajustado | Justificativa |
|--------|-------|----------|----------|---------------|
| ev_day5_001 | A | pro+2, ans+2 (soma 9) | pro+1, ans+1 (soma 7) | Invariante 7; narrativa mantida: preparação traz visibilidade mas cansa |
| ev_day5_003 | A | ene-3 (soma 8) | ene-2 (soma 7) | Invariante 7; narrativa mantida: horas extras drenam energia mas entregam resultado |

Alterações registradas em `game-rules.md §5` com nota inline.

---

## 8. Critério de aceite aplicado

- [x] Agent declarado (Engine/Content) com checkpoint no início.
- [x] Sprint declarada (1.2) e escopo delimitado.
- [x] `backend/engine/data/events.json` substituído com 15 + 2 eventos narrativos; deltas reais; condições de unlock; opções com 2–4 por evento.
- [x] `schemaVersion: "1.0"` mantido.
- [x] 5 dias × 3 eventos = 15 principais; sequences {1,2,3} por dia.
- [x] 2 secretos com `isMain: false`, `day: null`, `unlock` com condição real.
- [x] Opções D condicionais (ev_day3_002, ev_day5_003) com `requires.min_attrs` corretos.
- [x] Soma absoluta dos deltas ≤ 7 em todas as opções.
- [x] Tom corporativo brasileiro realista; sem estereótipos; sem opção claramente dominante.
- [x] `validate_events()` passou (test_placeholder_passes_validation).
- [x] pytest 44/44 — regressão zero.
- [x] `audit.ps1` passou — exit code 0.
- [x] 3 playthroughs criados com estados finais e scores verificados.
- [x] `game-rules.md` atualizado com os ajustes de balanceamento.
- [x] `backend/app.py`, `frontend/**`, `.cursor/rules/`, `scripts/` — não tocados.
- [x] Skills formais não declaradas falsamente.

---

## 9. Pendências

- Aceite humano desta sprint (campo na §10).
- Playthroughs para os demais 4 finais (`burnout`, `risco_op`, `invisivel`, `promessa`) — Sprint 4 (qualidade narrativa).
- Integração backend/engine (routers, use cases, SQLite, sessões, ranking) — Sprint 2/3.
- Frontend de jogo — Sprint 3 (UX completa).

---

## 10. Decisão de aceite humano

- Aceite humano: *(preencher após revisão)*
- Observações do aceite:
