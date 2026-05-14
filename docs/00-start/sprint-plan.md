# Sprint plan — Corporate Survivor

Derivado de `corporate-survivor-plano-v2.md`. Atualizar datas e checkboxes conforme execução.

## Sprint 0.1 — Estrutura de governança e documentação ✅ (estrutura base)

**Objetivo:** Contexto organizado (`docs/`), rules Cursor (`.cursor/rules/`), scripts stub, README/HANDOFF, arquivo canônico de regras do jogo e setup corporativo **dentro de `docs/`**.

**DoD (estrutura):**

- [x] Árvore `docs/` + subpastas `audits/`, `playthroughs/`  
- [x] Rules `.mdc` conforme plano  
- [x] `scripts/audit.sh`, `scripts/reset_db.sh`  
- [x] `_context/original/` com snapshots  

**Fora de escopo:** código backend/frontend/engine.

---

## Sprint 0.1-B — Correções de governança antes da Sprint 0 executável ⏳

**Objetivo:** Corrigir ressalvas da auditoria read-only antes de qualquer backend/frontend executável.

**DoD:**

- [x] Pastas temporárias `.preflight_*` removidas.  
- [x] Documentos legados da raiz arquivados em `_context/original/` e removidos da raiz.  
- [x] `scripts/audit.ps1` criado e passando no Windows PowerShell.  
- [x] `scripts/audit.sh` espelha os checks mínimos de governança.  
- [x] Critério de aceite/rejeição de output de LLM documentado.  
- [x] `PROJECT_STATUS.md` enxuto como status executivo.  
- [x] `HANDOFF.md` atualizado com evidências.

**Fora de escopo:** criar backend, frontend, engine, API, Vite, FastAPI ou instalar dependências.

**Gate:** backend healthcheck só começa depois desta etapa passar na auditoria mínima.

---

## Sprint 0.1-D — Reorganização visual da documentação ⏳

**Objetivo:** Reorganizar `docs/` em subpastas claras para navegação no Cursor, sem criar código de produto.

**DoD:**

- [x] `docs/00-start/` criado para início, sprint plan e setup.  
- [x] `docs/01-governance/` criado para agentes, workflow e decisões.  
- [x] `docs/02-product/` criado para arquitetura, API e regras do jogo.  
- [x] `docs/03-validation/` criado para auditorias e playthroughs.  
- [x] Referências internas atualizadas para os novos caminhos.  
- [x] Auditoria mínima PowerShell atualizada para os novos caminhos.

**Fora de escopo:** criar backend, frontend, engine, API, Skills formais ou relatórios novos.

---

## Sprint 0 — Foundation executável + ambiente empresa

**Objetivo:** Repo **rodando** localmente na máquina corporativa conforme `docs/00-start/setup-company-env.md`.

**DoD (plano v2):**

- [ ] `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` passa no Windows  
- [ ] `bash scripts/audit.sh` passa quando Git Bash/WSL estiver disponível  
- [ ] Backend sobe só com doc de setup  
- [x] Frontend sobe só com doc de setup  
- [x] `GET /api/health` → 200  
- [x] Frontend mostra “API: ok”  
- [x] README permite setup em menos de 5 minutos para novo dev  
- [ ] Todas as rules `.mdc` existem (✅ já na 0.1)  
- [ ] `HANDOFF.md` atualizado por cada sessão  

---

## Sprint 1.0 — Regras críticas do jogo e contrato da engine ✅ (fechada tecnicamente)

**Objetivo:** Decidir formalmente as regras críticas que a engine deverá seguir, antes de qualquer código de engine. Sem implementar engine.

**DoD:**

- [x] `docs/02-product/game-rules.md` §4.4 com decisão definitiva sobre final antecipado (substitui pendência da Sprint 0.1).  
- [x] `docs/02-product/game-rules.md` §11 com responsabilidades por camada (engine/backend/frontend) e fluxo de uma escolha.  
- [x] ADR-007 fechada como **Substituída**.  
- [x] ADR-010 — Final antecipado por atributo crítico — **Aceita**, com justificativa interpretativa do "atributo chega a zero" e da prioridade dos gatilhos.  
- [x] `docs/01-governance/decisions.md` "Pendências de ADR" sem o item de final antecipado.  
- [x] Sprint 1.1 definida (abaixo).  
- [x] Relatório em `docs/03-validation/audits/sprint-1.0.md`.  
- [x] `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` passou.

**Fora de escopo:** criar engine, `events.json`, código backend/frontend, API, banco, jogo, healthchecks, Skills formais do Cursor, alteração de rules `.cursor/rules/` ou de `scripts/`.

---

## Sprint 1.1 — Engine skeleton + schema `events.json` ⏳

**Objetivo:** Criar a primeira versão da game engine em Python puro (`backend/engine/`) e o schema do `events.json`, respeitando integralmente o contrato definido em `docs/02-product/game-rules.md` §4.4 e §11. Sem expor API e sem persistir estado ainda.

**DoD:**

- [ ] `backend/engine/` criado, em conformidade com `.cursor/rules/game-engine.mdc` (sem `fastapi`, `sqlalchemy`, `pydantic` de API, ou frontend).  
- [ ] Tipos imutáveis (`dataclasses` frozen ou equivalente) para `State`, `Attributes`, `Event`, `Option`, `Consequences`, `EarlyEndingTrigger`, `EndingResult`.  
- [ ] Função `validate_events(catalog)` cobrindo invariantes 1–11 de `docs/02-product/game-rules.md` §4.3 (incluindo presença de `demitido` e `burnout` no registry).  
- [ ] `backend/engine/data/events.json` mínimo (placeholder coerente com `schemaVersion: "1.0"`, validável; conteúdo final dos 15 + 2 fica para Sprint 1.2).  
- [ ] Função pura `apply_choice(state, option_id)` esqueleto com clamp + checagem de gatilho antecipado na ordem definida na ADR-010.  
- [ ] Testes unitários iniciais: validador (catálogo válido/ inválido) e cada um dos 3 gatilhos antecipados (incluindo prioridade `reputacao > energia > ansiedade`).  
- [ ] Relatório em `docs/03-validation/audits/sprint-1.1.md`.

**Fora de escopo:** API HTTP, persistência em SQLite, frontend, conteúdo final dos 15 + 2 eventos, ranking, score persistido, balanceamento.

**Gate:** só começa após aceite humano da Sprint 1.0.

---

## Sprint 1.2 — Catálogo completo dos eventos

- 15 eventos principais + 2 secretos opcionais conforme `docs/02-product/game-rules.md` (§5 e §6).  
- Validador `validate_events()` bloqueando boot se inválido (rodando contra catálogo real).  
- Checklist de balanceamento (§10) revisado.

## Sprint 2.0 — Persistência SQLite + modelos base ⏳

**Objetivo:** Criar a base de persistência SQLite (SQLAlchemy 2.0) do jogo — sem expor fluxo completo de gameplay. Modelos `Player`, `GameSession`, `SessionAttributes` (1:1), `Decision`, `RankingEntry`; repositories CRUD puros; `init_db()` via `Base.metadata.create_all()` no startup do FastAPI (ADR-006); fixtures de teste SQLite in-memory.

**DoD:**

- [ ] `backend/db/`, `backend/models/`, `backend/repositories/` criados e desacoplados de `backend/engine/**`.  
- [ ] 5 modelos com os campos exatos: `Player(id, name, created_at)`, `GameSession(id, player_id, status, current_day, current_sequence, current_event_id, ending_id?, score?, created_at, updated_at, finished_at?)`, `SessionAttributes(session_id, 6 atributos)`, `Decision(id, session_id, event_id, option_id, day, sequence, created_at)`, `RankingEntry(id, player_name, score, ending_id, session_id, created_at)`.  
- [ ] Repositories sem regra de jogo (sem clamp, sem `compute_score`, sem decisão de final).  
- [ ] `backend/app.py` com lifespan chamando `init_db()`; `/api/health` segue verde.  
- [ ] `backend/data/` (gitignored para `.db`) com `.gitkeep`.  
- [ ] Suite pytest verde (pré-existentes + novos testes de persistência).  
- [ ] `audit.ps1` → exit 0.  
- [ ] Relatório em `docs/03-validation/audits/sprint-2.0.md`.

**Fora de escopo:** endpoints de jogo, CORS, schemas Pydantic de API, use cases que chamam a engine, Alembic, ranking endpoint, frontend.

**Gate:** entrega só fecha após aceite humano.

---

## Sprint 2.1 — API de Player e Sessão Inicial ⏳

**Objetivo:** Expor os primeiros endpoints HTTP reais do jogo usando os repositórios da Sprint 2.0. Sem integração com `apply_choice` (essa entra na Sprint 2.2). Schemas Pydantic estritos, handlers globais de erro padronizados, CORS mínimo para o Vite dev. O catálogo `events.json` é validado pela engine no startup.

**DoD:**

- [ ] `POST /api/players` cria Player e valida nome (regex + length 1..64). Decisão: nome **não é único** — múltiplos Players podem ter o mesmo nome (alinhado com ranking global).  
- [ ] `POST /api/sessions` cria sessão para Player existente; popula `current_event_id` consultando o catálogo (`ev_day1_001`); retorna estado completo (sessão + atributos iniciais + evento atual).  
- [ ] `GET /api/sessions/{id}` retorna snapshot completo (sessão + atributos + evento atual carregado do catálogo).  
- [ ] Pacotes criados: `backend/core/` (config, exceptions, error_handlers), `backend/schemas/` (Pydantic v2), `backend/use_cases/` (player, session, catalog_loader), `backend/routers/` (players, sessions).  
- [ ] Erros padronizados: 422 (validação), 404 (não encontrado), 409 (conflito), 500 (genérico sem stack).  
- [ ] CORS habilitado para `http://localhost:5173` (lido de `CORS_ORIGINS`).  
- [ ] `engine.validate_events()` executado no startup do FastAPI; falha = boot falha.  
- [ ] Routers **finos** (sem regra de jogo); use cases podem consumir engine apenas via API pública.  
- [ ] Suite pytest verde + `audit.ps1` exit 0.  
- [ ] `docs/02-product/api.md` atualizado refletindo os 3 endpoints implementados.  
- [ ] Relatório `docs/03-validation/audits/sprint-2.1.md` produzido.

**Fora de escopo:** `POST /api/sessions/{id}/choices` (Sprint 2.2), ranking (sprint futura), restart, integração `apply_choice` com persistência, mudanças no frontend, mudanças na engine (salvo ajuste mínimo claramente justificado).

**Gate:** entrega só fecha após aceite humano.

---

## Sprint 2.2 — Choice integrada à engine ⏳

**Objetivo:** `POST /api/sessions/{id}/choices` que carrega o `State` da engine a partir do SQLite, chama `engine.apply_choice(state, catalog, option_id)`, persiste o novo estado, registra a decisão e — quando a sessão termina (antecipada ou fim de dia 5) — grava ranking, score e `ending_id`.

**DoD esperado (esboço):**

- [x] Adapter State (engine) ↔ Models (ORM) isolado em `backend/use_cases/session_state.py` + campo `secrets_seen_json` para `secret_ids_seen` (sem Decision).  
- [x] `POST /api/sessions/{id}/choices` (`ChoiceCreate`): 409 mismatch `event_id`, chama engine, persiste com `persist_apply_choice_turn` (transaction única — Decision + Attributes + sessão + ranking).  
- [x] Final antecipada / fim de semana gravam `RankingEntry`; score/ending vindos exclusivamente da engine.  
- [x] `inject_secret_event` em `SessionResponse` quando engine retorna `secret_event`; options sem `consequences`.  
- [x] Testes API: mismatch 409; Pydantic 422; ValueError→422 domain; primeiro passo feliz + caminho até `demitido` + banimento pós‑game. Cobertura fim‑de‑semana feliz pela suíte `engine/tests` (HTTP path longo fica backlog leve — citado no relatório).  
- [x] `docs/02-product/api.md` atualizado + relatório [`sprint-2.2.md`](../03-validation/audits/sprint-2.2.md).

**Fora de escopo:** ranking endpoint, frontend, alterações na engine.

---

## Sprint 2.3 — Ranking público ✅ (fechada tecnicamente)

**Objetivo:** expor o leaderboard global via `GET /api/ranking` consumindo o `RankingEntry` já persistido pela Sprint 2.2. Sem frontend, sem restart/continue, sem `apply_secret_choice`, sem nova lógica de jogo.

**DoD entregue:**

- [x] `GET /api/ranking?limit=10` (`Query(ge=1, le=100, default=10)`).
- [x] Envelope `RankingListResponse` `{items, limit, count}`; itens expõem `id, player_name, score, ending_id, created_at` (sem `session_id`).
- [x] Ordenação `score desc` + tie-break determinístico (`created_at asc, id asc`) — herdado de `ranking_repository.top_n`.
- [x] Ranking vazio devolve `{items: [], limit: 10, count: 0}`.
- [x] `limit` fora dos bounds → 422 com envelope padrão de erro.
- [x] Pacotes criados/alterados: `backend/schemas/ranking.py`, `backend/use_cases/ranking_use_cases.py`, `backend/routers/ranking.py`; wire-up nos `__init__.py` + `app.py`. Engine/repositórios/models/CORS intactos.
- [x] 116/116 pytest verdes (107 anteriores + **9 novos** incluindo smoke fim-a-fim que joga até `demitido` e verifica entrada no ranking). `audit.ps1` exit 0.
- [x] `docs/02-product/api.md` atualizado (endpoint Implementado 2.3 + schema + invariante de privacidade).
- [x] Relatório [`sprint-2.3.md`](../03-validation/audits/sprint-2.3.md) produzido.

**Fora de escopo (proibido — respeitado):** frontend, `POST /restart`, `continue`, `apply_secret_choice`, paginação cursor/offset, filtros, ordenação alternativa, alteração de CORS / engine / `events.json`, Sprint 3.

**Gate:** entrega só fecha após aceite humano (papel §10 do relatório).

---

## Sprint legada (substituída) — Robustez API genérica

- Handler global de erro / validação Pydantic estrita / CORS — **incorporada ao DoD da Sprint 2.1** acima.  

## Sprint 3 — UX completa

- Fluxos e feedback conforme plano (seção UX v2)  

## Sprint 4 — Qualidade narrativa / regressão

- Playthroughs documentados em `docs/03-validation/playthroughs/` cobrindo finais alcançáveis  

---

## CI/CD

Opcional / bônus — não obrigatório no plano v2.
