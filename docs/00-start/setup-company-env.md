> **Canônico no repositório:** este arquivo é `docs/00-start/setup-company-env.md`. Atualize aqui fricções de ambiente corporativo (Node portátil, `py -3.12`, winget). Snapshot em `_context/original/corporate-survivor-setup-company-env.md`.

# Corporate Survivor — Setup no Ambiente da Empresa

Documento operacional. Quem clona o repositório executa este guia e consegue rodar o projeto. Atualizar com qualquer fricção encontrada no ambiente real.

---

## 0. Status de execução

### Já validado neste ambiente

- Python 3.12 via `py -3.12`.
- Criação de venv e uso de pip.
- Node.js 20 e npm 10 por instalação portátil.
- Git funcional.
- SQLite disponível via biblioteca Python.
- Instalação npm controlada em pasta temporária.

### Referência futura

As seções de backend, frontend, engine, migrations, testes e reset de banco descrevem o alvo das próximas sprints. Não execute esses passos antes da sprint correspondente criar as pastas e arquivos citados.

### Bloqueios e TI

Node portátil está aceito enquanto não travar execução, onboarding ou atualização. Não abrir chamado de TI agora. Reabrir apenas se alguma tecnologia bloquear a Sprint 0 executável ou uma dependência obrigatória.

### Auditoria no Windows

No ambiente atual, use PowerShell como caminho principal:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/audit.ps1
```

`scripts/audit.sh` existe para Git Bash/WSL e deve espelhar os checks mínimos.

---

## 1. Pré-requisitos de sistema

| Ferramenta | Versão recomendada | Mínima aceita | Como verificar |
|---|---|---|---|
| Python | 3.11.x ou 3.12.x | 3.10 | `python --version` ou `python3 --version` |
| Node.js | 20.x LTS | 18.x | `node --version` |
| npm | 10.x | 9.x | `npm --version` |
| Git | qualquer recente | — | `git --version` |
| SQLite CLI (opcional) | 3.x | — | `sqlite3 --version` |

**Por que essas versões:**
- Python 3.11+: Pydantic v2 e SQLAlchemy 2.0 funcionam plenamente; sintaxe `match/case` disponível; melhores erros.
- Node 20 LTS: Vite 5.x recomenda; estabilidade até 2026.
- SQLite CLI é opcional, útil para inspecionar `corporate_survivor.db` manualmente.

**No ambiente da empresa, antes de tudo:**
```bash
python --version
python3 --version
node --version
npm --version
```

Anote o que encontrou. Se faltar algo ou versão estiver fora do range:
- Python: pedir TI para instalar 3.11+; alternativa pessoal segura é `pyenv` (se permitido).
- Node: pedir TI para 20 LTS; alternativa é `nvm` (se permitido).
- Se houver bloqueio corporativo de instalação, registrar em ADR e adaptar versões.

---

## 2. Estrutura do repositório (referência futura após Sprint 0)

```
corporate-survivor/
  README.md
  HANDOFF.md
  .gitignore
  .env.example
  scripts/
    audit.sh
    reset_db.sh
    seed.py
  .cursor/
    rules/
      _dispatcher.mdc
      frontend.mdc
      backend.mdc
      game-engine.mdc
      events-json.mdc
      tests.mdc
      docs-sync.mdc
  docs/
    architecture.md
    api.md
    game-rules.md
    decisions.md
    sprint-plan.md
    cursor-workflow.md
    setup-company-env.md
    audits/
    playthroughs/
  backend/
    pyproject.toml
    .python-version
    app.py
    routers/
    use_cases/
    schemas/
    db/
      models.py
      session.py
      repositories.py
    engine/
      __init__.py
      state.py
      events.py
      choices.py
      selection.py
      scoring.py
      endings.py
      validate_events.py
      data/
        events.json
    migrations/        # se Alembic ativo
    tests/
    data/               # SQLite runtime — fora do git
      .gitkeep
  frontend/
    package.json
    vite.config.ts
    tsconfig.json
    tailwind.config.js
    postcss.config.js
    index.html
    src/
      main.tsx
      App.tsx
      pages/
      components/
      hooks/
      services/
      types/
    public/
```

---

## 3. Clonagem inicial

```bash
# 1. Clonar
git clone <url-do-repo>
cd corporate-survivor

# 2. Copiar template de variáveis de ambiente
cp .env.example .env

# 3. Conferir conteúdo de .env (não commitar este arquivo)
cat .env
```

`.env.example` deve conter (sem valores sensíveis reais):

```env
# Backend
DATABASE_URL=sqlite:///./data/corporate_survivor.db
APP_ENV=development
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173

# Frontend
VITE_API_BASE_URL=http://localhost:8000/api
```

Para desenvolvimento local não há segredos. Para deploy interno, valores reais ficam em `.env` local + secrets management.

---

## 4. Setup do backend (referência futura)

Não executar antes da Sprint 0 criar o backend mínimo.

### 4.1 Criar e ativar venv

```bash
cd backend

# Criar venv com Python 3.11+
python3 -m venv .venv

# Ativar (Linux/macOS)
source .venv/bin/activate

# Ativar (Windows PowerShell)
# .venv\Scripts\Activate.ps1

# Confirmar
which python
python --version
```

**Se Python 3.11+ não estiver disponível como `python3`:**
```bash
# Ex: tentar python3.11 explicitamente
python3.11 -m venv .venv
```

**Se o ambiente da empresa bloqueia venv:** abrir ticket com TI. Última saída é usar Docker/devcontainer, mas isso é fora do escopo padrão e exige ADR-008.

### 4.2 Instalar dependências

```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar projeto + dependências (pyproject.toml)
pip install -e ".[dev]"
```

O `pyproject.toml` deve declarar (mínimo viável):

```toml
[project]
name = "corporate-survivor-backend"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "fastapi>=0.110",
  "uvicorn[standard]>=0.27",
  "sqlalchemy>=2.0",
  "pydantic>=2.6",
  "pydantic-settings>=2.0",
  "python-dotenv>=1.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "pytest-cov>=4.0",
  "httpx>=0.27",
  "ruff>=0.3",
  "mypy>=1.8",
  "alembic>=1.13",  # opcional — pode ser removido se ADR-006 ativada
]
```

**Se houver problema com algum pacote no proxy/registry da empresa:**
- Conferir se há proxy npm/pip interno: `pip config list`, `npm config list`.
- Se sim, configurar:
  ```bash
  pip config set global.index-url https://<proxy-interno>/simple
  ```
- Pedir TI o endereço do mirror oficial da empresa.

### 4.3 Inicializar o banco

**Caminho A — com Alembic (preferido):**

```bash
# A partir de backend/
alembic upgrade head
```

Se a primeira migration não existe ainda (Sprint 0):
```bash
alembic init migrations
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

**Caminho B — sem Alembic (fallback, ADR-006):**

Nada a fazer. O `app.py` chama `Base.metadata.create_all(engine)` no startup.

### 4.4 Validar `events.json`

```bash
python -m engine.validate_events
```

Saída esperada: `OK — 15 main events, N secret events validated.`

Se falhar: o boot do FastAPI **vai falhar**. Corrigir antes de seguir.

### 4.5 Rodar backend

```bash
# A partir de backend/
uvicorn app:app --reload --port 8000
```

Conferir:
```bash
# Em outro terminal
curl http://localhost:8000/api/health
# Esperado: {"status":"ok"}
```

### 4.6 Rodar testes backend

```bash
# A partir de backend/, com venv ativo
pytest -q

# Com coverage
pytest --cov=. --cov-report=term-missing

# Apenas engine
pytest tests/engine -q

# Apenas API
pytest tests/api -q
```

---

## 5. Setup do frontend (referência futura)

Não executar antes da Sprint 0 criar o frontend mínimo.

### 5.1 Instalar dependências

```bash
cd frontend
npm install
```

O `package.json` mínimo:

```json
{
  "name": "corporate-survivor-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "eslint src --ext ts,tsx",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0",
    "@tanstack/react-query": "^5.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "typescript": "^5.3.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "vitest": "^1.4.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.4.0",
    "jsdom": "^24.0.0",
    "eslint": "^8.57.0"
  }
}
```

**Se `npm install` falha por proxy:**
```bash
npm config get registry
npm config set registry https://<registry-interno>/
```

Pedir TI o endereço do registry interno.

### 5.2 Rodar frontend

```bash
# A partir de frontend/
npm run dev
```

Conferir: abrir `http://localhost:5173`. Deve aparecer a tela inicial com indicador "API: ok".

### 5.3 Rodar testes frontend

```bash
npm test          # modo watch
npm test -- --run # uma rodada
npm run typecheck
npm run lint
```

---

## 6. Onde fica o SQLite

Arquivo: `backend/data/corporate_survivor.db`

Pasta `backend/data/` é criada automaticamente no primeiro boot. Está no `.gitignore` (arquivo `.db` não vai pro repo).

Para inspecionar manualmente:
```bash
sqlite3 backend/data/corporate_survivor.db
> .tables
> SELECT * FROM players;
> .quit
```

---

## 7. Como resetar o banco

```bash
# Script de conveniência
bash scripts/reset_db.sh
```

Conteúdo do `scripts/reset_db.sh`:

```bash
#!/usr/bin/env bash
set -e
DB_PATH="backend/data/corporate_survivor.db"

read -p "Apagar $DB_PATH? [y/N] " confirm
if [[ "$confirm" != "y" ]]; then
  echo "Cancelado."
  exit 0
fi

rm -f "$DB_PATH"
echo "Banco apagado. Reinicie o backend para recriar via migrations (ou create_all)."
```

---

## 8. Comandos do dia a dia

| Tarefa | Comando |
|---|---|
| Subir backend | `cd backend && source .venv/bin/activate && uvicorn app:app --reload` |
| Subir frontend | `cd frontend && npm run dev` |
| Rodar testes back | `cd backend && pytest -q` |
| Rodar testes front | `cd frontend && npm test -- --run` |
| Rodar auditoria no Windows | `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` |
| Rodar auditoria no Git Bash/WSL | `bash scripts/audit.sh` |
| Resetar banco | `bash scripts/reset_db.sh` |
| Validar events.json | `cd backend && python -m engine.validate_events` |
| Criar migration | `cd backend && alembic revision --autogenerate -m "msg"` |
| Aplicar migrations | `cd backend && alembic upgrade head` |
| Lint backend | `cd backend && ruff check . && mypy .` |
| Lint frontend | `cd frontend && npm run lint && npm run typecheck` |

---

## 9. Problemas comuns e como resolver

### 9.1 `python: command not found`

Em alguns ambientes só há `python3`. Use sempre `python3` ou crie alias.

### 9.2 `permission denied` ao instalar pacotes

Você não está dentro do venv. Verifique com `which python` — deve apontar para `.venv/bin/python`. Ativar venv: `source .venv/bin/activate`.

### 9.3 `pip install` lento ou falhando

Possível bloqueio de rede corporativo. Verificar:
```bash
pip config list
curl -I https://pypi.org
```

Se PyPI não responde: solicitar configuração de mirror interno à TI.

### 9.4 `EACCES` no `npm install`

Não rode `npm install` com `sudo`. Configurar prefix para diretório do usuário se necessário:
```bash
npm config set prefix ~/.npm-global
export PATH=~/.npm-global/bin:$PATH
```

### 9.5 Frontend não conecta ao backend (CORS)

Conferir:
- Backend rodando em `http://localhost:8000`?
- `.env` do frontend tem `VITE_API_BASE_URL=http://localhost:8000/api`?
- CORS no backend permite `http://localhost:5173`?

Logs do navegador (F12) e do uvicorn ajudam.

### 9.6 `ImportError: cannot import name 'X' from 'pydantic'`

Versão errada de Pydantic. Confirmar:
```bash
pip show pydantic
```
Precisa ser >= 2.6. Se for v1, está usando ambiente antigo. Recriar venv:
```bash
deactivate
rm -rf backend/.venv
cd backend && python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
```

### 9.7 SQLite `database is locked`

Concorrência em SQLite. Para um app de desenvolvimento single-user, raríssimo. Se acontecer:
- Garantir que apenas uma instância do uvicorn está rodando.
- Não abrir o `.db` em um cliente externo em modo escrita enquanto o app roda.

### 9.8 `events.json` falha validação no boot

Ler o output do validador. Erros comuns:
- ID referenciado em `unlocks`/`blocks` não existe.
- Faltam eventos para um dia (precisa 3).
- Soma de deltas de uma opção > 7.

Corrigir o JSON, rodar `python -m engine.validate_events`, e só então subir o backend.

### 9.9 Cursor não carrega as rules

- Conferir que arquivos `.mdc` estão em `.cursor/rules/` (pasta `.cursor` no diretório raiz do workspace aberto no Cursor).
- Frontmatter precisa estar válido (entre `---`).
- Reiniciar a janela do Cursor após editar rules.

### 9.10 Bloqueio total de instalação (TI corporativa restritiva)

Última saída: solicitar VM/devcontainer com tudo pré-instalado. Registrar em ADR-008 e adaptar `setup-company-env.md` para o ambiente alternativo.

---

## 10. Definition of Done do Sprint 0 (referência futura)

Antes de declarar Sprint 0 concluído, executar **neste exato ambiente** (ambiente da empresa). Esta seção não deve ser executada na Sprint 0.1-B porque backend/frontend ainda não existem:

```bash
# Do zero, como se fosse um novo membro do time:
git clone <url>
cd corporate-survivor

# 2. Backend
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head   # ou nada se ADR-006
python -m engine.validate_events
uvicorn app:app --port 8000 &
sleep 3
curl -s http://localhost:8000/api/health | grep -q "ok"

# 3. Frontend
cd ../frontend
npm install
npm run typecheck
npm run dev &
sleep 5
curl -s http://localhost:5173 | grep -q "Corporate Survivor"

# 4. Audit
cd ..
powershell -ExecutionPolicy Bypass -File scripts/audit.ps1

# Se todas as etapas passam, Sprint 0 está fechado.
```

Se algum passo falhar no ambiente real: corrigir este documento E o código antes de seguir para Sprint 1.

---

## 11. Atualizações deste documento

Este doc é mantido pelo Agent Architect/Documentation. Toda fricção nova encontrada por qualquer agente vira entrada na seção 9.
