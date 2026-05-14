# Estrutura do repositório — mapa para humanos e LLMs

Este documento explica **onde está cada tipo de informação** após a Sprint **0.3**. Use-o como índice quando uma sessão nova precisar contexto sem reler arquivos gigantes.

Regra operacional: a raiz deve ficar limpa e servir como porta de entrada. Documentos canônicos ficam em `docs/`; snapshots e materiais de origem ficam em `_context/original/`.

## Como navegar este projeto

- Raiz = entrada e estado atual: `README.md`, `PROJECT_STATUS.md`, `HANDOFF.md`, `.env.example`, `.gitignore`.
- `docs/` = fonte canônica de arquitetura, regras, decisões, sprints e fluxo Cursor.
- `.cursor/rules/` = rules reais carregadas pelo Cursor para reforçar limites dos agentes.
- `_context/original/` = histórico/snapshot; não é fonte de verdade para novas tarefas.
- `scripts/` = validações e utilitários. No Windows, a auditoria principal é `scripts/audit.ps1`.
- `backend/` e `frontend/` existem em forma mínima de healthcheck; engine e jogo ainda não existem.

| Pasta/arquivo | Responsabilidade |
|---|---|
| `README.md` | Porta de entrada humana e orientação rápida |
| `PROJECT_STATUS.md` | Status executivo atual |
| `HANDOFF.md` | Registro do último trabalho e passagem entre agentes |
| `docs/00-start/` | Por onde começar: estrutura, sprint plan e setup |
| `docs/01-governance/` | Como a IA trabalha: agentes, workflow e decisões |
| `docs/02-product/` | O que será construído: arquitetura, API e regras do jogo |
| `docs/03-validation/` | Como validar: auditorias e playthroughs |
| `.cursor/rules/` | Regras reais do Cursor por domínio |
| `scripts/` | Auditoria e utilitários operacionais |
| `_context/original/` | Snapshots históricos dos documentos originais |
| `backend/` | Backend FastAPI mínimo com `GET /api/health` |
| `frontend/` | Frontend Vite + React + TypeScript mínimo que exibe o healthcheck |

## Árvore lógica

```
README.md                 → porta de entrada humana
HANDOFF.md                → última sessão / declaração do agente (obrigatório ao encerrar trabalho com mudanças)
PROJECT_STATUS.md         → status executivo atual
.env.example              → variáveis públicas esperadas (.env real ignorado pelo git)
.gitignore                → segredos, artefatos de build, DB local

docs/
  00-start/
    project-structure.md  → ESTE ARQUIVO — mapa do repo
    sprint-plan.md        → Sprints, DoD, ordem sugerida
    setup-company-env.md  → CANÔNICO — setup máquina corporativa / troubleshooting
  01-governance/
    agent-usage.md        → quem edita o quê + rules associadas
    cursor-workflow.md    → HANDOFF + fluxo Cursor
    decisions.md          → ADRs (Alembic vs create_all, finais, Node portátil, ...)
  02-product/
    architecture.md       → camadas e stack alvo (atualizar quando código existir)
    api.md                → contrato HTTP (stub → OpenAPI espelhado no futuro)
    game-rules.md         → CANÔNICO — regras do jogo + schema events.json + catálogo narrativo
  03-validation/
    audits/               → relatórios por sprint (Auditor preenche)
    playthroughs/         → roteiros manuais de regressão narrativa

.cursor/rules/
  _dispatcher.mdc         → sempre aplicado — escolha do agente + limites
  frontend.mdc            → ao trabalhar em frontend/**
  backend.mdc             → ao trabalhar em backend/** excluindo engine (ver texto da rule)
  game-engine.mdc         → ao trabalhar em backend/engine/**/*.py
  events-json.mdc         → ao trabalhar em backend/engine/data/events.json
  tests.mdc               → ao trabalhar em testes automatizados
  docs-sync.mdc           → ao trabalhar em docs/** ou README.md

scripts/
  audit.sh                → checagens leves do repo (expandir com código)
  audit.ps1               → auditoria principal no Windows/PowerShell
  reset_db.sh             → convenção para apagar SQLite local quando backend existir

_context/original/
  corporate-survivor-*.md → snapshots das especificações que estavam na raiz
  corporate-survivor-plano.md → snapshot do primeiro plano
  PROJECT_STATUS.md       → cópia do baseline na época da cópia (não substitui raiz)
```

## Fontes “canônicas” vs arquivo morto

| Tema | Canônico no dia a dia | Snapshot / histórico |
|------|------------------------|----------------------|
| Regras do jogo | **`docs/02-product/game-rules.md`** | `_context/original/corporate-survivor-game-rules.md` |
| Setup empresa | **`docs/00-start/setup-company-env.md`** | `_context/original/corporate-survivor-setup-company-env.md` |
| Plano macro | **`docs/00-start/sprint-plan.md`** + ADRs | `_context/original/corporate-survivor-plano-v2.md` |

Arquivos `corporate-survivor-*.md` ou `corporate-survivor-plano.md` **não devem ficar soltos na raiz**. Se existirem, a auditoria deve falhar, pois eles concorrem com as fontes canônicas.

## O que ainda não existe

- Engine, fluxo de jogo, sessões, ranking e persistência oficial de jogo — virão nas próximas sprints específicas.  
- **`events.json`** definitivo na árvore do produto — conteúdo está especificado em `docs/02-product/game-rules.md` até materialização pela Engine.

## Como uma LLM deve navegar uma tarefa típica

1. Começar por `README.md`, `PROJECT_STATUS.md` e `HANDOFF.md`.  
2. Ler **`docs/01-governance/agent-usage.md`** para saber qual agente simula.  
3. Abrir rule `.mdc` correspondente em `.cursor/rules/`.  
4. Ler docs citados pela rule (`docs/02-product/api.md`, `docs/02-product/game-rules.md`, ...).  
5. Ignorar arquivos legados na raiz como fonte de verdade.  
6. Ao terminar com mudanças, atualizar **`HANDOFF.md`** conforme `docs/01-governance/cursor-workflow.md`.

## Como um revisor humano audita

1. Confere **`HANDOFF.md`** vs `git diff`.  
2. Confere se mudanças respeitam limites em **`docs/01-governance/agent-usage.md`**.  
3. Para decisões estruturais, exige entrada em **`docs/01-governance/decisions.md`**.  
4. Rodar **`scripts/audit.ps1`** no Windows; `scripts/audit.sh` é alternativa para Git Bash/WSL.
