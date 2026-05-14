# Corporate Survivor — Dossiê Executivo

> Ponto de entrada para gestores, avaliadores e novos participantes.  
> Este documento aponta para as fontes técnicas detalhadas — não as duplica.  
> Atualizado por: **Agent Architect/Documentation** — Sprint 1.2-A (2026-05-14).

---

## 1. Resumo do projeto

**Corporate Survivor** é um mini RPG corporativo narrativo em que o jogador assume o papel de um trainee sobrevivendo à primeira semana em uma empresa. Cada decisão altera atributos do personagem (energia, reputação, networking, ansiedade, produtividade, aprendizado) e leva a um dos 7 finais possíveis.

O projeto atende ao **Desafio Trainees — Cursor + Engenharia de Contexto** ([`desafio_trainees_cursor_v3.pdf`](../../desafio_trainees_cursor_v3.pdf)), que avalia não apenas a entrega de software funcional, mas a **capacidade de organizar inteligência**: estruturar contexto, tomar decisões de arquitetura registradas, documentar conhecimento e governar a colaboração entre humanos e IA de forma rastreável.

O objetivo real não é só um jogo. É demonstrar:

- Arquitetura desacoplada e extensível.
- Uso correto de IA com regras, papéis e evidências.
- Documentação que permite que outra pessoa entenda e evolua o sistema rapidamente.
- Separação clara de responsabilidades entre frontend, backend e engine.

---

## 2. Estado atual (2026-05-14)

| Componente | Status |
|---|---|
| Governança (docs, rules, scripts) | Criada e validada |
| Backend healthcheck (`GET /api/health`) | Implementado e aceito |
| Frontend healthcheck (Vite + React, `API: ok`) | Implementado e aceito |
| Regras críticas do jogo (finais, gatilhos, engine contract) | Decididas e documentadas — ADR-010 aceita |
| Engine skeleton (Python puro, tipos, validate_events, apply_choice) | Criada e aceita — 44/44 testes |
| `events.json` — catálogo narrativo real | 15 eventos principais + 2 secretos; 3 playthroughs documentados — Sprint 1.2 fechada tecnicamente (aceite humano pendente) |
| API de sessão/jogo | Não implementada ainda |
| Persistência SQLite | Não implementada ainda |
| Frontend jogável | Não implementado ainda |
| Ranking | Não implementado ainda |

**Próxima ação:** aceite humano da Sprint 1.2; depois Sprint 2 — integração engine↔API e persistência SQLite.

Para o estado detalhado e atualizado em tempo real: [`PROJECT_STATUS.md`](../../PROJECT_STATUS.md).

---

## 3. Arquitetura em alto nível

O sistema é dividido em camadas com responsabilidades rígidas. Cada camada tem uma rule Cursor associada que reforça os limites para a IA.

```
┌─────────────────────────────────────────┐
│  Frontend  (React + Vite + TypeScript)  │  thin client: exibe estado, envia escolhas
│  Regra: nunca calcula score/final       │
└───────────────────┬─────────────────────┘
                    │ HTTP (JSON)
┌───────────────────▼─────────────────────┐
│  Backend  (FastAPI + Pydantic)          │  routers finos, validação de payload
│  Use cases: orquestram fluxo/transação  │
│  Repositories: única camada com SQLite  │
└───────────────────┬─────────────────────┘
                    │ chama
┌───────────────────▼─────────────────────┐
│  Engine  (Python puro)                  │  estado imutável, regras, score, finais
│  Regra: sem FastAPI/SQLAlchemy/React    │  carrega events.json, aplica consequências
└─────────────────────────────────────────┘
```

**Princípios:**

- O **backend** é a fonte da verdade para estado de jogo, score e finais.
- O **frontend** é thin client — nunca calcula consequências nem decide final.
- A **engine** é Python puro desacoplado — não conhece HTTP, banco ou UI.
- **Eventos** nunca são hardcoded na interface — vêm de `events.json` (configuração).
- **SQLite** é o banco obrigatório conforme desafio.
- **Governança** vive em `docs/` + `.cursor/rules/` + `HANDOFF.md` + `scripts/audit.ps1`.

Detalhes técnicos das camadas: [`docs/02-product/architecture.md`](../02-product/architecture.md).

---

## 4. Tecnologias usadas

### Já validadas neste ambiente

| Tecnologia | Versão | Para que serve |
|---|---|---|
| Python | 3.12 (via `py -3.12`) | Backend + engine |
| FastAPI | ≥ 0.110 | API HTTP do backend |
| pytest | ≥ 8.0 | Testes unitários do backend/engine |
| Node.js | 20 LTS (portátil) | Frontend |
| npm | 10 | Gerenciamento de dependências frontend |
| React | 18 | Interface do jogo |
| Vite | 5 | Build e dev server do frontend |
| TypeScript | 5 | Tipagem do frontend |
| PowerShell / `audit.ps1` | — | Auditoria de governança no Windows |
| Cursor rules (`.mdc`) | — | Reforço de papéis e limites para a IA |

### Planejadas para sprints futuras

| Tecnologia | Sprint alvo | Para que serve |
|---|---|---|
| SQLAlchemy 2.0 | Sprint 2+ | ORM + repositórios do backend |
| SQLite | Sprint 2+ | Persistência de sessões, ranking, decisões |
| Alembic (ou `create_all`) | Sprint 2+ | Migrations (ADR-006 define fallback) |
| Pydantic v2 | Sprint 2+ | Schemas da API |
| TanStack Query | Sprint 3+ | Cache de estado no frontend |
| Tailwind CSS | Sprint 3+ | Estilização da UI |
| CORS (FastAPI) | Sprint 2 | Integração browser ↔ API sem proxy |

Setup completo do ambiente: [`docs/00-start/setup-company-env.md`](setup-company-env.md).

---

## 5. Como usamos IA no projeto

A IA (Cursor + LLM) não é tratada como um desenvolvedor autônomo. É tratada como um **colaborador com papéis declarados e limites verificáveis**.

**Papéis operacionais (Agents):**

| Agent | Domínio | Rule associada |
|---|---|---|
| Architect/Documentation | `docs/**`, `README.md`, ADRs | `docs-sync.mdc` |
| Backend | `backend/**` exceto `engine/` | `backend.mdc` |
| Frontend | `frontend/**` | `frontend.mdc` |
| Engine/Content | `backend/engine/**`, `events.json` | `game-engine.mdc` |
| Auditor/QA | `**/tests/**`, relatórios | `tests.mdc` |

**Protocolo obrigatório a cada sessão:**

1. Declarar o Agent ativo.
2. Declarar a sprint ativa.
3. Listar arquivos que pretende ler, alterar e não tocar.
4. Listar riscos de violar arquitetura.
5. Só então propor ou executar mudanças.
6. Ao encerrar: atualizar `HANDOFF.md` com evidências.

**Skills formais do Cursor:** ainda não utilizadas neste projeto. A governança atual usa Rules + Docs + HANDOFF + Audit. Se Skills forem criadas no futuro, devem encapsular estes mesmos protocolos, não substituí-los.

Detalhes completos: [`docs/01-governance/agent-usage.md`](../01-governance/agent-usage.md) e [`docs/01-governance/cursor-workflow.md`](../01-governance/cursor-workflow.md).

---

## 6. Como validamos entregas

Toda sprint passa por um processo de validação antes de ser aceita:

| Mecanismo | Descrição |
|---|---|
| **Checkpoint de abertura** | Agent declarado, sprint declarada, escopo e proibições listados antes de qualquer mudança |
| **`audit.ps1`** | Script PowerShell que verifica presença dos arquivos de governança e raiz limpa. Resultado: `OK` ou `FAIL` com mensagem |
| **Testes automatizados** | `pytest` no backend/engine; `npm run typecheck` no frontend. Evidência: saída completa registrada no relatório de aceite |
| **Relatório de aceite** | Arquivo `docs/03-validation/audits/sprint-X.Y.md` com escopo, evidências, arquivos tocados/proibidos e DoD verificado item a item |
| **Aceite humano** | Campo explícito no relatório preenchido pelo humano após revisão |
| **HANDOFF** | `HANDOFF.md` atualizado ao final de cada sessão com o que foi feito, o que falta e as evidências |

Um output de LLM só é aceito se: declarou Agent, declarou sprint, ficou no escopo, não misturou domínios, trouxe evidências e atualizou o HANDOFF. Critério completo: [`docs/01-governance/agent-usage.md`](../01-governance/agent-usage.md) §"Critério de aceite/rejeição".

---

## 7. O que já foi concluído

| Sprint | Objetivo | Status | Evidência principal | Relatório |
|---|---|---|---|---|
| **0.1–0.1-D** | Governança: `docs/`, `.cursor/rules/`, scripts, README navegável | Concluída ✅ | Árvore `docs/`, rules `.mdc`, `audit.ps1` passando | — |
| **0.2** | Backend mínimo: `GET /api/health` → `{"status":"ok"}` | Aceita ✅ | `pytest` + `Invoke-RestMethod` | [`sprint-0.2.md`](../03-validation/audits/sprint-0.2.md) |
| **0.3** | Frontend mínimo: Vite + React + TS, UI com `API: ok` | Aceita tecnicamente ✅ | `npm run typecheck`, proxy Vite | [`sprint-0.3.md`](../03-validation/audits/sprint-0.3.md) |
| **1.0** | Regras críticas do jogo: finais, gatilhos antecipados, contrato da engine (ADR-010) | Aceita ✅ | `game-rules.md` §4.4 + §11, `decisions.md` ADR-010 | [`sprint-1.0.md`](../03-validation/audits/sprint-1.0.md) |
| **1.1** | Engine skeleton: tipos imutáveis, validate_events, apply_choice, 43 testes | Aceita ✅ | 44/44 pytest, `audit.ps1` OK, `backend/engine/` criado | [`sprint-1.1.md`](../03-validation/audits/sprint-1.1.md) |
| **1.2** | Catálogo narrativo real: 15 eventos principais + 2 secretos, balanceamento ajustado, 3 playthroughs | Fechada tecnicamente (aceite humano pendente) | 44/44 pytest, `audit.ps1` OK, 3 playthroughs verificados | [`sprint-1.2.md`](../03-validation/audits/sprint-1.2.md) |

Linha do tempo completa com todas as sub-sprints: [`docs/03-validation/sprint-history.md`](../03-validation/sprint-history.md).

---

## 8. O que falta construir

Em ordem de dependência (não iniciar o próximo sem aceite humano do anterior):

| Ordem | Ação / Sprint | Entregável | Agent responsável |
|---|---|---|---|
| 1 | **Aceite humano — Sprint 1.2** | Preencher campo §10 de `docs/03-validation/audits/sprint-1.2.md` | Humano |
| 2 | **Sprint 2** | API de sessão/jogo: routers finos, schemas Pydantic, use cases, persistência SQLite, CORS | Backend |
| 3 | **Sprint 3** | Frontend jogável: fluxo completo, save/continuar/reiniciar, ranking, UX responsiva | Frontend |
| 4 | **Sprint 4** | Auditoria final: playthroughs de todos os 7 finais, cobertura de testes, regressão narrativa | Auditor/QA |

Plano detalhado com DoD por sprint: [`docs/00-start/sprint-plan.md`](sprint-plan.md).

---

## 9. Se o gestor pedir documentação

| Necessidade | Onde encontrar |
|---|---|
| **Visão executiva** (este documento) | `docs/00-start/executive-overview.md` |
| Status atual do projeto | [`PROJECT_STATUS.md`](../../PROJECT_STATUS.md) |
| Histórico de sprints | [`docs/03-validation/sprint-history.md`](../03-validation/sprint-history.md) |
| Relatórios de aceite por sprint | [`docs/03-validation/audits/`](../03-validation/audits/) |
| Arquitetura técnica | [`docs/02-product/architecture.md`](../02-product/architecture.md) |
| Regras do jogo (catálogo, finais, schema) | [`docs/02-product/game-rules.md`](../02-product/game-rules.md) |
| Contrato da API HTTP | [`docs/02-product/api.md`](../02-product/api.md) |
| Governança de IA (Agents, critérios) | [`docs/01-governance/agent-usage.md`](../01-governance/agent-usage.md) |
| Workflow com Cursor e HANDOFF | [`docs/01-governance/cursor-workflow.md`](../01-governance/cursor-workflow.md) |
| Decisões arquiteturais (ADRs) | [`docs/01-governance/decisions.md`](../01-governance/decisions.md) |
| Setup do ambiente de desenvolvimento | [`docs/00-start/setup-company-env.md`](setup-company-env.md) |
| Estrutura do repositório (mapa) | [`docs/00-start/project-structure.md`](project-structure.md) |
| Plano de sprints e DoD | [`docs/00-start/sprint-plan.md`](sprint-plan.md) |
| Último trabalho feito (passagem entre agentes) | [`HANDOFF.md`](../../HANDOFF.md) |

---

## 10. Próximo passo

**Imediato — Aceite humano da Sprint 1.2:**

Preencher o campo §10 de [`docs/03-validation/audits/sprint-1.2.md`](../03-validation/audits/sprint-1.2.md) confirmando que o catálogo narrativo (`events.json`) está aprovado para uso na integração backend/engine.

**Após aceite — Sprint 2 (Agent Backend):**

- Integrar `backend/engine/` aos routers FastAPI (use cases finos, chamadas a `apply_choice`).
- Persistir estado de sessão, atributos e decisões em SQLite via SQLAlchemy.
- Expor API de sessão/jogo conforme [`docs/02-product/api.md`](../02-product/api.md).
- Habilitar CORS para comunicação browser ↔ API sem proxy de dev.
- Criar relatório `docs/03-validation/audits/sprint-2.md` com evidências.

**Não iniciar** a Sprint 2 antes do aceite humano da Sprint 1.2.
