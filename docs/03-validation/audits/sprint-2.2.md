# Sprint 2.2 — Choices integradas à engine — relatório técnico

## 1. Objetivo

Expor **`POST /api/sessions/{id}/choices`** que:

1. reidrata `engine.State` a partir das tabelas `game_sessions`, `session_attributes`, `decisions` e campo **`secrets_seen_json`** (lista JSON paralela aos `secret_ids_seen` da engine);
2. delega inteiramente consequências/transição/`compute_score`/endings ao **`engine.apply_choice`** + `RankingEntry` apenas persiste valores retornados;
3. responde com `SessionResponse` atualizado, incluindo **`inject_secret_event`** opcional (evento secreto retornado pela engine neste turno — options **SEM** consequences).

Fora do escopo: frontend, mutate `events.json`, endpoint GET ranking (Sprint 2.3), rota `/restart`.

## 2. Design resumido

| Camada | Responsabilidade |
|--------|------------------|
| Router `sessions.py` | `ChoiceCreate`; delega ao use case |
| `choice_use_cases.py` | 404/409/422 de orquestração; hydrate; `apply_choice`; monta payloads de persistência |
| `session_state.py` | Monta `engine.State` fiel aos ORM (`secrets_seen_json` + decisions ordenadas) |
| `session_repository.persist_apply_choice_turn` | Uma sessão SQLite transacional Decision+attrs+sessão+ranking opcional |
| Repos demais | **SEM** novo game logic |

## 3. Persistência nova

Campo **`GameSession.secrets_seen_json`** (`VARCHAR`, default `'[]'`). Razão técnica: `apply_choice` marca secretos elegíveis com `with_secret_seen` **sem criar Decision** até existir segundo endpoint dedicado; sem persistir esse tuple a hidratação divergiria das próximas chamadas (`_find_eligible_secret` ficaria repetido/errado).

ADR formal não criado — decisão infra local descrita aqui conforme backlog `apply_secret_choice`.

## 4. CORS tighter

Wildcard permissivo (`*`) em `allow_headers` (Starlette) substituído por whitelist **`Content-Type` + `Accept`**.

## 4.A Agent / Rules / Skills (padrão Sprint 2.1)

Seção acrescentada na Sprint 2.2-B para alinhar este relatório ao padrão estabelecido em [`sprint-2.1.md §4`](sprint-2.1.md).

- **Agent usado:** Backend (entrega original 2.2). Sprint 2.2-B (QA): Backend (testes) + Documentation (este relatório, HANDOFF, sprint-history, PROJECT_STATUS).
- **Rules consultadas:**
  - [`.cursor/rules/_dispatcher.mdc`](../../../.cursor/rules/_dispatcher.mdc) — protocolo de checkpoint inicial e disciplina de domínio.
  - [`.cursor/rules/backend.mdc`](../../../.cursor/rules/backend.mdc) — proibição de regra de jogo em routers/repositories/models; consumo da engine apenas via API pública.
  - [`.cursor/rules/tests.mdc`](../../../.cursor/rules/tests.mdc) — Auditor/QA consultado para a 2.2-B (correções mínimas em `tests/`).
  - [`.cursor/rules/docs-sync.mdc`](../../../.cursor/rules/docs-sync.mdc) — sincronia entre HANDOFF, relatório, sprint-history e PROJECT_STATUS.
- **Skills formais do Cursor:** **Skills formais não utilizadas nesta sprint** (frase obrigatória do padrão 2.1). Governança é Agent + Rules + Docs + HANDOFF + `audit.ps1`.
- **Como Agent/Rules ajudaram (verificável):**
  - Router permanece fino — `apply_choice` não é importado em `backend/routers/`. Verificável: `rg "apply_choice" backend/routers` → vazio.
  - Repositórios/Models/DB **não** importam `engine`. Verificável: `rg "from engine|import engine" backend/db backend/models backend/repositories` → vazio.
  - Engine livre de FastAPI/SQLAlchemy/Pydantic de API. Verificável: `rg -i "fastapi|sqlalchemy|pydantic" backend/engine/*.py` → apenas docstrings.
  - `Option` enviada ao cliente NÃO contém `consequences` (`schemas/sessions.py::OptionPayload` define apenas `id`+`label`).
  - Sprint 2.2-B respeitou escopo proibido: zero alteração em `backend/engine/**`, `backend/engine/data/events.json`, `frontend/**`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/game-rules.md`, `docs/02-product/architecture.md`, `docs/01-governance/decisions.md`, ou em qualquer arquivo de produção do backend (apenas testes + documentação).
- **Arquivos proibidos não tocados (2.2 + 2.2-B):** `backend/engine/**`, `backend/engine/data/events.json`, `frontend/**`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/game-rules.md`, `docs/02-product/architecture.md`.

## 5. Testes adicionados

`tests/test_choices_api.py` (5 casos na entrega original 2.2):

| Caso | Descrição |
|------|-----------|
| mismatch `event_id` (ID inexistente) | 409 conflict |
| `option_id="Z"` fora regex | Pydantic 422 |
| `option_id="D"` inexistente no evento | engine ValueError→`DomainValidationError` 422 |
| primeiro turno opcão `A` | avanço `ev_day1_001→ev_day1_002`, options JSON só `{id,label}` |
| caminho determinístico reputação até `demitido` (`score=49`) | status finished + `RankingEntry` count 1 + 409 segunda tentativa |

> Cobertura fim‑de‑semana **HTTP** inteiro (dia5 seq3 última escolha) não parametrizamos — cenário garantido pela suíte `engine/tests`; caminho feliz até final antecipado coberto via API regressão rápida.

### 5.A Testes adicionais — Sprint 2.2-B (correções QA)

A auditoria read-only desta sprint apontou 4 ressalvas de cobertura. Foram adicionadas no mesmo arquivo (sem alteração de código de produção):

| Caso (Sprint 2.2-B) | Descrição |
|------|-----------|
| `test_submit_choice_session_not_found_returns_404` | POST `/choices` em `session_id` inexistente → 404 com `error.code="not_found"` |
| `test_submit_choice_persists_decision_row` | Após escolha válida, exatamente 1 `Decision` gravada com `session_id`, `event_id`, `option_id`, `day`, `sequence` (coordenadas do evento RESPONDIDO) |
| `test_ranking_count_zero_before_session_finishes` | Antes da sessão finalizar, `RankingEntry` count permanece 0 |
| `test_submit_choice_existing_event_but_not_current_returns_409` | `event_id` válido no catálogo (ex.: `ev_day1_002`) mas diferente do `current_event_id` → 409 mismatch |

Total atualizado: **107 testes** (`backend/tests/` + `engine/tests/`). Detalhes em [`sprint-2.2-B.md`](sprint-2.2-B.md).

## 6. Evidências

### 6.1 Entrega original 2.2

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/ engine/tests/
# ============================= 103 passed ...
```

```powershell
powershell -ExecutionPolicy Bypass -File scripts/audit.ps1  # raiz repo — exit 0
```

Greps rápidos pós‑entrega:

- `rg apply_choice backend/routers` → vazio esperado (`use_cases` apenas).
- `rg from.engine backend/models backend/db backend/repositories` → vazio esperado (`use_cases/` + apenas serialização routers importam Tipos/Event para payload).

### 6.2 Pós Sprint 2.2-B (correções QA)

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest tests/ engine/tests/ -v
# ============================= 107 passed in 1.50s =============================
```

107 = 103 (entrega 2.2) + 4 testes novos da 2.2-B (ver §5.A). Auditoria mínima continua exit 0. Nenhum arquivo de produção tocado nas correções (apenas `tests/test_choices_api.py` + documentação).

## 7. Pendências conscientes

1. **Fluxo secreto completo** falta segunda chamada de escolha dedicada (**`apply_secret_choice`** engine + endpoint). Atualmente apenas notificação via campo `inject_secret_event` quando a engine devolve `secret_event`. A engine ainda **não expõe** `apply_secret_choice` — backlog explícito da próxima iteração de engine/UX, NÃO faz parte da Sprint 2.3.
2. **Schema migration sem Alembic — playbook operacional obrigatório antes de testes manuais locais:**
   - A Sprint 2.2 introduziu a coluna nova **`game_sessions.secrets_seen_json`**.
   - A política do projeto continua sendo `Base.metadata.create_all()` no startup do FastAPI (ADR-006).
   - **Limitação conhecida:** `create_all()` **NÃO altera** tabelas pré-existentes — só cria as ausentes. Em ambientes de **dev local** que já tenham um `backend/data/*.db` criado em uma sprint anterior à 2.2, a coluna nova **não será adicionada automaticamente** e qualquer escrita via `POST /choices` falhará com `OperationalError: no such column`.
   - **Procedimento dev (antes de subir o backend localmente para testes manuais pós-2.2):**

     ```powershell
     # PowerShell, na raiz do repo
     Remove-Item -ErrorAction SilentlyContinue backend\data\*.db
     ```

     ou (se preferir Git Bash / WSL):

     ```bash
     rm -f backend/data/*.db
     ```
   - O diretório `backend/data/` é mantido por `.gitkeep` e os `*.db` estão `.gitignored` — apagar é seguro e não afeta o repositório versionado.
   - **CI / pytest:** transparente. A suíte usa SQLite **in-memory** (`conftest.py::engine_test`) com `Base.metadata.create_all()` por teste — schema sempre fresco, problema não ocorre.
   - **Reavaliação Alembic:** continua valendo ADR-006. Se a Sprint 2.3+ introduzir mudança de schema novamente sem que ainda exista usuário em produção, considerar Alembic apenas quando o custo de "apagar `.db` local" virar fricção operacional real.
3. GET ranking e UX leaderboard — **Sprint 2.3**.

## 8. Aceite humano

**PENDENTE** campo formal papel (mirror §10 de relatórios anteriores). Sprint 2.2-B endereçou as ressalvas de cobertura sem alterar o veredito desta sprint. Checklist técnico inline (atualizado pós-2.2-B):

- [x] Fluxo aplicado apenas via endpoint + engine pública (`from engine import apply_choice`).
- [x] Repositório **não** importa engine.
- [x] `events.json` intocado (`git diff` esperado só em backend app layer + tests + docs).
- [x] **107 testes automatizados** (`backend/tests/` + `engine/tests/`) + audit script verde.
- [x] Ressalvas QA (1) 404 sessão inexistente, (2) Decision count após escolha, (3) ranking==0 antes do fim, (4) `event_id` existente diferente do atual → cobertas pelos 4 testes novos da 2.2-B.
- [x] Seção Agent/Rules/Skills explícita (§4.A) alinhada ao padrão da `sprint-2.1.md`.
- [x] Limitação operacional `secrets_seen_json` documentada como playbook (§7.2).

Relatório complementar: [`sprint-2.2-B.md`](sprint-2.2-B.md).

