# Sprint 0.3 — Frontend Healthcheck mínimo — Relatório de aceite

## 1. Resumo executivo

- Objetivo da sprint: validar Vite + React + TypeScript no ambiente da empresa e consumir `GET /api/health` a partir da UI mínima.
- Resultado: **FECHADA tecnicamente**, pendente de aceite humano formal.
- Decisão recomendada: aceitar a Sprint 0.3 após revisão; CORS para chamada absoluta do browser permanece para sprint futura (ver plano API, Sprint 2 em `docs/00-start/sprint-plan.md`).

## 2. Escopo aprovado

- `frontend/` com Vite + React + TypeScript.
- Tela inicial com título `Corporate Survivor`.
- Exibição de status da API (`API: ok` quando o healthcheck retorna `{"status":"ok"}`).
- Scripts mínimos, incluindo `npm run typecheck`.
- Integração de desenvolvimento via proxy do Vite (`/api` → `http://localhost:8000`), sem alterar o backend.
- Atualizações documentais mínimas correlatas (README, PROJECT_STATUS, `project-structure`, sprint-plan parcial, HANDOFF antes do fechamento 0.3-A).

## 3. Fora de escopo

- Engine, `events.json`, jogo, fluxo de jogador, ranking, sessões, score, finais.
- Hardcode de catálogo de eventos na interface.
- Alteração do backend (incluindo CORS).
- Sprint 1.

## 4. Agent / Rules / Skills

- Agent usado: Agent Frontend.
- Rules consultadas: `.cursor/rules/_dispatcher.mdc`, `.cursor/rules/frontend.mdc`; conteúdo em `docs/` conforme checkpoint da sprint.
- Skills formais do Cursor: **não utilizadas / não existentes** neste projeto no momento do relatório.
- Como Agent/Rules ajudaram: limites de domínio (frontend only); `frontend.mdc` reforça thin client e proibição de regra de jogo no cliente.

## 5. Evidências técnicas

- `npm install` em `frontend/` — concluído sem vulnerabilidades reportadas.
- `npm run typecheck` — passou.
- `npm run dev -- --host 127.0.0.1 --port 5173` — Vite em `http://127.0.0.1:5173/`.
- UI: título `Corporate Survivor`; estado `API: ok` após healthcheck bem-sucedido.
- `curl` (ou equivalente) em `http://localhost:8000/api/health` → `200`, `{"status":"ok"}`.
- `curl` (ou equivalente) em `http://127.0.0.1:5173/api/health` → `200`, `{"status":"ok"}` via proxy do Vite.
- `powershell -ExecutionPolicy Bypass -File scripts/audit.ps1` — passou (`OK - governanca minima presente e raiz limpa.`).

## 6. Limitações conhecidas

- **Porta 8000:** uma instância do backend já pode estar em uso; subir segunda instância falha por porta ocupada — não impede validação se o healthcheck já responde.
- **CORS:** o backend da Sprint 0.2 não expõe cabeçalhos CORS para `fetch` absoluto do browser para `http://localhost:8000`; a Sprint 0.3 validou integração no dev via **proxy do Vite**. Tratamento de CORS real: sprint futura (alinhado a `docs/02-product/api.md` e plano).

## 7. Validação documental

- `docs/02-product/api.md` continua consistente: healthcheck implementado; CORS descrito como alvo para dev.
- Relatório desta sprint: este arquivo.
- Histórico consolidado: `docs/03-validation/sprint-history.md`.

## 8. Critério de aceite aplicado

- [x] Agent declarado.
- [x] Sprint declarada.
- [x] Escopo respeitado (sem backend/engine/jogo).
- [x] Frontend sobe e exibe título + `API: ok`.
- [x] Healthcheck validado direto no backend e via proxy no dev.
- [x] `typecheck` passou.
- [x] `audit.ps1` passou na sprint de implementação.
- [x] Skills formais não declaradas falsamente.

## 9. Pendências

- Aceite humano desta sprint (campo abaixo).
- CORS no backend quando a sprint de robustez API liberar alteração de backend.
- Decisão sobre final antecipado antes da Sprint 1 (`PROJECT_STATUS.md` / ADRs).
- Item opcional do DoD Sprint 0: `bash scripts/audit.sh` quando Git Bash/WSL disponível (`docs/00-start/sprint-plan.md`).

## 10. Decisão de aceite humano

- Aceite humano: **pendente**.
- Observações do aceite: registrar aqui após revisão.
