# Sprint 3.0 — Frontend jogável mínimo com palco visual — Relatório de aceite

## 1. Resumo executivo

- **Objetivo da sprint:** entregar a primeira versão **jogável** do frontend consumindo a API real (POST /api/players, POST /api/sessions, GET /api/sessions/{id}, POST /api/sessions/{id}/choices, GET /api/ranking), com diferencial visual — não apenas um quiz seco. Quatro telas (Home, Game, Ending, Ranking), palco visual SVG por evento (cena de fundo + personas), painel de atributos com microanimação, banner discreto para `inject_secret_event`, sem implementar fluxo de escolha secreto, sem calcular score/final no cliente, sem hardcode de eventos.
- **Resultado:** **FECHADA tecnicamente** com smoke E2E em **§7.2** (HTTP, 2026-05-15) e **smoke E2E manual** (browser); aceite técnico consolidado em **§10**; fecho operacional **Sprint 3.0-A** em **§11** (bugfix `AttributePanel`, revalidação `npm run typecheck/lint/build`).
- **Decisão recomendada:** seguir para **Sprint 4.0** (polimento final / UX / auditoria de entrega) e backlog `apply_secret_choice`; aceites humanos burocráticos pendentes das 2.x podem ser fechados em lote.

## 2. Escopo entregue

### 2.1 Stack confirmada (decisões locais — sem ADR nova)

Frontend foi mantido **mínimo**: **plain CSS + CSS variables** (sem Tailwind, sem `@fontsource/inter`, sem `lucide-react`, sem `lottie-react`), **navegação por estado** (sem `react-router`), SVGs **inline em componentes `.tsx`** (sem `vite-plugin-svgr`), `fetch` nativo (sem TanStack Query). Nenhuma dependência foi adicionada ao [`frontend/package.json`](../../../frontend/package.json) — `npm install` continua reportando "up to date" sobre 154 pacotes.

Justificativa: o style-guide menciona Tailwind/Inter/Lucide como sugestão, mas (a) a Sprint 3.0 pede "minimum viable", (b) a paleta inteira foi reproduzida em variáveis CSS, (c) `system-ui` cobre tipografia sem instalar fonte web, (d) ícones SVG inline saem mais leves que Lucide importado, (e) navegação por estado é suficiente para 4 telas sem URLs distintas.

### 2.2 Camada de estilos (`frontend/src/styles/`)

- [`tokens.css`](../../../frontend/src/styles/tokens.css) — paleta completa do style-guide §1, tipografia §2, radius §4, sombras §5, transições §7. CSS variables consumidas por todos os componentes — zero hex hardcoded em código de produto.
- [`animations.css`](../../../frontend/src/styles/animations.css) — keyframes `cs-attr-pulse-up`, `cs-attr-pulse-down`, `cs-breathe`, `cs-fade-in`, `cs-skeleton-pulse` + bloco global `@media (prefers-reduced-motion: reduce)` zerando animações.

Atualizado: [`frontend/src/index.css`](../../../frontend/src/index.css) (import dos tokens/animations + reset mínimo) e [`frontend/src/App.css`](../../../frontend/src/App.css) (shell de header/main/footer).

### 2.3 Camada de API (`frontend/src/api/`)

- [`types.ts`](../../../frontend/src/api/types.ts) — `Attributes`, `OptionPayload`, `EventPayload`, `SessionResponse`, `PlayerResponse`, `RankingItem`, `RankingResponse`, `ApiErrorEnvelope`. Espelha **exatamente** [`backend/schemas/sessions.py`](../../../backend/schemas/sessions.py) — `OptionPayload` deliberadamente **não** tem `consequences`; `RankingItem` deliberadamente **não** tem `session_id`.
- [`client.ts`](../../../frontend/src/api/client.ts) — `createPlayer`, `createSession`, `getSession`, `submitChoice`, `getRanking` + classe `ApiError` que preserva o envelope `{ error: { code, message, details } }` do backend (`docs/02-product/api.md` §"Convenção de erros"). Suporta `VITE_API_BASE_URL` para produção; em dev o proxy do Vite cobre `/api/*`.

### 2.4 Persistência local (`frontend/src/state/sessionStorage.ts`)

Apenas duas chaves no `localStorage`:
- `cs.sessionId` — id da sessão ativa.
- `cs.traineeVariant` — 1, 2 ou 3 (variante visual do trainee, sorteada uma vez por player). Atende à autorização explícita do prompt: "usar localStorage apenas para sessionId e, se necessário, variante visual do trainee".

Robustez: funções não-quebráveis quando `localStorage` está indisponível (ambiente SSR teórico ou storage desabilitado).

### 2.5 Camada visual (`frontend/src/assets/visuals/`)

Estrutura conforme `Referencia_front_RPG/SKILL.md` §"Arquitetura de assets" (com adaptação: componentes `.tsx` em vez de `.svg` brutos, para evitar `vite-plugin-svgr` e ainda permitir `currentColor`/variáveis CSS).

**Personas (7 + 3 variantes do trainee — placeholders geométricos, asset-pipeline.md §"Opção D"):**

| Arquivo | PersonaId | Paleta | Origem |
|---|---|---|---|
| `personas/Trainee.tsx` | `trainee` | 3 variantes (skin #D4A574/#A86F4A/#E8C8A8, hair #2D2A28/#1A1614/#6B5544) | personas.md §"trainee" |
| `personas/Gestor.tsx` | `gestor` | skin #B98A6B + corp-blue + têmporas grisalhas + crachá | personas.md §"gestor" |
| `personas/Gerente.tsx` | `gerente` | skin #E8C8A8 + verde musgo + rabo baixo + caneca | personas.md §"gerente" |
| `personas/Colega.tsx` | `colega` | skin #D4A574 + terracota + cabelo médio (variante Marina) | personas.md §"colega" |
| `personas/Rh.tsx` | `rh` | skin #C99878 + caramelo + cabelo cacheado + crachá fita | personas.md §"rh" |
| `personas/Senior.tsx` | `senior` | skin #DDB69A + cinza-azulado + grisalho + barba curta + óculos | personas.md §"senior" |
| `personas/LiderExterno.tsx` | `lider-externo` | skin #6B4533 + blazer escuro + blusa clara | personas.md §"lider-externo" |
| `personas/_index.tsx` | — | registry + `personaLabels` (acessibilidade) | — |

Todos com viewBox `0 0 200 320` (SKILL.md). Cada componente tem `<title>` opcional para acessibilidade quando renderizado isoladamente.

**Cenas (8 — viewBox `0 0 800 400`, scenes.md):**

| Arquivo | SceneId | Eventos usuários |
|---|---|---|
| `scenes/SalaReuniao.tsx` | `sala-reuniao` | `ev_day1_001, ev_day2_003, ev_day3_001, ev_day4_003` |
| `scenes/MesaTrabalho.tsx` | `mesa-trabalho` | 8 eventos (cena mais usada) |
| `scenes/Restaurante.tsx` | `restaurante` | `ev_day1_002, ev_day5_002` |
| `scenes/Bar.tsx` | `bar` | `ev_day3_002` |
| `scenes/Banheiro.tsx` | `banheiro` | `ev_secret_002` (tratada com tom calmo, sem dramatização) |
| `scenes/SalaApresentacao.tsx` | `sala-apresentacao` | `ev_day5_001` |
| `scenes/Copa.tsx` | `copa` | reserva (não usada por evento atual) |
| `scenes/DefaultScene.tsx` | `_default` | fallback quando event_id é desconhecido |
| `scenes/_index.tsx` | — | registry | — |

**Ícones de atributo (6 — SVG inline, currentColor):**

- `icons/AttributeIcons.tsx` — `EnergiaIcon, ReputacaoIcon, NetworkingIcon, AnsiedadeIcon, ProdutividadeIcon, AprendizadoIcon` (style-guide §8).
- `icons/_index.ts` — `attributeIcons`, `attributeLabels`, `attributeColors` (mapa AttributeId → componente / label PT-BR / variável CSS).

**Mapeamentos:**

- `sceneAnchors.ts` — `Record<SceneId, Anchor[]>` com 1–3 pontos por cena (fração `[0..1]` de width/height). Persona é posicionada com `translate(-50%, -100%)` para que o ponto seja o "pé".
- `eventVisualsMap.ts` — `Record<event_id, { scene, personas[] }>` cobrindo os **15 principais + 2 secretos** (cobertura literal do `Referencia_front_RPG/event-visuals-map.md`). Comentário explícito em código: **"este mapa é camada de apresentação. NÃO é regra de jogo. NÃO é catálogo de eventos."** + fallback `defaultVisual` quando event_id é desconhecido + hook `getEventVisual(id)` que aplica a precedência `event.visuals (futuro API) ?? eventVisuals[id] ?? defaultVisual`.

### 2.6 Componentes UI (`frontend/src/components/`)

| Componente | Responsabilidade |
|---|---|
| `SceneSVG.tsx` | Lookup no `scenes` registry; renderiza o componente. Fallback `_default` se sceneId inválido. |
| `PersonaSVG.tsx` | Lookup no `personas` registry; aplica `variant` e `title` (a11y). Retorna `null` silenciosamente se personaId desconhecido. |
| `EventStage.tsx` + `.css` | Palco visual: SceneSVG no fundo + PersonaSVG sobreposta em cada anchor. `role="img"` + `aria-label` descritivo. Animações `cs-fade-in` ao entrar + `cs-breathe` sutil na persona. |
| `AttributePanel.tsx` + `.css` | 6 barras (ícone + label + barra de progresso + número + indicador "alto é ruim" para ansiedade). Detecta diff entre snapshots **oficiais** do backend e dispara microanimação CSS (pulse positivo/negativo) por 700ms. **Não calcula consequência — só visualiza a diferença entre dois estados oficiais.** Padrão "update during render" usado para evitar set-state-in-effect cascading. |
| `ChoiceList.tsx` + `.css` | `<fieldset>` com botões de opção (id + label apenas — sem `consequences`). `disabled` enquanto request está em voo. Estado `selectedId` momentâneo. `aria-pressed` correto. |
| `SecretEventBanner.tsx` + `.css` | Aviso discreto quando `inject_secret_event` vem na resposta. Texto: "Evento especial desbloqueado. {title}. O fluxo completo deste evento será tratado em uma sprint futura." Não bloqueia o jogo. Despachável por botão "Entendi". `role="status"` + `aria-live="polite"`. |
| `RankingPanel.tsx` + `.css` | Lista pública: `#`, `player_name`, `ending_id` (label PT-BR), `created_at`, `score`. Linha colorida na borda esquerda por tipo de final (verde/lilás/vermelho/cinza). Estado vazio explícito ("Nenhuma partida finalizada ainda."). **`session_id` não é exibido** (api.md §"Invariante de privacidade"). |
| `EndingView.tsx` + `.css` | Tela de final: avatar trainee + título PT-BR do final + descrição narrativa + AttributePanel com atributos finais + score grande em card + ações "Ver ranking global" / "Nova jornada". Cor do título varia por tom (positive/neutral/negative). |

### 2.7 Páginas (`frontend/src/pages/`)

- **`HomePage`** — título, subtítulo, input de nome (validação `1..64` chars no cliente como UX antes do 422), botão "Iniciar nova jornada", botão "Ver ranking global". Se `getSessionId()` existe ao mount, faz `getSession(id)` e exibe card "Continuar jornada (Dia X de 5)" / "Ver final" / nada se 404 (limpa storage). Inicializador `useState` lazy → sem set-state-in-effect.
- **`GamePage`** — recebe `initialSession` por prop. Renderiza topbar com progresso (Dia X/5, Evento Y/3) + SecretEventBanner (se aplicável) + EventStage + bloco com título/scene/ChoiceList + AttributePanel na coluna lateral. Ao escolher opção: chama `submitChoice`, atualiza `session` com response, captura `inject_secret_event` se presente, navega para EndingPage se `status === 'finished'`. Tratamento de erros do backend via `ApiError` (404 limpa storage; 409 mostra mensagem).
- **`EndingPage`** — wrap de `EndingView` + `clearSessionId` ao clicar "Nova jornada".
- **`RankingPage`** — `getRanking(10)` no mount, estados `loading | ready | error`, botão "← Voltar".

### 2.8 Orquestração (`frontend/src/App.tsx`)

Roteador por estado discriminado: `{ name: 'home' } | { name: 'game'; session } | { name: 'ending'; session } | { name: 'ranking' }`. Header com brand + nav (Início/Ranking). Footer mínimo. Sem URL bookmarkable nesta sprint — escopo "mínimo".

## 3. Fora de escopo (não implementado — proibido pelo enunciado)

- Cálculo de score, final ou consequência no frontend.
- Hardcode de eventos do catálogo (eventos vêm do backend).
- Fluxo completo do evento secreto (`apply_secret_choice` ainda não existe na engine — backlog).
- `POST /api/sessions/{id}/restart` / `continue` (não existe na API).
- Ranking fake / mock — `getRanking` vai sempre na API real.
- Asset externo por CDN (todas as imagens são SVG inline locais).
- GIF pesado / Lottie pesado — sem nenhum.
- Tailwind, react-router, @fontsource/inter, lucide-react, lottie-react — nenhum instalado.
- Sprint 4 (assets visuais finais via IA/vetorização) — fora do escopo.
- Modificações em `backend/**`, `backend/engine/**`, `backend/engine/data/events.json`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/**`, `docs/01-governance/**`, `docs/00-start/**`.

## 4. Agent / Rules / Skills

- **Agent usado:** Frontend (declaração inicial respondendo Agent / Sprint / arquivos lidos / alterados / proibidos / NÃO implementado / riscos / plano / DoD — protocolo do `_dispatcher.mdc`).
- **Rules consultadas:**
  - [`.cursor/rules/_dispatcher.mdc`](../../../.cursor/rules/_dispatcher.mdc) — protocolo obrigatório de checkpoint.
  - [`.cursor/rules/frontend.mdc`](../../../.cursor/rules/frontend.mdc) — UI fina; backend é fonte da verdade; sem cálculo de score/final; sem hardcode de catálogo; localStorage só para `sessionId` (e variante visual, autorizada pelo prompt).
  - Arquivos de referência visual (autorizados pelo prompt): `Referencia_front_RPG/SKILL.md`, `style-guide.md`, `asset-pipeline.md`, `event-visuals-map.md`, `personas.md`, `scenes.md`.
- **Skills formais do Cursor:** **Skills formais não utilizadas nesta sprint** (frase obrigatória do padrão 2.x). A "skill" `Referencia_front_RPG/SKILL.md` é um documento referencial fornecido pelo humano, não uma Skill formal instalada no painel do Cursor.
- **Como Agent/Rules ajudaram (verificável):**
  - Nenhum cálculo de regra de jogo no frontend. Verificável: `rg "consequences|compute_score|apply_choice|resolve_ending" frontend/src` retorna **apenas comentários** explicando "deliberadamente NÃO".
  - Nenhum acoplamento com stack backend. Verificável: `rg -i "fastapi|sqlalchemy|pydantic" frontend/src` → **0 matches**.
  - `session_id` não é exibido na UI do ranking. Verificável: `rg "session_id" frontend/src` retorna **apenas comentários** documentando a invariante.
  - `OptionPayload` em [`types.ts`](../../../frontend/src/api/types.ts) **não tem** campo `consequences` — espelha o `EventPayload` de [`backend/schemas/sessions.py`](../../../backend/schemas/sessions.py) que omite consequences deliberadamente.
  - Eventos não estão hardcoded no frontend. O único mapa local é [`eventVisualsMap.ts`](../../../frontend/src/assets/visuals/eventVisualsMap.ts) que liga `event_id → { scene, personas[] }` — camada de apresentação, **sem** texto/título/cena narrativa/opções/consequências.
  - `localStorage` armazena apenas `cs.sessionId` e `cs.traineeVariant`. Verificável: `rg "localStorage|setItem|getItem" frontend/src` → apenas em `state/sessionStorage.ts`.
- **Arquivos proibidos não tocados (verificado):** `backend/**`, `backend/engine/**`, `backend/engine/data/events.json`, `.cursor/rules/**`, `scripts/**`, `docs/02-product/**`, `docs/01-governance/**`, `docs/00-start/**`, `_context/**`, `Referencia_front_RPG/**`. Único cross-domain autorizado pelo prompt: criar/atualizar arquivos em `docs/03-validation/` + `HANDOFF.md` + `PROJECT_STATUS.md`.

## 5. Evidências técnicas

### 5.1 `npm install`

```powershell
cd frontend
npm install
```

```
up to date, audited 154 packages in 1s
42 packages are looking for funding
found 0 vulnerabilities
```

Exit code: **0**. Nenhuma dependência adicionada. `package.json` continua com **2 deps de runtime** (react, react-dom) e dev-deps existentes (vite, eslint, typescript, types).

### 5.2 `npm run typecheck`

```powershell
npm run typecheck
```

```
> tsc --noEmit
(saída vazia — sucesso)
```

Exit code: **0**. Zero erros TypeScript em 61 módulos.

### 5.3 `npm run build`

```powershell
npm run build
```

```
> tsc -b && vite build
vite v8.0.13 building client environment for production...
✓ 61 modules transformed.
dist/index.html                   0.47 kB │ gzip:  0.30 kB
dist/assets/index-BJs9JPu-.css   17.23 kB │ gzip:  3.65 kB
dist/assets/index-B6x592RJ.js   236.73 kB │ gzip: 70.21 kB
✓ built in 155ms
```

Exit code: **0**. Bundle final **gzipado: 74 KB** (HTML + CSS + JS) — dentro do orçamento do `SKILL.md` ("página inteira do jogo ≤ 500KB").

### 5.4 `npm run lint`

```powershell
npm run lint
```

Após correções (no-useless-assignment em `client.ts`, react-refresh em `icons/_index` via split em `AttributeIcons.tsx` + `_index.ts`, set-state-in-effect via "update during render" em `AttributePanel` e `useState` lazy initializer em `HomePage`):

```
> eslint .
(saída vazia — sucesso)
```

Exit code: **0**. Zero warnings, zero errors.

### 5.5 `audit.ps1`

```powershell
powershell -ExecutionPolicy Bypass -File scripts/audit.ps1
```

```
== Corporate Survivor - audit.ps1 (governance 0.1-D) ==
OK - governanca minima presente e raiz limpa.
Nota: backend/frontend ainda nao sao exigidos nesta auditoria.
```

Exit code: **0**.

### 5.6 Greps de governança

```powershell
rg "consequences|compute_score|apply_choice|resolve_ending" frontend/src
```

Resultado: 2 hits em **comentários** (`api/types.ts:7` e `components/ChoiceList.tsx:15`) explicando "deliberadamente NÃO inclui consequences". Zero hits em código executável.

```powershell
rg -i "fastapi|sqlalchemy|pydantic" frontend/src
```

Resultado: **0 matches**. Frontend totalmente desacoplado da stack backend.

```powershell
rg "session_id" frontend/src
```

Resultado: 2 hits em **comentários** (`api/types.ts:8` e `components/RankingPanel.tsx:14`) documentando a invariante de privacidade. Zero uso real.

```powershell
rg "localStorage|setItem|getItem" frontend/src
```

Resultado: matches **apenas em** `state/sessionStorage.ts` (centralizado).

### 5.7 Arquivos criados/alterados

**Criados (32 arquivos novos em `frontend/src/`):**

| Pasta | Arquivos |
|---|---|
| `styles/` | `tokens.css`, `animations.css` |
| `api/` | `types.ts`, `client.ts` |
| `state/` | `sessionStorage.ts` |
| `assets/visuals/` | `eventVisualsMap.ts`, `sceneAnchors.ts` |
| `assets/visuals/personas/` | `_index.tsx`, `Trainee.tsx`, `Gestor.tsx`, `Gerente.tsx`, `Colega.tsx`, `Rh.tsx`, `Senior.tsx`, `LiderExterno.tsx` (8 arquivos) |
| `assets/visuals/scenes/` | `_index.tsx`, `SalaReuniao.tsx`, `MesaTrabalho.tsx`, `Restaurante.tsx`, `Bar.tsx`, `Banheiro.tsx`, `SalaApresentacao.tsx`, `Copa.tsx`, `DefaultScene.tsx` (9 arquivos) |
| `assets/visuals/icons/` | `_index.ts`, `AttributeIcons.tsx` |
| `components/` | `SceneSVG.tsx`, `PersonaSVG.tsx`, `EventStage.tsx` + `.css`, `AttributePanel.tsx` + `.css`, `ChoiceList.tsx` + `.css`, `SecretEventBanner.tsx` + `.css`, `RankingPanel.tsx` + `.css`, `EndingView.tsx` + `.css` (16 arquivos) |
| `pages/` | `HomePage.tsx` + `.css`, `GamePage.tsx` + `.css`, `EndingPage.tsx`, `RankingPage.tsx` + `.css` (7 arquivos) |

**Alterados (3 arquivos):**

- [`frontend/src/App.tsx`](../../../frontend/src/App.tsx) — substituído o healthcheck pelo orquestrador de estado entre 4 telas.
- [`frontend/src/App.css`](../../../frontend/src/App.css) — substituído por shell mínimo (header/main/footer).
- [`frontend/src/index.css`](../../../frontend/src/index.css) — importa tokens/animations + reset; mantém tipografia base.

**Não alterados (intencionais):** `frontend/package.json`, `frontend/package-lock.json`, `frontend/vite.config.ts`, `frontend/tsconfig*.json`, `frontend/eslint.config.js`, `frontend/index.html`, `frontend/src/main.tsx`, `frontend/public/icons.svg`, `frontend/README.md`.

**Documentação (cross-domain autorizado):**

- Criado: `docs/03-validation/audits/sprint-3.0.md` (este arquivo).
- Alterado: [`HANDOFF.md`](../../../HANDOFF.md), [`PROJECT_STATUS.md`](../../../PROJECT_STATUS.md), [`docs/03-validation/sprint-history.md`](../sprint-history.md).

## 6. Decisões registradas

### 6.1 Stack mínima sem novas dependências

Decisão Sprint 3.0: **plain CSS + state-based nav + SVG-as-TSX**. Justificativas:

- Atende ao princípio do prompt: "minimum viable, no GIF, no CDN, SVG-first".
- Reproduzimos a paleta completa do `style-guide.md` via CSS variables — funcionalmente equivalente ao consumo via Tailwind theme, sem o custo de PostCSS + content paths + tailwind.config.
- `system-ui` é coerente com `Referencia_front_RPG/SKILL.md` em ambiente corporativo (Inter é stretch nice-to-have, não essencial).
- 4 telas comportam-se bem com state-based routing — react-router seria over-engineering nesta sprint.
- SVGs como componentes TSX permitem `currentColor`/CSS variables sem `vite-plugin-svgr`.

A decisão foi confirmada pelo humano via AskQuestion antes da execução. Não foi necessária ADR — é decisão de produto local da Sprint 3.0, registrada aqui.

### 6.2 Mapeamento `event_id → visual` no frontend (não na engine)

A API atual ([`backend/schemas/sessions.py`](../../../backend/schemas/sessions.py) `EventPayload`) **não** retorna campo `visuals`. Para entregar o palco visual sem alterar backend/engine, criamos [`eventVisualsMap.ts`](../../../frontend/src/assets/visuals/eventVisualsMap.ts) replicando literalmente `Referencia_front_RPG/event-visuals-map.md`.

Justificativas:

- Visuais são **camada de apresentação**, não regra de jogo (`Referencia_front_RPG/SKILL.md` §"Mapeamento evento → cena → personas": "A engine não valida `visuals` (não é regra de jogo)").
- Frontend respeita a regra "não hardcoda eventos": o mapa carrega **apenas IDs e referências visuais**, não título/cena/opções/consequências (tudo isso continua vindo do backend).
- Quando a API expor `visuals` (sprint futura), a precedência fica: `event.visuals ?? eventVisuals[event.id] ?? defaultVisual`. Hook pronto em `getEventVisual(id)`.
- Função `getEventVisual` cai em `_default` para eventos desconhecidos — UI nunca quebra.

### 6.3 Trainee com 3 variantes em `localStorage`

`personas.md` §"trainee" autoriza 3 variantes (`trainee-1/2/3`) sorteadas no nascimento do player. Aproveitei a autorização explícita do prompt ("se necessário, variante visual do trainee") para implementar com `localStorage` chave `cs.traineeVariant`. Mantém o jogador "consistente visualmente" entre sessões na mesma máquina sem violar a regra "persistir mais que sessionId no localStorage" — é exatamente o caso autorizado.

### 6.4 Diff visual de atributos NÃO é regra de jogo

`AttributePanel` calcula diff entre snapshots de atributos para disparar a microanimação. **Esse diff não é consequência calculada pelo cliente**: é a diferença entre dois `Attributes` que o **backend** já devolveu (snapshot do turno anterior vs. atual). Anotado explicitamente em `AttributePanel.tsx` linhas 39–46 — frontend não opina sobre o resultado.

### 6.5 Banner discreto para `inject_secret_event` (sem fluxo completo)

A engine ainda não expõe `apply_secret_choice` (backlog confirmado em PROJECT_STATUS / HANDOFF). Quando `inject_secret_event` vem na resposta de POST /choices, mostramos banner explícito **sem oferecer opções de escolha secreta**. Texto: "Evento especial desbloqueado. {title}. O fluxo completo deste evento será tratado em uma sprint futura."

Decisão alinhada com o prompt: "Não inventar fluxo de escolha secreto. Não bloquear o jogo por causa disso."

## 7. Limitações conhecidas

- **Smoke E2E em duas camadas:** **§7.2** — com backend + Vite ativos, **sem cliques no navegador** (validação via **HTTP** à API + `GET` ao HTML do Vite; **passou com ressalvas**). **Secção [Smoke E2E manual](#smoke-e2e-manual)** — execução **humana** no browser em `localhost:8000` / `localhost:5173` com checklist completo da UI (**passou**).
- **Sem URL bookmarkable** — estado de navegação não persiste em refresh exceto `sessionId` (que faz Home redirecionar para "Continuar"). Decisão de escopo (§6.1).
- **Ícones SVG inline (não Lucide)** — leve mas menos polidos que assets profissionais. Compromisso da Sprint 3 (placeholder) — substituir na Sprint 4 (assets gerados por IA + vetorização) conforme `asset-pipeline.md`.
- **Sem teste automatizado de UI** — Sprint 3 entrega componentes e fluxo manual jogável; testes de UI (React Testing Library / Playwright) ficam para Sprint 4 ou backlog QA.
- **Variante do trainee não muda entre `Bruno`/`Marina` para o `colega`** — `personas.md` autoriza mas Sprint 3 entrega apenas a variante Marina por simplicidade.
- **Cena `copa`** entregue mas **não** mapeada por nenhum evento atual (reserva para eventos futuros — coerente com `scenes.md`).
- **Limitações herdadas das sprints anteriores** continuam: playbook reset SQLite local pós-2.2 (ver `sprint-2.2.md §7.2`).

### 7.1 Playbook de smoke E2E (para o humano executar)

```powershell
# Terminal 1 — backend
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app:app --reload --port 8000

# Terminal 2 — frontend
cd frontend
npm run dev
```

Abrir `http://localhost:5173`. Esperado:

1. Home renderiza com título "Corporate Survivor", subtítulo, input de nome, botão "Iniciar nova jornada", botão "Ver ranking global".
2. Sem `cs.sessionId` no localStorage, não aparece card "Continuar".
3. Digitar "Diego" + clicar "Iniciar nova jornada" → POST /api/players + POST /api/sessions → redirecionado para GamePage.
4. GamePage mostra cena de fundo (`sala-reuniao` no `ev_day1_001`), persona `rh` + `trainee` sobrepostas, painel de atributos lateral, título do evento, scene, 3 opções.
5. Clicar em uma opção → POST /api/sessions/{id}/choices → atributos pulsam (verde/vermelho), próximo evento renderiza com cena/personas adequadas.
6. Jogar 15 eventos principais → tela de Final (`EndingPage`) com avatar, título PT-BR do final, descrição, atributos finais, score grande.
7. Clicar "Ver ranking global" → RankingPage com a partida finalizada listada por `player_name`, `ending_id` (label PT-BR), `score`. Sem `session_id` visível.
8. Clicar "Nova jornada" → `localStorage` limpo, volta para Home pronto para nova sessão.
9. Teste de acessibilidade: ativar `prefers-reduced-motion: reduce` no DevTools → animações de pulse, fade-in e breathe param. Navegar tudo por Tab + Enter — foco visível.
10. Teste de evento secreto: para disparar `ev_secret_002` (requer `ansiedade ≥ 7`), jogar caminho que sobe ansiedade. Banner discreto aparece sobre o próximo evento.

### 7.2 Registro de smoke E2E (execução)

| Campo | Valor |
|--------|--------|
| **Data/hora (UTC)** | `2026-05-15T13:07–13:08Z` (aprox.; execução em ambiente de desenvolvimento Windows) |
| **Backend** | `cd backend` → `.\\.venv\\Scripts\\Activate.ps1` → `uvicorn app:app --port 8000` (processo em background) |
| **Frontend** | `cd frontend` → `npm run dev` (Vite `127.0.0.1:5173`, proxy `/api` → `8000`) |
| **Resultado** | **Passou com ressalvas** — contrato API + shell HTML do SPA OK; itens §7.1.9–10 (a11y motion + evento secreto) **não** reexecutados nesta rodada; **sem print** anexado. |
| **Ressalvas** | Cliques reais no Chrome/Edge não foram feitos pelo agente; fluxo validado por chamadas HTTP idênticas às do cliente. `WebFetch` para localhost não está disponível a partir do runner isolado. |

**Passos executados (mapeamento ao checklist §7.1):**

1. `GET http://127.0.0.1:8000/api/health` → `{"status":"ok"}`.
2. `GET http://127.0.0.1:5173/` → HTTP 200; corpo HTML contém a string `Corporate Survivor` (substitui abrir o navegador para checar que o dev server entrega o app).
3. **Criar player + sessão + evento inicial + ≥3 escolhas + mudança de estado:** `POST /api/players` (`SmokeE2E_Partial_May15`) → `POST /api/sessions` → estado inicial `current_event.id = ev_day1_001`, atributos baseline. Três `POST /api/sessions/{id}/choices` com o mesmo corpo que o frontend enviaria: `(ev_day1_001, A)`, `(ev_day1_002, A)`, `(ev_day1_003, C)`. Após a 3ª escolha: `current_event.id = ev_day2_001` (evento avançou); atributos diferem do baseline (ex.: `reputacao` 5→3, `networking` 3→5, `aprendizado` 4→5).
4. **Recarregar / continuar sessão:** `GET /api/sessions/{id}` repetido após as escolhas → `status=active`, `current_day=2`, `current_sequence=1`, mesmo `current_event.id=ev_day2_001` (equivalente a HomePage + `getSession` após F5 com `cs.sessionId` no `localStorage`).
5. **Chegar ao final:** segunda sessão com player `SmokeE2E_Full_May15`; sete escolhas no caminho determinístico `_GREEDY_PATH_TO_DEMITIDO` (mesmo de `backend/tests/test_ranking_api.py`). Resposta final: `status=finished`, `ending_id=demitido`, `score=49`.
6. **Ranking:** `GET /api/ranking?limit=10` → `count=1`; primeiro item com chaves **apenas** `created_at`, `ending_id`, `id`, `player_name`, `score` — **nenhuma** chave `session_id`.
7. **Consequences na interface / payload consumido pelo frontend:** `GET` da sessão logo após criação — cada opção em `current_event.options` possui **somente** `id` e `label` (verificação explícita das propriedades do primeiro objeto). O frontend não recebe `consequences` pela API (alinhado a `api/types.ts` e `ChoiceList.tsx`).

**Evidência (trecho de saída do script PowerShell):**

```
=== 2) Frontend index (Vite) ===
Status: 200 len=628
OK: HTML contem Corporate Survivor
=== 3) Sessao parcial: 3 escolhas + GET (simula reload) ===
evento_inicial=ev_day1_001 attrs0={"energia":7,"reputacao":5,...}
apos_3_escolhas_evento=ev_day2_001 attrs3={"energia":7,"reputacao":3,...}
reload_GET_status=active dia=2 seq=1 evento=ev_day2_001
OK: evento avancou
OK: atributos mudaram
=== 4) Fim-a-fim ate demitido + ranking ===
final_status=finished ending=demitido score=49
primeiro_item_keys=created_at,ending_id,id,player_name,score
OK: nenhum item com session_id na resposta
```

**Print opcional (fluxo visual):** não capturado nesta execução; recomenda-se anexar na próxima revisão de produto se o PM quiser evidência gráfica do palco SVG.

## Smoke E2E manual

Registro da **execução humana** no navegador (complementa o smoke automatizado em **§7.2**, que usou HTTP sem cliques na UI).

| Campo | Valor |
|--------|--------|
| **Ambiente** | Backend em **`http://localhost:8000`** (uvicorn); frontend em **`http://localhost:5173`** (Vite; proxy `/api` → backend). |
| **Fluxo validado** | Abrir **Home** → criar **player** → criar **session** → carregar **evento** atual → escolher **opção** → confirmar atualização de **atributos** e de **evento** → **recarregar** a página e confirmar **continuar sessão** (via `cs.sessionId` + `GET /api/sessions/{id}`) quando aplicável → aceder **ranking**. |
| **Resultado** | **Passou** — fluxo jogável ponta-a-ponta na UI; evidência visual informal: captura de ecrã do painel de atributos (antes do bugfix) usada na revisão de alinhamento. |

## Bugfix observado no frontend

| Campo | Valor |
|--------|--------|
| **Bug** | No **AttributePanel**, os valores numéricos à direita **desalinhavam-se** e podiam **encostar ou ultrapassar a borda** do cartão quando a largura da barra de progresso mudava; a coluna de valor em **`2.5ch`** era **insuficiente** para `10` e para o sufixo **`!`** da Ansiedade; a combinação **`grid-template-columns: 22px 1fr auto 2.5ch`** com **`min-width: 100px`** na barra repartia o espaço de forma **instável**. |
| **Ficheiro corrigido** | [`frontend/src/components/AttributePanel.css`](../../../frontend/src/components/AttributePanel.css) apenas (sem alteração a `AttributePanel.tsx` nem a outros componentes). |
| **Correção** | Grid passou a **`22px minmax(0, max-content) minmax(0, 1fr) 2.75rem`**: coluna de rótulo alinhada ao maior rótulo; barra com **`minmax(0, 1fr)`** + **`width: 100%`** + **`min-width: 0`**; coluna de valor com **largura fixa** `2.75rem`; valor com **`inline-flex`**, **`justify-content: flex-end`**, **`white-space: nowrap`**; hint **`flex-shrink: 0`**; rótulo com ellipsis em falta de espaço. |
| **Validação pós-correção** | `npm run lint` e **`npm run typecheck` + `npm run build`** na pasta `frontend/` na entrega **Sprint 3.0-A** (ver §11). |

## Observação sobre encerramento dos processos

- Os processos **`uvicorn` em `:8000`** e **`npm run dev` (Vite) em `:5173`** foram corridos em **background** durante o smoke assistido por agente.
- Após **`Stop-Process`** (ou encerramento forçado do wrapper do terminal), o relatório do task pode mostrar **`exit_code=4294967295`** (valor não assinado típico no Windows quando o processo é terminado).
- **Isto não representa falha do smoke**: as **chamadas HTTP** e a **validação** já tinham sido concluídas com sucesso antes do encerramento.

## 8. Validação documental

- [`docs/03-validation/audits/sprint-3.0.md`](sprint-3.0.md) — este relatório (criado).
- [`HANDOFF.md`](../../../HANDOFF.md) — nova entrada (sessão 12) com declaração, deltas, escopo preservado, evidências, próximo passo.
- [`PROJECT_STATUS.md`](../../../PROJECT_STATUS.md) — sprint técnica mais recente atualizada para 3.0; status frontend.
- [`docs/03-validation/sprint-history.md`](../sprint-history.md) — linhas **3.0** e **3.0-A**.

Não alterados (proibidos / fora de escopo):

- [`docs/02-product/api.md`](../../02-product/api.md) — endpoints já documentados; frontend é cliente puro, não muda contrato.
- [`docs/02-product/game-rules.md`](../../02-product/game-rules.md) — regra de jogo intacta.
- [`docs/02-product/architecture.md`](../../02-product/architecture.md) — frontend faz exatamente o que arquitetura prevê ("UI fina, consumo da API, estados visuais"); sem mudança de arquitetura.
- [`docs/01-governance/decisions.md`](../../01-governance/decisions.md) — nenhuma ADR nova; decisões da §6 são locais da Sprint 3.0.
- [`docs/00-start/sprint-plan.md`](../../00-start/sprint-plan.md) — bloco "Sprint 3" continua descrevendo "UX completa". A entrega da Sprint 3.0 é o **mínimo jogável**; refinamento (Sprint 3.1 / Sprint 4) cobrirá assets visuais finais e polish, se necessário.

## 9. Critério de aceite aplicado

- [x] Agent Frontend declarado com checkpoint inicial completo (Agent / Sprint / arquivos lidos / alterados / proibidos / NÃO implementado / riscos / plano / DoD).
- [x] Sprint declarada (3.0); escopo exclusivamente Frontend; cross-domain limitado a `docs/03-validation/` + `HANDOFF.md` + `PROJECT_STATUS.md` (autorizado pelo prompt).
- [x] Quatro telas implementadas (Home, Game, Ending, Ranking).
- [x] Fluxo completo cobrindo `POST /api/players → POST /api/sessions → GET /api/sessions/{id} → POST /api/sessions/{id}/choices → GET /api/ranking`.
- [x] EventStage renderiza cena SVG + personas SVG sobrepostas usando mapeamento local + fallback `_default`.
- [x] 7 personas + 8 cenas (incluindo `_default`) criadas como componentes TSX placeholder geométricos.
- [x] AttributePanel com 6 atributos + ícones SVG inline + microanimação CSS de pulse após escolha + `prefers-reduced-motion` ativo globalmente.
- [x] SecretEventBanner aparece quando `inject_secret_event` vem na resposta; não bloqueia o jogo; não inventa fluxo.
- [x] RankingPanel exibe `player_name`, `ending_id` (label PT-BR), `score`, `created_at` — sem `session_id`.
- [x] `localStorage` armazena apenas `cs.sessionId` + `cs.traineeVariant` (autorizado).
- [x] Nenhum cálculo de regra de jogo no frontend (verificado por greps — apenas comentários defensivos).
- [x] Nenhum hardcode de evento no frontend — `eventVisualsMap.ts` carrega apenas IDs + referências visuais, não conteúdo narrativo.
- [x] Nenhuma dependência nova instalada — `package.json` intacto.
- [x] `npm install / typecheck / build / lint` exit 0.
- [x] `audit.ps1` exit 0.
- [x] Backend, engine, events.json, .cursor/rules/, scripts/, docs/02-product, docs/01-governance, docs/00-start, _context/, Referencia_front_RPG/: **zero alterações**.
- [x] Acessibilidade: `alt`/`aria-label` em SVGs e regiões, foco visível, contraste do style-guide, navegação por teclado, heading hierarchy, `prefers-reduced-motion`.
- [x] Smoke E2E registrado em **§7.2** (`2026-05-15`) — resultado **passou com ressalvas** (API + HTML inicial; sem passo manual completo de browser).
- [x] Smoke E2E **manual** registrado (secção dedicada) — resultado **passou** (UI no browser).
- [x] Bugfix **AttributePanel** documentado (secção **Bugfix observado no frontend**).
- [x] **Sprint 3.0-A:** `npm run typecheck`, `npm run lint`, `npm run build` em `frontend/` — exit 0 (§11).
- [x] Skills formais não declaradas falsamente — frase obrigatória registrada em §4.

## 10. Decisão de aceite humano

- Aceite técnico da implementação Sprint 3.0: **confirmado pelo PM** (mensagem 2026-05-15) para avanço pré-Sprint 4.
- **Sprint 3.0-A** (`2026-05-15`): registo do **smoke E2E manual** (passou), do **bugfix** do `AttributePanel`, da **observação sobre encerramento** dos processos em background, revalidação **typecheck/lint/build** — ver §11.
- Smoke E2E: **§7.2** — **passou com ressalvas** (HTTP + HTML inicial). **Smoke E2E manual** — **passou** (browser).
- Observações consolidadas no aceite:
  - `npm install / typecheck / build / lint` todos passaram (exit 0).
  - `audit.ps1` exit 0.
  - Greps de governança vazios (apenas comentários defensivos onde aparecem palavras-chave).
  - Nenhuma dependência nova introduzida.
  - 4 telas, 7 personas, 8 cenas, 17 eventos mapeados, microanimação CSS, banner secreto discreto.
  - Backend/engine/events.json/rules/scripts: zero alterações na Sprint 3.0.
  - Ranking JSON público sem `session_id`; opções da API sem `consequences` (smoke §7.2).
- Próximas etapas pós-aceite 3.0:
  1. Aceites humanos formais pendentes — Sprints **2.1 §11**, **2.2 §8**, **2.2-B §10**, **2.3 §10** podem ser aceitos em conjunto; **3.0 / 3.0-A** — aceite técnico no relatório; papel §10 só se o processo exigir.
  2. **Architect/Documentation** — fechar `docs/00-start/executive-overview.md` cobrindo Sprints 2.x + 3.0.
  3. **Backlog engine/UX:** `apply_secret_choice` (segunda etapa do fluxo secreto) na engine + ajuste no frontend para renderizar a escolha real (em sprint futura).
  4. **Sprint 4.0 — polimento final / UX / auditoria de entrega:** assets visuais finais via IA + vetorização (asset-pipeline.md §"Opção B"), testes automatizados de UI, paginação do ranking, URL bookmarkable se necessário.

## 11. Sprint 3.0-A — Registro, bugfix e aceite (micro-sprint)

**Objetivo:** fechar documentalmente a Sprint 3.0 com smoke **manual**, correcção de UI no painel de atributos e aceite técnico consolidado — **sem** nova feature, **sem** alterações a backend/engine/`events.json`/rules/scripts.

**Entregas:**

- Secções **Smoke E2E manual**, **Bugfix observado no frontend** e **Observação sobre encerramento dos processos** neste relatório.
- Atualização de [`HANDOFF.md`](../../../HANDOFF.md), [`PROJECT_STATUS.md`](../../../PROJECT_STATUS.md), [`docs/03-validation/sprint-history.md`](../sprint-history.md).

**Evidências `frontend/` (Sprint 3.0-A):**

```
> npm run typecheck
(tsc --noEmit — sucesso, exit 0)

> npm run lint
(eslint . — sucesso, exit 0)

> npm run build
vite v8.0.13 building client environment for production...
✓ 61 modules transformed.
dist/index.html                   0.47 kB │ gzip:  0.30 kB
dist/assets/index-CzFHZRFL.css   17.46 kB │ gzip:  3.71 kB
dist/assets/index-BYXuJ0om.js   236.73 kB │ gzip: 70.21 kB
✓ built in 177ms
```
