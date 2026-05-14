# Sprint 2.2-B — Correções QA mínimas pré-Sprint 2.3 — Relatório

## 1. Resumo executivo

- **Objetivo:** Endereçar as ressalvas da auditoria read-only da Sprint 2.2 ([`sprint-2.2.md`](sprint-2.2.md)) **sem** implementar feature nova, **sem** alterar engine/rota/repositórios/modelos/schemas, e **sem** inventar aceite humano da Sprint 2.1.
- **Resultado:** **FECHADA tecnicamente**, pendente de aceite humano formal (§10).
- **Veredito da auditoria 2.2 mantido:** APROVADA COM RESSALVAS → ressalvas endereçadas; veredito atualizado para AUDITORIA 2.2 + 2.2-B atendida em §10 abaixo.
- **Decisão recomendada:** aceitar a Sprint 2.2-B em conjunto com a 2.2; em seguida abrir a **Sprint 2.3 — `GET /api/ranking` + smoke tests**.

## 2. Escopo entregue

### 2.1 Cobertura de testes (Backend / Auditor-QA)

Em `backend/tests/test_choices_api.py` foram adicionados **4 testes novos** — uma por ressalva da auditoria — totalizando **107 testes verdes** na suíte.

| # | Teste | Ressalva endereçada |
|---|-------|---------------------|
| 1 | `test_submit_choice_session_not_found_returns_404` | Faltava teste dedicado para `POST /api/sessions/{id}/choices` com sessão inexistente → 404 |
| 2 | `test_submit_choice_persists_decision_row` | Faltava assert explícito de contagem de `Decision` após escolha válida |
| 3 | `test_ranking_count_zero_before_session_finishes` | Faltava teste explícito de `RankingEntry` count == 0 antes do fim |
| 4 | `test_submit_choice_existing_event_but_not_current_returns_409` | Teste de `event_id` errado usava ID inexistente; faltava caso com ID **existente** mas diferente do atual → 409 |

Notas de design dos testes:
- Nenhum mock — usam o `client` (TestClient) + `db` (Session SQLAlchemy) compartilhando o mesmo `engine_test` (StaticPool) já existente em `conftest.py`. Precedente: `test_full_path_early_ending_creates_ranking_and_blocks_new_choices`.
- O teste #4 distingue-se do pré-existente `test_submit_choice_wrong_event_returns_409` (que usa `ev_day2_999`, ID inexistente). Aqui usamos `ev_day1_002`, que **está** no catálogo mas não é o `current_event_id` da sessão recém-criada (`ev_day1_001`) — exercitando o branch de mismatch em `choice_use_cases.py:96-104` com semântica "evento legítimo, mas fora de posição".
- O teste #2 valida que `Decision.day`/`Decision.sequence` correspondem às coordenadas do evento RESPONDIDO (recorded_day/recorded_seq) — coerente com `choice_use_cases.py:116-117`, NÃO com a posição pós-engine.

### 2.2 Documentação (Architect/Documentation)

- [`docs/03-validation/audits/sprint-2.2.md`](sprint-2.2.md):
  - **§4.A** — nova seção explícita "Agent / Rules / Skills" no padrão da [`sprint-2.1.md §4`](sprint-2.1.md), com frase obrigatória **"Skills formais não utilizadas nesta sprint"**, lista de Rules consultadas, evidências verificáveis (`rg` greps de governança), e lista de arquivos proibidos não tocados.
  - **§5.A** — bloco "Testes adicionais — Sprint 2.2-B" detalhando os 4 testes novos.
  - **§6.2** — bloco de evidências pós-2.2-B (107/107 pytest + audit verde).
  - **§7.2 expandida** — playbook operacional de reset SQLite local antes de testes manuais pós-2.2 (limitação `Base.metadata.create_all()` × coluna nova `secrets_seen_json`).
  - **§7.1** — clarificação de que `apply_secret_choice` é backlog **fora da Sprint 2.3**.
  - **§8** — checklist atualizado com itens das ressalvas; aceite humano permanece **PENDENTE**.
- [`HANDOFF.md`](../../../HANDOFF.md) — nova entrada Sprint 2.2-B (sessão 10) + harmonização da linha 13: status da Sprint 2.1 alinhado ao que `sprint-2.1.md §11` afirma de fato (aceite humano pendente). **Sem inventar aceite humano** — se o relatório oficial diz pendente, fica pendente.
- [`PROJECT_STATUS.md`](../../../PROJECT_STATUS.md) — total de testes atualizado para 107; referência à 2.2-B; próximo passo continua sendo Sprint 2.3.
- [`docs/03-validation/sprint-history.md`](../sprint-history.md) — linha nova para Sprint 2.2-B.

## 3. Fora de escopo (não implementado)

Tudo o que o enunciado da 2.2-B explicitou como proibido foi respeitado integralmente:

- **Não** alterado: `frontend/**`, `backend/engine/**`, `backend/engine/data/events.json`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/game-rules.md`, `docs/02-product/architecture.md`, `docs/01-governance/decisions.md`.
- **Não** alterado: nenhum arquivo de produção do backend (routers, schemas, use_cases, repositories, models, app.py, pyproject.toml). Apenas `tests/test_choices_api.py` + documentação.
- **Não** implementado: `GET /api/ranking`, `POST /restart`, `continue`, `apply_secret_choice`, frontend jogável, nova lógica da engine, migração Alembic.

## 4. Agent / Rules / Skills

- **Agent usado:** Backend (testes) + Documentation (relatório, HANDOFF, sprint-history, PROJECT_STATUS). Cross-domain pré-autorizado pelo enunciado da Sprint 2.2-B.
- **Rules consultadas:**
  - [`.cursor/rules/_dispatcher.mdc`](../../../.cursor/rules/_dispatcher.mdc) — checkpoint inicial obrigatório (Agent / Sprint / arquivos lidos / alterados / proibidos / riscos / plano / DoD), respeito a domínios.
  - [`.cursor/rules/backend.mdc`](../../../.cursor/rules/backend.mdc) — proibição de regra de jogo em routers/repositories/models; engine consumida apenas via API pública.
  - [`.cursor/rules/tests.mdc`](../../../.cursor/rules/tests.mdc) — Auditor/QA: testes em `**/tests/**` sem alterar código de produção (correções mínimas combinadas caso a caso, conforme política).
  - [`.cursor/rules/docs-sync.mdc`](../../../.cursor/rules/docs-sync.mdc) — sincronia entre HANDOFF, relatórios, sprint-history e PROJECT_STATUS após qualquer entrega.
- **Skills formais do Cursor:** **Skills formais não utilizadas nesta sprint** (frase obrigatória do padrão 2.1). Governança real = Agent + Rules + Docs + HANDOFF + `audit.ps1`.
- **Como Agent/Rules ajudaram (verificável):**
  - O dispatcher impôs o checkpoint inicial declarando todos os arquivos proibidos antes de qualquer edição — nenhum arquivo proibido foi tocado.
  - `backend.mdc` reforça que a Sprint 2.2-B não pode "consertar" via mudança em routers/use_cases (essas camadas estão intactas; a correção é puramente test+docs).
  - `tests.mdc` autoriza expansão de cobertura em `tests/` sem violar o domínio do Backend.
  - `docs-sync.mdc` justifica a obrigatoriedade de tocar HANDOFF + sprint-history + PROJECT_STATUS em conjunto, evitando dossier dessincronizado.
- **Arquivos proibidos não tocados:** `frontend/**`, `backend/engine/**`, `backend/engine/data/events.json`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/game-rules.md`, `docs/02-product/architecture.md`, `docs/01-governance/decisions.md`, todos os arquivos de produção do backend (`backend/app.py`, `backend/routers/**`, `backend/schemas/**`, `backend/use_cases/**`, `backend/repositories/**`, `backend/models/**`, `backend/db/**`, `backend/core/**`, `backend/pyproject.toml`).

## 5. Evidências técnicas

### 5.1 pytest

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/ engine/tests/ -v
```

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.3, pluggy-1.6.0
collected 107 items

tests/test_attributes_repository.py ....                                 [  3%]
tests/test_catalog_loader.py ......                                      [  9%]
tests/test_choices_api.py .........                                      [ 17%]
tests/test_cors.py ..                                                    [ 19%]
tests/test_db_setup.py ...                                               [ 21%]
tests/test_decision_repository.py ...                                    [ 24%]
tests/test_error_handlers.py ....                                        [ 28%]
tests/test_health.py .                                                   [ 29%]
tests/test_player_repository.py ....                                     [ 33%]
tests/test_players_api.py .......                                        [ 39%]
tests/test_ranking_repository.py ...                                     [ 42%]
tests/test_schemas.py .......                                            [ 49%]
tests/test_session_repository.py ....                                    [ 53%]
tests/test_sessions_api.py .......                                       [ 60%]
engine/tests/test_apply_choice.py ...................                    [ 78%]
engine/tests/test_validate.py ........................                   [100%]

============================= 107 passed in 1.50s =============================
```

Exit code: **0**. **107/107** = 103 (entrega 2.2) + **4** novos da 2.2-B (item 2.1 acima). Zero regressões.

Os 4 testes novos aparecem no bloco `tests/test_choices_api.py` — 9 dots no total (5 originais + 4 novos):
- `test_submit_choice_session_not_found_returns_404` PASSED
- `test_submit_choice_persists_decision_row` PASSED
- `test_ranking_count_zero_before_session_finishes` PASSED
- `test_submit_choice_existing_event_but_not_current_returns_409` PASSED

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

### 5.3 Greps de governança (verificações)

- `rg "apply_choice" backend/routers` → vazio (router fino — `use_cases` apenas).
- `rg "from engine|import engine" backend/db backend/models backend/repositories` → vazio (zero acoplamento engine↔persistência).
- `rg -i "fastapi|sqlalchemy|pydantic" backend/engine/*.py` → apenas docstrings da engine (engine permanece pura).
- `git diff --stat` (esperado): apenas `backend/tests/test_choices_api.py` + documentação (`docs/03-validation/audits/sprint-2.2.md`, este arquivo, `docs/03-validation/sprint-history.md`, `HANDOFF.md`, `PROJECT_STATUS.md`).

## 6. Decisões registradas

### 6.1 Harmonização do HANDOFF sobre aceite da Sprint 2.1

A linha 13 anterior do `HANDOFF.md` afirmava `"Sprint 2.1: aceite técnico humano ✅ (conforme validação solicitada antes do papel §10)"`. O relatório oficial [`sprint-2.1.md §11`](sprint-2.1.md) diz textualmente `"Aceite humano: PENDENTE"`. O enunciado da 2.2-B é explícito: **"Não inventar aceite humano. Se o relatório oficial diz pendente, manter pendente."**

Decisão: HANDOFF foi alinhado para refletir aceite humano da 2.1 como **pendente §10 papel**, mantendo a linha do tempo do projeto sem afirmar aceite que não foi formalizado.

### 6.2 Não criação de ADR

Nenhuma decisão arquitetural nova. A clarificação operacional sobre reset SQLite local (`sprint-2.2.md §7.2`) é caso de **uso** da ADR-006 existente — não decisão arquitetural. Nenhuma alteração em `docs/01-governance/decisions.md`.

### 6.3 Não criação de Alembic / migração estrutural

Fora do escopo da 2.2-B (proibido). Continua valendo ADR-006 + playbook documentado (`sprint-2.2.md §7.2`).

## 7. Limitações conhecidas (carregadas da 2.2)

Permanecem inalteradas em relação à 2.2:

- **`apply_secret_choice`** continua não exposto pela engine — backlog explícito **fora da Sprint 2.3**.
- **Reset SQLite local** continua necessário em dev se houver `.db` pré-2.2 (playbook em `sprint-2.2.md §7.2`).
- **GET ranking** continua planejado para Sprint 2.3.
- **Sem auth / sem rate limiting** (intencional para UX local).

## 8. Validação documental

Arquivos sincronizados nesta sprint (todos no domínio Architect/Documentation, autorizado pelo escopo cross-domain da 2.2-B):

- [`docs/03-validation/audits/sprint-2.2.md`](sprint-2.2.md) — atualizado conforme §2.2 acima.
- [`HANDOFF.md`](../../../HANDOFF.md) — nova entrada sessão 10 + harmonização linha 13.
- [`PROJECT_STATUS.md`](../../../PROJECT_STATUS.md) — total de testes, referência 2.2-B.
- [`docs/03-validation/sprint-history.md`](../sprint-history.md) — linha 2.2-B.

Não tocados (proibidos):
- [`docs/02-product/api.md`](../../02-product/api.md) — sem mudança de contrato.
- [`docs/02-product/game-rules.md`](../../02-product/game-rules.md) — sem mudança de regra.
- [`docs/02-product/architecture.md`](../../02-product/architecture.md) — sem mudança de arquitetura.
- [`docs/01-governance/decisions.md`](../../01-governance/decisions.md) — sem ADR nova.
- [`docs/00-start/sprint-plan.md`](../../00-start/sprint-plan.md) — Sprint 2.2 já estava lá; 2.2-B é correção QA inline (não exige novo bloco no plano).
- [`docs/00-start/setup-company-env.md`](../../00-start/setup-company-env.md) — playbook de reset SQLite ficou no relatório `sprint-2.2.md §7.2` (mais próximo do contexto técnico) em vez de poluir o setup. Caso a Sprint 2.3 introduza outra mudança de schema, considerar promover para `setup-company-env.md`.

## 9. Critério de aceite aplicado

- [x] Agent declarado (Backend + Documentation) com checkpoint inicial respondendo: Agent ativo, Sprint, arquivos lidos/alterados/proibidos, riscos, plano, DoD.
- [x] Sprint declarada (2.2-B) e cross-domain (Backend+Documentation) explicitamente declarado/autorizado pelo enunciado.
- [x] Ressalva QA #1: 404 para POST /choices em sessão inexistente — coberta (`test_submit_choice_session_not_found_returns_404`).
- [x] Ressalva QA #2: count de `Decision` após escolha válida — coberta (`test_submit_choice_persists_decision_row`).
- [x] Ressalva QA #3: `RankingEntry` count == 0 antes do fim — coberta (`test_ranking_count_zero_before_session_finishes`).
- [x] Ressalva QA #4: `event_id` existente mas diferente do atual → 409 — coberta (`test_submit_choice_existing_event_but_not_current_returns_409`).
- [x] Ressalva #5: seção Agent/Rules/Skills em `sprint-2.2.md` — adicionada (§4.A).
- [x] Ressalva #6: limitação operacional `secrets_seen_json` × `create_all()` documentada como playbook — `sprint-2.2.md §7.2`.
- [x] Ressalva #7: `apply_secret_choice` continua pendente, agora explicitamente fora da Sprint 2.3 — `sprint-2.2.md §7.1`.
- [x] Ressalva #8: HANDOFF harmonizado sobre aceite da 2.1, sem inventar aceite humano.
- [x] 107/107 pytest verdes (103 + 4 novos).
- [x] `audit.ps1` exit 0.
- [x] Engine, frontend, events.json, rules, scripts, ADRs, game-rules, architecture: zero alterações.
- [x] Backend de produção: zero alterações (apenas testes + documentação).
- [x] Skills formais não declaradas falsamente — frase obrigatória registrada em §4.

## 10. Decisão de aceite humano

- Aceite humano: **PENDENTE**.
- Observações esperadas no aceite:
  - 4 ressalvas técnicas QA endereçadas via testes em `tests/test_choices_api.py` — 107/107 pytest verdes.
  - 4 ressalvas documentais endereçadas em `sprint-2.2.md` (§4.A, §5.A, §6.2, §7) e na harmonização do HANDOFF/PROJECT_STATUS/sprint-history.
  - Nenhum arquivo de código de produção tocado.
  - `audit.ps1` continua exit 0.
- Próximas etapas pós-aceite 2.2-B:
  1. **Sprint 2.3** — `GET /api/ranking` + smoke tests (Backend).
  2. Em paralelo: **Architect/Documentation** atualizar [`docs/00-start/executive-overview.md`](../../00-start/executive-overview.md) cobrindo Sprints 2.0/2.1/2.2/2.2-B (consolidando pendência 2.0-A/2.1-A).
  3. Em momento oportuno: aceite humano formal (papel) das Sprints 2.1, 2.2 e 2.2-B em conjunto.
