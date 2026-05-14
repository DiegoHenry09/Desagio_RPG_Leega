# Histórico de sprints — Corporate Survivor

Linha do tempo **curta**. Detalhes e evidências completas ficam em `docs/03-validation/audits/` e em commits/diffs.

| Sprint | Objetivo | Status | Evidência principal | Relatório |
|--------|----------|--------|---------------------|-----------|
| **0.0** | Baseline / contexto antes da governança estruturada | Concluído (histórico) | Material em `_context/original/`, baseline em docs iniciais | — |
| **0.1** | Governança: `docs/`, `.cursor/rules/`, scripts stub, README | Estrutura base ✅ | Árvore `docs/`, rules `.mdc`, `scripts/` | — |
| **0.1-B** | Governança: raiz limpa, `audit.ps1`, critérios LLM | Concluído tecnicamente | `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` | — |
| **0.1-C** | Navegação README / `project-structure` / agent-usage | Concluído tecnicamente | Navegação atual em `README.md` | — |
| **0.1-D** | Reorganização visual `docs/` (00–03) | Concluído tecnicamente | Pastas `docs/00-start` … `03-validation` | — |
| **0.2** | Backend mínimo: `GET /api/health` | Fechado tecnicamente | `pytest`, `Invoke-RestMethod` / curl → `{"status":"ok"}` | [`sprint-0.2.md`](audits/sprint-0.2.md) |
| **0.2-A** | Aceite / documentação Sprint 0.2 | Fechado tecnicamente | Relatório `sprint-0.2.md`, README gestor | [`sprint-0.2.md`](audits/sprint-0.2.md) |
| **0.3** | Frontend mínimo: Vite + React + TS, UI + healthcheck | Fechado tecnicamente | `npm run typecheck`, dev `5173`, proxy `/api/health` | [`sprint-0.3.md`](audits/sprint-0.3.md) |
| **0.3-A** | Fechamento doc: relatório 0.3, histórico, HANDOFF vivo | Fechado tecnicamente | Este arquivo + `sprint-0.3.md` + `HANDOFF.md` enxuto | [`sprint-0.3.md`](audits/sprint-0.3.md) |
| **1.0** | Regras críticas do jogo + contrato da engine (final antecipado decidido — ADR-010 substitui ADR-007) | Fechada tecnicamente (aceite humano ✅) | `game-rules.md` §4.4 + §11; `decisions.md` ADR-010; `sprint-plan.md` (Sprint 1.0/1.1/1.2) | [`sprint-1.0.md`](audits/sprint-1.0.md) |
| **1.1** | Engine skeleton + schema `events.json` (Python puro; 43 testes; placeholder validável) | Fechada tecnicamente (aceite humano ✅) | 44/44 pytest; `audit.ps1` OK; `backend/engine/` criado | [`sprint-1.1.md`](audits/sprint-1.1.md) |
| **1.1-A** | Fechamento documental Sprint 1.1 (aceite registrado, PROJECT_STATUS/HANDOFF atualizados) | Fechada | `sprint-1.1.md` §10 preenchido; `sprint-history.md` atualizado | — |
| **1.1-B** | Dossiê executivo + README atualizado (ponto de entrada para gestor/avaliador) | Fechada | `executive-overview.md` criado; README com link ao dossiê; `audit.ps1` OK | — |
| **1.2** | Catálogo completo dos 15 + 2 eventos (narrativa real, balanceamento, 3 playthroughs) | Fechada tecnicamente (aceite humano pendente) | 44/44 pytest; `audit.ps1` OK; 3 playthroughs verificados | [`sprint-1.2.md`](audits/sprint-1.2.md) |
| **1.2-A** | Atualização do dossiê executivo pós-auditoria (§2, §7, §8, §10 corrigidos para refletir Sprint 1.2 concluída) | Fechada | `executive-overview.md` atualizado; `audit.ps1` OK | — |
| **2.0** | Persistência SQLite + modelos base (SQLAlchemy 2.0; 5 modelos; repositories CRUD; `init_db()` no lifespan FastAPI conforme ADR-006; 21 novos testes) | Fechada tecnicamente (aceite humano ✅) | 65/65 pytest (44 pré-existentes + 21 novos); `audit.ps1` OK; `backend/db/`, `backend/models/`, `backend/repositories/` criados | [`sprint-2.0.md`](audits/sprint-2.0.md) |
| **2.1** | API de Player e Sessão Inicial (… 32 novos testes) | Fechada tecnicamente (aceite papel §10 opcional / aceite técnico humano ✅) | 97 pytest na entrega 2.1; ver §10bis atual checklist CORS/handlers | [`sprint-2.1.md`](audits/sprint-2.1.md) |
| **2.2** | Choices + engine persistidas (`POST /choices`, ranking ao fim; `secrets_seen_json`; CORS headers restritos) | Fechada tecnicamente (aceite papel pendente) | 103 pytest; `audit.ps1` OK — ver [`sprint-2.2.md`](audits/sprint-2.2.md) | [`sprint-2.2.md`](audits/sprint-2.2.md) |
| **2.2-B** | Correções QA pré-Sprint 2.3 (4 testes novos: 404 sessão inexistente, count Decision, ranking==0 antes do fim, mismatch `event_id` válido; `sprint-2.2.md` ganha §4.A Agent/Rules/Skills + §7.2 playbook reset SQLite; HANDOFF/PROJECT_STATUS sincronizados) | Fechada tecnicamente (aceite papel pendente) | 107 pytest (103 + 4); `audit.ps1` OK; zero alteração em código de produção | [`sprint-2.2-B.md`](audits/sprint-2.2-B.md) |
| **2.3** | Ranking API pública: `GET /api/ranking?limit=10` (envelope `{items, limit, count}`, ordem `score desc + tie-break determinístico`, `session_id` ocultado, bounds `1..100` no `limit`) + 9 testes novos (vazio, ordenação, default/custom limit, leak `session_id`, 3× bounds 422, smoke fim-a-fim até `demitido`). Engine/CORS/repositories/models intactos. | Fechada tecnicamente (aceite papel pendente) | 116 pytest (107 + 9); `audit.ps1` OK; `api.md` atualizado | [`sprint-2.3.md`](audits/sprint-2.3.md) |

## Próxima sprint

**Backlog engine/UX**: `apply_secret_choice` (segunda etapa do fluxo secreto) e **Sprint 3** (UX completa do frontend). Paralelo: **Architect/Documentation** fecha `executive-overview.md` cobrindo 2.x (`2.0-A/2.1-A` agregando 2.2 + 2.2-B + 2.3).

## Pendências transversais

- Aceites humanos burocráticos legados quando aplicável (Sprints **2.1 §11**, **2.2 §8**, **2.2-B §10**, **2.3 §10** com aceite papel pendente — podem ser aceitos em conjunto).  
- Dossier executivo (2.x).  
- Fluxo secreto completo (`apply_secret_choice`) — backlog de engine/UX.
- Reset SQLite local pós-2.2 (ver [`sprint-2.2.md §7.2`](audits/sprint-2.2.md#7-pendências-conscientes)).

Atualizar esta tabela quando fechar novas sprints; não duplicar aqui o conteúdo dos relatórios de auditoria.
