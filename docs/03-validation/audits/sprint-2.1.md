# Sprint 2.1 — API de Player e Sessão Inicial — Relatório de aceite

## 1. Resumo executivo

- **Objetivo da sprint:** expor os primeiros endpoints HTTP reais do jogo (`POST /api/players`, `POST /api/sessions`, `GET /api/sessions/{id}`), usando os repositórios da Sprint 2.0, com schemas Pydantic estritos, handlers globais de erro padronizados, CORS para Vite dev e validação do `events.json` no startup. Sem integração com `apply_choice` (Sprint 2.2).
- **Resultado:** **FECHADA tecnicamente**, pendente de aceite humano formal.
- **Decisão recomendada:** aceitar a Sprint 2.1; em seguida abrir a **Sprint 2.0-A/2.1-A documental** (Architect/Documentation atualiza `executive-overview.md` para refletir Sprints 2.0 e 2.1 entregues) e a **Sprint 2.2 — Choice integrada à engine**.

## 2. Escopo entregue

### 2.1 Infra transversal (`backend/core/`)

- `core/config.py` — `Settings` (pydantic-settings) lendo `APP_ENV`, `LOG_LEVEL`, `DATABASE_URL`, `CORS_ORIGINS` (CSV). `get_settings()` é singleton (`lru_cache`).
- `core/exceptions.py` — `DomainError` (base), `NotFoundError` (404), `ConflictError` (409), `DomainValidationError` (422). Não importa fastapi: são puro domínio do backend.
- `core/error_handlers.py` — handlers globais convertendo `DomainError`/subclasses em JSON padronizado, `RequestValidationError` em 422 com lista normalizada, qualquer outra exceção em 500 genérico **sem stack**.

### 2.2 Schemas Pydantic v2 (`backend/schemas/`)

- `schemas/players.py` — `PlayerCreate` (`name` 1..64, regex `^[\w\s\-_.'À-ÿ]+$`, trim, `extra="forbid"`) e `PlayerResponse`.
- `schemas/sessions.py` — `SessionCreate` (`player_id` > 0, `extra="forbid"`), `SessionResponse` (snapshot completo: identidade, atributos, evento atual), `AttributesPayload`, `EventPayload`, `OptionPayload` (option **sem** consequences — campo de regra de jogo não escapa do backend).
- `schemas/errors.py` — `ErrorBody` + `ErrorResponse` (envelope para OpenAPI).

### 2.3 Use cases (`backend/use_cases/`)

- `catalog_loader.py` — `load_events_dict`, `validate_or_raise` (chama `engine.validate_events`), `get_catalog` (singleton lazy → `engine.Catalog`), `reset_catalog_cache` (para testes). Suporta override via env `EVENTS_JSON_PATH`.
- `player_use_cases.py` — `create_player`, `get_player` (lança `NotFoundError`).
- `session_use_cases.py` — `create_session` (verifica Player → cria sessão+atributos via repository da Sprint 2.0 → carrega `ev_day1_001` do catálogo → persiste em `current_event_id`), `get_session_snapshot`. Retornam `SessionSnapshot` (dataclass) com `session`, `attributes`, `current_event`.

### 2.4 Routers (`backend/routers/`)

- `routers/players.py` — `POST /api/players` (status 201).
- `routers/sessions.py` — `POST /api/sessions` (201), `GET /api/sessions/{id}` (200). Routers **finos**: dependem de `get_db`, delegam ao use case, serializam via `SessionResponse` (mapeamento Event→EventPayload sem expor `consequences`).

### 2.5 Boot (`backend/app.py`)

- Lifespan chama `init_db()` (ADR-006) + `validate_or_raise()` + `get_catalog()` para falhar cedo em caso de catálogo inválido.
- `CORSMiddleware` com `allow_origins=settings.cors_origins_list`, `allow_methods=["GET","POST","OPTIONS"]`, `allow_credentials=False`.
- `register_error_handlers(app)` registra todos os handlers globais.
- Include routers de players e sessions. `GET /api/health` preservado intacto.

### 2.6 Testes (`backend/tests/`)

- `conftest.py` ganhou fixture `client` que usa o `engine_test` in-memory via `app.dependency_overrides[get_db]`. **Não dispara lifespan** (evita criar banco real em disco).
- 32 novos testes:
  - `test_players_api.py` (7): 201, trim, 422 (vazio/regex/length/extra), idempotência por nome (criação sempre nova).
  - `test_sessions_api.py` (6): 201 com estado completo, 404 player inexistente, 422 payloads inválidos, GET 200, GET 404, GET 422 (id não numérico).
  - `test_error_handlers.py` (4): payload 404/409/500 genérico, ausência de stack/segredos em 500.
  - `test_cors.py` (2): preflight com origin permitido + ausência de header sem `Origin`.
  - `test_catalog_loader.py` (6): schema v1, validação aceita catálogo real, singleton, falha em catálogo quebrado, override via env.
  - `test_schemas.py` (7): casos unitários Pydantic (unicode, whitespace, limites, `player_id > 0`, `extra=forbid`).

## 3. Fora de escopo (não implementado)

- `POST /api/sessions/{id}/choices` (Sprint 2.2).
- Integração com `engine.apply_choice` para mutação de estado (Sprint 2.2).
- Adapter State (engine) ↔ Models (ORM) para escrita pós-escolha (Sprint 2.2).
- Endpoint `GET /api/ranking` (Sprint 2.3 provisória).
- `POST /api/sessions/{id}/restart` (sprint futura).
- Mudanças no frontend.
- Mudanças na engine — confirmado: zero alterações em `backend/engine/**`.

## 4. Agent / Rules / Skills

- **Agent usado:** Backend.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](../../../.cursor/rules/_dispatcher.mdc), [`.cursor/rules/backend.mdc`](../../../.cursor/rules/backend.mdc); demais rules carregadas como contexto pelo dispatcher sem alterar arquivos dos domínios delas.
- **Skills formais do Cursor:** **Skills formais não utilizadas nesta sprint**.
- **Como Agent/Rules ajudaram:**
  - `backend.mdc` proíbe regra de jogo em routers e em camadas backend. Verificável: `rg "compute_score|apply_choice|resolve_ending|\.clamp\(" backend/routers backend/db backend/models backend/repositories` → **0 matches**.
  - `backend.mdc` autoriza consumir API pública via `from engine import ...` — feito em `use_cases/catalog_loader.py` e `use_cases/session_use_cases.py`. Verificável: `rg "from engine|import engine" backend/db backend/models backend/repositories` → **0 matches** (a engine é consumida apenas em `use_cases/` e `routers/`).
  - Engine permanece livre de FastAPI/SQLAlchemy/Pydantic: `rg -i "fastapi|sqlalchemy|pydantic" backend/engine/*.py` → apenas **docstrings** explicando a proibição.
  - Cross-domain (patch em `sprint-plan.md`) autorizado pelo humano antes da execução e declarado neste relatório (§7).

## 5. Evidências técnicas

### 5.1 pytest — suite completa

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ engine/tests/ -v
```

Saída resumida:

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.3
collected 97 items

tests/test_attributes_repository.py ....                                 [  4%]
tests/test_catalog_loader.py ......                                      [ 10%]
tests/test_cors.py ..                                                    [ 12%]
tests/test_db_setup.py ...                                               [ 15%]
tests/test_decision_repository.py ...                                    [ 18%]
tests/test_error_handlers.py ....                                        [ 22%]
tests/test_health.py .                                                   [ 23%]
tests/test_player_repository.py ....                                     [ 27%]
tests/test_players_api.py .......                                        [ 35%]
tests/test_ranking_repository.py ...                                     [ 38%]
tests/test_schemas.py .......                                            [ 45%]
tests/test_session_repository.py ....                                    [ 49%]
tests/test_sessions_api.py ......                                        [ 55%]
engine/tests/test_apply_choice.py ...................                    [ 75%]
engine/tests/test_validate.py ........................                   [100%]

============================= 97 passed in 0.78s ==============================
```

Exit code: **0**. **97/97** (65 pré-existentes + 32 novos da Sprint 2.1). Zero regressões.

### 5.2 audit.ps1

```
== Corporate Survivor - audit.ps1 (governance 0.1-D) ==
OK - governanca minima presente e raiz limpa.
```

Exit code: **0**.

### 5.3 Smoke das rotas registradas

```powershell
python -c "from app import app; print([r.path for r in app.routes if hasattr(r,'path')])"
```

```
['/openapi.json', '/docs', '/docs/oauth2-redirect', '/redoc',
 '/api/players', '/api/sessions', '/api/sessions/{session_id}', '/api/health']
```

### 5.4 Instalação de dependências

```
Successfully installed corporate-survivor-backend-0.1.0 pydantic-settings-2.14.1
```

`pydantic-settings>=2.0` e `pydantic>=2.5` declarados em `backend/pyproject.toml`. SQLAlchemy 2.0 mantido da Sprint 2.0.

### 5.5 Ajuste mínimo de build (`pyproject.toml`)

Após a Sprint 2.0 o backend ganhou múltiplos pacotes top-level (`db`, `models`, `repositories`, `engine`). Setuptools recusou o auto-discovery em flat-layout. Solução **mínima e padrão**: declarar `[tool.setuptools.packages.find]` com `include` explícito (também já cobrindo `core`, `routers`, `schemas`, `use_cases`). Não é regra de jogo — é configuração de empacotamento.

## 6. Decisões registradas

### 6.1 Player duplicado por nome

Decisão Sprint 2.1: **sempre criar novo Player** com novo `id`. Nome NÃO é único. Justificativa:
- O ranking global comporta entradas com o mesmo nome humano (`Bruno score 551`, `Bruno score 280`).
- A semântica de `POST /api/players` fica "create" pura — sem misturar com "find or create".
- Reduz superfície de side-effects e ambiguidade em testes.

Não foi necessária nova ADR — é decisão de produto local da Sprint 2.1, registrada aqui e refletida em `docs/02-product/api.md`.

### 6.2 Reescopo da Sprint 2.1 (cross-domain)

A versão original do `sprint-plan.md` listava "Sprint 2.1 — Robustez API" como item genérico (handler de erro + Pydantic estrito + CORS). O escopo desta sprint reescreveu para "API de Player e Sessão Inicial" — incorporando os 3 itens originais como DoD — e inseriu **Sprint 2.2** explícita para choices+engine. Patch mínimo cross-domain (Architect/Documentation), autorizado pelo humano no início da sessão.

## 7. Limitações conhecidas

- **GET /api/sessions/{id} não inclui histórico de decisões** — só estado atual. A Sprint 2.2 pode adicionar (ou criar endpoint separado) se a UX exigir.
- **Sem rate limiting / auth.** Backend está sem autenticação; CORS está aberto apenas para `http://localhost:5173`. Para intranet/produção, ajustar via env.
- **Sessão "finished" ainda não pode ser produzida via API** — ~~só pelo repository diretamente (`session_repository.finish`)~~. **OBSOLETO pós Sprint 2.2** — fluxo oficial agora fecha via `POST /api/sessions/{id}/choices` + engine.
- **`current_event` no GET é sempre `None` quando `status="finished"`** — pelo construtor `_current_event`. Bom para evitar "evento fantasma" pós-jogo; UX da Sprint 4 (telas de final) decide o display.
- **Não há paginação ou listagem** de Players/Sessions; só create/get pontual. Suficiente para 2.2 e UX inicial.

## 8. Validação documental

- [`docs/02-product/api.md`](../../02-product/api.md) — reescrito para marcar 3 endpoints como **Implementados (Sprint 2.1)**, com schema `SessionResponse` documentado e envelope de erro detalhado.
- [`docs/00-start/sprint-plan.md`](../../00-start/sprint-plan.md) — patch cross-domain: Sprint 2.1 detalhada, Sprint 2.2 inserida, Sprint 2.3 (ranking) listada provisoriamente.
- [`docs/02-product/architecture.md`](../../02-product/architecture.md) — sem alteração: a sprint implementa exatamente as camadas previstas (FastAPI fino + use cases + repositórios + engine pura) e a "Segurança mínima" descrita (Pydantic, regex em nome, 422/409/404/500 sem stack).
- [`docs/02-product/game-rules.md`](../../02-product/game-rules.md) — não tocado. Schemas e routers obedecem a §11 (responsabilidades por camada) — `Option` viaja para o cliente sem `consequences`.
- [`docs/01-governance/decisions.md`](../../01-governance/decisions.md) — não tocado; nenhuma decisão arquitetural nova.

## 9. Critério de aceite aplicado

- [x] Agent declarado (Backend) com checkpoint inicial.
- [x] Sprint declarada (2.1) e cross-domain (`sprint-plan.md`) explicitamente declarado/autorizado.
- [x] `POST /api/players` cria Player, valida regex+length, retorna 201.
- [x] `POST /api/sessions` cria sessão para Player existente, popula `current_event_id` com `ev_day1_001`, retorna 201 com snapshot completo.
- [x] `GET /api/sessions/{id}` retorna snapshot completo ou 404.
- [x] Erros padronizados: 422 / 404 / 409 / 500 sem stack.
- [x] CORS habilitado para `http://localhost:5173`.
- [x] `engine.validate_events` no startup; falha = boot falha.
- [x] Routers finos (sem regra de jogo). `rg compute_score|apply_choice|resolve_ending|\.clamp\(` em `backend/routers backend/db backend/models backend/repositories` → 0 matches.
- [x] 97/97 pytest verdes (65 pré-existentes + 32 novos).
- [x] `audit.ps1` exit 0.
- [x] Engine, frontend, events.json, rules, scripts: zero alterações.
- [x] Skills formais não declaradas falsamente — frase obrigatória registrada em §4.

## 10bis. Checklist pré-aceite técnico (revisão 2026)

Validação solicitada antes do aceite formal no §10:

| Item | Evidência |
|------|-----------|
| CORS não reflete todas as origens (`*`). | `backend/app.py` usa `allow_origins=settings.cors_origins_list` (lista explícita, default apenas `http://localhost:5173`). `allow_credentials=False`. `allow_methods` limitados. **Pós‑revisão:** `allow_headers` restringiu-se a `Content-Type` + `Accept` (não aceita wildcard). |
| `GET /api/sessions/{id}` não expõe `consequences`. | Router monta opções apenas com `{id,label}` (`routers/sessions.py` `_event_to_payload`; schema `OptionPayload`). |
| `HANDOFF.md` cobre última sprint (2.1) com sessão estruturada + links. | Seção HANDOFF Sprint 2.1 (sessão 8) lista arquivos, evidências grep, pendências — **mantido válido até aceite §10.** |
| `sprint-2.1.md` completo até §10. | Relatório traz §1–10 (exceto marcador pendente humane). |

*(Checklist atualizado durante validação solicitada antes do aceite humano §10.)*

## 11. Decisão de aceite humano

- Aceite humano: **PENDENTE**.
- Observações esperadas no aceite (contexto quando o relatório foi fechado tecnicamente):
  - 97/97 testes pytest (`sprint-2.1.md` §5 — números da entrega original).  
  - `audit.ps1` → exit 0 (evidências na §5).  
  - Nenhum import cruzado entre `backend/engine/**` e `backend/{db,models,repositories}/`.  
  - Engine consumida apenas via API pública em `use_cases/` + `routers/`.  

- **Depois das entregas 2.2**: CORS ficou menos permissivo nos cabeçalhos pré‑flight (**`Content-Type` / `Accept` apenas** — ver checklist §10bis e `HANDOFF`). O endpoint de choices e o relatório **`sprint-2.2.md`** cobrem a sprint seguinte; aceite §11 deste documento refere‑se apenas à **Sprint 2.1** (marcar campo humano quando houver).

- Próximas etapas sugeridas pós‑aceite 2.1: **Sprint 2.0-A/2.1-A documental** (`executive-overview.md`); aceite técnico **Sprint 2.2** (`sprint-2.2.md`); depois `/api/ranking` (plano Sprint 2.3).
