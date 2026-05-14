# Uso dos agentes — Corporate Survivor

Este projeto opera com **cinco papéis** consolidados (plano v2). Cada papel tem limites claros para reduzir “vazamento” de responsabilidade entre LLM e para facilitar revisão humana.

## Onde estão os agentes?

Agent Backend, Frontend, Engine/Content, Auditor/QA e Architect/Docs são **papéis operacionais**. Eles não dependem de um botão visual específico do Cursor.

Cada agente é ativado pelo prompt da tarefa e reforçado pelas Cursor rules em `.cursor/rules/`. O dispatcher `_dispatcher.mdc` exige que a LLM declare o agente antes de alterar arquivos ou definir comportamento de produto.

Não há Skill formal obrigatória neste momento. Se no futuro criarmos Skills no Cursor, elas devem apenas encapsular estes mesmos protocolos, não substituir rules, docs, handoff ou auditoria.

## Tabela rápida

| Agente | Escopo típico | Rules Cursor | Docs principais |
|--------|-----------------|---------------|-----------------|
| **Architect / Documentation** | `docs/**`, `README.md`, ADRs — **sem código de produção** | `docs-sync.mdc` | `docs/02-product/architecture.md`, `docs/00-start/sprint-plan.md`, `docs/01-governance/decisions.md` |
| **Backend** | `backend/**` exceto `backend/engine/**` | `backend.mdc` | `docs/02-product/api.md`, `docs/02-product/architecture.md` |
| **Frontend** | `frontend/**` | `frontend.mdc` | `docs/02-product/api.md` |
| **Engine / Content** | `backend/engine/**`, `backend/engine/data/events.json` | `game-engine.mdc`, `events-json.mdc` | `docs/02-product/game-rules.md` |
| **Auditor / QA** | `**/tests/**`, `docs/03-validation/audits/**` — sem mudar código de produção salvo política explícita | `tests.mdc` | `docs/00-start/sprint-plan.md` |

## Protocolo comum

1. Declarar no início da resposta: **“Atuando como Agent …”**  
2. Listar rules `.mdc` e docs lidos.  
3. Só então propor edits.  
4. Cruzamento de domínios: declarar e **pausar** para confirmação humana entre Engine ↔ Backend ↔ Frontend.

## Como eu sei que uma LLM usou a governança?

Checklist mínimo:

- Declarou agente.
- Declarou sprint.
- Listou docs/rules lidos.
- Listou arquivos alterados.
- Ficou no escopo.
- Atualizou `HANDOFF.md` quando alterou arquivos.
- Rodou auditoria/teste aplicável.
- Trouxe evidências.
- Não misturou domínios.

## Evidência de uso de Agent / Rules / Skills

Para **toda sprint**, o relatório de aceite em `docs/03-validation/audits/` deve registrar:

- **Agent usado** (papel declarado e respeitado).
- **Rules consultadas** (paths em `.cursor/rules/` ou referência explícita quando o trabalho for só documentação).
- **Skills formais** do Cursor: **usadas** (como e onde) **ou** a frase obrigatória **"Skills formais não utilizadas nesta sprint"** quando não houver Skill no projeto ou não foram usadas.
- **Evidência de como Agent/Rules ajudaram** (ex.: escopo mantido, domínio correto, arquivos proibidos listados e não tocados).
- **Arquivos proibidos não tocados** (ou justificativa excepcional autorizada pelo humano).
- **Validações executadas** (testes, curls, `audit.ps1`, etc., conforme aplicável).

Regras explícitas:

- **Não é permitido** afirmar uso de Skill formal **sem evidência** (registro no relatório ou artefato verificável).
- Se não houver Skill formal no repositório ou na sprint, registrar **"Skills formais não utilizadas nesta sprint"** — isso é esperado no Corporate Survivor até Skills existirem.
- A utilidade do **Agent** é validada pelo **escopo respeitado**, **evidências objetivas** e **ausência de violação** de domínio — não basta declarar o papel sem prova.

## Critério de aceite/rejeição de output de LLM

### Output aceito somente se:

- Declarou Agent ativo.
- Declarou Sprint/etapa ativa.
- Listou arquivos lidos.
- Listou arquivos alterados.
- Respeitou arquivos permitidos/proibidos do agente.
- Ficou dentro da sprint ativa.
- Não misturou domínios sem autorização.
- Explicou riscos.
- Registrou decisões relevantes em `docs/01-governance/decisions.md`.
- Atualizou `HANDOFF.md` quando alterou arquivos.
- Trouxe evidências: comandos, testes, validações ou diff.
- Declarou pendências e próximo passo.

### Output rejeitado se:

- Implementou fora da sprint.
- Tocou backend/frontend/engine fora do agente correto.
- Criou código sem validação mínima.
- Criou decisão arquitetural sem ADR.
- Alterou API sem atualizar `docs/02-product/api.md`.
- Alterou regra de jogo sem atualizar `docs/02-product/game-rules.md`.
- Ignorou `_dispatcher.mdc`.
- Disse "feito" sem evidência.
- Usou arquivos legados da raiz como fonte da verdade.
- Inventou comportamento não previsto no desafio ou nos docs.

### Template de abertura

- Agent ativo:
- Sprint ativa:
- Arquivos lidos:
- Arquivos que pretende alterar:
- Arquivos proibidos:
- Riscos:
- Plano:
- DoD:

### Template de encerramento

- Agent usado:
- Arquivos alterados:
- Comandos/testes executados:
- Evidências:
- Docs atualizados:
- Pendências:
- Próximo passo:
- Pode fechar a sprint? sim/não e por quê.

## Onde está cada coisa

| Necessidade | Onde ler |
|-------------|----------|
| Organização do repo | `docs/00-start/project-structure.md` |
| Estado macro / baseline | `PROJECT_STATUS.md` |
| Contrato HTTP (stub → vivo) | `docs/02-product/api.md` |
| Regras do jogo / JSON | `docs/02-product/game-rules.md` |
| Ambiente Windows / empresa | `docs/00-start/setup-company-env.md` |
| Fluxo HANDOFF | `docs/01-governance/cursor-workflow.md` |
| Linha do tempo de sprints | `docs/03-validation/sprint-history.md` |

## Snapshot histórico

A pasta **`_context/original/`** guarda cópias dos grandes Markdown que estavam na raiz antes da Sprint 0.1 — útil para diff mental e auditoria, mas **`docs/02-product/game-rules.md`** e **`docs/00-start/setup-company-env.md`** são os caminhos **canônicos** para trabalho diário.
