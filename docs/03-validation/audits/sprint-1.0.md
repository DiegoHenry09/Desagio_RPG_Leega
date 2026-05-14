# Sprint 1.0 — Regras críticas do jogo e contrato da engine — Relatório de aceite

## 1. Resumo executivo

- Objetivo da sprint: fechar formalmente as regras críticas do jogo (fim de jogo, final antecipado, regra dos 5×3, eventos secretos, responsabilidades por camada) **antes** de qualquer código de engine, e registrar a decisão como ADR.
- Resultado: **FECHADA tecnicamente**, pendente de aceite humano formal.
- Decisão recomendada: aceitar a Sprint 1.0 após revisão; em seguida abrir a Sprint **1.1 — Engine skeleton + schema `events.json`** com Agent Engine/Content (sem invadir backend/frontend; sem expor API).

## 2. Escopo aprovado

- Atualização de [`docs/02-product/game-rules.md`](../../02-product/game-rules.md):
  - **§3** — nota explicando coexistência entre predicados de fim de semana e final antecipado, com reuso dos IDs `demitido`/`burnout`.
  - **§4.3** — incluído item 11 sobre coerência entre IDs antecipados e registry de finais.
  - **§4.4** — substituiu o bloco "pendente (ADR-007)" pela decisão definitiva (ADR-010) com gatilhos, mapeamento gatilho→final, ordem de avaliação, momento da checagem (após clamp), score em final antecipado, ranking de sessões antecipadas e exclusão explícita do destaque (`trainee_lenda`) como antecipado.
  - **§9** — incluído item 11 (coerência com finais antecipados) na lista do `validate_events` CLI.
  - **§11 (novo)** — Responsabilidades por camada (engine pura / backend / frontend) e fluxo de uma escolha em texto + ASCII.
- Atualização de [`docs/01-governance/decisions.md`](../../01-governance/decisions.md):
  - **ADR-007** marcada como `Substituída por ADR-010 (2026-05-14)`, com pointer para a nova ADR.
  - **ADR-010 (nova, Aceita)** — Final antecipado por atributo crítico: contém decisão, **justificativa interpretativa** do requisito "algum atributo chega a zero" do desafio, **justificativa narrativa da prioridade dos gatilhos** (`reputacao` → `energia` → `ansiedade`) e consequências para engine / ranking / UX.
  - "Pendências de ADR" sem o item de final antecipado.
- Atualização de [`docs/00-start/sprint-plan.md`](../../00-start/sprint-plan.md): Sprint 1.0 (fechada tecnicamente) e Sprint 1.1 (engine skeleton + schema). O catálogo completo dos 15 + 2 eventos foi renumerado para Sprint 1.2.
- Atualização de `PROJECT_STATUS.md`: sprint atual, pendências, próximo passo.
- Atualização de `HANDOFF.md`: estado, links rápidos, entrada de sessão segundo template de `cursor-workflow.md`.
- Atualização de [`docs/03-validation/sprint-history.md`](../sprint-history.md): linha 1.0 adicionada.
- Criação deste relatório.

## 3. Fora de escopo

- Engine, `events.json`, jogo, fluxo de sessão, ranking, score, conteúdo dos 15 + 2 eventos.
- `backend/`, `frontend/`, qualquer código de produto.
- API, persistência SQLite, healthchecks (sem alterações).
- Rules `.cursor/rules/*.mdc` e `scripts/*.ps1`/`*.sh` (não tocados).
- Skills formais do Cursor.

## 4. Agent / Rules / Skills

- **Agent usado:** Engine/Content + Architect/Documentation (cross-domain limitado a `docs/**`, `PROJECT_STATUS.md` e `HANDOFF.md`; nenhuma alteração em código de produto).
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](../../../.cursor/rules/_dispatcher.mdc), [`.cursor/rules/game-engine.mdc`](../../../.cursor/rules/game-engine.mdc), [`.cursor/rules/docs-sync.mdc`](../../../.cursor/rules/docs-sync.mdc).
- **Skills formais do Cursor:** **Skills formais não utilizadas nesta sprint** (frase obrigatória conforme [`docs/01-governance/agent-usage.md`](../../01-governance/agent-usage.md) §"Evidência de uso de Agent / Rules / Skills").
- **Como Agent/Rules ajudaram:**
  - `_dispatcher.mdc` exigiu o checkpoint inicial (agent, sprint, arquivos pretendidos, proibidos), o que evitou que a sessão deslizasse para escrever engine antecipadamente.
  - `game-engine.mdc` reforça que a engine é Python pura — refletido na §11 de `game-rules.md` e na descrição da Sprint 1.1.
  - `docs-sync.mdc` proíbe código de produção pelo Architect, e foi respeitado (todas as edições são `.md`).
  - **Domínio respeitado:** zero alteração em `backend/`, `frontend/`, `engine/`, `events.json`, `scripts/`, rules `.cursor/rules/`.

## 5. Evidências técnicas

- **Comando de auditoria:** `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1`
  - **Resultado:** `OK - governanca minima presente e raiz limpa.` (registrado abaixo na §11).
- **Arquivos alterados:**
  - [`docs/02-product/game-rules.md`](../../02-product/game-rules.md) — §3 nota, §4.3 item 11, §4.4 reescrita, §9 item 11, §11 nova.
  - [`docs/01-governance/decisions.md`](../../01-governance/decisions.md) — ADR-007 substituída, ADR-010 adicionada, Pendências atualizadas.
  - [`docs/00-start/sprint-plan.md`](../../00-start/sprint-plan.md) — Sprint 1.0 + 1.1 + 1.2.
  - `PROJECT_STATUS.md` — sprint atual, pendências, próximo passo.
  - `HANDOFF.md` — estado, links rápidos, entrada por template `cursor-workflow.md`.
  - [`docs/03-validation/sprint-history.md`](../sprint-history.md) — linha 1.0.
- **Arquivo criado:**
  - [`docs/03-validation/audits/sprint-1.0.md`](sprint-1.0.md) — este relatório.
- **Nenhum arquivo proibido tocado.**

## 6. Limitações conhecidas / decisões controversas justificadas

- **Restrição dos gatilhos antecipados a 3 atributos críticos** (energia/reputação/ansiedade) — o enunciado fala genericamente em "algum atributo chega a zero", mas a interpretação adotada (lendo conjuntamente com "demitido" e "burnout" da mesma lista) restringe os gatilhos antecipados aos canais de **colapso narrativo objetivo**. `produtividade`/`aprendizado`/`networking` permanecem influenciando finais (predicados `risco_op`, `invisivel`) e score. Justificativa completa em ADR-010.
- **Reuso dos IDs `demitido` e `burnout`** entre fim antecipado e fim de semana — escolhido para evitar "endings fantasmas" no ranking e manter o registry de finais simples. A engine pode logar diagnóstico (`trigger: reputation_zero` vs `trigger: end_of_week`) sem mudar o ID exibido.
- **Ordem de prioridade dos gatilhos** (rep > ene > ans) só é observável quando dois ou mais disparam no mesmo passo; é justificada por gravidade narrativa decrescente (ADR-010).

## 7. Validação documental

Pares consistentes (exigência de [`.cursor/rules/docs-sync.mdc`](../../../.cursor/rules/docs-sync.mdc)):

- Decisão (`decisions.md` ADR-010) ↔ regra de jogo (`game-rules.md` §4.4) ↔ plano (`sprint-plan.md` Sprint 1.0/1.1) — alinhados.
- Responsabilidades por camada (`game-rules.md` §11) ↔ arquitetura (`docs/02-product/architecture.md`) — `game-rules.md` §11 espelha a arquitetura existente, sem contradizê-la, e adiciona o detalhamento por etapa do fluxo de uma escolha. `architecture.md` não precisou ser alterado nesta sprint.
- API (`docs/02-product/api.md`) — sem alteração; o contrato HTTP atual (apenas healthcheck implementado) continua válido.
- Histórico (`sprint-history.md`) e status (`PROJECT_STATUS.md` / `HANDOFF.md`) refletem o fechamento técnico da Sprint 1.0.

## 8. Critério de aceite aplicado

- [x] Agent declarado (Engine/Content + Architect/Documentation) com checkpoint completo no início da sessão.
- [x] Sprint declarada (1.0).
- [x] Escopo respeitado (apenas `docs/**`, `PROJECT_STATUS.md`, `HANDOFF.md`).
- [x] Regra de fim de jogo (normal + antecipado) documentada em `game-rules.md` §4.4.
- [x] ADR-010 registrada (Aceita) com justificativa interpretativa do "atributo chega a zero" e justificativa da prioridade dos gatilhos.
- [x] ADR-007 fechada (Substituída).
- [x] Pendência sobre final antecipado removida de `PROJECT_STATUS.md`, `HANDOFF.md`, `decisions.md` "Pendências de ADR" e `sprint-history.md`.
- [x] Responsabilidades engine/backend/frontend claras (`game-rules.md` §11 + `architecture.md`).
- [x] Próxima sprint definida (Sprint 1.1 em `sprint-plan.md`).
- [x] `audit.ps1` passou (§11).
- [x] Nenhum código de produto alterado (sem diffs em `backend/`, `frontend/`, engine, `events.json`, `scripts/`, rules).
- [x] Skills formais não declaradas falsamente (frase obrigatória registrada em §4).

## 9. Pendências

- Aceite humano desta sprint (campo na §10).
- Aceites humanos pendentes anteriores (0.2 / 0.3 / 0.3-A) seguem registrados nos respectivos relatórios.
- CORS no backend (sprint futura, não bloqueia 1.0).
- Item opcional do DoD Sprint 0: `bash scripts/audit.sh` quando Git Bash/WSL disponível (não bloqueia 1.0).

## 10. Decisão de aceite humano

- Aceite humano: **ACEITO — 2026-05-14**.
- Observações do aceite:
  - Decisão sobre final antecipado considerada suficiente (`reputacao<=0` → demitido; `energia<=0` → burnout; `ansiedade>=10` → burnout; produtividade/aprendizado/networking não encerram imediatamente e impactam finais/score).
  - Justificativa registrada na ADR-010 aceita.
  - Skills formais não utilizadas nesta sprint — aceito.
  - Governança aplicada: Agent + Rules + Docs + HANDOFF + `audit.ps1` — aceita.
  - Próxima etapa autorizada: **Sprint 1.1 — Engine skeleton + schema `events.json`** (sem API, banco, frontend de jogo ou catálogo completo).

## 11. Evidência objetiva — saída de `audit.ps1`

Comando executado em **2026-05-14**, na raiz do repositório, em PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/audit.ps1
```

Saída literal:

```
== Corporate Survivor - audit.ps1 (governance 0.1-D) ==
OK - governanca minima presente e raiz limpa.
Nota: backend/frontend ainda nao sao exigidos nesta auditoria.
```

Exit code: **0**.
