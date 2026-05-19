# Corporate Survivor — Dossiê Final de Entrega

> Documento para **gestores**, **avaliadores** e **liderança técnica**. Complementa o [Dossiê Executivo](executive-overview.md) com visão de **entrega**, **linha do tempo**, **evidências** e **governança de IA**.  
> Estado da arte do produto e da stack: ver também [`PROJECT_STATUS.md`](../../PROJECT_STATUS.md), [`docs/02-product/architecture.md`](../02-product/architecture.md), [`docs/02-product/api.md`](../02-product/api.md).

---

## 1. Resumo executivo

**Corporate Survivor** é um RPG narrativo corporativo em primeira pessoa: o jogador é um **trainee** na primeira semana de uma empresa, enfrenta situações realistas (reuniões, entregas, pressão social) e **cada escolha altera atributos** que moldam o desfecho e a pontuação.

O projeto atende ao desafio de **engenharia de contexto e uso disciplinado de IA**: a entrega valoriza tanto o software jogável quanto **arquitetura em camadas**, **documentação canônica em `docs/`**, **rules do Cursor por domínio**, **relatórios de aceite por sprint**, **HANDOFF** entre sessões e **auditoria** (`scripts/audit.ps1`). O objetivo declarado **não foi apenas codificar**, mas demonstrar que é possível **reduzir erro** e **rastrear decisões** quando humanos e LLMs colaboram com papéis e limites explícitos.

---

## 2. Storytelling do produto

Você chega como **trainee**. Durante **cinco dias úteis** (15 eventos principais, três por dia), vive um **onboarding** com tom de escritório brasileiro realista: sem vilão caricato, com trade-offs em cada decisão.

À medida que escolhe como reagir a RH, gestores, colegas e demandas, seus **atributos** (energia, reputação, networking, ansiedade, produtividade, aprendizado) **sobem ou descem** dentro de limites de jogo. **Finais antecipados** podem encerrar a semana antes do dia 5 (por exemplo, desfechos ligados a reputação, energia ou ansiedade crítica, conforme regras formais). Se completar a semana, o **registry de finais** escolhe um dos desfechos de encerramento por predicados sobre o estado.

Ao terminar, a **sessão vira histórico**: **score** e **final** são registrados no **ranking global**, visível na aplicação.

Isto é **RPG narrativo com palco visual** (cena + personas), **não** um questionário seco: texto de cena, opções com rótulos e feedback vêm do **catálogo**; a interface reforça contexto corporativo sem substituir a narrativa por um formulário anônimo.

---

## 3. Experiência do usuário

| Etapa | O que o jogador vê / faz |
|--------|---------------------------|
| **Home** | Título, subtítulo, campo de nome, “Iniciar nova jornada”, acesso ao ranking. Se existir sessão salva localmente, opção de continuar (conforme implementação atual). |
| **Criação de jogador** | Nome enviado à API; criação de **player** e de **sessão** no backend. |
| **Sessão** | Estado ativo: dia (1–5), sequência do evento, evento atual retornado pela API. |
| **Tela de evento** | Texto da cena, tags, opções (apenas `id` e `label` para o cliente). |
| **Palco visual** | **Cena SVG** de fundo e **personas SVG** ancoradas no palco, conforme mapeamento de apresentação (IDs de evento → cena/personas). |
| **Painel de atributos** | Seis atributos com barras e microanimação ao mudar valores **oficiais** devolvidos pelo servidor (o cliente não aplica consequência). |
| **Escolhas** | Lista de opções; ao escolher, `POST` de escolha; resposta traz novo snapshot (e eventual sinal de evento secreto sem fluxo completo na UI). |
| **Tela final** | Final, descrição, atributos finais, score, atalhos para ranking ou nova jornada. |
| **Ranking** | Lista pública: nome, final, score, data **sem** exposição de `session_id` na API de listagem. |

Detalhes de implementação e smoke: [`docs/03-validation/audits/sprint-3.0.md`](../03-validation/audits/sprint-3.0.md).

---

## 4. Arquitetura do sistema

- **Frontend (thin client):** React + Vite + TypeScript; exibe o estado recebido, envia escolhas; **não** é fonte da verdade para score/final/consequências.
- **Backend (fonte da verdade operacional):** FastAPI; routers finos; **use cases** orquestram transações; **repositórios** são a única camada que persiste em SQLite.
- **Engine (Python pura):** Módulos em `backend/engine/`; validação do `events.json`, `apply_choice`, clamp, gatilhos de final antecipado, score e resolução de final; **sem** FastAPI, SQLAlchemy ou UI.
- **Persistência:** SQLite; modelos e CRUD sem regra de jogo nas queries.
- **Catálogo:** `events.json` versionado com o repositório (15 principais + 2 secretos); validado no **boot** da API.
- **Governança:** `docs/` (produto, governança, validação), `.cursor/rules/`, `HANDOFF.md`, relatórios em `docs/03-validation/audits/`, `scripts/audit.ps1`.

Diagrama textual:

```
┌──────────────────────┐
│  Browser (React)     │  UI + palco visual; fetch JSON
└──────────┬───────────┘
           │ HTTP /api/*
┌──────────▼───────────┐
│  FastAPI             │  Pydantic, erros padronizados, CORS controlado
│  use_cases → engine  │  Orquestra + persiste
│  repositories → DB   │
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│  Engine (Python puro)│  events.json + regras + score/final
└──────────────────────┘

SQLite ←── única persistência de jogo
```

Referência: [`docs/02-product/architecture.md`](../02-product/architecture.md), [`docs/02-product/game-rules.md`](../02-product/game-rules.md) §11.

---

## 5. Tecnologias usadas

**Frontend**

- React  
- Vite  
- TypeScript  
- CSS (tokens alinhados ao style-guide; ver `Referencia_front_RPG/style-guide.md`)  
- SVG (componentes TSX, placeholders geométricos na Sprint 3 — ver `Referencia_front_RPG/asset-pipeline.md`)

**Backend**

- Python 3.12  
- FastAPI  
- Pydantic  
- SQLAlchemy 2.x  
- SQLite  

**Qualidade / governança**

- pytest (backend + testes da engine)  
- `scripts/audit.ps1` (governança mínima e raiz limpa)  
- Cursor rules (`.cursor/rules/`)  
- Documentação Markdown em `docs/`  
- `HANDOFF.md` (passagem de contexto entre sessões)  
- Relatórios de aceite por sprint em `docs/03-validation/audits/`

---

## 6. Como usamos IA com governança

- **Agents operacionais:** papéis declarados no prompt (**Architect/Documentation**, **Backend**, **Frontend**, **Engine/Content**, **Auditor/QA**) com escopo de pastas e responsabilidades definidos em [`docs/01-governance/agent-usage.md`](../01-governance/agent-usage.md) e no dispatcher (`.cursor/rules/_dispatcher.mdc`).
- **Rules:** arquivos `.mdc` reforçam proibições por domínio (ex.: frontend não calcula score; engine sem ORM/Web).
- **Checkpoints:** protocolo de abertura — agente, sprint, arquivos lidos/alterados/proibidos, riscos, DoD — antes de editar código ou comportamento de produto.
- **Definition of Done:** por sprint, em [`docs/00-start/sprint-plan.md`](sprint-plan.md) e nos relatórios `sprint-*.md`.
- **Relatórios por sprint:** escopo, evidências de teste/comando, greps de governança quando aplicável, o que ficou fora de escopo.
- **Auditorias read-only:** QA documenta lacunas sem se apropriar de código de produção salvo política explícita.
- **Aceite humano:** campos nos relatórios para formalizar aprovação onde o processo exige; várias sprints ficaram **tecnicamente fechadas** com aceite humano **pendente** em papel (registros honestos nas auditorias).
- **Skills formais do Cursor:** **não foram utilizadas** neste projeto. O ficheiro `Referencia_front_RPG/SKILL.md` é **referência humana** de UX/visual, não Skill instalada no painel — alinhado ao que relatórios da Sprint 3.0 declaram.

---

## 7. Linha do tempo das sprints

| Sprint | Objetivo | Entrega | Evidência | Status |
|--------|----------|---------|-----------|--------|
| **0.1-D** | Governança navegável (`docs/00-start` … `03-validation`) | Estrutura de pastas + auditoria atualizada | Pastas, `audit.ps1` | Concluída tecnicamente ([`sprint-history.md`](../03-validation/sprint-history.md)) |
| **0.2** | Backend healthcheck | `GET /api/health` | pytest, relatório [`sprint-0.2.md`](../03-validation/audits/sprint-0.2.md) | Fechada tecnicamente |
| **0.3** | Frontend healthcheck | Vite + React + TS + UI “API: ok” | typecheck, [`sprint-0.3.md`](../03-validation/audits/sprint-0.3.md) | Fechada tecnicamente |
| **1.0** | Regras críticas + contrato da engine | `game-rules.md` §4.4/§11, **ADR-010** | [`sprint-1.0.md`](../03-validation/audits/sprint-1.0.md) | Fechada tecnicamente |
| **1.1** | Engine skeleton | `backend/engine/`, validador, `apply_choice`, testes | 44/44 pytest na época, [_sprint-1.1.md_](../03-validation/audits/sprint-1.1.md) | Fechada tecnicamente |
| **1.2** | Catálogo real 15+2 | `events.json` narrativo, playthroughs | pytest + [`sprint-1.2.md`](../03-validation/audits/sprint-1.2.md) | Fechada tecnicamente (aceite papel opcional pendente) |
| **2.0** | SQLite + modelos + repositórios | `db/`, `models/`, `repositories/` | 65/65 pytest na entrega, [`sprint-2.0.md`](../03-validation/audits/sprint-2.0.md) | Fechada tecnicamente |
| **2.1** | Player + sessão inicial | Endpoints players/sessions, CORS, Pydantic | ~97 pytest na entrega, [`sprint-2.1.md`](../03-validation/audits/sprint-2.1.md) | Fechada tecnicamente |
| **2.2** | Choice integrada à engine | `POST /choices`, persistência + ranking ao fim | 103 pytest, [`sprint-2.2.md`](../03-validation/audits/sprint-2.2.md) | Fechada tecnicamente |
| **2.2-B** | Correções QA | +4 testes API, playbook reset DB | 107 pytest, [`sprint-2.2-B.md`](../03-validation/audits/sprint-2.2-B.md) | Fechada tecnicamente |
| **2.3** | Ranking público | `GET /api/ranking` | 116 pytest, [`sprint-2.3.md`](../03-validation/audits/sprint-2.3.md) | Fechada tecnicamente |
| **3.0** | Frontend jogável visual | 4 telas, palco SVG, API real | typecheck/build/lint, greps, smoke HTTP §7.2, [`sprint-3.0.md`](../03-validation/audits/sprint-3.0.md) | Fechada tecnicamente |
| **3.0-A** | Smoke manual + bugfix painel | Documentação §11 + `AttributePanel.css` | Smoke manual **passou**, [`sprint-3.0.md`](../03-validation/audits/sprint-3.0.md) §11 | Fechada documentalmente |
| **4.0** | Dossiê final de entrega | `docs/00-start/final-delivery.md` + README/PROJECT_STATUS/HANDOFF/`sprint-history` | `audit.ps1` exit 0 após alterações documentais | Fechada documentalmente |

(Sub-sprints 0.1, 0.1-B, 0.1-C e documentais 1.1-A/B, 1.2-A continuam detalhadas em [`sprint-history.md`](../03-validation/sprint-history.md).)

---

## 8. Validações e evidências

| Validação | Registo / onde comprovar |
|-----------|---------------------------|
| **Testes backend + engine** | Cadeia documentada até **116** testes pytest na Sprint **2.3**; correções e features posteriores podem alterar o total — rerrodar `pytest` em `backend/` para número atual. Evidência histórica: [`sprint-2.3.md`](../03-validation/audits/sprint-2.3.md), [`HANDOFF.md`](../../HANDOFF.md). |
| **Typecheck / lint / build (frontend)** | Exit 0 na Sprint **3.0** e revalidado na **3.0-A**: ver saídas em [`sprint-3.0.md`](../03-validation/audits/sprint-3.0.md) §5 e §11. |
| **Smoke E2E** | §7.2 HTTP: **passou com ressalvas** (sem cliques pelo agente). **Smoke manual (browser):** **passou** — mesmo relatório, secções dedicadas. |
| **`audit.ps1`** | Exit **0** registado nos relatórios; rerrodar na raiz: `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1`. |
| **Greps de governança (frontend)** | Em [`sprint-3.0.md`](../03-validation/audits/sprint-3.0.md) §5.6: termos de engine ausentes do código executável; `consequences` / `session_id` só em comentários onde aplicável; `localStorage` centralizado. |
| **Frontend não calcula regra de jogo** | API não envia `consequences` nas opções ([`api.md`](../02-product/api.md)); tipos TS espelham isso; greps da §5.6; fluxo em `game-rules.md` §11. |

**Nota:** Este dossiê **não substitui** rerrodar comandos no ambiente do avaliador; serve como mapa das evidências já arquivadas.

---

## 9. Decisões arquiteturais importantes

1. **Engine pura** — sem FastAPI/SQLAlchemy no núcleo; testável e reutilizável; ver [`game-rules.md`](../02-product/game-rules.md) §11.1.  
2. **Frontend não recebe `consequences`** — evita “adiantar” regra no cliente e simplifica o contrato ([`api.md`](../02-product/api.md)).  
3. **Score e final** calculados pela **engine**; backend **persiste** resultado oficial, não reimplementa matemática de opção em router.  
4. **`Base.metadata.create_all` vs Alembic** — ADR-006: fallback por escopo corporativo/demo; sem migrações formais no histórico deste repo.  
5. **SVG placeholders na Sprint 3** — `asset-pipeline.md` Opção D: entregar UX jogável sem bloquear em arte final.  
6. **Mapeamento visual local** (`event_id` → cena/personas): camada de **apresentação** até eventual campo `visuals` no JSON/API; não é catálogo narrativo ([`sprint-3.0.md`](../03-validation/audits/sprint-3.0.md) §6.2, `Referencia_front_RPG/SKILL.md`).  
7. **CORS e cabeçalhos** — origens configuráveis; evolução documentada nas sprints de API (restrição de headers em entregas 2.x).  
8. **`localStorage`** — apenas `cs.sessionId` e `cs.traineeVariant` (variante visual autorizada), ver [`sprint-3.0.md`](../03-validation/audits/sprint-3.0.md).

---

## 10. Limitações conhecidas

- **Evento secreto:** fluxo completo de escolha secreta **não** implementado de ponta a ponta; `apply_secret_choice` permanece backlog (engine/UX); banner informativo na UI.  
- **Arte:** personas/cenas são **placeholders geométricos**, não ilustração final ([`asset-pipeline.md`](../../Referencia_front_RPG/asset-pipeline.md)).  
- **Autenticação:** não há login; nomes não são identidade forte.  
- **Deploy:** **não** há entrega de deploy descrita como concluída; CORS/domínios definitivos seguem como pendência em [`decisions.md`](../01-governance/decisions.md) (“Deploy intranet / domínios CORS definitivos”).  
- **Schema SQLite:** `create_all` **não** migra automaticamente bases antigas; após mudanças de modelo, pode ser necessário apagar `*.db` local (playbook em [`sprint-2.2.md`](../03-validation/audits/sprint-2.2.md) §7.2).  
- **Restart / continue refinados:** endpoints dedicados não fazem parte do escopo aceite até a última auditoria de frontend.  
- **Testes de UI automatizados:** não entregues; smoke manual + HTTP.  
- **Dossiê executivo** (`executive-overview.md`): pode estar **desatualizado** face a 2.x + 3.0 — pendência já citada em `PROJECT_STATUS` / `HANDOFF`; **este** documento consolida a narrativa de entrega na Sprint 4.0 documental.

---

## 11. Como planejamento e arquitetura pouparam erros

- **Engine antes da API jogável completa** — impôs que **router** não virasse “mini-engine”; regra de jogo ficou em um lugar testável.  
- **Catálogo JSON + validador no boot** — impede subir API com eventos inconsistentes; reduz “bug só na produção”.  
- **Repositórios só CRUD** — dificulta espalhar clamp/score/sql ad hoc na camada de banco.  
- **Auditorias read-only** — apontaram lacunas (ex.: 2.2-B) antes de rank público.  
- **Smoke E2E** — validou fluxo real (UI manual + contrato HTTP), além de testes unitários.  
- **HANDOFF + relatórios** — reduz perda de contexto ao trocar de sessão ou de modelo LLM; o “estado do mundo” fica em ficheiros versionáveis.

---

## 12. Próximos passos sugeridos

1. Polimento visual e **assets finais** (pipeline Opção B ou refinamento da D).  
2. **`apply_secret_choice`** na engine + API + UI para fechar o arco dos secretos.  
3. **Testes de UI** (Playwright / RTL) para regressão de fluxo.  
4. **Deploy** (ambiente alvo, CORS, variáveis) quando houver decisão institucional.  
5. Atualizar **`executive-overview.md`** para refletir 2.x–3.0 num único dossiê navegável (se ainda pendente).  
6. Opcional: exportar este dossiê para **PDF** ou **apresentação** para comitês que não usem o repositório.

---

*Última atualização documental: Sprint **4.0** — Dossiê Final de Entrega (Architect/Documentation + Auditor/QA).*
