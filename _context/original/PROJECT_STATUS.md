# Corporate Survivor — Status do projeto

**Última atualização:** 2026-05-14  
**Agente responsável por este artefato:** Architect / Documentation  
**Etapa:** Sprint 0.0 — baseline de contexto **+ Sprint 0.1 — estrutura de governança criada**  

Este arquivo registra o **estado atual** do workspace. Após a Sprint **0.1**, existe árvore `docs/`, `.cursor/rules/` e `scripts/` conforme plano — mas **sem** código `backend/`/`frontend/` ainda. Atualizar quando o executável existir.

---

## 1. Estado atual do projeto

- **Código:** não há aplicação Corporate Survivor implementada neste workspace (sem `backend/`, sem `frontend/`, sem engine em código).
- **Documentação:** existe **`docs/`** com arquivos canônicos (`game-rules.md`, `setup-company-env.md`, etc.), índice em **`docs/project-structure.md`** e snapshots em **`_context/original/`**. Os Markdown grandes na raiz (`corporate-survivor-*.md`) permanecem como legado até decisão de remoção — **preferir editar `docs/`**.
- **Governança Cursor:** `.cursor/rules/` criado (**dispatcher + agentes**) na Sprint 0.1.
- **Ambiente da empresa:** ferramentas necessárias **validadas em uso controlado** (Node 20 + npm 10, Python 3.12 via launcher, Git, pip em venv, sqlite3 via biblioteca Python). Detalhes na seção 4.
- **Alinhamento com desafio:** requisitos principais estão cobertos nos documentos base (semana corporativa em torno de decisões, progressão 5×3 eventos principais, impacto em estado futuro via condicionais e secretos, ranking/score no desenho — ver plano + game rules).

---

## 2. Resumo do desafio

**Corporate Survivor** é uma narrativa interativa “trainee na primeira semana” em tom corporativo brasileiro realista: escolhas com trade-offs, sem vilão óbvio. O jogador percorre **5 dias úteis** com **exatamente 3 eventos principais por dia** (15 principais no catálogo), mais **eventos secretos opcionais** injetados quando condições são atendidas.

- **Estado:** seis atributos inteiros 0–10 (energia, reputação, networking, ansiedade, produtividade, aprendizado), com valores iniciais definidos em `corporate-survivor-game-rules.md`.
- **Conteúdo:** catálogo em `events.json` (schema `1.0`), com validação obrigatória no boot da API (`validate_events`).
- **Finais:** sete finais previstos, resolvidos **sempre ao fim do dia 5** (sem encerramento antecipado por atributo zerado — decisão registrável como ADR-007 no plano).
- **Backend como fonte da verdade:** frontend fino; sem cálculo oficial de score/final/consequências na UI.
- **Persistência:** SQLite via SQLAlchemy 2.0; estado de sessão, decisões e ranking persistidos.

---

## 3. Documentos base disponíveis

| Arquivo | Função |
|---------|--------|
| `corporate-survivor-plano-v2.md` | Plano revisado: stack, cinco agentes, dispatcher/rules, Sprint 0 DoD, UX por tela, segurança mínima, riscos R13–R17. |
| `corporate-survivor-game-rules.md` | Regras do jogo e catálogo narrativo/schema: atributos, `events.json`, progressão, secretos, finais, score, invariantes de validação. |
| `corporate-survivor-setup-company-env.md` | Guia operacional de ambiente corporativo (versões, estrutura esperada do repo pós-Sprint 0, comandos típicos, troubleshooting). |

**Observação:** no futuro repo “oficial”, o conteúdo relevante deve convergir para `docs/` + README/HANDOFF conforme o plano; **este arquivo não substitui** `HANDOFF.md` nem ADRs formais quando existirem.

---

## 4. Tecnologias validadas no ambiente da empresa

Condições verificadas por **preflight / instalação controlada / revalidação** (sem depender de SQLite CLI):

| Área | Estado |
|------|--------|
| **Node.js** | **v20.20.2** — instalado de forma **portátil** em `%LOCALAPPDATA%\CorporateSurvivorTools\node-v20\node-v20.20.2-win-x64\`; PATH do usuário ajustado para preceder o helper do Cursor. |
| **npm** | **v10.8.2** — funcional; `npm ping` ao registry público OK na validação. |
| **Python** | **3.12.10** disponível via **`py -3.12`** (alinha à faixa recomendada 3.11/3.12 do setup). O launcher pode manter **3.14** como default (`py -0p`); o projeto deve documentar uso explícito de **3.12** para backend/venv. |
| **venv** | Funcional (`py -3.12 -m venv`). |
| **pip** | Funcional dentro do venv; upgrade de pip testado em pasta temporária de validação. |
| **Git** | Funcional (versão observada nas sessões de setup). |
| **SQLite** | Disponível via **`sqlite3` embutido no Python** (versão da biblioteca conferida nos testes); **CLI opcional**, não bloqueante. |
| **Vite / npm install** | `npm install vite --save-dev` executado com sucesso em pasta temporária de teste (detalhe: `npm init -y` pode falhar se o nome da pasta começa com `.`; usar nome pacote válido ou `npm pkg set name=...`). |

**Instalação Node via winget:** tentativa `winget install OpenJS.NodeJS.20 --scope user` falhou com **acesso negado** ao copiar para `...\Microsoft\WinGet\Packages\`. **Chamado à TI não está aberto por decisão atual**; reabrir apenas se o método portátil impedir padronização, atualização ou políticas futuras.

---

## 5. Decisões já tomadas

- **Stack (plano v2):** FastAPI + Pydantic v2 + SQLAlchemy 2.0 + SQLite; engine Python pura em `backend/engine/`; frontend Vite + React 18 + TypeScript + Tailwind + React Query; testes pytest/httpx e Vitest/Testing Library.
- **Migrations:** tentar Alembic no Sprint 0; se houver fricção corporativa, fallback `create_all()` no startup com **ADR-006**.
- **Progressão:** 5 dias × 3 eventos principais fixos; secretos opcionais com regras de elegibilidade determinísticas (menor `id` lexicográfico em empate).
- **Finais:** sempre ao fim do dia 5; sem “game over” mecânico no meio da semana (**ADR-007** no plano).
- **Governança de agentes:** cinco papéis consolidados + dispatcher `_dispatcher.mdc` + validação por diff e **HANDOFF.md** (quando o repo existir).
- **Ambiente notebook:** Python **3.12** como linha base para backend; Node **20 LTS** via layout portátil aprovado na prática até nova decisão corporativa.

---

## 6. Pendências importantes

- **Scaffold Sprint 0:** ✅ Sprint **0.1** — estrutura `docs/`, `.cursor/rules/`, `scripts/`, `_context/original/`, `README.md`, `HANDOFF.md`, `.gitignore`, `.env.example` criados.
- **Rules Cursor:** ✅ Pacote `.mdc` conforme plano v2.
- **`docs/setup-company-env.md`:** ✅ Canônico em `docs/` (snapshot também em `_context/original/`).
- **ADR iniciais:** rascunhos em `docs/decisions.md` — revisar números/status quando código estabilizar.
- **Primeira API e contrato:** definir/implementar `GET /api/health` e documentar evolução em `docs/api.md` quando Backend entrar (fora do escopo desta baseline).

---

## 7. Riscos conhecidos

| Risco | Impacto | Mitigação planejada |
|-------|---------|---------------------|
| **Node portátil** não padronizado pela TI | Atualização e suporte dependem do usuário/pasta PATH | Documentar caminho e procedimento em `setup-company-env.md`; revisitar winget/TI se travar CI ou onboarding de terceiros |
| **`py` default ≠ 3.12** | Builds/scripts podem usar Python errado por engano | Padronizar em README/scripts `py -3.12` e `.python-version` quando repo existir |
| **Versões npm/Vite** em testes isolados ≠ pinadas no projeto | Pequeno drift até `package.json` oficial | Ao criar frontend, fixar versões alinhadas ao plano (Vite 5.x etc.) |
| **Alembic vs política corporativa** | Atraso na Sprint 0 | Fallback `create_all` + ADR-006 |
| **LLM violando dispatcher / domínios** | Mistura Engine/API/UI | Rules + auditoria por diff + intervenção humana (plano v2) |

---

## 8. Próxima sprint planejada

**Sprint 0 — foundation executável:** backend + frontend mínimos (`GET /api/health`, tela “API: ok”), seguindo `docs/setup-company-env.md`, DoD completo em `docs/sprint-plan.md`.

**Nota:** Sprint **0.1** (estrutura docs/rules/scripts) foi concluída para governança antes do código.

---

## 9. O que NÃO deve ser feito ainda

- Não criar **backend** FastAPI completo nem routers com regra de jogo.
- Não criar **frontend** React/Vite do produto nem fluxos de jogo.
- Não criar **engine** executável nem `events.json` definitivo em árvore de produto até a Agent Engine/Content assumir com validação.
- **`.cursor/rules/`** já existe após Sprint **0.1** — não improvisar novas rules sem revisão Architect / Documentation.
- Não expandir escopo para **CI/CD obrigatório** (é bônus no plano v2).
- Não alterar os três Markdown raiz **`corporate-survivor-plano-v2.md`**, **`corporate-survivor-game-rules.md`**, **`corporate-survivor-setup-company-env.md`** nesta baseline sem decisão explícita — a sincronização futura deve ir para `docs/`.

---

## 10. Critério para avançar para Sprint 0 (executável)

Avançar quando **todas** forem verdadeiras:

1. **Governança aceita pelo humano:** estrutura Sprint **0.1** revisada (`docs/project-structure.md`, rules `.mdc`, HANDOFF habituais).
2. **Ambiente:** Python **3.12** + Node **20** + npm **10** repetíveis conforme `docs/setup-company-env.md`.
3. **Escopo Sprint 0 fechado:** backend + frontend mínimos + health check acordados (ver DoD em `docs/sprint-plan.md`).
4. **Sem bloqueadores de toolchain:** qualquer novo bloqueio corporativo registrado em `docs/setup-company-env.md` + `docs/decisions.md` antes de codificar dependências sensíveis.

Com isso, **Agent Backend**, **Agent Frontend** e **Agent Setup** (ambiente) podem iniciar o código executável mantendo domínios separados entre sessões.
