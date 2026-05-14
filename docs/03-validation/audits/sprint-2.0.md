# Sprint 2.0 — Persistência SQLite + modelos base — Relatório de aceite

## 1. Resumo executivo

- **Objetivo da sprint:** criar a base de persistência SQLite do Corporate Survivor (SQLAlchemy 2.0): 5 modelos, repositories CRUD puros, `init_db()` via `Base.metadata.create_all()`, fixtures de teste in-memory. Sem expor fluxo completo de gameplay.
- **Resultado:** **FECHADA tecnicamente**, pendente de aceite humano formal.
- **Decisão recomendada:** aceitar a Sprint 2.0; em seguida abrir a **Sprint 2.0-A documental** (Architect/Documentation) para sincronizar `executive-overview.md`, e depois a **Sprint 2.1 — Robustez API** com Agent Backend.

## 2. Escopo entregue

### 2.1 Persistência (`backend/db/`)

- `backend/db/base.py` — `Base(DeclarativeBase)` centralizando o metadata SQLAlchemy 2.0.
- `backend/db/session.py` — engine SQLAlchemy a partir de `DATABASE_URL` (env, default `sqlite:///./data/corporate_survivor.db`), `SessionLocal`, `get_db()` generator. Cria automaticamente a pasta-pai se for SQLite-file.
- `backend/db/init_db.py` — `init_db(bind=None)` chama `Base.metadata.create_all()`. Importa `models` em modo lazy para registrar o metadata antes do `create_all` (idempotente).
- `backend/db/__init__.py` — API pública: `Base`, `engine`, `SessionLocal`, `get_db`, `init_db`, `DATABASE_URL`.

### 2.2 Modelos (`backend/models/`)

5 modelos com exatamente os campos especificados pela Sprint 2.0:

| Modelo | Campos | Observações |
|---|---|---|
| `Player` (`players`) | `id`, `name` (index, 64), `created_at` (server_default `now()`) | Relacionamento `sessions: list[GameSession]` com cascade. |
| `GameSession` (`game_sessions`) | `id`, `player_id` (FK→players, index), `status` (`active`/`finished`, default `active`), `current_day` (default 1), `current_sequence` (default 1), `current_event_id` (nullable), `ending_id` (nullable), `score` (nullable), `created_at`, `updated_at` (onupdate), `finished_at` (nullable) | Relacionamentos: `player`, `attributes` (1:1 via `uselist=False`), `decisions` (cascade). Constantes `SESSION_STATUS_ACTIVE`/`SESSION_STATUS_FINISHED` exportadas. |
| `SessionAttributes` (`session_attributes`) | `session_id` (FK→game_sessions, **PK** 1:1), 6 atributos `Int NOT NULL` com defaults dos valores iniciais do jogo (`energia=7, reputacao=5, networking=3, ansiedade=2, produtividade=5, aprendizado=4` — espelha `game-rules.md §1`). | Método utilitário `to_dict()`. |
| `Decision` (`decisions`) | `id`, `session_id` (FK→game_sessions, index), `event_id` (64), `option_id` (1), `day`, `sequence`, `created_at` | Ordenação natural por `id ASC` na relação inversa. |
| `RankingEntry` (`ranking_entries`) | `id`, `player_name` (64), `score` (index), `ending_id` (32), `session_id` (FK→game_sessions, index), `created_at` | Score armazenado é o calculado pela engine — não recalcula. |

### 2.3 Repositories (`backend/repositories/`)

5 repositórios módulo-style, sem regra de jogo:

- `player_repository`: `create`, `get`, `get_by_name`.
- `session_repository`: `create` (em uma transação cria `GameSession` ativa + `SessionAttributes` iniciais), `get`, `update_progress`, `finish`.
- `attributes_repository`: `get`, `update` (parcial, ignora chaves desconhecidas, sem clamp).
- `decision_repository`: `record`, `list_by_session`.
- `ranking_repository`: `add`, `top_n` (ordenado por score desc, desempate por `created_at asc, id asc`).

### 2.4 Boot e diretórios runtime

- `backend/app.py` ganhou lifespan FastAPI minimalista chamando `init_db()`. **Nenhum endpoint novo.** `/api/health` segue intacto.
- `backend/data/.gitkeep` preserva o diretório runtime; `.db` continua ignorado pelo `.gitignore` raiz (`*.db`, `backend/data/*.db`).

### 2.5 Testes

- `backend/tests/conftest.py` — fixtures `engine_test` (SQLite in-memory com `StaticPool` para que múltiplas sessões compartilhem a mesma conexão e enxerguem o mesmo schema) e `db` (Session por teste com cleanup no teardown). Importa `models` por side-effect para registrar metadata.
- **21 novos testes** em 6 arquivos:
  - `test_db_setup.py` (3): metadata contém as 5 tabelas, `init_db` cria todas, é idempotente.
  - `test_player_repository.py` (4): create, get, get_by_name, missing.
  - `test_session_repository.py` (4): create com attributes iniciais, update_progress, finish (status+ending+score+finished_at), missing.
  - `test_attributes_repository.py` (4): get inicial, update parcial, ignora chaves desconhecidas, missing.
  - `test_decision_repository.py` (3): record, list em ordem de inserção, lista vazia.
  - `test_ranking_repository.py` (3): add com payload completo, ordenação por score desc, limite N.

## 3. Fora de escopo (não implementado)

- Endpoints de jogo (`/api/players`, `/api/sessions`, `/api/sessions/:id/choices`, `/api/ranking`, `/api/sessions/:id/restart`).
- Use cases / serviços orquestradores que chamem a engine.
- Schemas Pydantic de API.
- CORS.
- Alembic / migrations (decisão ADR-006 — ver §6).
- Conversão completa State (engine) ↔ Models (ORM).
- Frontend.

## 4. Agent / Rules / Skills

- **Agent usado:** Backend.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](../../../.cursor/rules/_dispatcher.mdc), [`.cursor/rules/backend.mdc`](../../../.cursor/rules/backend.mdc); leitura paralela das rules `game-engine.mdc`, `events-json.mdc`, `docs-sync.mdc`, `tests.mdc` que apareceram automaticamente nos arquivos lidos (efeito do dispatcher) — nenhuma alteração nos domínios delas foi feita.
- **Skills formais do Cursor:** **Skills formais não utilizadas nesta sprint**.
- **Como Agent/Rules ajudaram:**
  - `backend.mdc` proíbe regra de jogo em routers e em camadas backend: **repositórios são CRUD puro**, sem `clamp`, sem `compute_score`, sem decisão de final. Verificável: `grep -rn "compute_score\|apply_choice\|clamp\|resolve_ending" backend/db backend/models backend/repositories` → vazio.
  - `_dispatcher.mdc` exigiu checkpoint inicial (agent, sprint, arquivos lidos/alterados/proibidos, riscos, plano, DoD) antes de qualquer edição.
  - Cross-domain (patch em `sprint-plan.md`) foi declarado explicitamente e autorizado pelo humano antes da execução.
  - `backend/engine/**` e `backend/engine/data/events.json` não foram tocados.
  - Nenhum import cruzado: `backend/db/`, `backend/models/`, `backend/repositories/` **não importam** `backend.engine` em momento algum.

## 5. Evidências técnicas

### 5.1 pytest — suite completa

Executado em **2026-05-14**, em `backend/`, com venv ativado:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ engine/tests/ -v
```

Resultado:

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.3, pluggy-1.6.0
collected 65 items

tests/test_attributes_repository.py ....                                 [  6%]
tests/test_db_setup.py ...                                               [ 10%]
tests/test_decision_repository.py ...                                    [ 15%]
tests/test_health.py .                                                   [ 16%]
tests/test_player_repository.py ....                                     [ 23%]
tests/test_ranking_repository.py ...                                     [ 27%]
tests/test_session_repository.py ....                                    [ 33%]
engine/tests/test_apply_choice.py ...................                    [ 63%]
engine/tests/test_validate.py ........................                   [100%]

============================= 65 passed in 0.72s ==============================
```

Exit code: **0**. **65/65** (44 pré-existentes + 21 novos). Zero regressões.

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

### 5.3 Instalação do SQLAlchemy

```
Successfully installed corporate-survivor-backend-0.1.0 greenlet-3.5.0 sqlalchemy-2.0.49
```

`backend/pyproject.toml` ganhou `"sqlalchemy>=2.0"` em `dependencies`.

### 5.4 Arquivos criados/alterados

| Categoria | Arquivo | Tipo |
|---|---|---|
| Camada DB | `backend/db/base.py`, `backend/db/session.py`, `backend/db/init_db.py`, `backend/db/__init__.py` | criados |
| Modelos | `backend/models/__init__.py`, `backend/models/player.py`, `backend/models/game_session.py`, `backend/models/session_attributes.py`, `backend/models/decision.py`, `backend/models/ranking_entry.py` | criados |
| Repositórios | `backend/repositories/__init__.py`, `backend/repositories/player_repository.py`, `backend/repositories/session_repository.py`, `backend/repositories/attributes_repository.py`, `backend/repositories/decision_repository.py`, `backend/repositories/ranking_repository.py` | criados |
| Runtime | `backend/data/.gitkeep` | criado |
| Boot | `backend/app.py` | alterado (lifespan + `init_db()`) |
| Dependências | `backend/pyproject.toml` | alterado (`sqlalchemy>=2.0`) |
| Testes | `backend/tests/conftest.py` + 6 arquivos `test_*.py` (db_setup, player, session, attributes, decision, ranking) | criados |
| Plano | `docs/00-start/sprint-plan.md` | alterado (cross-domain autorizado: inserida Sprint 2.0, antiga "Sprint 2" renomeada para "Sprint 2.1") |
| Status / Handoff | `PROJECT_STATUS.md`, `HANDOFF.md`, `docs/03-validation/sprint-history.md` | alterados |
| Relatório | `docs/03-validation/audits/sprint-2.0.md` | criado (este documento) |

## 6. Decisão sobre migrations — ADR-006

A [`docs/01-governance/decisions.md`](../../01-governance/decisions.md) **ADR-006** prevê: "tentar Alembic primeiro; se inviável, usar `Base.metadata.create_all(engine)` no startup do FastAPI". Esta Sprint 2.0 **executou o fallback** dessa ADR:

- **Justificativa:** escopo desta sprint não inclui mudanças de schema iterativas; ambiente corporativo tende a fricção extra com Alembic; complexidade Alembic não é proporcional ao valor entregue agora.
- **Implementação:** `init_db()` em `backend/db/init_db.py` chama `Base.metadata.create_all(bind=engine)` e é invocado no lifespan FastAPI (`backend/app.py`).
- **Idempotência:** verificada em `test_init_db_is_idempotent`.
- **Reavaliação:** Alembic deve ser reconsiderado se uma sprint futura introduzir migrations destrutivas (renomear coluna, drop com dados, FK adicional sem null).

Nenhuma ADR nova foi criada nesta sprint — a decisão da Sprint 2.0 é caso de **uso** da ADR-006 existente, não decisão arquitetural nova.

## 7. Limitações conhecidas

- **Sem startup de produção real:** `init_db()` no lifespan cobre dev/test; setup multiusuário em produção/intranet poderá precisar de Alembic real (ver §6).
- **Conversão State (engine) ↔ Models (ORM):** intencionalmente **não** existe nesta sprint — repositórios são CRUD puro. A camada de adaptação (use case) entra na Sprint 2.1 / 2.2 quando os endpoints aparecerem.
- **`get_by_name` não normaliza nome:** sem trim/lower/regex (regra de validação é Sprint 2.1).
- **Sem CORS / sem endpoint de jogo:** continua planejado para Sprint 2.1 e posteriores.

## 8. Validação documental

- `api.md` — sem alteração nesta sprint; endpoints de jogo continuam marcados como "Planejado para sprints futuras; não implementado na Sprint 0.2", o que segue verdadeiro. Próxima sprint (2.1) deve atualizar este arquivo quando introduzir endpoints reais.
- `architecture.md` — sem alteração; a sprint implementa exatamente as camadas previstas em §"Visão em camadas" e §"Persistência" (SQLite + SQLAlchemy + ADR-006).
- `game-rules.md` — não tocado. Repositórios não impõem regra de jogo; defaults dos atributos em `SessionAttributes` espelham §1, sem conflito.
- `decisions.md` — ADR-006 citada e utilizada; nenhuma ADR nova foi criada.
- `sprint-plan.md` — patch mínimo cross-domain autorizado pelo humano: inserida "Sprint 2.0 — Persistência SQLite + modelos base" e renomeada "Sprint 2 — Robustez API" → "Sprint 2.1 — Robustez API". Declarado em §4 e no HANDOFF.

## 9. Critério de aceite aplicado

- [x] Agent declarado (Backend) com checkpoint no início.
- [x] Sprint declarada (2.0) e cross-domain (`sprint-plan.md`) declarado/autorizado.
- [x] `backend/db/`, `backend/models/`, `backend/repositories/` criados respeitando `backend.mdc` (sem regra de jogo, sem import da engine).
- [x] 5 modelos com **exatamente** os campos do enunciado, FKs íntegras, defaults coerentes.
- [x] Repositories CRUD puros (sem `compute_score`, sem `apply_choice`, sem `clamp`).
- [x] SQLAlchemy adicionado a `backend/pyproject.toml`.
- [x] `backend/app.py` com lifespan chamando `init_db()`; `/api/health` segue verde.
- [x] `backend/data/.gitkeep` presente; `.gitignore` cobre `.db` (já cobria — verificado).
- [x] 65/65 pytest verdes (44 pré-existentes + 21 novos).
- [x] `audit.ps1` exit 0.
- [x] Sem regressão no `test_health` ou nos 43 testes da engine.
- [x] `backend/engine/**` e `frontend/**` zero alterações.
- [x] `docs/01-governance/decisions.md` e `docs/02-product/game-rules.md` zero alterações.
- [x] Skills formais não declaradas falsamente (frase obrigatória registrada em §4).

## 10. Decisão de aceite humano

- Aceite humano: **PENDENTE**.
- Observações esperadas no aceite:
  - 65/65 testes pytest passaram (1 healthcheck + 43 engine + 21 persistência).
  - `audit.ps1` passou — exit 0.
  - Nenhum import cruzado entre `backend/engine/**` e `backend/{db,models,repositories}/**`.
  - ADR-006 utilizada conforme previsto (fallback `create_all()`).
  - Próxima etapa recomendada: **Sprint 2.0-A documental** (Architect/Documentation atualiza `executive-overview.md`); em seguida **Sprint 2.1 — Robustez API** (Agent Backend: schemas Pydantic, handler global de erro, CORS, integração engine↔routers).
