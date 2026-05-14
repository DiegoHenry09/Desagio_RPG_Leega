# Corporate Survivor — Plano v2 (revisado para ambiente corporativo)

Substitui o plano v1. Aplica os ajustes solicitados após validação.

---

## Changelog v1 → v2

| Mudança | Motivo |
|---|---|
| Alembic vira opcional com fallback documentado | Reduzir fricção no ambiente da empresa no Sprint 0 |
| 7 agentes → 5 agentes consolidados | Operação real com uma pessoa |
| Adicionado mecanismo de invocação dos agentes (dispatcher + templates + validação por diff) | "Não adianta ter rule se não for usada" |
| Sprint 0 inclui validação de setup no ambiente real | Sprint 0 só fecha se rodar na empresa |
| Adicionado `docs/setup-company-env.md` como deliverable do Sprint 0 | Setup reproduzível |
| UX detalhada por tela com estados de feedback | Provar impacto das escolhas visualmente |
| Regra dura: exatamente 3 eventos principais por dia, fixos no catálogo | Aderência literal ao desafio |
| Engine simplificada: não há seleção de pool entre principais | Consequência da regra anterior |
| Finais sempre resolvidos no fim do dia 5 (jogo nunca interrompe antes) | Simplificação; documentado em ADR |
| Adicionado checklist de segurança mínima | Boa prática mostrável |
| CI/CD removido do escopo obrigatório, vira bônus | Foco no essencial |

---

## 1. Mecanismo de invocação dos agentes

Esta é a parte mais importante e a mais frágil em projetos com IA. A regra que rege tudo: **o agente correto é invocado automaticamente pelo Cursor (via globs) na maioria dos casos; quando ambíguo, você usa um template; em todos os casos, há validação a posteriori por diff.**

### 1.1 Camada 1 — Carregamento automático por `globs`

As rules `.mdc` de cada agente declaram `globs`. Quando você abre/edita um arquivo que casa, a rule é injetada no contexto da LLM sem ação manual. Funciona dentro de uma sessão de chat normal do Cursor.

Exemplo: ao editar `backend/engine/scoring.py`, a rule `game-engine.mdc` carrega automaticamente porque seu glob é `backend/engine/**/*.py`.

### 1.2 Camada 2 — Dispatcher `alwaysApply: true`

Existe uma rule chamada `_dispatcher.mdc` que é **carregada em toda sessão**, independente de arquivo aberto. Conteúdo (resumido — versão completa no Bloco C atualizado):

> Antes de qualquer ação que toque código, você DEVE:
> 1. Identificar qual agente é responsável pela tarefa (consultar tabela abaixo).
> 2. Declarar em uma frase no início da sua resposta: "Atuando como Agent X. Consultando: <lista de rules/docs>."
> 3. Ler os arquivos declarados em 2.
> 4. Só então propor mudanças.
>
> Se a tarefa cruza domínios de mais de um agente, declare isso explicitamente, faça primeiro o trabalho do agente mais "puro" (Engine antes de API antes de Front) e pare entre os domínios para confirmar com o humano.

Esse dispatcher é a sua trava. Se a LLM começa a editar código sem declarar o agente, você corta a resposta e reinicia.

### 1.3 Camada 3 — Prompt templates para tarefas ambíguas

Para tarefas cross-cutting (ex.: "implementar feature de ranking") onde os globs não decidem sozinhos, há templates prontos em `docs/cursor-workflow.md`. Você copia e cola no início da nova sessão. Cada template:

- Identifica explicitamente o agente.
- Lista as rules e docs a serem lidos.
- Define o output esperado (código + entrada em HANDOFF.md).
- Define a Definition of Done daquela tarefa específica.

### 1.4 Tabela de dispatch (vai no `_dispatcher.mdc` e em `cursor-workflow.md`)

| Tarefa | Agente | Rules que devem ser lidas |
|---|---|---|
| Editar `frontend/**` | Frontend | `frontend.mdc` + `docs/api.md` |
| Editar `backend/engine/**` ou `events.json` | Engine/Content | `game-engine.mdc` + `events-json.mdc` + `docs/game-rules.md` |
| Editar `backend/**` exceto engine | Backend | `backend.mdc` + `docs/api.md` |
| Editar `**/tests/**` | Auditor/QA | `tests.mdc` |
| Editar `docs/**` ou `README.md` | Architect/Docs | `docs-sync.mdc` |
| Encerrar sprint / rodar auditoria | Auditor/QA | `docs/sprint-plan.md` (DoD da sprint atual) + executar `scripts/audit.sh` |
| Decisão arquitetural nova | Architect/Docs | criar ADR em `decisions.md` |

### 1.5 Validação por diff (a chave do mecanismo)

Cada sessão termina com o agente atualizando `HANDOFF.md`:

```markdown
## HANDOFF — <data/hora> — Agent <Nome>

### Declaração
- Atuei como: Agent Backend
- Rules consultadas: backend.mdc, docs/api.md
- Arquivos tocados: backend/routers/sessions.py, backend/schemas/session_dto.py
- Não toquei: backend/engine/**

### O que fiz
- ...

### O que falta / próximo agente
- ...
```

O Auditor, ao rodar `scripts/audit.sh`, compara essa declaração com `git diff`:

```bash
# Pseudo-check no audit.sh — verifica que o que o agente disse bate com o que fez
declared_files=$(grep "Arquivos tocados:" HANDOFF.md | ...)
actual_files=$(git diff --name-only HEAD~1)
# Se actual_files contém arquivos fora dos limites do agente declarado, falha.
```

**Por que isso funciona:** garante traceabilidade humano-legível e blocos de violação são óbvios. Quando o Cursor "vaza" entre agentes, o diff denuncia.

### 1.6 Quando humano interrompe

Você (Diego) interrompe a sessão da LLM quando:

- Ela começa a editar sem declarar agente.
- Ela toca arquivos fora do escopo do agente declarado.
- Ela ignora rule que era para ler.
- Ela inventa decisão arquitetural sem ADR.

Não é desperdício de tempo — é o trabalho real do humano nesse modelo: governança, não digitação.

---

## 2. Stack confirmada (sem mudanças desde v1)

| Camada | Escolha |
|---|---|
| Backend | Python 3.11+ / FastAPI |
| Persistência | SQLite via SQLAlchemy 2.0 |
| Migrations | **Alembic se ambiente permitir; senão `Base.metadata.create_all()` no startup com ADR registrada** |
| Validação | Pydantic v2 |
| Engine | Módulo Python puro em `backend/engine/` |
| Frontend | Vite + React 18 + TypeScript |
| Estilo | Tailwind CSS |
| Estado server | React Query |
| Testes back | pytest + httpx |
| Testes front | Vitest + Testing Library |

**Decisão sobre Alembic:** o Sprint 0 tenta com Alembic. Se houver fricção de instalação ou execução no ambiente corporativo, troca para `create_all()` no startup do FastAPI e registra ADR-006 explicando. Não é regressão técnica — para um banco do tamanho deste projeto, ambas abordagens são razoáveis.

---

## 3. Camada de agentes — 5 agentes consolidados

### Agent 1 — Architect / Documentation

**Responsabilidade:** decisões arquiteturais, ADRs, manter `docs/` vivo, manter README executável, atualizar `sprint-plan.md`, validar coerência entre docs e código.

**Quando atuar:** início de cada sprint (planejamento), fim de cada sprint (atualizar docs), e sob demanda quando outro agente registra "decisão pendente" em HANDOFF.

**Limites:**
- Não escreve código de produção.
- Toda ADR tem contexto, opções, decisão, consequências.
- Não inventa documentação que não corresponde ao código.

**Rules:** `docs-sync.mdc` + leitura de `decisions.md` e `HANDOFF.md`.

### Agent 2 — Backend

**Responsabilidade:** FastAPI, routers, use cases, SQLAlchemy 2.0, repositórios, schemas Pydantic, migrations Alembic (ou create_all), configuração de boot, scripts de seed.

**Limites:**
- Não importa de `frontend/`.
- Não importa de `backend/engine/**` exceto via API pública declarada em `engine/__init__.py`.
- Routers não contêm regra de jogo.
- Nunca aceita atributos/score do frontend.

**Rules:** `backend.mdc` + `docs/api.md` + `docs/architecture.md`.

### Agent 3 — Frontend

**Responsabilidade:** páginas React, componentes, hooks React Query, roteamento, responsividade, estados visuais (loading, erro, vazio), acessibilidade básica, integração com API.

**Limites:**
- Nunca calcula score, decide final ou aplica consequência.
- Nunca tem cópia local de eventos ou consequências.
- Trata backend como única fonte da verdade.
- `localStorage` apenas para `sessionId`.

**Rules:** `frontend.mdc` + `docs/api.md`.

### Agent 4 — Engine / Content

**Responsabilidade (lógica):** carregamento e validação de `events.json`, aplicação de consequências, seleção do próximo evento (na nova regra: simplesmente o próximo principal do dia, mais checagem de secretos), cálculo de score, resolução de final, registry de finais.

**Responsabilidade (conteúdo):** escrever os 15 eventos principais + secretos opcionais, mantendo tom corporativo realista e balanceamento (sem opção dominante).

**Limites:**
- `engine/**` não importa FastAPI, SQLAlchemy ou qualquer I/O.
- Funções puras com estado imutável.
- Edição de evento existente OU adição de evento secreto = só toca `events.json` + validador.
- Mudança na engine = teste novo obrigatório.

**Rules:** `game-engine.mdc` + `events-json.mdc` + `docs/game-rules.md`.

### Agent 5 — Auditor / QA

**Responsabilidade:** testes automatizados (unit da engine, contrato de API, componentes front), execução de `scripts/audit.sh` ao fim de cada sprint, produção de `docs/audits/sprint-N.md`, validação de DoD.

**Limites:**
- **Read-only no código de produção.** Único arquivo de produção que pode escrever é `docs/audits/`.
- Pode escrever testes em `tests/`.
- Não declara sprint fechada se algum check falhou.
- Cada apontamento vem com evidência (path:linha ou comando que reproduz).

**Rules:** `tests.mdc` + `docs/sprint-plan.md`.

---

## 4. Cursor rules atualizadas

A lista de rules muda ligeiramente em relação ao v1 para incluir o dispatcher:

```
.cursor/rules/
  _dispatcher.mdc        # alwaysApply: true — meta-rule de invocação
  frontend.mdc           # globs: frontend/**
  backend.mdc            # globs: backend/** exceto engine/
  game-engine.mdc        # globs: backend/engine/**/*.py
  events-json.mdc        # globs: backend/engine/data/events.json
  tests.mdc              # globs: **/tests/**, **/*.test.{ts,tsx}
  docs-sync.mdc          # globs: docs/**, README.md
```

### Conteúdo do `_dispatcher.mdc` (novo)

```mdc
---
description: Meta-rule de invocação. Aplicado em todas as sessões.
alwaysApply: true
---

# Dispatcher de Agentes — Corporate Survivor

Você é uma LLM operando no Cursor. Este projeto tem 5 agentes especializados e regras estritas de domínio. Antes de qualquer ação que toque código, siga este protocolo.

## Protocolo obrigatório no início de cada tarefa

1. **Identifique o agente** consultando a tabela:

| Caminho da tarefa | Agente |
|---|---|
| `frontend/**` | Frontend |
| `backend/engine/**` ou `events.json` | Engine/Content |
| `backend/**` exceto engine | Backend |
| `**/tests/**` | Auditor/QA |
| `docs/**`, `README.md`, `decisions.md` | Architect/Docs |

2. **Declare em uma frase no início da sua resposta:**
   "Atuando como Agent <Nome>. Consultando: <lista de rules/docs>."

3. **Leia as rules e docs declarados antes de propor mudanças.**

4. **Se a tarefa cruza domínios**, declare isso explicitamente. Faça o trabalho do agente mais isolado primeiro (Engine antes de Backend antes de Frontend). Pare entre os domínios e peça confirmação humana.

## O que NÃO fazer

- Tocar arquivo fora do domínio do agente declarado.
- Inventar decisão arquitetural sem propor ADR em `docs/decisions.md`.
- Pular leitura das rules dizendo "já conheço o projeto".
- Editar mais de um domínio em uma única resposta sem confirmação humana entre eles.

## Ao final de cada tarefa

Atualize `HANDOFF.md` na raiz seguindo o template em `docs/cursor-workflow.md`. Sem isso, o Auditor reprova a tarefa.

## Em caso de dúvida

Pare e pergunte ao humano. É preferível a tarefa demorar mais a você violar uma regra de domínio.
```

As outras rules do v1 (frontend.mdc, backend.mdc, game-engine.mdc, etc.) permanecem como no v1 com pequeno ajuste: cada uma agora inclui no final a frase **"este agente segue o protocolo descrito em `_dispatcher.mdc`."** Isso é redundância intencional para reforço.

---

## 5. Documentação obrigatória — atualizada

```
docs/
  architecture.md
  game-rules.md
  api.md
  decisions.md
  sprint-plan.md
  cursor-workflow.md
  setup-company-env.md    # ★ NOVO — específico para o ambiente da empresa
  audits/
    sprint-0.md
    sprint-1.md
    ...
  playthroughs/           # exemplos de partidas completas, para teste
    full_run_1.md
    ...
```

Conteúdo do `setup-company-env.md` está em arquivo separado deste plano (entregue como artefato 3).

---

## 6. UX detalhada — fluxo do jogador

### 6.1 Tela inicial (`/`)

**Estado A — sem sessão salva:**
- Título "Corporate Survivor"
- Subtítulo curto: "Sobreviva à sua primeira semana como trainee."
- Botão primário: **Começar nova jornada** → leva para `/new`
- Link secundário: **Ver ranking global** → leva para `/ranking`

**Estado B — sessionId encontrado no localStorage:**
- Mesmo título
- Card destacado: "Você tem uma jornada em andamento — Dia X de 5."
- Botão primário: **Continuar** → leva para `/game/:sessionId`
- Botão secundário: **Começar nova** → confirma e abandona a anterior

### 6.2 Cadastro (`/new`)

- Campo único: "Seu nome" (input texto, max 60 chars, validação client + server)
- Texto explicativo curto: "Você vai viver 5 dias na empresa. Cada decisão importa."
- Botão: **Iniciar** (desabilitado enquanto nome inválido)
- Estados: loading durante POST `/api/players` + POST `/api/sessions`

### 6.3 Tela de jogo (`/game/:sessionId`)

Layout responsivo. Mobile (360px+): vertical. Desktop: header + cena + opções, com painel lateral de atributos.

**Cabeçalho:**
- Nome do jogador
- Indicador de progresso: **Dia 2/5 — Evento 1/3** (claramente visível)
- Barrinha de progresso semanal (15 segmentos, 3 por dia, atual destacado, passados marcados)

**Painel de atributos:**
- 6 barras pequenas com label e valor numérico:
  - Energia 7/10
  - Reputação 5/10
  - Networking 3/10
  - Ansiedade 2/10
  - Produtividade 5/10
  - Aprendizado 4/10
- Atributos "negativos" (ansiedade) coloridos diferente para sinalizar que alto = ruim
- Tooltip no hover/tap explicando cada atributo

**Cena do evento:**
- Título do evento
- Texto narrativo (1-3 parágrafos)
- Cards de opções (2-4)
- Cada opção mostra apenas o texto — **não mostra consequências**. (Decisão narrativa intencional: o jogador descobre depois.)

**Após escolher (feedback):**
- Brief overlay/toast: "Você escolheu: [opção]"
- Animação curta nas barras de atributos: cada delta mostrado por +1s com cor (verde positivo, vermelho negativo, amarelo neutro/contextual)
- Texto narrativo de resposta curto opcional (campo `feedback` no evento, opcional)
- Botão **Próximo** ou auto-avanço em 2-3s

### 6.4 Tela de final (`/end/:sessionId`)

- Título dramático: "Final: [Nome do final]"
- Texto curto descrevendo o final (campo opcional `description` em endings.py)
- Estado final dos atributos (mesmas barras)
- Score: **127 pontos**
- Comparação rápida: "Você está no top 23% do ranking."
- Botões:
  - **Ver ranking completo** → `/ranking`
  - **Jogar novamente com novo personagem** → `/new`
  - **Compartilhar resultado** (opcional, gera texto copyable)

### 6.5 Ranking (`/ranking`)

- Título "Ranking Global"
- Tabela:
  | # | Jogador | Final | Score | Data |
  |---|---|---|---|---|
- Sua linha destacada
- Paginação se > 50

### 6.6 Reset

- A partir de qualquer tela durante o jogo, há um menu pequeno (canto superior) com **Reiniciar jornada**
- Confirma com modal: "Tem certeza? Você perde o progresso atual."
- Em yes → POST `/api/sessions/:id/restart` e estado volta ao dia 1

### 6.7 Estados de erro e loading

- Loading inicial: skeleton dos componentes principais
- Erro de rede: toast "Sem conexão. Tentando novamente..." + retry automático
- Erro 404 sessão: redireciona para `/` e limpa localStorage
- Erro 409 escolha inválida: toast "Esta escolha não está mais disponível" + refetch do estado

### 6.8 Por que essa UX prova o impacto das escolhas

- Animação nas barras a cada escolha torna o efeito tangível.
- Indicador "Dia X/5 — Evento Y/3" deixa claro que cada evento é único e há progressão real.
- Tela de final com nome e descrição prova que o estado importou.
- Ranking põe seu score em contexto.

---

## 7. Regra dura: 5 dias × 3 eventos principais

### Definições

- **Evento principal:** `isMain: true`, atribuído a um `day: 1..5`. Existem exatamente 3 por dia. Total: 15.
- **Evento secreto:** `isMain: false`, sem `day` fixo, com `unlock` condicional. Pode ser injetado entre eventos principais quando suas condições se satisfazem.
- **Progressão:** a sessão tem 15 "slots principais" ordenados. Em qualquer slot, se um evento secreto é elegível, ele é injetado **antes** do próximo principal. Eventos secretos não consomem slots principais.

### Garantias (verificadas pelo `validate_events()`)

1. Existem exatamente 3 eventos com `isMain: true` para cada `day` 1..5.
2. Total de eventos principais ≥ 15 (= 5×3).
3. Eventos secretos ≥ 0, sem limite superior obrigatório (sugestão: 2-4).
4. Eventos principais não têm `unlock` (sempre rolam no seu dia).
5. Eventos secretos têm pelo menos uma condição em `unlock`.

### Por que essa regra é mais simples que pool dinâmico

- Não há seleção entre principais → engine de seleção é trivial.
- Garantia matemática de 3 por dia, sem edge cases.
- Variabilidade vem de (a) escolhas dentro dos principais, (b) eventos secretos opcionais, (c) opções condicionais.

### O "impacto em eventos futuros" pedido pelo desafio

Manifesta-se via:
- **Opções condicionais dentro de principais futuros.** Ex.: o principal `ev_day3_002` tem 4 opções; a opção D só aparece se `networking ≥ 5`. O JSON suporta isso via `unlock` no nível da opção.
- **Eventos secretos.** Ex.: se ao final do dia 3 o jogador tem reputação ≥ 7, o secreto "Convite para projeto especial" é injetado no início do dia 4.
- **Final atingido.** Estado final no fim do dia 5 determina o final via registry de predicados.

---

## 8. Segurança mínima

### Backend
- Validação Pydantic de input em todos os endpoints.
- `name`: regex `^[\w\s\-'.]{1,60}$`, trim, sem caracteres de controle.
- `event_id` recebido em `POST /choices`: precisa bater com o `current_event_id` da sessão. Se não bater → 409.
- `option_id`: precisa existir nas opções do evento atual. Se não → 422.
- Nunca aceitar `attributes`, `score`, `ending` no body.
- Handler global de exceção: erros 500 retornam payload genérico `{"error": "internal_error", "request_id": "..."}`. Stack trace só nos logs, nunca no response.
- CORS configurado para `http://localhost:5173` (Vite dev) e o domínio interno da empresa quando deploy.

### Frontend
- React por padrão escapa text content; nunca usar `dangerouslySetInnerHTML`.
- Não armazenar nada além de `sessionId` em localStorage.
- Não logar dados do jogador no console em produção.
- Validação local do nome antes de enviar (UX), mas backend é a fonte da verdade.

### Repositório
- `.env` real fora do git (`.gitignore`).
- `.env.example` no git, sem valores reais.
- Arquivo SQLite `data/corporate_survivor.db` fora do git (`.gitignore`).
- Migrations versionadas (se Alembic ativo).

### Logs
- Sem PII além do nome do jogador.
- Logger configurado para nível INFO em produção.

---

## 9. Sprint plan atualizado

### Sprint 0 — Foundation + ambiente da empresa (1-2 dias)

**Objetivo:** repo executável vazio rodando no ambiente da empresa, com `docs/setup-company-env.md` validado.

**Tarefas adicionais ao v1:**
- Escrever `docs/setup-company-env.md` antes de iniciar Sprint 1.
- Executar passo-a-passo do setup-company-env no ambiente real.
- Registrar problemas encontrados como troubleshooting no próprio doc.
- Decidir Alembic vs `create_all` baseado no resultado.

**DoD revisado:**
- [ ] `bash scripts/audit.sh` passa.
- [ ] Backend sobe seguindo só `docs/setup-company-env.md`.
- [ ] Frontend sobe seguindo só `docs/setup-company-env.md`.
- [ ] Endpoint `GET /api/health` retorna 200.
- [ ] Frontend mostra "API: ok" na tela.
- [ ] README ensina setup em < 5 min para alguém que nunca viu o projeto.
- [ ] Todas as rules `.mdc` (incluindo `_dispatcher.mdc`) existem.
- [ ] `HANDOFF.md` na raiz com template inicial.

### Sprints 1-4

Mesma estrutura do v1, com ajustes:
- Sprint 1: 15 eventos principais + 2 secretos opcionais (não "15-18 com seleção").
- Sprint 2: adicionar handler global de erro, validação Pydantic estrita, CORS configurado.
- Sprint 3: UX detalhada como na seção 6 desta v2.
- Sprint 4: validar manualmente todos os finais alcançáveis via playthroughs documentados em `docs/playthroughs/`.

---

## 10. Riscos e mitigações — atualizado

Riscos do v1 mantidos. Adicionados:

| # | Risco novo | Mitigação |
|---|---|---|
| R13 | Ambiente da empresa bloqueia instalação de algo (Python version, npm registry, etc.) | Sprint 0 valida tudo cedo; setup-company-env documenta workarounds |
| R14 | LLM no Cursor ignora dispatcher e edita sem declarar agente | Humano interrompe; audit.sh detecta no diff |
| R15 | LLM "vaza" entre domínios em uma única resposta | Dispatcher exige parar entre domínios; audit.sh cruza HANDOFF com diff |
| R16 | Alembic não roda no ambiente, atrasa Sprint 0 | Fallback `create_all` documentado em ADR-006 |
| R17 | Eventos secretos confundem o jogador (aparecem do nada) | UI sinaliza visualmente (ex.: badge "evento inesperado") |

---

## Próximos artefatos

Entregues junto com este v2:

1. `corporate-survivor-game-rules.md` — schema final, atributos, finais, regra de progressão, 15 eventos + 2 secretos
2. `corporate-survivor-setup-company-env.md` — setup completo para ambiente da empresa
