# Corporate Survivor — Status Executivo

**Última atualização:** 2026-05-14 — Agent **Backend** (Sprint **2.3**).  
**Sprint técnica mais recente:** **2.3 — Ranking API + smoke tests** (aceite papel §10 pendente). Sprints anteriores: 2.0 (persistência) ✅; 2.1 (Player+Sessão) técnica fechada; 2.2 (Choices+engine) técnica fechada; 2.2-B (correções QA) técnica fechada.  
**Gestores:** continuam usando [`docs/00-start/executive-overview.md`](docs/00-start/executive-overview.md) — esse doc de status é operacional rápido; dossiê ainda atrás da linha **2.x** (Architect).

## Estado agora

- API joga turnos persistidos (`POST /api/sessions/{id}/choices`), encerra sessão quando engine devolve ending, calcula ranking via valores engine-only, grava `RankingEntry`.
- **Leaderboard público:** `GET /api/ranking?limit=10` (Sprint 2.3) — envelope `{items, limit, count}`, ordenado por score desc + tie-break determinístico, `session_id` ocultado, bounds `1..100` no `limit` (422 fora).
- Persistência SQLite com coluna `secrets_seen_json` em `game_sessions` (mirror de `secret_ids_seen` até existir segunda etapa secreta oficial).
- CORS: origens whitelist via env (`CORS_ORIGINS`); apenas cabeçalhos `Content-Type`/`Accept` no preflight para reduzir superfície (mantido intacto na 2.3 — apenas `include_router(ranking_router)` foi adicionado em `app.py`).
- Frontend ainda apenas health minimal — **sem** UX jogo nesta linha 2.x.
- `events.json` + engine **intocados**.
- QA automático: **`116` testes pytest** backend+engine (`cd backend`) — 107 da linha 2.2-B + 9 novos da Sprint 2.3 (vazio, ordenação, default limit, custom limit, sem leak `session_id`, 3× bounds 422, smoke fim-a-fim que joga até `demitido` e verifica entrada no ranking); `scripts/audit.ps1` **OK**.
- **Playbook dev local pós-2.2 (operacional, segue válido):** se houver `backend/data/*.db` criado em sprint anterior à 2.2, **apagar antes de subir o backend** — `Base.metadata.create_all()` (ADR-006) não adiciona colunas novas em tabelas existentes. Detalhes em `docs/03-validation/audits/sprint-2.2.md §7.2`.

## Próximo passo

1. Formalizar aceite papel das Sprints **2.1 (§11)**, **2.2 (§8)**, **2.2-B (§10)** e **2.3 (§10)** — as quatro têm aceite humano formal pendente (podem ser aceitas em conjunto).
2. Architect fecha `executive-overview.md` cobrindo 2.0/2.1/2.2/2.2-B/2.3.
3. **Backlog engine/UX:** `apply_secret_choice` (segunda etapa do fluxo secreto) e Sprint 3 (UX completa do frontend).

## Ligaduras

[`HANDOFF.md`](HANDOFF.md) · [`docs/03-validation/sprint-history.md`](docs/03-validation/sprint-history.md) · [`docs/03-validation/audits/sprint-2.3.md`](docs/03-validation/audits/sprint-2.3.md) · [`docs/03-validation/audits/sprint-2.2.md`](docs/03-validation/audits/sprint-2.2.md) · [`docs/03-validation/audits/sprint-2.2-B.md`](docs/03-validation/audits/sprint-2.2-B.md) · [`docs/02-product/api.md`](docs/02-product/api.md)
