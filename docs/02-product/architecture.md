# Arquitetura — Corporate Survivor

Documento vivo: atualizar quando código existir e decisões forem registradas em `docs/01-governance/decisions.md`.

## Visão em camadas

| Camada | Responsabilidade | Tecnologia alvo |
|--------|-------------------|-----------------|
| **Cliente web** | UI fina, roteamento, consumo da API, estados visuais | Vite + React 18 + TypeScript + Tailwind + TanStack Query |
| **API HTTP** | Rotas HTTP finas, validação de entrada; **sem** regra de jogo inline | FastAPI + Pydantic v2 |
| **Casos de uso / orquestração** | Fluxos transacionais (sessão, escolhas, ranking) | Python (serviço da API) |
| **Persistência** | Modelos e repositórios — única camada que toca SQLite | SQLAlchemy 2.0 |
| **Engine** | Estado imutável, validação de `events.json`, seleção de eventos, score, finais — **sem** FastAPI/SQLAlchemy | Python puro em `backend/engine/` |

## Fonte da verdade

- Estado oficial da sessão, atributos, histórico de escolhas, score persistido e finais vêm **do backend**.  
- O frontend **não** calcula score oficial nem resolve final.

## Persistência

- **SQLite** via arquivo (`DATABASE_URL` em `.env.example`).  
- Migrations: tentar **Alembic** na Sprint 0 executável; fallback **`create_all()`** no startup + ADR-006 se ambiente corporativo bloquear.

## Segurança mínima (alvo)

Resumo — detalhar na implementação conforme `corporate-survivor-plano-v2.md`:

- Inputs validados com Pydantic; nome com regex e limite de tamanho.  
- Escolhas validadas contra estado atual (`409` quando inconsistente).  
- Corpo não aceita `attributes`, `score`, `ending` arbitrários do cliente.  
- Erros 500 com payload genérico + logs sem stack trace exposto.

## Pacotes esperados no repo (futuro)

```
backend/      # FastAPI app, routers finos, use cases, db/, engine/
frontend/     # Vite React app
scripts/      # audit.sh, reset_db.sh, ...
docs/         # especificações e ADRs
```

Esta Sprint **0.1** não inclui essas pastas de código até as sprints seguintes.
