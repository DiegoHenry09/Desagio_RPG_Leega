# Sprint 2.3 — Ranking API + smoke tests — Relatório de aceite

## 1. Resumo executivo

- **Objetivo da sprint:** expor o leaderboard global via `GET /api/ranking`, com envelope `{items, limit, count}` ordenado por score desc + tie-break determinístico, sem implementar frontend, restart, continue, `apply_secret_choice` ou nova lógica de jogo. Apenas **leitura** sobre `RankingEntry` (já persistido desde a Sprint 2.2).
- **Resultado:** **FECHADA tecnicamente**, pendente de aceite humano formal (§10).
- **Decisão recomendada:** aceitar a Sprint 2.3 e seguir para o backlog operacional (aceites burocráticos pendentes 2.1/2.2/2.2-B; dossiê executivo 2.x; `apply_secret_choice` em sprint futura de engine/UX).

## 2. Escopo entregue

### 2.1 Schema (`backend/schemas/ranking.py`)

- `RankingEntryResponse` — Pydantic v2 (`from_attributes=True`); expõe **`id`, `player_name`, `score`, `ending_id`, `created_at`**. **NÃO** expõe `session_id` (FK interna).
- `RankingListResponse` — envelope `{items: list[RankingEntryResponse], limit: int, count: int}`. Sem cursor/offset (escopo).

### 2.2 Use case (`backend/use_cases/ranking_use_cases.py`)

- `list_top_ranking(db, *, limit) -> list[RankingEntry]` — camada FINA que delega ao `ranking_repository.top_n` da Sprint 2.0. **Não** calcula score, **não** recalcula ordenação, **não** importa `engine`. Bounds de `limit` são responsabilidade da camada de transporte.

### 2.3 Router (`backend/routers/ranking.py`)

- `GET /api/ranking?limit=10` — `limit` validado por `Query(default=10, ge=1, le=100)`. Default 10. Limite máximo 100 (evita resposta absurdamente grande, valor razoável para ranking público).
- Router **fino**: depende de `get_db`, delega ao use case, serializa via `RankingEntryResponse.model_validate(row)`. Zero regra de jogo.

### 2.4 Wire-up

- `backend/routers/__init__.py` — adiciona `ranking` ao reexport.
- `backend/schemas/__init__.py` — adiciona `RankingEntryResponse`, `RankingListResponse`.
- `backend/use_cases/__init__.py` — adiciona `ranking_use_cases`.
- `backend/app.py` — `app.include_router(ranking_router)` ao lado dos `players_router`/`sessions_router`. CORS, lifespan, error handlers e demais routers permanecem **intactos**.

### 2.5 Testes (`backend/tests/test_ranking_api.py`)

**9 novos testes** cobrindo todos os critérios técnicos da DoD:

| # | Teste | Cobertura |
|---|-------|-----------|
| 1 | `test_ranking_empty_returns_200_with_empty_envelope` | Ranking vazio devolve `{items:[], limit:10, count:0}` (200) |
| 2 | `test_ranking_orders_by_score_desc` | 3 entradas → ordem `551, 280, 100` |
| 3 | `test_ranking_default_limit_is_ten` | 12 entradas → `limit=10`, top 10 retornadas |
| 4 | `test_ranking_respects_custom_limit` | `?limit=2` → apenas 2 itens, top 2 |
| 5 | `test_ranking_response_omits_session_id_field` | Keys do item == `{id, player_name, score, ending_id, created_at}` |
| 6 | `test_ranking_limit_zero_returns_422` | `?limit=0` → 422 com `error.code="validation_error"` |
| 7 | `test_ranking_limit_above_max_returns_422` | `?limit=101` → 422 |
| 8 | `test_ranking_limit_non_integer_returns_422` | `?limit=abc` → 422 |
| 9 | `test_ranking_smoke_end_to_end_finished_session_appears` | Smoke: criar player → sessão → jogar `_GREEDY_PATH_TO_DEMITIDO` → `GET /api/ranking` mostra entrada com `score=49`, `ending_id="demitido"`, `player_name="SmokeRunner"` |

Total atualizado: **116 testes** (`backend/tests/` + `engine/tests/`) = 107 (após Sprint 2.2-B) + 9 (Sprint 2.3).

## 3. Fora de escopo (não implementado — proibido pelo enunciado)

- Frontend / UI de leaderboard.
- `POST /api/sessions/{id}/restart` ou `continue`.
- `apply_secret_choice` (engine + endpoint secreto) — backlog de engine/UX.
- Nova regra de jogo, mutação de score, recálculo de ranking.
- Paginação cursor/offset, filtros (por `ending_id`/`player_name`), ordenação alternativa.
- Alteração de CORS, engine, `events.json`, `events`-related rules.
- Sprint 3 (UX completa) — fora do escopo.
- Migração Alembic — continua valendo ADR-006.

## 4. Agent / Rules / Skills

- **Agent usado:** Backend (entrega completa: schema + use case + router + wire-up + testes + docs).
- **Rules consultadas:**
  - [`.cursor/rules/_dispatcher.mdc`](../../../.cursor/rules/_dispatcher.mdc) — protocolo de checkpoint inicial obrigatório (Agent / Sprint / arquivos lidos / alterados / proibidos / riscos / plano / DoD).
  - [`.cursor/rules/backend.mdc`](../../../.cursor/rules/backend.mdc) — proibição de regra de jogo em routers/repositories/models; engine consumida apenas via API pública. Nesta sprint a engine **não foi consumida** (endpoint é leitura pura sobre persistência).
  - [`.cursor/rules/docs-sync.mdc`](../../../.cursor/rules/docs-sync.mdc) — sincronia entre `api.md`, HANDOFF, sprint-history e PROJECT_STATUS.
  - [`.cursor/rules/tests.mdc`](../../../.cursor/rules/tests.mdc) — Auditor/QA: cobertura das condições críticas (vazio, ordenação, bounds, leak de session_id, smoke fim-a-fim).
- **Skills formais do Cursor:** **Skills formais não utilizadas nesta sprint** (frase obrigatória do padrão 2.1). Governança real continua sendo Agent + Rules + Docs + HANDOFF + `audit.ps1`.
- **Como Agent/Rules ajudaram (verificável):**
  - Router permanece fino — `apply_choice`, `compute_score`, `resolve_ending`, `clamp` não aparecem em nenhum router/use_case desta sprint. Verificável: `rg "compute_score|apply_choice|resolve_ending|\.clamp\(" backend/routers/ranking.py backend/use_cases/ranking_use_cases.py` → vazio.
  - Repositórios/Models/DB **não** importam `engine`. Verificável: `rg "from engine|import engine" backend/db backend/models backend/repositories` → vazio.
  - Endpoint de leitura **não importa engine** — leitura sobre `RankingEntry` persistido. Verificável: `rg "from engine|import engine" backend/routers/ranking.py backend/use_cases/ranking_use_cases.py backend/schemas/ranking.py` → vazio.
  - `RankingEntryResponse` declara explicitamente os campos expostos — `session_id` não está na lista (verificado por teste `test_ranking_response_omits_session_id_field`).
- **Arquivos proibidos não tocados:** `frontend/**`, `backend/engine/**`, `backend/engine/data/events.json`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/game-rules.md`, `docs/02-product/architecture.md`, `docs/01-governance/decisions.md`, `backend/repositories/ranking_repository.py` (apenas consumo de `top_n` existente), `backend/models/**`, `backend/db/**`, `backend/core/**`, `backend/routers/players.py`, `backend/routers/sessions.py`, `backend/schemas/{sessions,players,errors}.py`, `backend/use_cases/{choice_use_cases,session_use_cases,session_state,player_use_cases,catalog_loader}.py`. CORS de `backend/app.py` mantido (apenas adicionei `include_router`).

## 5. Evidências técnicas

### 5.1 pytest — suite completa

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/ engine/tests/ -v
```

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.3, pluggy-1.6.0
collected 116 items

tests/test_attributes_repository.py ....                                 [  3%]
tests/test_catalog_loader.py ......                                      [  9%]
tests/test_choices_api.py .........                                      [ 16%]
tests/test_cors.py ..                                                    [ 18%]
tests/test_db_setup.py ...                                               [ 20%]
tests/test_decision_repository.py ...                                    [ 23%]
tests/test_error_handlers.py ....                                        [ 26%]
tests/test_health.py .                                                   [ 27%]
tests/test_player_repository.py ....                                     [ 30%]
tests/test_players_api.py .......                                        [ 37%]
tests/test_ranking_api.py .........                                      [ 44%]
tests/test_ranking_repository.py ...                                     [ 47%]
tests/test_schemas.py .......                                            [ 53%]
tests/test_session_repository.py ....                                    [ 57%]
tests/test_sessions_api.py .......                                       [ 62%]
engine/tests/test_apply_choice.py ...................                    [ 79%]
engine/tests/test_validate.py ........................                   [100%]

============================= 116 passed in 1.70s =============================
```

Exit code: **0**. **116/116** = 107 (após Sprint 2.2-B) + **9** novos da Sprint 2.3 (ver §2.5). Zero regressões.

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

### 5.3 Smoke das rotas registradas

```powershell
python -c "from app import app; print([r.path for r in app.routes if hasattr(r,'path')])"
```

Esperado:

```
['/openapi.json', '/docs', '/docs/oauth2-redirect', '/redoc',
 '/api/players', '/api/sessions', '/api/sessions/{session_id}',
 '/api/sessions/{session_id}/choices', '/api/ranking', '/api/health']
```

### 5.4 Greps de governança

- `rg "compute_score|apply_choice|resolve_ending|\.clamp\(" backend/routers/ranking.py backend/use_cases/ranking_use_cases.py backend/schemas/ranking.py` → vazio (nada de regra de jogo).
- `rg "from engine|import engine" backend/routers/ranking.py backend/use_cases/ranking_use_cases.py backend/schemas/ranking.py` → vazio (endpoint de leitura, sem dependência de engine).
- `rg "session_id" backend/schemas/ranking.py` → vazio (campo proibido, não aparece no schema).
- `rg "from engine|import engine" backend/db backend/models backend/repositories` → vazio (zero acoplamento engine↔persistência, mantido).
- `rg -i "fastapi|sqlalchemy|pydantic" backend/engine/*.py` → apenas docstrings (engine permanece pura).

### 5.5 Arquivos criados/alterados

| Categoria | Arquivo | Tipo |
|---|---|---|
| Schema | `backend/schemas/ranking.py` | criado |
| Use case | `backend/use_cases/ranking_use_cases.py` | criado |
| Router | `backend/routers/ranking.py` | criado |
| Teste | `backend/tests/test_ranking_api.py` | criado |
| Wire-up | `backend/routers/__init__.py` | alterado (export ranking) |
| Wire-up | `backend/schemas/__init__.py` | alterado (export RankingEntryResponse + RankingListResponse) |
| Wire-up | `backend/use_cases/__init__.py` | alterado (export ranking_use_cases) |
| Boot | `backend/app.py` | alterado (`include_router(ranking_router)`; CORS/lifespan intactos) |
| Doc API | `docs/02-product/api.md` | alterado (endpoint marcado Implementado 2.3 + schema `RankingListResponse` + invariante de privacidade) |
| Plano | `docs/00-start/sprint-plan.md` | alterado (Sprint 2.3 marcada como fechada tecnicamente) |
| Status / Handoff | `PROJECT_STATUS.md`, `HANDOFF.md`, `docs/03-validation/sprint-history.md` | alterados |
| Relatório | `docs/03-validation/audits/sprint-2.3.md` | criado (este documento) |

## 6. Decisões registradas

### 6.1 Envelope `{items, limit, count}` em vez de array puro

Decisão Sprint 2.3: usar envelope. Justificativas:
- Cliente sabe imediatamente quantos itens vieram (`count`) e qual era o limite (`limit`) sem inferir.
- Evolução para paginação cursor/offset futura é compatível com este shape (basta adicionar campos opcionais como `next_cursor` ou `total`).
- Padrão consistente para evolução de outros endpoints de listagem futuros (ex.: histórico por player, etc.).

Não foi necessária ADR — é decisão de produto local da Sprint 2.3, registrada aqui e refletida em `docs/02-product/api.md`.

### 6.2 `session_id` NÃO exposto no response

Decisão Sprint 2.3: `RankingEntryResponse` declara explicitamente os campos expostos e **omite** `session_id`. Justificativas:
- `session_id` é chave estrangeira interna; exposição revelaria informação operacional (quantas sessões um jogador teve) sem benefício para o produto público.
- Mantém `RankingEntry` no banco (FK necessária para integridade) mas controla a saída pública.
- Verificável por teste (`test_ranking_response_omits_session_id_field`).

### 6.3 Limite máximo `100`

Decisão Sprint 2.3: `Query(ge=1, le=100, default=10)`. Justificativas:
- Default `10` cobre UX típica de "top 10 da semana".
- Máximo `100` evita resposta absurdamente grande sem necessidade real (a UX desta sprint não pede mais do que isso).
- Bounds rejeitados pelo Pydantic → `RequestValidationError` → handler global → 422 com envelope `{"error": {"code": "validation_error", ...}}` consistente com o resto da API.

### 6.4 Sem paginação cursor/offset

Escopo proibiu. O envelope `{items, limit, count}` foi escolhido para permitir adicionar paginação **sem quebrar contrato** em sprint futura (basta acrescentar campos opcionais como `offset` ou `next_cursor`).

## 7. Limitações conhecidas

- **Sem paginação cursor/offset** — apenas `?limit=N` (decisão §6.4). Top 100 cobre UX inicial.
- **Sem filtros** — não há `?ending_id=...` nem `?player_name=...`. Caso necessário, adicionar em sprint futura (UX driven).
- **Sem ordenação alternativa** — só `score desc`. Tie-break determinístico (`created_at asc, id asc`) já vem do repository.
- **Sem auth / sem rate limiting** — intencional para UX local; ranking é endpoint público de leitura.
- **Sem cache** — leitura direta no banco. Para SQLite local com volumes pequenos é apropriado; reconsiderar se houver carga real.
- **Datetime sem timezone** — `RankingEntry.created_at` é `DateTime` (sem tz), coerente com os outros responses do projeto. Sprint futura pode normalizar para UTC explícito se necessário.
- Limitações herdadas da Sprint 2.2 (playbook reset SQLite local pós-`secrets_seen_json`) continuam válidas — ver `sprint-2.2.md §7.2`.

## 8. Validação documental

- [`docs/02-product/api.md`](../../02-product/api.md) — endpoint marcado **Implementado (2.3)** com schema `RankingListResponse` documentado, invariante de privacidade explícita (`session_id` ocultado), exemplo JSON completo, nota sobre paginação futura.
- [`docs/00-start/sprint-plan.md`](../../00-start/sprint-plan.md) — bloco "Sprint 2.3 (provisória) — Ranking público" marcado como fechado tecnicamente.
- [`HANDOFF.md`](../../../HANDOFF.md) — nova entrada (sessão 11) com declaração, deltas, escopo preservado, evidências, próximo passo.
- [`PROJECT_STATUS.md`](../../../PROJECT_STATUS.md) — sprint técnica mais recente atualizada para 2.3; total de testes 116; ligações atualizadas com `sprint-2.3.md`.
- [`docs/03-validation/sprint-history.md`](../sprint-history.md) — linha nova 2.3.

Não tocados (proibidos):
- [`docs/02-product/game-rules.md`](../../02-product/game-rules.md) — sem mudança de regra.
- [`docs/02-product/architecture.md`](../../02-product/architecture.md) — sem mudança de arquitetura (a sprint implementa exatamente as camadas previstas: router fino + use case fino + repository já existente).
- [`docs/01-governance/decisions.md`](../../01-governance/decisions.md) — nenhuma ADR nova; envelope/limit/`session_id`-hide são decisões locais de produto registradas aqui.

## 9. Critério de aceite aplicado

- [x] Agent declarado (Backend) com checkpoint inicial respondendo Agent / Sprint / arquivos lidos / alterados / proibidos / riscos / plano / DoD.
- [x] Sprint declarada (2.3); escopo exclusivamente Backend; sem cross-domain além do esperado (`api.md`, `sprint-plan.md`, HANDOFF, PROJECT_STATUS, sprint-history — sincronia documental rotineira).
- [x] `GET /api/ranking` retorna 200 com envelope `{items, limit, count}`.
- [x] Suporta `?limit=N` com `1 ≤ N ≤ 100` (default `10`); valores inválidos → 422 com envelope padrão.
- [x] Items ordenados por `score` desc, tie-break (`created_at` asc, `id` asc) determinístico.
- [x] Items expõem **apenas** `id, player_name, score, ending_id, created_at` — `session_id` ocultado (verificado por teste).
- [x] Ranking vazio devolve `{items: [], limit: 10, count: 0}`.
- [x] Smoke fim-a-fim: criar player → sessão → jogar até `demitido` → ranking expõe entrada com `score=49`, `ending_id="demitido"`, `player_name="SmokeRunner"`.
- [x] 116/116 pytest verdes (107 anteriores + 9 novos). Zero regressões.
- [x] `audit.ps1` exit 0.
- [x] Engine, frontend, events.json, rules, scripts, ADRs, game-rules, architecture: zero alterações.
- [x] Repositories, models, DB, core, demais routers/schemas/use_cases: zero alterações.
- [x] CORS preservado (apenas `include_router` foi adicionado em `app.py`).
- [x] Skills formais não declaradas falsamente — frase obrigatória registrada em §4.

## 10. Decisão de aceite humano

- Aceite humano: **PENDENTE**.
- Observações esperadas no aceite:
  - 116/116 testes pytest passaram (107 anteriores + 9 novos da Sprint 2.3, incluindo smoke fim-a-fim).
  - `audit.ps1` exit 0.
  - Nenhum import cruzado entre `backend/engine/**` e `backend/{db,models,repositories}/`; nenhum import de engine no novo router/use_case/schema (endpoint de leitura puro).
  - Camadas respeitadas: router fino → use case fino → repository já existente (`top_n` da Sprint 2.0).
  - Privacidade: `session_id` não vaza no response.
  - Compatibilidade: envelope `{items, limit, count}` permite evolução futura sem quebrar contrato.
- Próximas etapas pós-aceite 2.3:
  1. Aceites humanos formais pendentes — Sprints **2.1 §11**, **2.2 §8**, **2.2-B §10**, **2.3 §10** podem ser aceitos em conjunto.
  2. **Architect/Documentation** — fechar `docs/00-start/executive-overview.md` cobrindo Sprints 2.0/2.1/2.2/2.2-B/2.3 (consolidando pendência 2.0-A/2.1-A).
  3. Backlog de engine/UX: `apply_secret_choice` (segunda etapa do fluxo secreto) e Sprint 3 (UX completa do frontend).
