# Corporate Survivor — Plano de Arquitetura, Agentes e Sprints

Documento de planejamento para o desafio Trainees Cursor. Versão para validação humana antes de executar com IA no Cursor.

---

## Stack confirmada

| Camada | Escolha | Justificativa |
|---|---|---|
| Backend | Python 3.11+ / FastAPI | Skill consolidada, velocidade máxima |
| Persistência | SQLite (via SQLAlchemy 2.0) | Obrigatório pelo desafio; SQLAlchemy padroniza com prática profissional |
| Migrations | Alembic | Mostra maturidade. Alternativa: DDL no boot |
| Validação | Pydantic v2 | Schemas tipados front↔back |
| Engine | Módulo Python puro dentro de `backend/engine/` | Roda só no server; frontend nem importa |
| Frontend | Vite + React 18 + TypeScript | Leve, sem framework full-stack |
| Estilo | Tailwind CSS | Sem dependência pesada de UI kit |
| Estado server | React Query (TanStack) | Cache + invalidação corretos |
| Estado UI local | Hooks nativos / Zustand se precisar | Não duplicar estado do server |
| Testes back | pytest + httpx para API | Padrão FastAPI |
| Testes front | Vitest + Testing Library | Padrão Vite |
| E2E (opcional) | Playwright | Smoke do fluxo completo |

---

## Bloco A — Arquitetura técnica

### A.1 Diagrama de camadas

```
┌────────────────────────────────────────────────────────────────┐
│  Frontend (Vite + React + TS)                                  │
│  ─ Pages: HomePage, NewGamePage, GamePage, EndingPage, Ranking │
│  ─ Components: AttributeBar, EventCard, OptionButton, etc.     │
│  ─ Hooks: useSession, useChoice, useRanking (React Query)      │
│  ─ Services: api.ts (camada fina sobre fetch)                  │
│  ─ Sem lógica de jogo. Sem cálculo de score. Sem decisão de    │
│    final. Sem lista de eventos hardcoded.                      │
└────────────────────────────────────────────────────────────────┘
                              │  HTTP/JSON
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  API HTTP (FastAPI routers)                                    │
│  ─ routers/players.py, sessions.py, ranking.py                 │
│  ─ Recebe DTO Pydantic, chama use case, devolve DTO Pydantic.  │
│  ─ Zero regra de jogo aqui. Validação de input apenas.         │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│  Use Cases (backend/use_cases/)                                │
│  ─ create_player, start_session, apply_choice,                 │
│    get_session_state, restart_session, get_ranking             │
│  ─ Orquestra: carrega estado via repository → chama engine →   │
│    persiste novo estado.                                       │
│  ─ Aqui mora a transação. Apenas aqui.                         │
└────────────────────────────────────────────────────────────────┘
              │                                       │
              ▼                                       ▼
┌──────────────────────────┐         ┌────────────────────────────┐
│  Game Engine (engine/)   │         │  Repositories (db/)        │
│  ─ Funções puras.        │         │  ─ PlayerRepo, SessionRepo,│
│  ─ Carrega events.json   │         │    ChoiceLogRepo           │
│  ─ apply_consequences()  │         │  ─ SQLAlchemy 2.0 + UnitOfW│
│  ─ resolve_next_event()  │         │  ─ Único lugar que toca DB │
│  ─ compute_score()       │         └────────────────────────────┘
│  ─ resolve_ending()      │                       │
│  ─ Sem I/O. Sem DB. Sem  │                       ▼
│    FastAPI. Sem rede.    │              ┌─────────────────┐
└──────────────────────────┘              │   SQLite file   │
                                          └─────────────────┘
```

### A.2 Fluxo completo de uma escolha

```
Usuário clica opção "B" no evento ev_day2_004
    │
    ▼
Frontend: POST /api/sessions/{id}/choices { event_id, option_id }
    │
    ▼
Router sessions.py: valida DTO, chama apply_choice_use_case
    │
    ▼
Use Case apply_choice:
    1. session_repo.get(session_id) → GameState atual
    2. engine.validate_choice(state, event_id, option_id)
       └─ event_id é o evento atual? option existe?
    3. engine.apply_consequences(state, event_id, option_id)
       → new_state (atributos + lista de unlocked/blocked)
    4. engine.resolve_next(new_state)
       → próximo evento | "session_finished"
    5. Se finished:
       ├─ engine.compute_score(new_state) → score
       └─ engine.resolve_ending(new_state) → ending_id
    6. session_repo.save(new_state, score?, ending_id?)
    7. choice_log_repo.append(session_id, event_id, option_id, applied)
    8. COMMIT (transação única)
    │
    ▼
Retorna DTO: { state, next_event | ending, score? }
    │
    ▼
Frontend: React Query invalida sessão, hidrata UI nova
```

**Pontos críticos:**
- O frontend manda `event_id` + `option_id` apenas. Nunca atributos calculados, nunca delta. O backend reaplica tudo do JSON canônico.
- Toda a operação é uma transação SQLAlchemy. Save automático = consequência natural do commit.
- O `choices_log` é append-only e permite auditoria/replay.

### A.3 Modelo de dados SQLite

```python
# backend/db/models.py — SQLAlchemy 2.0 com typed mappings

class Player(Base):
    __tablename__ = "players"
    id: Mapped[str] = mapped_column(primary_key=True)  # UUID
    name: Mapped[str] = mapped_column(String(60))
    created_at: Mapped[datetime]

class Session(Base):
    __tablename__ = "sessions"
    id: Mapped[str] = mapped_column(primary_key=True)
    player_id: Mapped[str] = mapped_column(ForeignKey("players.id"))
    status: Mapped[str]  # "in_progress" | "finished" | "abandoned"
    current_day: Mapped[int]                    # 1..5
    current_event_id: Mapped[str | None]
    state_json: Mapped[str]                     # JSON: atributos, unlocked, blocked, history
    score: Mapped[int | None]
    ending_id: Mapped[str | None]
    schema_version: Mapped[str]                 # versão do schema de eventos usada
    started_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    finished_at: Mapped[datetime | None]

class ChoiceLog(Base):
    __tablename__ = "choices_log"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.id"))
    sequence: Mapped[int]                       # ordem global na sessão
    day: Mapped[int]
    event_id: Mapped[str]
    option_id: Mapped[str]
    applied_consequences_json: Mapped[str]      # snapshot do que foi aplicado
    made_at: Mapped[datetime]
    __table_args__ = (UniqueConstraint("session_id", "sequence"),)
```

**Por que `state_json` e não tabelas normalizadas para atributos?**

Decisão registrada em `decisions.md`. Atributos do jogador são denormalizados em JSON porque (a) são lidos/escritos sempre juntos, (b) o jogo é single-player sem queries analíticas sobre atributos individuais, (c) o `choices_log` já fornece histórico granular para qualquer auditoria. Normalizar aqui seria over-engineering.

**Índices:**
- `sessions(player_id)` para "minhas partidas"
- `sessions(status, score DESC)` para ranking
- `choices_log(session_id, sequence)` já vem do UniqueConstraint

### A.4 Schema do evento JSON

Arquivo único: `backend/engine/data/events.json`

```json
{
  "schemaVersion": "1.0",
  "events": [
    {
      "id": "ev_day1_001",
      "day": 1,
      "title": "O primeiro café",
      "scene": "São 9h12. Você chega à copa e três pessoas do time já estão lá rindo de algo. Ninguém se vira para te cumprimentar imediatamente.",
      "weight": 10,
      "tags": ["social", "onboarding"],
      "unlock": {
        "requires_all": [],
        "requires_any": [],
        "blocked_by": [],
        "min_attrs": {},
        "max_attrs": {}
      },
      "options": [
        {
          "id": "A",
          "label": "Puxar conversa: \"oi pessoal, sou novo aqui\".",
          "consequences": {
            "networking": 2,
            "ansiedade": 1,
            "energia": -1
          },
          "unlocks": ["ev_day2_005"],
          "blocks": []
        },
        {
          "id": "B",
          "label": "Pegar o café em silêncio e voltar para a mesa.",
          "consequences": {
            "energia": 1,
            "networking": -1
          },
          "unlocks": [],
          "blocks": ["ev_day2_005"]
        },
        {
          "id": "C",
          "label": "Esperar alguém te perceber.",
          "consequences": {
            "ansiedade": 2,
            "energia": -1
          },
          "unlocks": [],
          "blocks": []
        }
      ]
    }
  ]
}
```

**Regras do schema:**

| Campo | Tipo | Obrigatório | Notas |
|---|---|---|---|
| `id` | string | sim | Convenção: `ev_dayN_NNN` |
| `day` | int 1..5 | sim | Dia em que o evento pode aparecer |
| `scene` | string | sim | Texto narrativo apresentado ao jogador |
| `weight` | int | não | Default 1; influencia seleção quando há vários elegíveis |
| `unlock.requires_all` | string[] | não | Todos esses event_ids precisam ter sido vivenciados |
| `unlock.requires_any` | string[] | não | Pelo menos um |
| `unlock.blocked_by` | string[] | não | Se algum desses foi vivenciado, este NÃO aparece |
| `unlock.min_attrs` | object | não | Ex: `{"reputacao": 3}` |
| `unlock.max_attrs` | object | não | Ex: `{"ansiedade": 7}` |
| `options[].consequences` | object | sim | Delta por atributo |
| `options[].unlocks` | string[] | não | event_ids adicionados ao pool após esta escolha |
| `options[].blocks` | string[] | não | event_ids removidos do pool após esta escolha |

**Validação na carga** (Pydantic):
- `schemaVersion` precisa bater com o suportado.
- Toda referência em `unlocks`/`blocks`/`requires_*`/`blocked_by` aponta para um evento que existe no arquivo (referential integrity em build time).
- Cada `day` 1..5 tem pelo menos 3 eventos sempre elegíveis em estado inicial (senão o jogador trava).
- Total ≥ 15 eventos.
- Cada evento tem 2..4 opções.

Falha de validação na inicialização do servidor = boot falha. Princípio "fail fast".

### A.5 Registry de finais

Predicados em código Python registrados via decorator. Avaliação ordenada por prioridade (maior primeiro). Sempre existe um fallback.

```python
# backend/engine/endings.py

ENDINGS_REGISTRY: list[Ending] = []

def register_ending(id: str, name: str, priority: int):
    def decorator(fn):
        ENDINGS_REGISTRY.append(Ending(
            id=id, name=name, priority=priority, predicate=fn
        ))
        return fn
    return decorator

@register_ending("demitido", "Demitido no Período de Experiência", priority=100)
def _demitido(state: GameState) -> bool:
    return state.reputacao <= 0

@register_ending("burnout", "Burnout em Tempo Recorde", priority=95)
def _burnout(state: GameState) -> bool:
    return state.energia <= 0 or state.ansiedade >= 10

@register_ending("risco_op", "Risco Operacional", priority=80)
def _risco(state: GameState) -> bool:
    return state.produtividade <= 1 and state.reputacao <= 2

@register_ending("invisivel", "Funcionário Invisível", priority=60)
def _invisivel(state: GameState) -> bool:
    return state.networking <= 1 and state.reputacao <= 3

@register_ending("trainee_lenda", "Trainee Lenda", priority=50)
def _lenda(state: GameState) -> bool:
    return (state.reputacao >= 8 and state.networking >= 7
            and state.aprendizado >= 7 and state.produtividade >= 7)

@register_ending("promessa", "Promessa Corporativa", priority=40)
def _promessa(state: GameState) -> bool:
    return state.reputacao >= 6 and state.aprendizado >= 6

@register_ending("sobrevivente", "Sobrevivente do Onboarding", priority=0)
def _sobrevivente(state: GameState) -> bool:
    return True  # fallback
```

**Por que registry e não DSL no JSON:**
- Predicados são testáveis em isolamento com pytest.
- Lógica de "e/ou/comparação" expressa em Python é mais segura que DSL caseira.
- Adicionar final continua sendo "uma decisão" em um arquivo (`endings.py`), o que cabe perfeitamente na regra "adicionar conteúdo não exige tocar lógica principal" — endings são conteúdo de jogo, não lógica de orquestração.

### A.6 Contrato da API

Prefixo `/api`. Todos os endpoints retornam JSON.

| Método | Rota | Body | Retorna |
|---|---|---|---|
| POST | `/api/players` | `{name}` | `{id, name, created_at}` |
| POST | `/api/sessions` | `{player_id}` | `SessionStateDTO` (estado inicial + primeiro evento) |
| GET | `/api/sessions/{id}` | — | `SessionStateDTO` (continuar partida) |
| POST | `/api/sessions/{id}/choices` | `{event_id, option_id}` | `SessionStateDTO` (com `next_event` ou `ending`) |
| POST | `/api/sessions/{id}/restart` | — | `SessionStateDTO` (zerada) |
| GET | `/api/ranking?limit=50` | — | `[{rank, player_name, score, ending_name, finished_at}, ...]` |
| GET | `/api/health` | — | `{status: "ok"}` |

**`SessionStateDTO`** (camelCase no wire, snake_case no Python via alias Pydantic):

```json
{
  "sessionId": "uuid",
  "playerName": "Diego",
  "status": "in_progress",
  "currentDay": 2,
  "attributes": {
    "energia": 5,
    "reputacao": 6,
    "networking": 4,
    "ansiedade": 3,
    "produtividade": 5,
    "aprendizado": 7
  },
  "nextEvent": {
    "id": "ev_day2_004",
    "title": "Reunião sem pauta",
    "scene": "...",
    "options": [
      {"id": "A", "label": "..."},
      {"id": "B", "label": "..."}
    ]
  },
  "ending": null,
  "score": null,
  "history": [
    {"day": 1, "eventId": "ev_day1_001", "optionId": "A"}
  ]
}
```

**Importante:** o `consequences` das opções NÃO vai no payload. O jogador descobre o efeito após escolher. Isso preserva tensão narrativa e impede o frontend de ter qualquer cópia local de consequências.

Erros padrão FastAPI: 400 (input inválido), 404 (sessão não existe), 409 (escolha inválida — opção/evento não bate com estado atual), 422 (Pydantic), 500.

### A.7 Cálculo de score

Fórmula em `engine/scoring.py`. Determinística, testável.

```python
ATTR_WEIGHTS = {
    "reputacao": 12,
    "produtividade": 10,
    "aprendizado": 9,
    "networking": 8,
    "energia": 5,
    "ansiedade": -7,  # ansiedade penaliza
}

ENDING_BONUS = {
    "trainee_lenda": 200,
    "promessa": 120,
    "sobrevivente": 60,
    "invisivel": 20,
    "risco_op": 0,
    "burnout": -50,
    "demitido": -100,
}

def compute_score(state: GameState, ending_id: str) -> int:
    base = sum(getattr(state, attr) * w for attr, w in ATTR_WEIGHTS.items())
    diversity = len(set(c.day for c in state.history))  # bonus por chegar longe
    return max(0, base + ENDING_BONUS[ending_id] + diversity * 5)
```

**Anti-cheat conceitual (documentar em `decisions.md`):**
O score é computado server-side a partir do estado final que o server controla. O frontend nunca calcula nem envia score. Isso não impede um atacante de chamar a API e tentar maximizar — para isso precisaria de rate limit, auth real, etc., que estão fora de escopo do desafio. O objetivo arquitetural é manter o frontend como cliente burro.

---

## Bloco B — Camada de agentes refinada

Cada agente é uma **persona de invocação no Cursor**. Você abre o Cursor com Claude/GPT, prefixa a sessão com a identidade do agente (ex: "Você é o Agent Game Engine, leia `.cursor/rules/game-engine.mdc` e `docs/game-rules.md` antes de tudo"), e ele opera dentro daquele escopo.

### B.1 Agent Backend

**Responsabilidade:** API FastAPI, routers, use cases, repositórios SQLAlchemy, migrations Alembic, configuração de boot. Setup do `pyproject.toml`/`uv`. Validação Pydantic.

**Limites:**
- Nunca importa de `frontend/`.
- Nunca importa nenhum item de `engine/` que não seja função pública documentada do `engine/__init__.py`.
- Routers não contêm regra de jogo. Routers chamam use cases.
- Use cases não calculam atributos manualmente — sempre delegam à engine.
- Nunca confia em deltas/scores vindos do frontend.

**Lê antes de cada tarefa:** `docs/architecture.md`, `docs/api.md`, `.cursor/rules/backend.mdc`, `HANDOFF.md` (se existir).

**Produz:** código em `backend/`, atualização de `docs/api.md` quando muda contrato, entrada em `decisions.md` quando muda arquitetura.

**Gatilho:** qualquer tarefa que toque `backend/**` exceto `backend/engine/**`.

**Prompt de invocação (template):**
```
Você é o Agent Backend do projeto Corporate Survivor.
Leia, NESTA ORDEM, antes de qualquer coisa:
  1. .cursor/rules/backend.mdc
  2. docs/architecture.md (seção "Backend")
  3. docs/api.md
  4. HANDOFF.md (se existir)

Tarefa: <descrição>

Restrições não-negociáveis:
- Nenhuma regra de jogo em routers ou use cases. Engine é fonte da verdade.
- Pydantic para todo DTO de entrada/saída.
- Transação única por escolha aplicada.

Ao terminar, atualize HANDOFF.md descrevendo o que mudou.
```

### B.2 Agent Frontend

**Responsabilidade:** componentes React, páginas, roteamento, integração com API via React Query, responsividade, estados de loading/erro/vazio, acessibilidade básica.

**Limites:**
- Nunca calcula score, nunca decide final, nunca aplica consequências.
- Nunca tem cópia local de eventos ou consequências.
- Trata o backend como única fonte de verdade.
- Nenhum `localStorage` com estado de jogo (apenas com `sessionId` para retomar).

**Lê:** `docs/architecture.md` (seção "Frontend"), `docs/api.md`, `.cursor/rules/frontend.mdc`.

**Produz:** código em `frontend/`, screenshots/notas em `HANDOFF.md` quando concluir tela.

**Gatilho:** qualquer tarefa em `frontend/**`.

### B.3 Agent Game Engine

**Responsabilidade:** lógica pura. Carregamento e validação de `events.json`. Aplicação de consequências. Seleção do próximo evento elegível. Cálculo de score. Resolução de final. Registry de finais.

**Limites:**
- `backend/engine/**` não importa FastAPI, SQLAlchemy, requests, nem qualquer biblioteca de I/O. Só `pydantic` (validação), `json` da stdlib, `dataclasses`/`typing`.
- Não tem `print` em código de produção (logger se necessário, injetado).
- Funções são puras: mesmo input → mesmo output.
- Adicionar evento = editar `events.json`. Adicionar regra nova de unlock = mudar engine **e** documentar em `decisions.md`.

**Lê:** `docs/game-rules.md`, `.cursor/rules/game-engine.mdc`.

**Produz:** código em `backend/engine/`, testes em `backend/tests/engine/`, atualização de `docs/game-rules.md`.

**Gatilho:** tarefas em `backend/engine/**` ou no schema dos eventos.

### B.4 Agent Content/Narrative

**Responsabilidade:** escrever os 15+ eventos. Tom, voz, coerência narrativa, balanceamento de consequências (sem opção sempre dominante), variedade entre dias.

**Limites:**
- Só toca `backend/engine/data/events.json`.
- Não toca código.
- Cada evento que escreve passa pelo validador Pydantic da engine antes de ser commitado.
- Mantém uma "tabela de tensão" em `docs/game-rules.md` mostrando, por dia, que atributos cada evento tende a estressar (evita que um dia inteiro seja só sobre energia).

**Lê:** `docs/game-rules.md` (seção "Tom e voz", "Atributos e o que significam").

**Produz:** eventos JSON, anotações em `docs/game-rules.md`.

**Gatilho:** sprint de conteúdo (Sprint 1 majoritariamente, e ajustes em Sprint 4).

### B.5 Agent QA/Tests

**Responsabilidade:** testes automatizados. Unit da engine (consequências, unlock, scoring, ending resolution). Testes de contrato dos endpoints (httpx + ASGI). Smoke E2E opcional (Playwright). Configuração de coverage.

**Limites:**
- Não altera código de produção para fazer teste passar. Se há bug, abre nota em `HANDOFF.md` para o agente responsável.
- Coverage mínimo: engine ≥ 90%, use cases ≥ 80%, routers ≥ 70%.

**Lê:** `.cursor/rules/tests.mdc`, código que está testando.

**Produz:** `backend/tests/`, `frontend/tests/`, relatório de coverage em `docs/test-report.md` (gerado por script).

**Gatilho:** ao fim de cada sprint, ou sob demanda quando código novo é mergeado.

### B.6 Agent Auditor Read-Only

**Responsabilidade:** ao final de cada sprint, executa `scripts/audit.sh` e produz relatório em `docs/audits/sprint-N.md`. Verifica DoD.

**Limites:**
- **Modo leitura.** Não edita arquivos de código. Único arquivo que pode escrever é o relatório de auditoria.
- Não declara sprint fechada se algum check falhou — apenas reporta.
- Não opina sem evidência. Cada apontamento vem com path:linha ou comando que reproduz o problema.

**O que o `audit.sh` checa (todos os checks são scripts, não opinião do LLM):**

```bash
#!/usr/bin/env bash
# scripts/audit.sh — executado pelo Agent Auditor ao fim de cada sprint
set -e

echo "== 1. Hardcode de eventos no frontend =="
! grep -r -E '(ev_day[1-5]_|"scene"\s*:)' frontend/src \
  && echo "OK: nenhum evento hardcoded no frontend" \
  || (echo "FAIL: evento hardcoded encontrado"; exit 1)

echo "== 2. Engine não importa FastAPI/SQLAlchemy =="
! grep -rE 'from (fastapi|sqlalchemy|httpx)' backend/engine \
  && echo "OK: engine isolada" \
  || (echo "FAIL: engine acoplada"; exit 1)

echo "== 3. Routers sem cálculo de atributo =="
# heurística: routers não devem referenciar nomes de atributos diretamente
! grep -rE '(energia|reputacao|networking|ansiedade|produtividade|aprendizado)' \
    backend/routers \
  && echo "OK: routers limpos" \
  || (echo "WARN: router referencia atributo — revisar")

echo "== 4. Lint + typecheck backend =="
cd backend && ruff check . && mypy . && cd ..

echo "== 5. Lint + typecheck frontend =="
cd frontend && npm run lint && npm run typecheck && cd ..

echo "== 6. Testes backend =="
cd backend && pytest --cov=. --cov-report=term --cov-fail-under=75 && cd ..

echo "== 7. Testes frontend =="
cd frontend && npm test -- --run && cd ..

echo "== 8. Validação do events.json =="
cd backend && python -m engine.validate_events && cd ..

echo "== 9. README mencionado nos docs =="
test -s README.md && test $(wc -l < README.md) -gt 30 \
  && echo "OK: README com conteúdo" \
  || (echo "FAIL: README vazio ou pequeno"; exit 1)

echo "== 10. decisions.md atualizado =="
# Última modificação de decisions.md deve ser desta sprint
# (verificação manual ou via git log — o agente Auditor faz)

echo "== AUDITORIA CONCLUÍDA =="
```

**Prompt do Auditor:**
```
Você é o Agent Auditor Read-Only. Sua tarefa:
1. Execute `bash scripts/audit.sh` e capture output.
2. Compare o estado do código com a DoD da Sprint N (em docs/sprint-plan.md).
3. Verifique se docs/decisions.md teve nova entrada nesta sprint quando houve mudança arquitetural.
4. Verifique se docs/api.md está coerente com os endpoints reais (lista as rotas via FastAPI OpenAPI e compara).
5. Produza docs/audits/sprint-N.md no formato:
   - Resumo executivo (passou / com ressalvas / falhou)
   - Cada check com status e evidência
   - Riscos para a próxima sprint

Você NÃO altera nenhum arquivo além de docs/audits/sprint-N.md.
```

### B.7 Agent Documentation/Context

**Responsabilidade:** manter `/docs/` vivo. Manter `README.md` sempre executável (alguém clona, segue os passos, roda). Registrar decisões reais com justificativa em `decisions.md`. Atualizar `sprint-plan.md` ao fim de cada sprint.

**Limites:**
- Não inventa documentação. Se algo não está no código, não está no doc.
- Texto técnico, sem marketing, sem floreio.
- Cada decisão arquitetural relevante tem entrada com: contexto, opções consideradas, escolha, consequências.

**Lê:** todo o repo, especialmente `decisions.md` existente e `HANDOFF.md`.

**Produz:** todos os arquivos em `docs/`, README.md.

**Gatilho:** ao fim de cada sprint + sob demanda quando um outro agente registrou "doc desatualizado" em HANDOFF.

---

## Bloco C — Cursor rules (`.cursor/rules/*.mdc`)

Formato MDC com frontmatter. `alwaysApply: false` + `globs` = aplicam só quando o Cursor abre arquivos que casam.

### C.1 `.cursor/rules/frontend.mdc`

```mdc
---
description: Regras do Agent Frontend. Aplicam ao tocar qualquer arquivo do frontend.
globs:
  - "frontend/**/*.{ts,tsx,js,jsx,css}"
alwaysApply: false
---

# Agent Frontend — Regras

Você está editando código do frontend Vite + React + TypeScript do projeto Corporate Survivor.

## Princípios não-negociáveis

1. **Backend é fonte da verdade.** Score, próximo evento, final do jogo, consequências aplicadas — tudo vem do backend. O frontend renderiza, não decide.

2. **Zero hardcode de eventos.** Os textos das cenas, opções e consequências vêm sempre da API. Se você precisa de placeholder durante desenvolvimento, use mocks em `frontend/src/__mocks__/` e nunca em componentes de produção.

3. **Estado do servidor mora em React Query.** Não duplicar em Zustand/Redux. Zustand só para UI local (modal aberto, tema, etc.).

4. **Componentes pequenos e tipados.** Cada componente recebe props tipadas. Sem `any`. Sem `// @ts-ignore` sem comentário explicando.

5. **Acessibilidade básica.** Botões são `<button>`. Imagens decorativas têm `alt=""`. Foco visível. Contraste suficiente.

6. **Responsividade.** Mobile-first via Tailwind. Layout funcional em 360px.

## Estrutura esperada

```
frontend/src/
  pages/         # HomePage, NewGamePage, GamePage, EndingPage, RankingPage
  components/    # AttributeBar, EventCard, OptionButton, etc.
  hooks/         # useSession, useCreatePlayer, useApplyChoice, useRanking
  services/api.ts  # camada fina sobre fetch, tipada
  types/         # tipos compartilhados (derivados do contrato da API)
  App.tsx
  main.tsx
```

## Anti-padrões (vão fazer o Auditor reprovar)

- Calcular score no cliente.
- `if (state.energia <= 0) showBurnout()` — final é decidido pelo backend.
- Importar arquivo de `backend/`.
- Lista de eventos em constante local.
- `localStorage` com estado de jogo (apenas `sessionId` para retomar é OK).

## Quando em dúvida

Consulte `docs/architecture.md` (seção Frontend) e `docs/api.md`. Se a dúvida é nova decisão arquitetural, **pare** e peça humano + atualização de `decisions.md`.
```

### C.2 `.cursor/rules/backend.mdc`

```mdc
---
description: Regras do Agent Backend. Aplicam ao tocar backend exceto engine.
globs:
  - "backend/**/*.py"
alwaysApply: false
---

# Agent Backend — Regras

Você está editando o backend FastAPI do Corporate Survivor.

## Princípios não-negociáveis

1. **Engine é fonte da verdade do jogo.** Routers e use cases nunca calculam atributos manualmente. Sempre delegam à engine (`from engine import ...`).

2. **Routers são finos.** Recebem DTO Pydantic, chamam use case, retornam DTO Pydantic. Sem if/else de regra de negócio.

3. **Use cases orquestram transação.** Um use case = uma operação de domínio = uma transação SQLAlchemy.

4. **Repositórios são a única camada que toca DB.** Use cases não escrevem SQL nem `session.execute(...)` diretamente.

5. **Nunca confie em payload do frontend para atributos ou score.** Aceite apenas `event_id` + `option_id`. Reaplique tudo do JSON canônico.

6. **Pydantic v2 com alias camelCase no wire.** Front recebe `currentDay`, back trabalha com `current_day`.

7. **Fail fast no boot.** Se `events.json` é inválido, o app não sobe.

## Estrutura esperada

```
backend/
  app.py              # FastAPI app + lifespan + boot validation
  routers/            # players.py, sessions.py, ranking.py, health.py
  use_cases/          # create_player.py, apply_choice.py, etc.
  db/
    models.py         # SQLAlchemy 2.0
    repositories.py
    session.py        # engine + SessionLocal
  engine/             # ★ NÃO TOQUE AQUI. Agent Game Engine cuida.
  schemas/            # Pydantic DTOs
  migrations/         # Alembic
  tests/
  pyproject.toml
```

## Anti-padrões

- `if state["energia"] <= 0:` dentro de router/use case.
- Aceitar `score` ou `attributes` no body de `POST /choices`.
- `commit()` em mais de um lugar por use case.
- Engine importando router ou repositório.

## Quando criar novo endpoint

1. Atualize `docs/api.md` PRIMEIRO com o contrato.
2. Adicione DTO em `schemas/`.
3. Adicione use case.
4. Adicione router.
5. Adicione teste de contrato.
6. Registre em `decisions.md` se houver decisão não-óbvia.
```

### C.3 `.cursor/rules/game-engine.mdc`

```mdc
---
description: Regras do Agent Game Engine. Pureza obrigatória.
globs:
  - "backend/engine/**/*.py"
  - "backend/engine/**/*.json"
alwaysApply: false
---

# Agent Game Engine — Regras

Você está editando a **lógica pura** do Corporate Survivor.

## Princípios não-negociáveis

1. **Zero I/O.** Sem rede. Sem disco (exceto leitura única de `data/events.json` na inicialização). Sem `print`. Sem logger global.

2. **Zero acoplamento com framework.** Proibido importar: `fastapi`, `sqlalchemy`, `httpx`, `requests`, `starlette`. Permitido: stdlib, `pydantic` (só validação).

3. **Funções puras.** Mesmo input → mesmo output. Não muta argumentos. Retorna novo estado.

4. **Estado é dataclass imutável (frozen).** `GameState` é `@dataclass(frozen=True)`. `replace()` para criar novo.

5. **Validação na carga.** `validate_events()` falha alto e cedo se schema quebrar.

6. **Score e final são determinísticos.** Mesma sessão completa = mesmo resultado.

## API pública (exportada de `engine/__init__.py`)

```python
from .state import GameState, Attributes
from .events import EventCatalog, load_events
from .choices import apply_choice, validate_choice
from .selection import next_event_or_finish
from .scoring import compute_score
from .endings import resolve_ending, list_endings
```

Nada além disso deve ser importado de fora da engine.

## Anti-padrões

- `import fastapi`
- `session.commit()` dentro de engine
- mutação de estado: `state.energia -= 1` (errado; use `replace`)
- `random` sem seed quando determinismo é necessário (use seed da sessão)
- regra de jogo nova sem teste correspondente

## Adicionar evento

1. Edite `engine/data/events.json` seguindo o schema.
2. Rode `python -m engine.validate_events`.
3. Pronto. Não tocar nenhum outro arquivo.

## Adicionar final

1. Edite `engine/endings.py` adicionando um `@register_ending(...)`.
2. Adicione teste em `tests/engine/test_endings.py`.
3. Atualize `docs/game-rules.md`.
4. Atualize `docs/decisions.md` se a regra muda a balança.
```

### C.4 `.cursor/rules/events-json.mdc`

```mdc
---
description: Regras de edição do catálogo de eventos JSON.
globs:
  - "backend/engine/data/events.json"
alwaysApply: false
---

# Catálogo de eventos — Regras

Este arquivo é o conteúdo do jogo. Cada edição precisa preservar invariantes.

## Schema obrigatório

Cada evento tem: `id`, `day`, `title`, `scene`, `options` (2..4 opções).
Cada opção tem: `id`, `label`, `consequences` (delta por atributo).

## Invariantes que precisam continuar valendo após sua edição

- `schemaVersion: "1.0"` continua compatível.
- Total de eventos ≥ 15.
- Cada dia 1..5 tem ≥ 3 eventos com `unlock` vazio ou trivialmente satisfeito (senão jogador trava no estado inicial).
- Todo `id` referenciado em `unlocks`, `blocks`, `requires_all`, `requires_any`, `blocked_by` existe.
- Nenhum evento referencia a si mesmo em `requires_*` ou `blocks`.
- Soma absoluta das `consequences` de uma opção ≤ 6 (balanceamento — evita opções "milagrosas").

## Após editar

Sempre rode:
```
cd backend && python -m engine.validate_events
```

Se falhar, NÃO commite.

## Tom narrativo

Cenas em terceira pessoa próxima, presente do indicativo. Português brasileiro corporativo realista. Sem clichês ("o gestor maquiavélico", "o RH vilão"). Sem humor que dependa de estereótipo. Cada opção precisa ser razoável — não pode haver "a opção certa óbvia". Toda escolha tem custo.
```

### C.5 `.cursor/rules/tests.mdc`

```mdc
---
description: Regras do Agent QA/Tests.
globs:
  - "backend/tests/**/*.py"
  - "frontend/src/**/*.test.{ts,tsx}"
alwaysApply: false
---

# Agent QA/Tests — Regras

## Princípios

1. **Testes da engine são prioridade.** Engine é o coração do jogo. Cobertura mínima 90%.
2. **Não modifique código de produção para fazer teste passar.** Se há bug, abra entrada em HANDOFF.md.
3. **Testes determinísticos.** Sem `random` sem seed. Sem dependência de relógio (use `freezegun` se preciso).
4. **Nomes descritivos.** `test_burnout_ending_triggers_when_energia_zero_and_ansiedade_above_8` em vez de `test_burnout`.

## Estrutura

```
backend/tests/
  engine/
    test_choices.py
    test_scoring.py
    test_endings.py
    test_selection.py
    test_event_validation.py
  api/
    test_players.py
    test_sessions.py
    test_ranking.py
  conftest.py     # fixtures: db em memória, client httpx
```

## Padrão de teste de engine

```python
def test_apply_choice_decreases_energia_and_increases_networking():
    state = make_initial_state()
    new_state = apply_choice(state, "ev_day1_001", "A", catalog=test_catalog)
    assert new_state.attributes.networking == state.attributes.networking + 2
    assert new_state.attributes.energia == state.attributes.energia - 1
    assert state.attributes.networking != new_state.attributes.networking  # imutabilidade
```

## Padrão de teste de API

```python
def test_apply_choice_returns_next_event_and_persists(client, session_in_progress):
    resp = client.post(f"/api/sessions/{session_in_progress.id}/choices",
                       json={"event_id": "ev_day1_001", "option_id": "A"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["nextEvent"] is not None
    assert body["currentDay"] >= 1
```
```

### C.6 `.cursor/rules/docs-sync.mdc`

```mdc
---
description: Garante que docs/ evoluem junto com o código.
globs:
  - "docs/**/*.md"
  - "README.md"
alwaysApply: false
---

# Documentation/Context — Regras

## Quando você muda arquitetura, atualize `docs/decisions.md`

Toda mudança que afeta:
- Estrutura de pastas
- Contrato da API
- Schema do banco
- Schema dos eventos
- Stack/dependência

...precisa de entrada em `decisions.md` no formato:

```
## ADR-NNN — Título da decisão
**Data:** YYYY-MM-DD
**Status:** aceito | substituído por ADR-XXX | rejeitado
**Contexto:** ...
**Opções consideradas:** A, B, C
**Decisão:** ...
**Consequências:** o que ganhamos e o que abrimos mão
```

## README.md sempre roda

Quem clonar o repo precisa conseguir rodar seguindo o README. Se você muda comando de boot, dependência, ou variável de ambiente, **atualize o README na mesma mudança**.

## docs/api.md espelha a API real

Não invente endpoint. Não documente o que não existe. Se mudou contrato, mudou o `.md`.
```

---

## Bloco D — Documentação obrigatória

### `/docs/architecture.md` — esqueleto

```
# Arquitetura — Corporate Survivor

## Visão geral
[Diagrama de camadas em ASCII]

## Backend
### Camadas e responsabilidades
### Estrutura de pastas
### Convenções

## Frontend
### Páginas e fluxo
### Estado server vs UI
### Convenções

## Game Engine
### Pureza e isolamento
### API pública
### Carregamento e validação de eventos

## Persistência
### Modelo de dados
### Migrations
### Estratégia de save automático

## Decisões transversais
- Linguagem: PT-BR no produto, EN nos identificadores de código
- Identificadores: UUID v4 para player/session
- camelCase no wire, snake_case em Python
```

### `/docs/game-rules.md` — esqueleto

```
# Regras do Jogo — Corporate Survivor

## Atributos
| Atributo | Range | Inicial | Significado |
|---|---|---|---|
| energia | 0..10 | 7 | ... |
| reputacao | 0..10 | 5 | ... |
| networking | 0..10 | 3 | ... |
| ansiedade | 0..10 | 2 | ... |
| produtividade | 0..10 | 5 | ... |
| aprendizado | 0..10 | 4 | ... |

## Duração e ritmo
- 5 dias, exatamente 3 eventos por dia.
- Cada dia tem pool maior que 3; engine seleciona 3 entre os elegíveis.

## Schema dos eventos
[Tabela do bloco A.4]

## Tom e voz
[Diretrizes para o Agent Content]

## Tabela de tensão por dia
[Quais atributos cada dia estressa — preenchida pelo Content Agent]

## Finais
[Lista dos finais com critério e prioridade]
```

### `/docs/api.md` — esqueleto

```
# API — Corporate Survivor

Prefixo: /api
Autenticação: nenhuma (single-player, sem login)
Erros: padrão FastAPI

## POST /api/players
Cria um jogador.
### Request
{ "name": "Diego" }
### Response 201
{ "id": "...", "name": "...", "createdAt": "..." }
### Erros
- 422: name inválido

[... outros endpoints ...]

## DTOs
### SessionStateDTO
[campo a campo]
```

### `/docs/decisions.md` — esqueleto

```
# Architecture Decision Records (ADRs)

## ADR-001 — Stack: FastAPI + Vite/React + SQLite
[contexto / opções / decisão / consequências]

## ADR-002 — Engine como módulo Python puro no backend
[...]

## ADR-003 — State do jogador como JSON denormalizado em sessions.state_json
[...]

## ADR-004 — Finais como registry de predicados em Python (não DSL)
[...]

## ADR-005 — Score computado server-side, anti-cheat fora de escopo
[...]
```

### `/docs/sprint-plan.md` — documento vivo

Estado por sprint, DoD, riscos abertos. Atualizado ao fim de cada sprint pelo Agent Documentation.

### `/docs/cursor-workflow.md` — como humano + IA colaboram

```
# Cursor Workflow

## Agentes
Lista os 7 agentes, sua identidade e onde encontrar suas rules.

## Fluxo de uma tarefa
1. Humano decide sprint e abre HANDOFF.md.
2. Humano invoca o agente apropriado com o prompt template (Bloco B).
3. Agente lê suas rules + docs relevantes.
4. Agente executa.
5. Agente atualiza HANDOFF.md.
6. Próximo agente pega o handoff.

## HANDOFF.md
[template]

## Fim de sprint
1. Agent QA/Tests roda suite completa.
2. Agent Auditor roda audit.sh e produz relatório.
3. Agent Documentation atualiza sprint-plan.md e decisions.md.
4. Humano fecha sprint.
```

---

## Bloco E — Protocolo HANDOFF e governança

### E.1 `HANDOFF.md` — template

Arquivo na raiz do repo. Reescrito a cada passagem entre agentes/sessões.

```markdown
# HANDOFF — Sprint N — <data/hora>

## Estado atual
- Última coisa concluída:
- Em andamento:
- Bloqueado por:

## O que o próximo agente precisa fazer
- [ ] Tarefa específica 1
- [ ] Tarefa específica 2

## Decisões tomadas nesta sessão
- ...

## Arquivos tocados
- backend/engine/scoring.py (criado)
- docs/game-rules.md (atualizado seção "Atributos")

## Notas para o Auditor
- Coverage da engine após mudança: 92%
- Não atualizei docs/api.md porque não mudei API — confirmar
```

### E.2 `scripts/audit.sh`

Conteúdo completo já no Bloco B.6.

### E.3 Política de `decisions.md`

Toda PR/sprint que altere uma das categorias do `docs-sync.mdc` exige nova entrada ADR. O Auditor faz `git diff` entre o início e fim da sprint e flagga se houve mudança arquitetural sem ADR correspondente.

---

## Bloco F — Sprint plan

Total estimado: 5 sprints curtos, ~8-12 dias úteis dependendo da intensidade.

### Sprint 0 — Foundation (1 dia)

**Objetivo:** repo executável vazio, com toda a estrutura de rules e docs no lugar.

**Tarefas:**
- Scaffold de pastas (`/frontend`, `/backend`, `/docs`, `/.cursor/rules`).
- `backend/`: `pyproject.toml` com FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, ruff, mypy, pytest.
- `frontend/`: `npm create vite@latest`, TS, Tailwind, React Query, react-router-dom, vitest.
- `/.cursor/rules/*.mdc` com conteúdo do Bloco C.
- `/docs/*.md` com esqueletos do Bloco D (cabeçalhos preenchidos, conteúdo TBD).
- `README.md` com setup local funcional.
- `scripts/audit.sh` com os checks já existentes (lint, typecheck, vazios para o resto).
- Health endpoint `GET /api/health` + página inicial mínima do front consumindo.

**DoD verificável:**
- [ ] `bash scripts/audit.sh` roda sem erro.
- [ ] `cd backend && uvicorn app:app --reload` sobe.
- [ ] `cd frontend && npm run dev` abre página dizendo "Corporate Survivor — API: ok".
- [ ] Todas as rules `.mdc` existem com frontmatter válido.
- [ ] README ensina a rodar do zero em < 5 minutos.

### Sprint 1 — Engine pura + conteúdo (2-3 dias)

**Objetivo:** engine completa testada + 15 eventos de qualidade.

**Tarefas:**
- `engine/state.py`: `Attributes`, `GameState` (frozen dataclasses).
- `engine/events.py`: `Event`, `EventCatalog`, `load_events()`, `validate_events()`.
- `engine/choices.py`: `validate_choice`, `apply_choice`.
- `engine/selection.py`: `next_event_or_finish` (seleção entre elegíveis, considerando unlock/block/atributos).
- `engine/scoring.py`: `compute_score`.
- `engine/endings.py`: registry + 7 finais (Trainee Lenda, Promessa, Sobrevivente, Invisível, Risco Operacional, Burnout, Demitido).
- `engine/data/events.json` com 15-18 eventos (Agent Content).
- Testes: pytest cobrindo engine ≥ 90%.

**DoD:**
- [ ] `python -m engine.validate_events` sai 0.
- [ ] `pytest backend/tests/engine -q` passa.
- [ ] Coverage engine ≥ 90%.
- [ ] Doc `docs/game-rules.md` preenchida com atributos, ranges, iniciais, finais.
- [ ] Tabela de tensão por dia em `game-rules.md`.

### Sprint 2 — API + Persistência + Save automático (2 dias)

**Objetivo:** API completa funcionando contra SQLite.

**Tarefas:**
- `db/models.py`, `db/repositories.py`, `db/session.py`.
- Alembic init + primeira migration.
- DTOs Pydantic em `schemas/`.
- Use cases: `create_player`, `start_session`, `apply_choice`, `get_session_state`, `restart_session`, `get_ranking`.
- Routers: `players.py`, `sessions.py`, `ranking.py`.
- Boot: validação do `events.json` antes de aceitar requests.
- Testes de contrato (httpx).
- Atualizar `docs/api.md`.

**DoD:**
- [ ] `pytest backend/tests/api -q` passa.
- [ ] Curl manual passa pelos 6 endpoints e produz resultados coerentes.
- [ ] `audit.sh` continua verde.
- [ ] `docs/api.md` 100% bate com endpoints reais (Auditor verifica).
- [ ] ADRs 1-5 escritas em `decisions.md`.

### Sprint 3 — Frontend (2-3 dias)

**Objetivo:** experiência completa do jogador, responsiva.

**Tarefas:**
- Páginas: HomePage (tela inicial), NewGamePage (cadastro de nome), GamePage (evento + opções + barra de atributos), EndingPage (final + score), RankingPage (top global).
- Componentes: `AttributeBar`, `EventCard`, `OptionButton`, `DayIndicator`, `RankingTable`, `LoadingState`, `ErrorState`.
- Hooks React Query: `useCreatePlayer`, `useStartSession`, `useSession`, `useApplyChoice`, `useRestartSession`, `useRanking`.
- Roteamento react-router-dom: `/`, `/new`, `/game/:sessionId`, `/end/:sessionId`, `/ranking`.
- Persistência de `sessionId` em `localStorage` para retomar (e SÓ o id; estado vem do server).
- Estilo Tailwind, responsivo 360px+.
- Animações leves nas transições de evento.
- Testes Vitest dos componentes-chave.

**DoD:**
- [ ] Fluxo completo: cadastro → 5 dias → final → ranking, sem mock.
- [ ] Recarregar a aba retoma a partida exata.
- [ ] Reset funciona.
- [ ] Responsivo testado em 360px, 768px, 1280px.
- [ ] `audit.sh` continua verde.
- [ ] Nenhum string narrativa hardcoded no frontend (Auditor com grep).

### Sprint 4 — Polish + Auditoria final (1 dia)

**Objetivo:** entrega.

**Tarefas:**
- Eventos secretos/desbloqueáveis (opcional do desafio — 2-3 eventos com `unlock` complexo).
- Balanceamento final dos finais (algumas rodadas para confirmar que vários finais são alcançáveis).
- README com screenshots, fluxo de execução, decisões principais resumidas.
- `docs/audits/sprint-4.md` final.
- Vídeo curto (opcional, mas pesa em avaliação de "experiência").

**DoD:**
- [ ] Todos os finais alcançáveis em pelo menos uma trajetória (manual).
- [ ] 3+ trajetórias completas registradas em `docs/playthroughs/`.
- [ ] README permite clone+run em < 5 minutos.
- [ ] `audit.sh` 100% verde.
- [ ] Todas as 7 ADRs escritas e coerentes com código.

---

## Bloco G — Riscos e mitigações

| # | Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| R1 | Eventos saem genéricos, narrativa fraca | Alta | Alto (avaliação UX) | Agent Content separado; tabela de tensão por dia; revisão manual de cada evento antes do commit |
| R2 | Engine acopla acidentalmente ao framework | Média | Alto | `audit.sh` check #2 (grep por imports proibidos); rules `.mdc` explícitas; testes da engine sem fixtures de DB |
| R3 | Frontend acaba com lógica de jogo | Média | Alto | Auditor grep por nomes de atributos no frontend; React Query força fonte única; rules explícitas |
| R4 | Deriva entre `events.json` e código (refs quebradas) | Alta | Médio | `validate_events()` no boot + no audit; fail fast |
| R5 | Balanceamento ruim (sempre cai no mesmo final) | Média | Médio | Sprint 4 inclui 3+ playthroughs; ajuste de `ENDING_BONUS` e thresholds |
| R6 | Save automático com race condition | Baixa | Alto | Transação única por escolha; teste de concorrência (opcional) |
| R7 | Cobertura de teste cai ao longo das sprints | Média | Médio | `--cov-fail-under=75` no CI/audit; bloqueia merge |
| R8 | Docs ficam desatualizadas | Alta | Médio (avaliação técnica) | Auditor compara API real com `api.md`; ADR exigida para mudanças arquiteturais |
| R9 | Cursor "alucina" eventos em código durante refactor de frontend | Média | Alto | Rule `frontend.mdc` explícita + `audit.sh` check #1 |
| R10 | Sobreposição entre rules causa conflito (Cursor escolhe a errada) | Baixa | Baixo | Rules têm `globs` mutuamente exclusivos |
| R11 | Trabalho do Content bloqueia QA por falta de eventos | Média | Médio | Sprint 1 entrega eventos suficientes (15+) antes da Sprint 2 começar |
| R12 | Reavaliação do desafio espera funcionalidade não-óbvia | Baixa | Alto | Releitura final do PDF do desafio no Sprint 4; checklist de requisitos |

---

## Próximos passos imediatos

1. **Você valida este documento.** Pontos onde quer mudar: stack, escopo de agente, formato de rule, ordem de sprint.
2. **Eu produzo, a partir disto:** (a) o conteúdo cheio de cada arquivo `docs/`; (b) o `events.json` inicial com 15 eventos prontos para revisar; (c) o `scripts/audit.sh` versão final; (d) o prompt-template por agente em arquivo separado para colar no Cursor.
3. **Você abre o Cursor.** Sprint 0 começa.

Se quiser, posso já entregar agora um desses (sugestão: `events.json` com os 15 eventos, porque é o maior risco de qualidade narrativa e onde o LLM mais erra sozinho).
