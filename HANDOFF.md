# HANDOFF — Corporate Survivor

Arquivo **vivo e curto**. O histórico resumido das sprints está em [`docs/03-validation/sprint-history.md`](docs/03-validation/sprint-history.md). Evidências completas por sprint: [`docs/03-validation/audits/`](docs/03-validation/audits/).

Template detalhado por sessão (quando necessário): `docs/01-governance/cursor-workflow.md`.

---

## HANDOFF — 2026-05-19T11:03-03:00 — Agent Architect/Documentation — README GitHub

### Declaração

- **Atuei como:** Agent Architect/Documentation.
- **Sprint / escopo:** ajuste documental pós-publicação no GitHub; README como vitrine pública do projeto.
- **Rules consultadas:** `.cursor/rules/_dispatcher.mdc`, `.cursor/rules/docs-sync.mdc`; docs lidos: `docs/01-governance/agent-usage.md`, `PROJECT_STATUS.md`, `docs/00-start/final-delivery.md`, `docs/03-validation/sprint-history.md`, `docs/02-product/api.md`.
- **Arquivos tocados:** `README.md`, `HANDOFF.md`.
- **Não toquei:** `backend/**`, `frontend/**`, `backend/engine/**`, `docs/02-product/game-rules.md`, testes, scripts e configuração de ambiente.

### O que fiz

- Reescrevi o `README.md` para refletir o estado atual do projeto no GitHub: produto jogável, arquitetura, como rodar, governança de IA, validação e próximos passos.
- Removi referências antigas a backend/frontend mínimo e à Sprint 1.2 como próxima ação.
- Mantive seção explícita de documentação de referência, apontando para dossiê final, status, histórico de sprints, arquitetura, API, regras do jogo, decisões, governança, auditorias e referências visuais.

### O que falta / próximo agente

- Se houver nova entrega de produto, atualizar `PROJECT_STATUS.md`, `docs/03-validation/sprint-history.md` e relatórios aplicáveis.
- Para evolução técnica, acionar o agente do domínio correspondente antes de editar código.

### Evidências

- Validação documental por leitura cruzada dos documentos acima.
- Comandos Git/auditoria registrados na sessão após este handoff.

---

## HANDOFF — 2026-05-15 (sessão 18) — Agent Architect/Documentation + Auditor/QA — Sprint 4.0 (dossiê final)

### Declaração

- **Agents:** Architect/Documentation + Auditor/QA (`docs/**`, `README.md`, `PROJECT_STATUS.md`, `HANDOFF.md`, `docs/03-validation/sprint-history.md` — sem código de produção).
- **Sprint:** **4.0 — Dossiê Final de Entrega e Validação Documental.**
- **Rules consultadas:** `.cursor/rules/_dispatcher.mdc`, `.cursor/rules/docs-sync.mdc`; leitura obrigatória conforme prompt: README, PROJECT_STATUS, HANDOFF, `docs/00-start/*`, `docs/01-governance/*`, `docs/02-product/*`, `docs/03-validation/sprint-history.md`, `docs/03-validation/audits/sprint-3.0.md`, `Referencia_front_RPG/SKILL.md`, `style-guide.md`, `asset-pipeline.md`, `event-visuals-map.md`, `personas.md`, `scenes.md`.

### Deltas

- **Criado:** [`docs/00-start/final-delivery.md`](docs/00-start/final-delivery.md) — dossiê em 12 secções (resumo executivo, storytelling, UX, arquitetura, tecnologias, IA+governança, tabela de sprints, evidências, decisões, limitações, lições, próximos passos).
- **Alterados:** [`README.md`](README.md) — link ao dossiê final; [`PROJECT_STATUS.md`](PROJECT_STATUS.md) — fase validação final/entrega, Sprint 4.0 documental; [`docs/03-validation/sprint-history.md`](docs/03-validation/sprint-history.md) — linha **4.0** + “Próxima sprint” pós-4.0; este **HANDOFF**.

### Evidência

- `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` — exit **0**; saída: `OK - governanca minima presente e raiz limpa.`

### Pendências

- Atualizar `docs/00-start/executive-overview.md` para 2.x + 3.0 + 3.0-A (pendência histórica; `final-delivery.md` cobre gestores para entrega).
- Evolução de produto: assets finais, `apply_secret_choice`, testes UI, deploy quando decidido.
- Aceites papel **2.x** em lote, se o processo exigir.

### Skills formais

- **Skills formais do Cursor não utilizadas nesta sessão.** `Referencia_front_RPG/SKILL.md` é documento de referência humano, não Skill instalada.

---

## HANDOFF — 2026-05-15 (sessão 17) — Agent Setup/Frontend — atalho Windows para dev

### Declaração

- **Agents:** Setup/Environment + Frontend (scripts + npm).
- **Rules:** `_dispatcher.mdc`.

### Deltas

- **`Abrir-Jogo.bat`** (raiz) + **`scripts/dev-jogo.ps1`**: duplo clique abre 2 terminais (uvicorn `:8000`, Vite `:5173`) e o browser em `http://127.0.0.1:5173/`.
- **`frontend/package.json`**: script `npm run dev:open` (só Vite + browser).
- **`README.md`**: secção Scripts atualizada.

### Pendências

- Na primeira vez: `pip install -e ".[dev]"` no backend e `npm install` no frontend (como no README).

---

## HANDOFF — 2026-05-15 (sessão 16) — Agent Backend + Frontend — Perfil / histórico do jogador

### Declaração

- **Agents:** Backend (`backend/**` exceto engine) + Frontend (`frontend/**`).
- **Sprint:** **3.0+** — feature UX de ranking (histórico + stats).
- **Rules:** `_dispatcher.mdc`, `backend.mdc`, `frontend.mdc`; contrato em `docs/02-product/api.md`.

### Deltas

- **Backend:** `player_id` em `RankingEntryResponse`; `GET /api/players/{id}/profile`; `GET /api/players/{id}/runs/{ranking_entry_id}/choices`; repositório `list_for_player_profile`; use case `player_profile_use_cases`; testes `test_player_profile_api.py`; `test_ranking_api` atualizado (campos da linha).
- **Frontend:** `PlayerProfilePage` (stats, finais, partidas, timeline de escolhas); ranking com nome clicável; `getPlayerProfile` / `getPlayerRunChoices`.
- **Docs:** `docs/02-product/api.md`.

### Evidência

- `pytest tests/test_ranking_api.py tests/test_player_profile_api.py` — **14 passed**.
- `npm run build` (frontend) — **ok**.

### Pendências

- Nenhuma crítica; opcional: mover schemas de perfil no `api.md` para secção própria após `SessionResponse`.

---

## HANDOFF — 2026-05-15 (sessão 15) — Agent Frontend + Backend — UX sessão (nick, semana, nomes de personas)

### Declaração

- **Agents:** Frontend (`frontend/**`) + Backend (`backend/**` exceto engine) — extensão mínima de contrato para expor `player_name` no snapshot de sessão (evita persistir nick no `localStorage`, alinhado a `frontend.mdc`).
- **Sprint:** **3.0 / pós-3.0-A** — melhoria de UI jogável.
- **Rules consultadas:** `_dispatcher.mdc`, `frontend.mdc`, `backend.mdc`, `Referencia_front_RPG/SKILL.md`, `Referencia_front_RPG/personas.md`.

### Deltas

- **Backend:** `SessionResponse` + `SessionSnapshot` passam a incluir `player_name` (join lógico via `player_repository`); `choice_use_cases._snapshot_after_persist` preenche o campo; testes `test_sessions_api.py` ajustados.
- **Docs:** `docs/02-product/api.md` — exemplo JSON com `player_name`.
- **Frontend:** `SessionResponse` em `api/types.ts`; `App.tsx` + `App.css` — nick no header em **game** e **ending**; `GamePage` — faixa Seg–Sex numerada (1–5) + dia da semana por extenso no pill; `dialogueSpeakerName` + rótulos de personas alinhados ao catálogo de referência; `GamePage.css`.
- **Evidência:** `npm run build` no frontend **passou**. Pytest local não executado aqui (ambiente sem `pytest` no `python` global); rodar `pip install -e ".[dev]"` no `backend` e `pytest tests/test_sessions_api.py` antes do merge.

### Pendências

- Garantir backend atualizado em conjunto com o frontend (campo novo obrigatório no JSON).

---

## HANDOFF — 2026-05-15 (sessão 14) — Agent Frontend + Documentation — Sprint 3.0-A

### Declaração

- **Agent:** Frontend + Documentation.
- **Sprint:** **3.0-A** — Registo do smoke E2E manual, bugfix do `AttributePanel`, aceite técnico consolidado da Sprint 3.0; **sem** nova feature; **sem** alterar backend/engine/`events.json`/rules/scripts.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](.cursor/rules/_dispatcher.mdc), [`.cursor/rules/frontend.mdc`](.cursor/rules/frontend.mdc).

### Deltas

- [`docs/03-validation/audits/sprint-3.0.md`](docs/03-validation/audits/sprint-3.0.md) — secções **Smoke E2E manual**, **Bugfix observado no frontend**, **Observação sobre encerramento dos processos**; **§11 Sprint 3.0-A**; §7, §9 e §10 actualizados.
- [`HANDOFF.md`](HANDOFF.md) — esta entrada; bloco **Estado atual** / **Próximo passo** / **Pendências** sincronizados.
- [`PROJECT_STATUS.md`](PROJECT_STATUS.md) — Sprint 3.0 validada por smoke manual; próxima fase **4.0**.
- [`docs/03-validation/sprint-history.md`](docs/03-validation/sprint-history.md) — linha **3.0-A**.

### Smoke E2E

- **Manual (browser):** **passou** — `localhost:8000` + `localhost:5173`; Home → player → session → evento → escolha → atributos/evento → reload/continuar quando aplicável → ranking (detalhe em `sprint-3.0.md`).
- **Automatizado (§7.2):** mantém registo **passou com ressalvas** (HTTP sem UI completa).

### Bugfix

- **`AttributePanel`:** alinhamento da coluna numérica e da barra — [`frontend/src/components/AttributePanel.css`](frontend/src/components/AttributePanel.css) (ver relatório Sprint 3.0).

### Aceite / próxima sprint

- **Sprint 3.0:** tecnicamente **aceite** (implementação + smoke manual + documentação 3.0-A).
- **Smoke E2E global:** **passou** (manual); §7.2 permanece como evidência complementar com ressalvas.
- **Próxima sprint recomendada:** **4.0** — polimento final / UX / auditoria de entrega (e.g. assets IA, testes UI, paginação ranking).

---

## HANDOFF — 2026-05-15 (sessão 13) — Smoke E2E Sprint 3.0 (registro)

### Declaração

- **Agent:** Frontend (execução de smoke + atualização de `docs/03-validation/audits/sprint-3.0.md` e `HANDOFF.md` apenas).
- **Sprint:** **3.0** — encerramento operacional com smoke conforme [`sprint-3.0.md` §7.1 / §7.2](docs/03-validation/audits/sprint-3.0.md).
- **Escopo:** não alterar `backend/**`, `engine/**`, `events.json`, `.cursor/rules/**`, `scripts/**` (cumprido).

### Smoke E2E — resultado

- **Status:** **passou com ressalvas** — servidores locais (`uvicorn` :8000 + `npm run dev` :5173); validação do fluxo via **HTTP à API** + `GET` da raiz do Vite (HTML contém `Corporate Survivor`). Itens §7.1.9–10 (motion no DevTools + evento secreto) e **print** não executados nesta rodada; sem cliques manuais no navegador pelo agente.
- **Evidência canônica:** [`docs/03-validation/audits/sprint-3.0.md` §7.2](docs/03-validation/audits/sprint-3.0.md) (data/hora UTC, passos, trecho de saída, ranking sem `session_id`, opções só `id`/`label`).

### Aceite / próxima sprint

- **Sprint 3.0:** tecnicamente **fechada** (implementação aceita pelo PM; smoke registrado).
- **Próxima sprint recomendada:** **Sprint 4** (assets visuais finais / polish) em paralelo ao backlog **engine/UX** `apply_secret_choice`; opcional: testes de UI automatizados e paginação do ranking.

---

## HANDOFF — 2026-05-15 (sessão 12) — Agent Frontend — Sprint 3.0 (Frontend jogável mínimo com palco visual)

### Declaração

- **Agent:** Frontend.
- **Sprint:** **3.0 — Frontend jogável mínimo com palco visual**.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](.cursor/rules/_dispatcher.mdc), [`.cursor/rules/frontend.mdc`](.cursor/rules/frontend.mdc) + arquivos de referência visual autorizados pelo prompt: `Referencia_front_RPG/SKILL.md`, `style-guide.md`, `asset-pipeline.md`, `event-visuals-map.md`, `personas.md`, `scenes.md`.

### Principais deltas

**Criados (32 arquivos em `frontend/src/` + 1 audit + esta seção):**

- `frontend/src/styles/` — `tokens.css` (paleta + tipografia do style-guide), `animations.css` (keyframes + bloco global `prefers-reduced-motion`).
- `frontend/src/api/` — `types.ts` (espelho do `SessionResponse` real; `OptionPayload` sem `consequences`; `RankingItem` sem `session_id`), `client.ts` (5 endpoints + `ApiError` que preserva envelope `{error:{code,message,details}}`).
- `frontend/src/state/sessionStorage.ts` — helpers `getSessionId/setSessionId/clearSessionId/getTraineeVariant` (3 variantes).
- `frontend/src/assets/visuals/personas/` — `_index.tsx` + 7 componentes (Trainee com 3 variantes, Gestor, Gerente, Colega, Rh, Senior, LiderExterno). Placeholders geométricos viewBox `0 0 200 320` conforme `asset-pipeline.md` §"Opção D".
- `frontend/src/assets/visuals/scenes/` — `_index.tsx` + 8 componentes (SalaReuniao, MesaTrabalho, Restaurante, Bar, Banheiro, SalaApresentacao, Copa, DefaultScene). viewBox `0 0 800 400`.
- `frontend/src/assets/visuals/icons/` — `AttributeIcons.tsx` (6 ícones SVG inline com `currentColor`) + `_index.ts` (registry + labels + cores). Split por causa do lint react-refresh.
- `frontend/src/assets/visuals/sceneAnchors.ts` — pontos de ancoragem por cena (fração x/y).
- `frontend/src/assets/visuals/eventVisualsMap.ts` — `Record<event_id, { scene, personas[] }>` cobrindo os 17 eventos (15 principais + 2 secretos). Camada **de apresentação**, comentário explícito "NÃO é regra de jogo, NÃO é catálogo".
- `frontend/src/components/` — `SceneSVG`, `PersonaSVG`, `EventStage` + css, `AttributePanel` + css, `ChoiceList` + css, `SecretEventBanner` + css, `RankingPanel` + css, `EndingView` + css.
- `frontend/src/pages/` — `HomePage` + css, `GamePage` + css, `EndingPage`, `RankingPage` + css.
- `docs/03-validation/audits/sprint-3.0.md` — relatório completo no padrão das sprints anteriores.

**Alterados (mínimos):**

- `frontend/src/App.tsx` — substituído o healthcheck pelo orquestrador de estado entre Home/Game/Ending/Ranking.
- `frontend/src/App.css` — substituído por shell mínimo (header/main/footer).
- `frontend/src/index.css` — importa `styles/tokens.css` + `styles/animations.css`; mantém reset.
- `HANDOFF.md` (esta seção), `PROJECT_STATUS.md`, `docs/03-validation/sprint-history.md` — sincronia documental rotineira.

### Escopo preservado (proibido — verificado)

- `backend/**`, `backend/engine/**`, `backend/engine/data/events.json`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/**`, `docs/01-governance/**`, `docs/00-start/**`, `_context/**`, `Referencia_front_RPG/**` → **zero alterações**.
- `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig*.json`, `frontend/eslint.config.js`, `frontend/index.html`, `frontend/src/main.tsx`, `frontend/public/icons.svg`, `frontend/README.md` → **zero alterações** (zero deps novas instaladas).

### Evidências

- `npm install` em `frontend/` → "up to date, audited 154 packages, found 0 vulnerabilities". Exit 0.
- `npm run typecheck` → tsc --noEmit, saída vazia. Exit 0.
- `npm run build` → `dist/index.html 0.47kB | gzip 0.30kB`, `dist/assets/index-*.css 17.23kB | gzip 3.65kB`, `dist/assets/index-*.js 236.73kB | gzip 70.21kB`. 61 módulos transformados. Exit 0. Bundle final gzipado **74 KB** (dentro do orçamento do SKILL.md "página inteira ≤ 500KB").
- `npm run lint` → saída vazia. Exit 0. Inicialmente reportou 10 erros (no-useless-assignment, react-refresh, set-state-in-effect) — todos corrigidos antes do fechamento.
- `audit.ps1` → "OK - governanca minima presente e raiz limpa." Exit 0.
- Greps de governança:
  - `rg "consequences|compute_score|apply_choice|resolve_ending" frontend/src` → 2 hits, **apenas em comentários** explicando "deliberadamente NÃO".
  - `rg -i "fastapi|sqlalchemy|pydantic" frontend/src` → **0 matches** (desacoplamento total).
  - `rg "session_id" frontend/src` → 2 hits, **apenas em comentários** documentando a invariante de privacidade.
  - `rg "localStorage|setItem|getItem" frontend/src` → matches **apenas em** `state/sessionStorage.ts` (centralizado).
- Skills formais não utilizadas nesta sprint.

### O que NÃO foi implementado (intencional)

- Cálculo de score, final ou consequência no cliente.
- Hardcode de eventos do catálogo (somente mapeamento visual id → cena/personas).
- Fluxo completo do evento secreto — `inject_secret_event` apenas mostra banner discreto sem opções (`apply_secret_choice` continua backlog da engine).
- `POST /api/sessions/{id}/restart` / `continue` — não existem na API.
- Ranking fake — `getRanking` sempre vai na API real.
- GIF pesado / Lottie pesado — nenhum.
- Tailwind, react-router, @fontsource/inter, lucide-react, lottie-react — nenhum instalado.
- Sprint 4 — fora do escopo.
- Smoke E2E operacional: **executado e registrado** em [`sprint-3.0.md` §7.2](docs/03-validation/audits/sprint-3.0.md) (sessão 13 deste HANDOFF). Passo opcional: repetir §7.1 no navegador com print se o PM quiser evidência visual.

### Próximo passo

- ~~Smoke E2E manual com `uvicorn app:app --port 8000` + `npm run dev` em `frontend/` (playbook §7.1 do relatório).~~ **Concluído** (registro §7.2; ressalvas documentadas).
- Aceites humanos formais das Sprints 2.1, 2.2, 2.2-B, 2.3 e 3.0 (em conjunto se conveniente).
- **Architect/Documentation** — atualizar `executive-overview.md` cobrindo 2.x + 3.0.
- **Backlog engine/UX:** `apply_secret_choice` (segunda etapa secreta) e Sprint 4 opcional (assets visuais finais por IA, testes automatizados de UI, paginação ranking, URL bookmarkable).

---

## HANDOFF — 2026-05-14 — Agent Setup/Environment

### Declaração
- Atuei como: Agent Setup/Environment  
- Sprint / escopo: Git inicial no disco + orientação para GitHub privado `desafio_rpg_leega`  
- Rules consultadas: `.cursor/rules/_dispatcher.mdc`, `docs/01-governance/cursor-workflow.md`  
- Arquivos tocados: apenas histórico Git local (`.git/`), commit raiz no projeto existente; **HANDOFF.md** (esta entrada)  
- Não toquei: código de backend/engine/frontend além do que já estava versionado pelo primeiro commit  

### O que fiz
- `git init -b main`, staging completo respeitando `.gitignore`, commit inicial (**132 arquivos**).  
- GitHub CLI **não** estava no PATH; `winget install GitHub.cli` (incl. `--silent`) continua a terminar em **exit 1602** (MSI “cancelado” — comum com UAC/política).  
- **GitHub CLI portátil** extraído para `%LOCALAPPDATA%\Programs\gh-portable\bin\gh.exe` (release `gh_2.92.0_windows_amd64.zip` em [cli/cli releases](https://github.com/cli/cli/releases)) — evita o instalador MSI.  
- Tentativa `gh auth login --web` nesta máquina: fluxo device aberto, **login ainda não concluído** na sessão automatizada (`gh auth status` sem host).  

### O que falta / próximo passo humano
**Opção A (recomendada):** no **PowerShell teu** (para concluir o browser / device flow), na pasta do projeto:

```powershell
Set-Location "c:\Users\dpfreitas\Desktop\Desagio_RPG_Leega"
$gh = "$env:LOCALAPPDATA\Programs\gh-portable\bin\gh.exe"
& $gh auth login -h github.com -p https -w --skip-ssh-key
& $gh repo create desafio_rpg_leega --private --source=. --remote=origin --push
```

- Se `repo create` disser que o repositório já existe: `git remote remove origin` (se aplicável), depois `git remote add origin https://github.com/SEU_LOGIN/desafio_rpg_leega.git` e `git push -u origin main`.  
- Antes do push, faça commit do que estiver pendente (ex.: alterações neste **HANDOFF**).  

**Opção B:** criar manualmente no site o repo vazio privado **`desafio_rpg_leega`** (sem README) e só então:

```powershell
Set-Location "c:\Users\dpfreitas\Desktop\Desagio_RPG_Leega"
git remote add origin https://github.com/SEU_LOGIN/desafio_rpg_leega.git
git push -u origin main
```

**(Opcional)** Autor Git global: `git config --global user.name "..."` e `git config --global user.email "..."`; para corrigir só o commit raiz antes do primeiro push: `git commit --amend --reset-author`.  

### Evidências
- Branch `main`, commit raiz presente localmente (`git log -1 --oneline`).  

---

## Estado atual (2026-05-15)

- **Git local:** repositório inicializado nesta pasta (`main`), primeiro commit local pronto para `git push` após criar o remoto privado **`desafio_rpg_leega`** (instruções na sessão HANDOFF de Setup/Environment abaixo).  
- **Repositório:** backend com `GET /api/health` + persistência SQLite + fluxo jogável (`POST /api/sessions/{id}/choices` + ranking gravado ao fim) + leaderboard público (`GET /api/ranking?limit=10`, envelope `{items, limit, count}`, `session_id` ocultado). **Frontend jogável mínimo (Sprint 3.0)**: 4 telas Home/Game/Ending/Ranking consumindo a API real; palco visual SVG (7 personas + 8 cenas placeholder); microanimação CSS com `prefers-reduced-motion`; banner discreto para `inject_secret_event`. Zero dependências novas. Catálogo `events.json` intacto.
- **Última sprint executável fechada tecnicamente:** Sprint **3.0** + fecho **3.0-A** — Frontend jogável mínimo com palco visual; smoke **manual** no browser (**passou**); smoke **§7.2** HTTP (**passou com ressalvas**); bugfix **AttributePanel** (`AttributePanel.css`); [`sprint-3.0.md`](docs/03-validation/audits/sprint-3.0.md) §§7–11. `npm run typecheck/lint/build` em `frontend/` revalidados na **3.0-A**; bundle ~74 KB gzip; `audit.ps1` OK; greps de governança limpos.
- **Última sprint documental:** **4.0** — [`docs/00-start/final-delivery.md`](docs/00-start/final-delivery.md) (dossiê final de entrega); README / PROJECT_STATUS / `sprint-history` / HANDOFF sincronizados; sem código de produto.
- **Sprint 2.3** continua intacta — Ranking API ([`sprint-2.3.md`](docs/03-validation/audits/sprint-2.3.md)); 116/116 pytest verdes.
- **Sprint 2.2 / 2.2-B** intactas — engine integrada às choices + persistência + correções QA.
- **Sprint 2.1:** aceite humano formal §11 papel **PENDENTE** (entrega técnica intacta).
- **Última sprint documental aceita:** Sprint **1.2-A**.  
- **Últimas sprints aceitas formalmente (registro papel):** 2.0 ✅; aceites burocráticos pendentes para **2.1, 2.2, 2.2-B, 2.3**; **3.0 / 3.0-A** com aceite **técnico** e smoke documentados no relatório (papel §10 só se o processo exigir).

## Próximo passo recomendado

1. ~~Smoke E2E manual do frontend com backend rodando — playbook em [`sprint-3.0.md §7.1`](docs/03-validation/audits/sprint-3.0.md).~~ **Feito** (secção **Smoke E2E manual** + §7.2 no relatório).
2. ~~**Sprint 4.0 documental** — dossiê final [`docs/00-start/final-delivery.md`](docs/00-start/final-delivery.md).~~ **Feito** (sessão 18 deste HANDOFF).
3. Aceite humano das **Sprints 2.1 + 2.2 + 2.2-B + 2.3** (§10/§11 dos respectivos relatórios — podem ser aceitos em conjunto). **3.0 / 3.0-A:** aceite técnico consolidado no relatório; papel formal opcional.
4. **Architect/Documentation** — `executive-overview.md` (pendência histórica consolidando 2.2 + 2.2-B + 2.3 + 3.0 + 3.0-A; `final-delivery.md` já cobre entrega para gestores).
5. **Pós-4.0 (produto)** — polimento final / UX (assets visuais finais via IA + vetorização, testes automatizados de UI, paginação do ranking, URL bookmarkable se necessário). Paralelo: backlog **engine/UX** `apply_secret_choice`.

## Pendências abertas

- Aceites humanos burocráticos onde o processo exigir (0.3 / 0.3‑A / 1.2 / **2.1 §11 papel** / **2.2 §10 papel** / **2.2-B §10 papel** / **2.3 §10 papel**); **3.0 / 3.0-A** — aceite **técnico** no relatório; papel §10 só se o processo exigir duplicata.
- ~~Smoke E2E manual da Sprint 3.0 (playbook §7.1) — execução pelo humano com backend ativo.~~ **Feito** — ver [`sprint-3.0.md`](docs/03-validation/audits/sprint-3.0.md) secção **Smoke E2E manual**.
- Atualização do dossier executivo cobrindo 2.x + 3.0 + 3.0-A (complementado por **`docs/00-start/final-delivery.md`**).  
- `apply_secret_choice` explícito (engine UX de opção secreta) — backlog de engine/UX; atualmente apenas `inject_secret_event` aparece + banner discreto no frontend.
- **Playbook operacional dev local pós-2.2:** se houver `backend/data/*.db` criado em sprint anterior à 2.2, **apagar antes de subir o backend** (`Remove-Item backend\data\*.db`). Detalhes: `docs/03-validation/audits/sprint-2.2.md §7.2`.
- **Pós-4.0 (produto):** polimento final / UX (assets visuais finais, testes UI, paginação ranking, URL bookmarkable) — próxima fase **de código/UX**, não confundir com **4.0 documental** (fechada).

## Links rápidos

| Artefato | Caminho |
|---------|---------|
| **Dossiê final de entrega (Sprint 4.0 doc)** | `docs/00-start/final-delivery.md` |
| Aceite backend 0.2 | `docs/03-validation/audits/sprint-0.2.md` |
| Aceite frontend 0.3 | `docs/03-validation/audits/sprint-0.3.md` |
| Aceite regras engine 1.0 | `docs/03-validation/audits/sprint-1.0.md` |
| Aceite engine skeleton 1.1 | `docs/03-validation/audits/sprint-1.1.md` |
| Catálogo narrativo 1.2 | `docs/03-validation/audits/sprint-1.2.md` |
| Decisão final antecipado | `docs/01-governance/decisions.md` (ADR-010) |
| Regras do jogo (§4.4 + §11) | `docs/02-product/game-rules.md` |
| Status executivo | `PROJECT_STATUS.md` |
| Aceite persistência SQLite 2.0 | `docs/03-validation/audits/sprint-2.0.md` |
| Aceite API Player+Sessão 2.1 | `docs/03-validation/audits/sprint-2.1.md` |
| Aceite choices+engine 2.2 | `docs/03-validation/audits/sprint-2.2.md` |
| Correções QA 2.2-B (pré-2.3) | `docs/03-validation/audits/sprint-2.2-B.md` |
| Aceite ranking API 2.3 | `docs/03-validation/audits/sprint-2.3.md` |
| **Aceite frontend jogável 3.0** | **`docs/03-validation/audits/sprint-3.0.md`** |

---

## HANDOFF — 2026-05-14 (sessão 11) — Agent Backend — Sprint 2.3 (Ranking API + smoke tests)

### Declaração

- **Agent:** Backend.
- **Sprint:** **2.3 — Ranking API + smoke tests**.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](.cursor/rules/_dispatcher.mdc), [`.cursor/rules/backend.mdc`](.cursor/rules/backend.mdc), [`.cursor/rules/docs-sync.mdc`](.cursor/rules/docs-sync.mdc), [`.cursor/rules/tests.mdc`](.cursor/rules/tests.mdc).

### Principais deltas

**Criados**
- `backend/schemas/ranking.py` — `RankingEntryResponse` (sem `session_id`) + `RankingListResponse` (envelope `{items, limit, count}`).
- `backend/use_cases/ranking_use_cases.py` — `list_top_ranking(db, *, limit)` consumindo `ranking_repository.top_n`.
- `backend/routers/ranking.py` — `GET /api/ranking?limit=10` (`Query(ge=1, le=100, default=10)`).
- `backend/tests/test_ranking_api.py` — **9 testes novos** (vazio, ordenação, default limit, custom limit, leak `session_id`, 3× bounds 422, smoke fim-a-fim).
- `docs/03-validation/audits/sprint-2.3.md` — relatório completo no padrão das sprints anteriores.

**Alterados (mínimos / wire-up + docs)**
- `backend/routers/__init__.py` — export `ranking`.
- `backend/schemas/__init__.py` — exports `RankingEntryResponse` + `RankingListResponse`.
- `backend/use_cases/__init__.py` — export `ranking_use_cases`.
- `backend/app.py` — `app.include_router(ranking_router)`. CORS, lifespan, error handlers e demais routers permanecem **intactos**.
- `docs/02-product/api.md` — endpoint marcado **Implementado (2.3)** + schema `RankingListResponse` + invariante de privacidade explícita (sem `session_id`) + nota sobre paginação futura.
- `docs/00-start/sprint-plan.md` — Sprint 2.3 marcada como fechada tecnicamente.
- `HANDOFF.md`, `PROJECT_STATUS.md`, `docs/03-validation/sprint-history.md` — sincronia documental rotineira.

### Escopo preservado (proibido — verificado)

- `frontend/**`, `backend/engine/**`, `backend/engine/data/events.json`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/game-rules.md`, `docs/02-product/architecture.md`, `docs/01-governance/decisions.md` → **zero alterações**.
- `backend/repositories/**`, `backend/models/**`, `backend/db/**`, `backend/core/**`, `backend/routers/{players,sessions}.py`, `backend/schemas/{sessions,players,errors}.py`, `backend/use_cases/{choice_use_cases,session_use_cases,session_state,player_use_cases,catalog_loader}.py` → **zero alterações** (apenas wire-up nos `__init__.py`/`app.py`).
- CORS de `backend/app.py` mantido — apenas `include_router(ranking_router)` foi adicionado. Não alterei `allow_origins`, `allow_methods` (`GET` já estava) nem `allow_headers`.

### Evidências

- `pytest tests/ engine/tests/ -v` em `backend/` → **116 passed in 1.70s** (107 anteriores + 9 novos da Sprint 2.3). Exit code 0.
- `audit.ps1` → exit 0.
- Greps de governança:
  - `rg "compute_score|apply_choice|resolve_ending|\.clamp\(" backend/routers/ranking.py backend/use_cases/ranking_use_cases.py backend/schemas/ranking.py` → vazio.
  - `rg "from engine|import engine" backend/routers/ranking.py backend/use_cases/ranking_use_cases.py backend/schemas/ranking.py` → vazio (endpoint de leitura, sem dependência de engine).
  - `rg "session_id" backend/schemas/ranking.py` → vazio (campo proibido não aparece no schema).
  - `rg "from engine|import engine" backend/db backend/models backend/repositories` → vazio.
  - `rg -i "fastapi|sqlalchemy|pydantic" backend/engine/*.py` → apenas docstrings.
- Skills formais não utilizadas nesta sprint.

### O que NÃO foi implementado (intencional)

- Frontend / UI de leaderboard, `POST /restart`, `continue`, `apply_secret_choice`, nova regra de jogo, paginação cursor/offset, filtros, ordenação alternativa, alteração de CORS / engine / events.json — **todos fora do escopo** da Sprint 2.3.
- Sprint 3 e demais — fora do escopo.

### Próximo passo

- Aceites humanos formais das Sprints 2.1, 2.2, 2.2-B, 2.3 (em conjunto se conveniente).
- **Architect/Documentation** — atualizar `executive-overview.md` cobrindo 2.0/2.1/2.2/2.2-B/2.3.
- **Backlog engine/UX:** `apply_secret_choice` (segunda etapa do fluxo secreto) e Sprint 3 (UX completa do frontend).

---

## HANDOFF — 2026-05-14 (sessão 10) — Agent Backend + Documentation — Sprint 2.2-B (correções QA pré-2.3)

### Declaração

- **Agent:** Backend (testes) + Documentation (relatório/HANDOFF/sprint-history/PROJECT_STATUS). Cross-domain pré-autorizado pelo enunciado da Sprint 2.2-B.
- **Sprint:** **2.2-B — Correções QA mínimas antes da Sprint 2.3**.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](.cursor/rules/_dispatcher.mdc), [`.cursor/rules/backend.mdc`](.cursor/rules/backend.mdc), [`.cursor/rules/tests.mdc`](.cursor/rules/tests.mdc), [`.cursor/rules/docs-sync.mdc`](.cursor/rules/docs-sync.mdc).

### Principais deltas

**Criados**
- `docs/03-validation/audits/sprint-2.2-B.md` — relatório completo da sprint de correção.

**Alterados**
- `backend/tests/test_choices_api.py` — **+4 testes** endereçando ressalvas QA (`test_submit_choice_session_not_found_returns_404`, `test_submit_choice_persists_decision_row`, `test_ranking_count_zero_before_session_finishes`, `test_submit_choice_existing_event_but_not_current_returns_409`).
- `docs/03-validation/audits/sprint-2.2.md` — §4.A (Agent/Rules/Skills no padrão 2.1), §5.A (lista dos 4 testes 2.2-B), §6.2 (107 pytest), §7.1 clarificada (`apply_secret_choice` fora da 2.3), §7.2 expandida (playbook operacional reset SQLite local), §8 atualizada.
- `HANDOFF.md` — linha 13 harmonizada (aceite 2.1 = pendente §11 papel, alinhado ao relatório oficial; **sem inventar aceite humano**); links rápidos inclui 2.2-B; esta seção 10.
- `PROJECT_STATUS.md` — total de testes 107; referência à Sprint 2.2-B.
- `docs/03-validation/sprint-history.md` — linha nova 2.2-B.

### Escopo preservado (proibido — verificado)

- `backend/engine/**`, `backend/engine/data/events.json`, `frontend/**`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/game-rules.md`, `docs/02-product/architecture.md`, `docs/01-governance/decisions.md` → **zero alterações**.
- Backend de produção (`backend/app.py`, `backend/routers/**`, `backend/schemas/**`, `backend/use_cases/**`, `backend/repositories/**`, `backend/models/**`, `backend/db/**`, `backend/core/**`, `backend/pyproject.toml`) → **zero alterações** (sprint cobre apenas testes + docs).

### Evidências

- `pytest tests/ engine/tests/ -v` em `backend/` → **107 passed in 1.50s** (103 atuais + 4 novos da 2.2-B). Exit code 0.
- `audit.ps1` → exit 0.
- Greps de governança: `rg "apply_choice" backend/routers` → vazio; `rg "from engine|import engine" backend/db backend/models backend/repositories` → vazio; `rg -i "fastapi|sqlalchemy|pydantic" backend/engine/*.py` → apenas docstrings.
- Skills formais não utilizadas nesta sprint.

### O que NÃO foi implementado (intencional)

- `GET /api/ranking`, `POST /restart`, `continue`, `apply_secret_choice`, frontend jogável, nova lógica de engine, migração Alembic — fora do escopo da 2.2-B.
- Nenhuma alteração em endpoints existentes — entrega 2.2 está intacta.
- Não inventei aceite humano da Sprint 2.1 — o relatório oficial diz pendente, então fica pendente.

### Próximo passo

- Aceite humano formal das Sprints 2.1, 2.2 e 2.2-B (em conjunto se conveniente).
- **Sprint 2.3 — Backend** — `GET /api/ranking` + smoke tests.
- **Architect/Documentation** — atualizar `executive-overview.md` para cobrir 2.0/2.1/2.2/2.2-B (consolidando pendência 2.0-A/2.1-A).

---

## HANDOFF — 2026-05-14 (sessão 9) — Agent Backend — Sprint 2.2

### Declaração

- **Agent:** Backend (`.cursor/rules/_dispatcher.mdc`, `.cursor/rules/backend.mdc`).
- **Sprint:** **2.2 — Choices integradas à engine**.

### Principais deltas

**Criados**
- `backend/use_cases/session_state.py` — hidrata `engine.State`.
- `backend/use_cases/choice_use_cases.py` — orquestra `apply_choice` + persistência.
- `backend/tests/test_choices_api.py`.
- `docs/03-validation/audits/sprint-2.2.md`.

**Alterados**
- `backend/models/game_session.py` — `secrets_seen_json` (lista JSON IDs de secreto vistas — engine não sempre gera Decision).
- `backend/repositories/session_repository.py` — `persist_apply_choice_turn` transação única (Decision + atributos + progresso/`finish` + `RankingEntry` opcional).
- `backend/routers/sessions.py` — `POST /api/sessions/{session_id}/choices`.
- `backend/schemas/sessions.py` — `ChoiceCreate`, campo `inject_secret_event` opcional na resposta.
- `backend/schemas/__init__.py`, `backend/app.py` (CORS: cabeçalhos permitidos apenas `Content-Type` + `Accept`).
- Produto/docs: [`docs/02-product/api.md`](docs/02-product/api.md), [`docs/00-start/sprint-plan.md`](docs/00-start/sprint-plan.md), checklist extra em [`sprint-2.1.md`](docs/03-validation/audits/sprint-2.1.md).

### Escopo preservado

- `backend/engine/**` + `engine/data/events.json` **não** alterados; frontend intacto.

### Evidências

- `pytest` `backend/tests/` + `backend/engine/tests/` → **103 passed**.
- `scripts/audit.ps1` (`repo root`) → exit **0**.
- `apply_choice` não aparece em `backend/routers/` (delegado ao use case).

### Pendências relacionadas

- Engine ainda não expõe **`apply_secret_choice`** — apenas `inject_secret_event` até UX/engine fecharem o segundo passo secreto.

### Próximo passo

- Sprint **2.3** — `GET /api/ranking` + testes smoke.

---

## HANDOFF — 2026-05-14 (sessão 8) — Agent Backend — Sprint 2.1

### Declaração

- **Atuei como:** Agent Backend.
- **Sprint / escopo:** Sprint **2.1 — API de Player e Sessão Inicial**.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](.cursor/rules/_dispatcher.mdc), [`.cursor/rules/backend.mdc`](.cursor/rules/backend.mdc).
- **Arquivos criados:**
  - `backend/core/__init__.py`, `backend/core/config.py`, `backend/core/exceptions.py`, `backend/core/error_handlers.py`
  - `backend/schemas/__init__.py`, `backend/schemas/players.py`, `backend/schemas/sessions.py`, `backend/schemas/errors.py`
  - `backend/use_cases/__init__.py`, `backend/use_cases/catalog_loader.py`, `backend/use_cases/player_use_cases.py`, `backend/use_cases/session_use_cases.py`
  - `backend/routers/__init__.py`, `backend/routers/players.py`, `backend/routers/sessions.py`
  - `backend/tests/test_players_api.py`, `backend/tests/test_sessions_api.py`, `backend/tests/test_error_handlers.py`, `backend/tests/test_cors.py`, `backend/tests/test_catalog_loader.py`, `backend/tests/test_schemas.py`
  - `docs/03-validation/audits/sprint-2.1.md`
- **Arquivos alterados:**
  - `backend/app.py` (lifespan agora valida catálogo via `validate_or_raise` + `get_catalog`; CORS middleware; `register_error_handlers`; include routers de players e sessions)
  - `backend/pyproject.toml` (deps: `pydantic>=2.5`, `pydantic-settings>=2.0`; `[tool.setuptools.packages.find]` declarado para acomodar múltiplos pacotes top-level)
  - `backend/tests/conftest.py` (fixture `client` com `dependency_overrides[get_db]` apontando para o engine in-memory; lifespan suprimido para não criar banco real em disco)
  - `backend/core/error_handlers.py` (uso de literais 422/500 para evitar DeprecationWarning do Starlette)
  - `docs/00-start/sprint-plan.md` (cross-domain autorizado: Sprint 2.1 reescrita para "API de Player e Sessão Inicial"; Sprint 2.2 "Choice integrada à engine" inserida)
  - `docs/02-product/api.md` (3 endpoints saem de "Planejado" para "Implementado na Sprint 2.1"; schema `SessionResponse` documentado; envelope de erro padronizado)
  - `PROJECT_STATUS.md`, `HANDOFF.md`, `docs/03-validation/sprint-history.md`
- **Não toquei:** `backend/engine/**`, `backend/engine/data/events.json`, `backend/db/**`, `backend/models/**`, `backend/repositories/**` (Sprint 2.0 está intacta), `frontend/**`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/game-rules.md`, `docs/02-product/architecture.md`, `docs/01-governance/**`, `docs/00-start/executive-overview.md`, `README.md`, `docs/00-start/setup-company-env.md`, `_context/**`.

### Cross-domain declarado

Patch mínimo em [`docs/00-start/sprint-plan.md`](docs/00-start/sprint-plan.md) (domínio de Architect/Documentation) autorizado pelo humano no início da sessão: reescreveu Sprint 2.1 (antes "Robustez API" genérica) para "API de Player e Sessão Inicial" com DoD detalhado, e inseriu Sprint 2.2 "Choice integrada à engine" explícita. A consequência (dossiê executivo desatualizado para 2.0+2.1) fica como pendência **Sprint 2.0-A/2.1-A documental**.

### O que fiz

- Adicionei `pydantic-settings` ao backend e ajustei `pyproject.toml` para o `setuptools` aceitar os múltiplos pacotes top-level (`db`, `engine`, `models`, `repositories`, `core`, `routers`, `schemas`, `use_cases`).
- Criei `backend/core/` (settings + exceções de domínio + error handlers globais com payload `{ "error": { "code", "message", "details?" } }`).
- Criei `backend/schemas/` (Pydantic v2 estrito; nome com regex+length 1..64; `extra="forbid"` em todos os requests; `SessionResponse` com snapshot completo SEM expor `consequences`).
- Criei `backend/use_cases/` (catalog_loader singleton + use cases de Player e Session, consumindo apenas a API pública da engine).
- Criei `backend/routers/` (3 endpoints finos, `Depends(get_db)`, delegação total ao use case).
- Atualizei `backend/app.py`: lifespan agora também valida o catálogo via `engine.validate_events` e aquece o singleton — falha de catálogo derruba o boot, conforme `game-rules.md §4.3` e §9.
- Atualizei `tests/conftest.py` com fixture `client` (TestClient + dependency override + ZERO toque em disco).
- 32 novos testes cobrindo todos os endpoints, handlers, CORS, schemas e catalog loader.
- 97/97 pytest verdes. `audit.ps1` verde.

### O que falta / próximo agente

- **Humano:** aceite formal da Sprint 2.1 (campo §10 em `docs/03-validation/audits/sprint-2.1.md`).
- **Próximo agente: Architect/Documentation** — Sprint **2.0-A/2.1-A** (documental): atualizar `docs/00-start/executive-overview.md` §7/§8/§10 para refletir Sprints 2.0 e 2.1.
- **Em seguida — Agent Backend** — Sprint **2.2 — Choice integrada à engine**: `POST /api/sessions/{id}/choices` chamando `engine.apply_choice`, persistindo o novo estado e a decisão, registrando ranking ao terminar a sessão.

### Evidências

- `.\.venv\Scripts\python.exe -m pytest tests/ engine/tests/` → `97 passed in 0.78s`, exit code 0.
- `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` → `OK - governanca minima presente e raiz limpa.`, exit code 0.
- Greps de governança:
  - `rg "compute_score|apply_choice|resolve_ending|\.clamp\(" backend/routers backend/db backend/models backend/repositories` → 0 matches.
  - `rg "from engine|import engine" backend/db backend/models backend/repositories` → 0 matches.
  - `rg -i "fastapi|sqlalchemy|pydantic" backend/engine/*.py` → apenas docstrings.
- Skills formais não utilizadas nesta sprint.

---

## HANDOFF — 2026-05-14 (sessão 7) — Agent Backend — Sprint 2.0

### Declaração

- **Atuei como:** Agent Backend.
- **Sprint / escopo:** Sprint **2.0 — Persistência SQLite + modelos base**.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](.cursor/rules/_dispatcher.mdc), [`.cursor/rules/backend.mdc`](.cursor/rules/backend.mdc); rules `game-engine.mdc`/`events-json.mdc`/`docs-sync.mdc`/`tests.mdc` foram lidas como contexto pelo dispatcher mas nenhum arquivo dos domínios delas foi alterado.
- **Arquivos criados:**
  - `backend/db/__init__.py`, `backend/db/base.py`, `backend/db/session.py`, `backend/db/init_db.py`
  - `backend/models/__init__.py`, `backend/models/player.py`, `backend/models/game_session.py`, `backend/models/session_attributes.py`, `backend/models/decision.py`, `backend/models/ranking_entry.py`
  - `backend/repositories/__init__.py`, `backend/repositories/player_repository.py`, `backend/repositories/session_repository.py`, `backend/repositories/attributes_repository.py`, `backend/repositories/decision_repository.py`, `backend/repositories/ranking_repository.py`
  - `backend/data/.gitkeep`
  - `backend/tests/conftest.py`, `backend/tests/test_db_setup.py`, `backend/tests/test_player_repository.py`, `backend/tests/test_session_repository.py`, `backend/tests/test_attributes_repository.py`, `backend/tests/test_decision_repository.py`, `backend/tests/test_ranking_repository.py`
  - `docs/03-validation/audits/sprint-2.0.md`
- **Arquivos alterados:**
  - `backend/app.py` (lifespan + `init_db()`; sem novos endpoints)
  - `backend/pyproject.toml` (`sqlalchemy>=2.0`)
  - `docs/00-start/sprint-plan.md` (cross-domain autorizado: inserida Sprint 2.0 e renomeada antiga "Sprint 2 → Sprint 2.1")
  - `PROJECT_STATUS.md`, `HANDOFF.md`, `docs/03-validation/sprint-history.md`
- **Não toquei:** `backend/engine/**`, `backend/engine/data/events.json`, `frontend/**`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/game-rules.md`, `docs/02-product/api.md`, `docs/02-product/architecture.md`, `docs/01-governance/**`, `docs/00-start/executive-overview.md`, `README.md`, `docs/00-start/setup-company-env.md`, `_context/**`.

### Cross-domain declarado

Houve uma única violação de domínio explicitamente autorizada pelo humano antes do início da execução: patch mínimo em [`docs/00-start/sprint-plan.md`](docs/00-start/sprint-plan.md) (domínio de Architect/Documentation) para inserir o bloco "Sprint 2.0 — Persistência SQLite + modelos base" e renomear a antiga "Sprint 2 — Robustez API" para "Sprint 2.1 — Robustez API". A consequência (dossiê executivo desatualizado) está registrada como pendência para **Sprint 2.0-A documental**.

### O que fiz

- Adicionei `sqlalchemy>=2.0` em `backend/pyproject.toml` e reinstalei via `pip install -e ".[dev]"` (SQLAlchemy 2.0.49 + greenlet 3.5.0).
- Criei a camada `backend/db/` com Base declarativa SQLAlchemy 2.0, engine derivada de `DATABASE_URL` (env), `SessionLocal`, `get_db()` generator e `init_db()` idempotente.
- Criei os 5 modelos exatamente com os campos pedidos: `Player`, `GameSession`, `SessionAttributes` (1:1 via `session_id PK`), `Decision`, `RankingEntry`. FKs com `ondelete=CASCADE` onde adequado, índices em colunas de leitura quente.
- Criei 5 repositórios módulo-style com CRUD puro — nenhum import de `backend.engine`, nenhum cálculo de score/clamp/final/consequência.
- Adicionei lifespan minimalista a `backend/app.py` chamando `init_db()`. `/api/health` continua funcionando sem alteração de payload.
- Criei `backend/tests/conftest.py` com fixture SQLite in-memory + `StaticPool` (necessário para que múltiplas sessões compartilhem a mesma conexão) e 6 arquivos de teste cobrindo todos os repositórios + setup de DB.
- 65/65 pytest verdes (44 pré-existentes + 21 novos). `audit.ps1` verde.

### O que falta / próximo agente

- **Humano:** aceite formal da Sprint 2.0 (campo §10 em `docs/03-validation/audits/sprint-2.0.md`).
- **Próximo agente: Architect/Documentation** — Sprint **2.0-A** (documental): atualizar `docs/00-start/executive-overview.md` §7/§8/§10 para refletir Sprint 2.0 entregue e a renomeação "Sprint 2 → 2.1".
- **Em seguida — Agent Backend** — Sprint **2.1 — Robustez API**: schemas Pydantic estritos, handler global de erro, CORS, integração engine↔routers usando os repositórios desta sprint.

### Evidências

- `.\.venv\Scripts\python.exe -m pytest tests/ engine/tests/ -v` → `65 passed in 0.72s`, exit code 0.
- `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` → `OK - governanca minima presente e raiz limpa.`, exit code 0.
- `pip install -e ".[dev]"` → `Successfully installed corporate-survivor-backend-0.1.0 greenlet-3.5.0 sqlalchemy-2.0.49`.
- Nenhum arquivo em `backend/engine/**`, `frontend/**`, `.cursor/rules/**`, `scripts/**` foi modificado.
- Skills formais não utilizadas nesta sprint.

---

## HANDOFF — 2026-05-14 (sessão 6) — Agent Architect/Documentation — Sprint 1.2-A

### Declaração

- **Atuei como:** Agent Architect/Documentation.
- **Sprint / escopo:** Sprint **1.2-A — Atualização do Dossiê Executivo pós-auditoria da Sprint 1.2**.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](.cursor/rules/_dispatcher.mdc), [`.cursor/rules/docs-sync.mdc`](.cursor/rules/docs-sync.mdc).
- **Arquivos alterados:** `docs/00-start/executive-overview.md`, `docs/03-validation/sprint-history.md`, `HANDOFF.md`.
- **Não toquei:** `backend/**`, `frontend/**`, `events.json`, testes, scripts, rules.

### O que fiz

- A auditoria da Sprint 1.2 classificou a documentação como COMPLETA COM RESSALVAS: `executive-overview.md` estava desatualizado, ainda referenciando `events.json` como placeholder e Sprint 1.2 como trabalho futuro.
- Corrigi `executive-overview.md` em 4 seções:
  - §2 Estado atual: linha `events.json` reflete catálogo narrativo real (15 + 2 eventos, 3 playthroughs, Sprint 1.2 fechada tecnicamente).
  - §7 O que foi concluído: nova linha Sprint 1.2 com evidências e link para `sprint-1.2.md`.
  - §8 O que falta construir: removida Sprint 1.2 como pendente; tabela reordenada com aceite humano como primeiro item, seguido de Sprint 2, 3 e 4.
  - §10 Próximo passo: substituído bloco "Sprint 1.2 — Catálogo" pelo blocos "Aceite humano da Sprint 1.2" e "Sprint 2 (Agent Backend)".
- Adicionei linha da Sprint 1.2-A em `sprint-history.md`.

### O que falta / próximo agente

- **Humano:** aceite formal da Sprint 1.2 (campo §10 em `docs/03-validation/audits/sprint-1.2.md`).
- **Próximo agente: Backend** — Sprint **2**: integração engine↔routers FastAPI, persistência SQLite, CORS, schemas Pydantic.

### Evidências

- `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` → `OK - governanca minima presente e raiz limpa.`, exit code 0.
- Nenhum arquivo de backend, frontend, engine, eventos, testes, scripts ou rules foi modificado.

---

## HANDOFF — 2026-05-14 (sessão 5) — Agent Engine/Content — Sprint 1.2

### Declaração

- **Atuei como:** Agent Engine/Content.
- **Sprint / escopo:** Sprint **1.2 — Catálogo completo dos 15 + 2 eventos**.
- **Rules consultadas:** `.cursor/rules/_dispatcher.mdc`, `.cursor/rules/game-engine.mdc`, `.cursor/rules/events-json.mdc`.
- **Arquivos tocados:**
  - `backend/engine/data/events.json` (conteúdo narrativo real)
  - `docs/02-product/game-rules.md` (ajuste de 2 deltas — balanceamento)
  - `docs/03-validation/playthroughs/run_optimista.md` (criado)
  - `docs/03-validation/playthroughs/run_demitido.md` (criado)
  - `docs/03-validation/playthroughs/run_medio.md` (criado)
  - `docs/03-validation/audits/sprint-1.2.md` (criado)
  - `docs/03-validation/sprint-history.md`, `PROJECT_STATUS.md`, `HANDOFF.md`
- **Não toquei:** `backend/app.py`, `backend/tests/`, `backend/engine/*.py`, `frontend/**`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/api.md`, `docs/01-governance/decisions.md`.

### O que fiz

- Substituí o `events.json` placeholder por catálogo narrativo real: 15 eventos principais (5 dias × 3) + 2 secretos, todos com cenas corporativas em português, opções com trade-offs reais, sem opção dominante.
- Ajustei 2 deltas que excediam invariante 7 (soma ≤ 7): `ev_day5_001 A` (soma 9→7) e `ev_day5_003 A` (soma 8→7); registrado em `game-rules.md §5`.
- Criei 3 playthroughs completos com estados verificados: `trainee_lenda` (score 551), `demitido` antecipado (score 49), `sobrevivente` (score 280).
- 44/44 pytest — regressão zero. `audit.ps1` — exit code 0.

### O que falta / próximo agente

- **Humano:** aceite formal da Sprint 1.2 (campo §10 de `sprint-1.2.md`).
- **Próximo agente: Backend** — Sprint **2**: integração engine↔routers, CORS, handler de erro, Pydantic estrito.

### Evidências

- `.\.venv\Scripts\python.exe -m pytest tests/ engine/tests/ -v` → 44 passed, exit code 0.
- `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` → `OK - governanca minima presente e raiz limpa.`, exit code 0.
- 3 playthroughs com atributos finais verificados e predicados de final checados manualmente.
- Skills formais não utilizadas nesta sprint.

---

## HANDOFF — 2026-05-14 (sessão 4) — Agent Architect/Documentation — Sprint 1.1-B

### Declaração

- **Atuei como:** Agent Architect/Documentation.
- **Sprint / escopo:** Sprint **1.1-B — Dossiê Executivo e Mapa de Entrega**.
- **Rules consultadas:** `.cursor/rules/_dispatcher.mdc`, `.cursor/rules/docs-sync.mdc`.
- **Arquivos criados:** `docs/00-start/executive-overview.md`.
- **Arquivos alterados:** `README.md` (link ao dossiê, texto stale corrigido), `PROJECT_STATUS.md` (referência ao dossiê), `HANDOFF.md`, `docs/03-validation/sprint-history.md`.
- **Não toquei:** `backend/`, `frontend/`, `.cursor/rules/`, `scripts/`, `docs/02-product/`, `docs/01-governance/`, `docs/00-start/sprint-plan.md`, `events.json`.

### O que fiz

- Criei `docs/00-start/executive-overview.md` com 10 seções obrigatórias: resumo do projeto, estado atual, arquitetura em alto nível, tecnologias (validadas vs planejadas), uso de IA/Agents, validação de entregas, o que foi concluído (tabela com links), o que falta (tabela ordenada), mapa de documentos para gestor, próximo passo.
- Atualizei `README.md`: adicionado link proeminente ao dossiê na seção "Comece aqui"; seção "Se o gestor pedir documentação" com dossiê como ponto de entrada único; "Estado do repositório" atualizado com sprints reais; "Próxima ação" atualizada para Sprint 1.2.
- Atualizei `PROJECT_STATUS.md`: referência ao dossiê no cabeçalho.
- Atualizei `sprint-history.md` com linha da Sprint 1.1-B.

### O que falta / próximo agente

- **Próximo agente: Engine/Content** — Sprint **1.2**: conteúdo narrativo real dos 15 + 2 eventos em `backend/engine/data/events.json`.

### Evidências

- `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` → `OK - governanca minima presente e raiz limpa.`, exit code 0.
- Nenhum arquivo de código de produto foi alterado.
- Skills formais não utilizadas nesta sprint.

---

## HANDOFF — 2026-05-14 (sessão 3) — Agent Architect/Documentation — Sprint 1.1-A

### Declaração

- **Atuei como:** Agent Architect/Documentation.
- **Sprint / escopo:** Sprint **1.1-A — Fechamento e aceite da Sprint 1.1**.
- **Rules consultadas:** `.cursor/rules/_dispatcher.mdc`, `.cursor/rules/docs-sync.mdc`.
- **Arquivos tocados:** `docs/03-validation/audits/sprint-1.1.md` (aceite humano registrado), `PROJECT_STATUS.md`, `HANDOFF.md`, `docs/03-validation/sprint-history.md`.
- **Não toquei:** `backend/`, `frontend/`, `.cursor/rules/`, `scripts/`, `docs/02-product/`, `docs/00-start/sprint-plan.md`.

### O que fiz

- Registrei aceite humano da Sprint 1.1 em `sprint-1.1.md` §10 com as observações fornecidas.
- Atualizei `PROJECT_STATUS.md`: sprint aceita, pendências, próximo passo (Sprint 1.2).
- Atualizei `sprint-history.md`: Sprint 1.1 marcada como aceita (✅), Sprint 1.1-A registrada, seção "Próxima sprint" apontando para 1.2.
- Atualizei `HANDOFF.md` com estado atual e entrada desta sessão.

### O que falta / próximo agente

- **Próximo agente: Engine/Content** — Sprint **1.2**: conteúdo narrativo real dos 15 + 2 eventos em `backend/engine/data/events.json` (substituir placeholders usando §5 e §6 de `game-rules.md`), checklist §10, 3 playthroughs.

### Evidências

- `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` → `OK - governanca minima presente e raiz limpa.`, exit code 0.
- Nenhum arquivo de código de produto foi alterado.

---

## HANDOFF — 2026-05-14 (sessão 2) — Agent Engine/Content

### Declaração

- **Atuei como:** Agent Engine/Content.
- **Sprint / escopo:** Sprint **1.1 — Engine skeleton + schema `events.json`**.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](.cursor/rules/_dispatcher.mdc), [`.cursor/rules/game-engine.mdc`](.cursor/rules/game-engine.mdc).
- **Arquivos tocados (criados):** `backend/engine/__init__.py`, `backend/engine/types.py`, `backend/engine/endings.py`, `backend/engine/engine.py`, `backend/engine/data/events.json`, `backend/engine/tests/__init__.py`, `backend/engine/tests/test_validate.py`, `backend/engine/tests/test_apply_choice.py`; atualizado `docs/03-validation/audits/sprint-1.0.md` (aceite humano registrado).
- **Documentação atualizada:** `docs/03-validation/audits/sprint-1.1.md` (criado), `docs/03-validation/sprint-history.md`, `PROJECT_STATUS.md`, `HANDOFF.md`.
- **Não toquei:** `backend/app.py`, `backend/tests/test_health.py`, `frontend/**`, `.cursor/rules/`, `scripts/`, `docs/02-product/api.md`, `docs/02-product/architecture.md`.

### O que fiz

- Criei a game engine Python pura em `backend/engine/` (sem FastAPI/SQLAlchemy/frontend).
- Tipos imutáveis (frozen dataclasses), registry de endings, validate_events (invariantes 1–11), apply_choice com clamp e gatilhos antecipados na ordem ADR-010, resolve_ending, compute_score.
- Placeholder `events.json` mínimo (15 + 2, schemaVersion 1.0, deltas zerados) que passa na validação.
- 43 testes unitários: validador e apply_choice (gatilhos, prioridade, progressão, clamp, fim de semana).
- 44/44 pytest (engine + healthcheck pré-existente) — regressão zero.

### O que falta / próximo agente

- **Humano:** aceite formal da Sprint 1.1 no campo de `sprint-1.1.md`.
- **Próximo agente: Engine/Content** — Sprint **1.2**: conteúdo narrativo real dos 15 + 2 eventos em `events.json` (substituir placeholders), checklist de balanceamento §10, 3 playthroughs em `docs/03-validation/playthroughs/`.

### Evidências

- `pytest tests/ engine/tests/ -v` → 44 passed, exit code 0.
- `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` → `OK - governanca minima presente e raiz limpa.`, exit code 0.
- Nenhum arquivo de `backend/app.py`, `frontend/`, rules ou scripts foi modificado.

---

## HANDOFF — 2026-05-14 — Agent Engine/Content + Architect/Documentation

### Declaração

- **Atuei como:** Agent Engine/Content + Architect/Documentation (cross-domain limitado a `docs/**`, `PROJECT_STATUS.md` e `HANDOFF.md`; nenhum código de produto).
- **Sprint / escopo:** Sprint **1.0 — Regras críticas do jogo e contrato da engine**.
- **Rules consultadas:** [`.cursor/rules/_dispatcher.mdc`](.cursor/rules/_dispatcher.mdc), [`.cursor/rules/game-engine.mdc`](.cursor/rules/game-engine.mdc), [`.cursor/rules/docs-sync.mdc`](.cursor/rules/docs-sync.mdc).
- **Arquivos tocados:** [`docs/02-product/game-rules.md`](docs/02-product/game-rules.md), [`docs/01-governance/decisions.md`](docs/01-governance/decisions.md), [`docs/00-start/sprint-plan.md`](docs/00-start/sprint-plan.md), `PROJECT_STATUS.md`, `HANDOFF.md`, [`docs/03-validation/sprint-history.md`](docs/03-validation/sprint-history.md), [`docs/03-validation/audits/sprint-1.0.md`](docs/03-validation/audits/sprint-1.0.md) (criado).
- **Não toquei:** `backend/`, `frontend/`, qualquer engine, `events.json`, `scripts/`, `.cursor/rules/`, `.env*`, `package*.json`, `pyproject.toml`.

### O que fiz

- Decidi formalmente as regras críticas do jogo: existência e gatilhos de **final antecipado** (§4.4 de `game-rules.md`), com mapeamento gatilho→final (`reputacao<=0`→`demitido`; `energia<=0`→`burnout`; `ansiedade>=10`→`burnout`) e ordem de prioridade `rep > ene > ans` justificada.
- Documentei §11 — **responsabilidades por camada** (engine pura / backend / frontend) e o fluxo de uma escolha.
- Fechei **ADR-007** como `Substituída` e abri **ADR-010** com:
  - Justificativa interpretativa do requisito "algum atributo chega a zero" do desafio (por que apenas energia/reputação/ansiedade encerram; por que produtividade/aprendizado/networking influenciam finais e score em vez de encerrar).
  - Justificativa narrativa da prioridade dos gatilhos (demissão = perda objetiva da posição; energia = esgotamento físico; ansiedade = burnout psicológico).
- Atualizei `sprint-plan.md` adicionando Sprint 1.0 (fechada) e Sprint 1.1 (engine skeleton + schema), e renumerando o catálogo completo para Sprint 1.2.
- Atualizei `PROJECT_STATUS.md`, `sprint-history.md` e este HANDOFF; criei o relatório `sprint-1.0.md`.

### O que falta / próximo agente

- **Humano:** aceite formal da Sprint 1.0 no campo do relatório `sprint-1.0.md`.
- **Próximo agente:** **Engine/Content** abre Sprint **1.1 — Engine skeleton + schema `events.json`** (Python puro, sem invadir backend/frontend; sem expor API).

### Evidências

- `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` → `OK - governanca minima presente e raiz limpa.` (registrado em `docs/03-validation/audits/sprint-1.0.md`).
- Diff: 6 arquivos alterados em `docs/**` + `PROJECT_STATUS.md` + `HANDOFF.md`; 1 arquivo criado: `docs/03-validation/audits/sprint-1.0.md`. Nenhum arquivo proibido tocado.
