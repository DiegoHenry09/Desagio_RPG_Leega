# Corporate Survivor

Narrativa interativa corporativa em primeira pessoa — trainee na primeira semana. Este repositório usa **governança por agentes** (Cursor rules + documentação em `docs/`) para separar backend, frontend, engine e QA.

## Comece aqui

> **Para gestores, avaliadores ou novos participantes:** leia primeiro o **[Dossiê Executivo](docs/00-start/executive-overview.md)** — ele explica o projeto, o que já foi entregue, o que falta e onde encontrar cada documento.  
> **Entrega / validação / storytelling técnico consolidado:** **[Dossiê Final de Entrega](docs/00-start/final-delivery.md)** (Sprint 4.0 documental) — resumo executivo, UX, arquitetura, tecnologias, linha do tempo das sprints, evidências, governança de IA e limitações.

Este projeto tem backend mínimo (`GET /api/health`), frontend mínimo (`API: ok`), regras críticas do jogo formalizadas e engine skeleton criada e testada. O ambiente corporativo foi validado.

Antes de qualquer tarefa, a LLM deve declarar o agente ativo, a sprint ativa, os arquivos lidos/alterados e seguir o protocolo em `docs/01-governance/agent-usage.md` + `.cursor/rules/_dispatcher.mdc`.

| Quero encontrar... | Onde olhar |
|---|---|
| **Dossiê final (entrega / validação)** | **`docs/00-start/final-delivery.md`** |
| Estado atual | `PROJECT_STATUS.md` |
| Histórico de sprints (linha do tempo) | `docs/03-validation/sprint-history.md` |
| Último trabalho feito | `HANDOFF.md` |
| Estrutura do projeto | `docs/00-start/project-structure.md` |
| Como usar agentes | `docs/01-governance/agent-usage.md` |
| Fluxo com Cursor | `docs/01-governance/cursor-workflow.md` |
| Plano de sprints | `docs/00-start/sprint-plan.md` |
| Decisões arquiteturais | `docs/01-governance/decisions.md` |
| Rules reais do Cursor | `.cursor/rules/` |
| Histórico dos documentos originais | `_context/original/` |
| Auditoria no Windows | `scripts/audit.ps1` |

## Se o gestor pedir documentação

**Ponto de entrada único:** [`docs/00-start/executive-overview.md`](docs/00-start/executive-overview.md) — dossiê com resumo, estado atual, arquitetura, tecnologias, o que foi feito, o que falta e mapa completo de documentos.

Atalhos diretos:

| Necessidade | Arquivo |
|---|---|
| **Dossiê executivo** | `docs/00-start/executive-overview.md` |
| **Dossiê final de entrega (gestão / avaliação)** | `docs/00-start/final-delivery.md` |
| Status atual | `PROJECT_STATUS.md` |
| Histórico de sprints | `docs/03-validation/sprint-history.md` |
| Relatórios de aceite | `docs/03-validation/audits/` |
| Governança de IA | `docs/01-governance/agent-usage.md` |
| Decisões arquiteturais (ADRs) | `docs/01-governance/decisions.md` |
| Arquitetura técnica | `docs/02-product/architecture.md` |
| Regras do jogo | `docs/02-product/game-rules.md` |
| API atual | `docs/02-product/api.md` |

## Estado do repositório

- **Governança** (Sprints 0.1–0.1-D): `docs/`, `.cursor/rules/`, `scripts/audit.ps1` criados e validados.
- **Backend** (Sprint 0.2): `GET /api/health` implementado e aceito.
- **Frontend** (Sprint 0.3): Vite + React + TypeScript com healthcheck na UI, aceito.
- **Regras do jogo** (Sprint 1.0): finais, gatilhos antecipados e contrato da engine formalizados (ADR-010 aceita).
- **Engine skeleton** (Sprint 1.1): `backend/engine/` criado em Python puro, 44/44 testes, `events.json` placeholder validável — aceito.
- **Próxima sprint:** 1.2 — catálogo completo dos eventos.

## Por onde começar

| Audiência | Documento |
|-----------|-----------|
| Visão geral + navegação | **`docs/00-start/project-structure.md`** |
| Baseline de contexto | **`PROJECT_STATUS.md`** |
| Arquitetura alvo | `docs/02-product/architecture.md` |
| Regras do jogo / catálogo | `docs/02-product/game-rules.md` |
| Contrato HTTP (stub → evoluir) | `docs/02-product/api.md` |
| Decisões (ADRs) | `docs/01-governance/decisions.md` |
| Sprints e DoD | `docs/00-start/sprint-plan.md` |
| Fluxo Cursor / HANDOFF | `docs/01-governance/cursor-workflow.md` |
| Ambiente corporativo | `docs/00-start/setup-company-env.md` |
| Quem faz o quê (agentes) | `docs/01-governance/agent-usage.md` |
| Histórico / snapshots | `_context/original/` |

## Variáveis de ambiente

Copie `.env.example` para `.env` quando existir backend/frontend (valores locais **nunca** commitados).

## Scripts

- **`COMO-RODAR.txt`** — instruções rápidas (duplo clique vs dois terminais).
- **`Abrir-Jogo.bat`** (na raiz) — duplo clique no Windows: abre **backend** (`:8000`) e **frontend** (`:5173`) em janelas separadas e carrega o jogo no navegador. Reinicie fechando cada janela ou `Ctrl+C`, depois rode de novo.
- `scripts/dev-jogo.ps1` — mesmo fluxo pela linha de comando (`.\scripts\dev-jogo.ps1`). Opções: `-SkipBrowser`, `-SecondsBeforeBrowser 8`.
- `scripts/audit.ps1` — auditoria principal no Windows/PowerShell.
- `scripts/audit.sh` — auditoria equivalente para Git Bash/WSL (expandir quando houver código).
- `scripts/reset_db.sh` — reset convenção SQLite quando backend existir.

No Windows, use `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1`.

## Backend Healthcheck

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -e ".[dev]"
uvicorn app:app --reload --port 8000
```

(No PowerShell corporativo, `Activate.ps1` pode bloquear por política de execução — prefira `activate.bat`.)

Validar em outro terminal:

```powershell
Invoke-RestMethod http://localhost:8000/api/health
```

## Frontend Healthcheck

Com o backend rodando em `http://localhost:8000`:

```powershell
cd frontend
npm install
npm run dev
```

Abrir `http://localhost:5173`. A tela deve mostrar `Corporate Survivor` e `API: ok`.

Em desenvolvimento, o consumo de `/api/health` costuma passar pelo proxy do Vite; CORS explícito no backend entra em sprint futura (ver `docs/02-product/api.md`).

## Sobre Agents e Skills

Os Agents deste projeto são **papéis operacionais**, não necessariamente botões visuais do Cursor. Eles são invocados por prompt, reforçados pelas rules em `.cursor/rules/` e guiados pelos documentos em `docs/`.

Ainda não há Skills formais criadas no painel do Cursor para este projeto. Por enquanto, a governança usa **Rules, HANDOFF, Docs e Audit**. Se Skills forem criadas no futuro, elas devem encapsular estes mesmos protocolos, não substituir as rules/docs.

## Próxima ação permitida

**Sprint 1.2 — Catálogo completo dos 15 + 2 eventos** (Agent Engine/Content): substituir placeholders em `backend/engine/data/events.json` pelo conteúdo narrativo real. Não iniciar API, persistência ou frontend jogável antes do catálogo estar aceito.

Plano detalhado: [`docs/00-start/sprint-plan.md`](docs/00-start/sprint-plan.md).

## Fonte da verdade

- **Backend** é fonte da verdade para estado de jogo, score e finais (quando implementado).
- **Frontend** é thin client (sem calcular score/final oficialmente).
- **`docs/02-product/game-rules.md`** define invariantes narrativos/mecânicos esperados pela engine.
