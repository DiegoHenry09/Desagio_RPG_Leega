# API HTTP — Corporate Survivor

**Estado:** Sprint 2.1 (Player + Sessão inicial) + Sprint 2.2 (`POST …/choices` integrado à engine) + Sprint 2.3 (`GET /api/ranking`).

Prefixo base: `/api`.

## Convenção de erros

Todos os endpoints respondem em erro com envelope:

```json
{
  "error": {
    "code": "<not_found|conflict|validation_error|internal_error>",
    "message": "Mensagem segura.",
    "details": { "campo": "valor" }
  }
}
```

Códigos:

- **422** — payload inválido (Pydantic) **ou** rejeição declarada pela engine (`DomainValidationError` — ex.: `option_id` inexistente no evento atual).  
- **404** — `Player`, `Session` ou `SessionAttributes` ausentes.  
- **409** — sessão já finalizada, ou `event_id` ≠ `current_event_id`.  
- **500** — erro interno **sem stack** no payload.

## Saúde

| Método | Caminho | Descrição |
|--------|---------|-----------|
| `GET` | `/api/health` | **Implementado.** `{"status":"ok"}` |

## Jogador / sessão

| Método | Caminho | Estado | Descrição |
|--------|---------|--------|-----------|
| `POST` | `/api/players` | **Implementado (2.1).** | `{ "name": string (1..64) }`. `201`: `{ id, name, created_at }`. Nome pode repetir entre Players. |
| `POST` | `/api/sessions` | **Implementado (2.1).** | `{ "player_id": int > 0 }`. `201`: snapshot `SessionResponse`. |
| `GET` | `/api/sessions/{id}` | **Implementado (2.1 + 2.2).** | Snapshot completo. `inject_secret_event` é sempre `null` no GET — só é preenchido imediatamente após alguns POST `/choices`. |
| `POST` | `/api/sessions/{id}/choices` | **Implementado (2.2).** | `{ "event_id": string, "option_id": "A"|"B"|"C"|"D" }`. `200`: snapshot atualizado; `RankingEntry` criada ao terminar sessão (`status=finished`). |

## Schema `SessionResponse`

Campos principais incluem estado da sessão, `attributes`, `current_event` (slot principal atual enquanto `active`) e o opcional **`inject_secret_event`** (evento secreto que a engine sinaliza neste turno — mesmo shape de evento SEM `consequences` nas options).

```jsonc
{
  "id": 1,
  "player_id": 1,
  "status": "active",
  "current_day": 1,
  "current_sequence": 2,
  "current_event_id": "ev_day1_002",
  "ending_id": null,
  "score": null,
  "created_at": "...",
  "updated_at": "...",
  "finished_at": null,
  "attributes": { "energia": 6, "reputacao": 5, "networking": 3,
    "ansiedade": 2, "produtividade": 5, "aprendizado": 6 },
  "current_event": { /* próximo principal */ },
  "inject_secret_event": null        // opcional — presente só no retorno recente do POST choices
}
```

> **Invariante de segurança / regra de produto:** o backend **nunca** envia `consequences` dentro de `options`. O cliente manda apenas `option_id`; toda matemática fica na engine.

## Ranking

| Método | Caminho | Estado | Descrição |
|--------|---------|--------|-----------|
| `GET` | `/api/ranking` | **Implementado (2.3).** | Lista pública do leaderboard global. Query opcional `?limit=N` (`1 ≤ N ≤ 100`, default `10`). `200`: envelope `RankingListResponse`. Valor de `limit` fora dos bounds retorna `422` com envelope de erro padrão. |

### Schema `RankingListResponse`

Envelope `{items, limit, count}`. Itens ordenados por `score` desc; tie-break `created_at` asc + `id` asc (determinístico). `count` é o tamanho real da lista retornada (≤ `limit`).

```jsonc
{
  "items": [
    {
      "id": 12,
      "player_name": "Bruno",
      "score": 551,
      "ending_id": "trainee_lenda",
      "created_at": "2026-05-14T18:23:11.412"
    },
    {
      "id": 7,
      "player_name": "Cris",
      "score": 280,
      "ending_id": "sobrevivente",
      "created_at": "2026-05-14T18:18:02.001"
    }
  ],
  "limit": 10,
  "count": 2
}
```

> **Invariante de privacidade:** o response do ranking **não** expõe `session_id` (chave estrangeira interna). O cliente recebe apenas o necessário para renderizar a lista pública: `id` da entrada, `player_name`, `score`, `ending_id`, `created_at`.

> **Observação:** o `score` e o `ending_id` retornados são exatamente os valores calculados pela engine ao final da partida (`backend/engine/endings.py::compute_score`) e persistidos via `RankingEntry`. O endpoint **não recalcula nada** — é leitura pura.

> **Sem paginação cursor/offset nesta sprint** (escopo proibido). O envelope foi pensado para evolução futura sem quebrar contrato.

## Restart

| Método | Caminho | Estado |
|--------|---------|--------|
| `POST` | `/api/sessions/{id}/restart` | Futuro conforme UX. |

## CORS

- Lista explícita de origens: `CORS_ORIGINS` CSV (default `http://localhost:5173`). **Sem** `Access-Control-Allow-Origin: *`.  
- Credenciais: desativadas (`allow_credentials=False`).  
- Métodos permitidos no preflight: `GET`, `POST`, `OPTIONS`.  
- Cabeçalhos permitidos nos preflight: **`Content-Type` e `Accept` apenas**.
