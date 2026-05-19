# Corporate Survivor

RPG narrativo corporativo em primeira pessoa. O jogador é um trainee na primeira semana de empresa, toma decisões em situações realistas de escritório e acompanha como cada escolha altera atributos como energia, reputação, networking, ansiedade, produtividade e aprendizado.

O projeto também demonstra governança de IA aplicada ao desenvolvimento: cada domínio tem agente, regras, documentação de referência, handoff e evidências de validação.

## Estado atual

Entrega funcional e documentada:

- Frontend jogável em React + Vite + TypeScript.
- Backend FastAPI com API de jogadores, sessões, escolhas, ranking e perfil/histórico do jogador.
- Engine em Python puro, desacoplada de HTTP, banco e interface.
- Persistência SQLite via SQLAlchemy.
- Catálogo narrativo versionado em `backend/engine/data/events.json`.
- Documentação de arquitetura, API, regras de jogo, sprints, auditorias e decisões em `docs/`.

Resumo executivo consolidado: [`docs/00-start/final-delivery.md`](docs/00-start/final-delivery.md).

## Como rodar no Windows

Opção rápida:

```powershell
.\Abrir-Jogo.bat
```

O script abre backend e frontend em janelas separadas e carrega o jogo no navegador.

Opção via PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/dev-jogo.ps1
```

O frontend roda em `http://localhost:5173` e o backend em `http://localhost:8000`.

## Rodar manualmente

Backend:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -e ".[dev]"
uvicorn app:app --reload --port 8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Healthcheck:

```powershell
Invoke-RestMethod http://localhost:8000/api/health
```

## Arquitetura

O backend é a fonte da verdade para estado, escolhas, score e final. O frontend é thin client: renderiza o estado recebido da API e envia a escolha do jogador, sem calcular consequências oficiais.

Camadas principais:

- `frontend/`: interface jogável, páginas, componentes visuais, consumo da API.
- `backend/routers/`: endpoints FastAPI finos.
- `backend/use_cases/`: orquestração de fluxo e transações.
- `backend/repositories/`: única camada que acessa o banco.
- `backend/engine/`: regras de jogo, validação do catálogo, score e finais.
- `docs/`: fonte de referência para arquitetura, produto, governança e validação.

## Documentação de referência

| Tema | Documento |
|---|---|
| Entrega final / avaliação | [`docs/00-start/final-delivery.md`](docs/00-start/final-delivery.md) |
| Status executivo atual | [`PROJECT_STATUS.md`](PROJECT_STATUS.md) |
| Histórico de sprints | [`docs/03-validation/sprint-history.md`](docs/03-validation/sprint-history.md) |
| Último handoff | [`HANDOFF.md`](HANDOFF.md) |
| Arquitetura técnica | [`docs/02-product/architecture.md`](docs/02-product/architecture.md) |
| API HTTP | [`docs/02-product/api.md`](docs/02-product/api.md) |
| Regras do jogo | [`docs/02-product/game-rules.md`](docs/02-product/game-rules.md) |
| Decisões arquiteturais | [`docs/01-governance/decisions.md`](docs/01-governance/decisions.md) |
| Governança de agentes | [`docs/01-governance/agent-usage.md`](docs/01-governance/agent-usage.md) |
| Fluxo Cursor / handoff | [`docs/01-governance/cursor-workflow.md`](docs/01-governance/cursor-workflow.md) |
| Relatórios de aceite | [`docs/03-validation/audits/`](docs/03-validation/audits/) |
| Referências visuais | [`Referencia_front_RPG/`](Referencia_front_RPG/) |

## Governança de IA

Antes de qualquer alteração, a LLM deve declarar:

- agente ativo;
- sprint ou etapa ativa;
- documentos e rules consultados;
- arquivos que pretende alterar;
- arquivos que não deve tocar;
- riscos de violar arquitetura.

Regras centrais:

- Frontend não calcula score, final ou consequências oficiais.
- Engine não importa FastAPI, SQLAlchemy ou frontend.
- Routers são finos; use cases orquestram; repositories acessam banco.
- Mudança de API atualiza `docs/02-product/api.md`.
- Mudança de regra de jogo atualiza `docs/02-product/game-rules.md`.
- Toda sessão com alteração registra fechamento em `HANDOFF.md`.

## Validação

Auditoria principal no Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/audit.ps1
```

Testes e validações completos por sprint ficam em [`docs/03-validation/audits/`](docs/03-validation/audits/).

## Próximos passos

O produto está em fase de validação final / entrega. Evoluções futuras previstas incluem polimento visual, testes automatizados de UI, paginação do ranking, URL bookmarkable e fluxo completo de evento secreto (`apply_secret_choice`).
