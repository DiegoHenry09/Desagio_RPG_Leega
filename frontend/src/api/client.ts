/**
 * Cliente HTTP fino do frontend. Toda chamada passa por aqui.
 *
 * - Em dev, o proxy do Vite (`/api → http://localhost:8000`) cuida do CORS.
 * - Em produção, a base pode ser sobrescrita via `VITE_API_BASE_URL`
 *   (documentado, mas não obrigatório nesta sprint — Sprint 3.0 é DEV-only).
 * - Erros do backend vêm com envelope { error: { code, message, details? } }.
 *   ApiError preserva o envelope para a UI traduzir códigos quando útil.
 *
 * Importante (frontend.mdc):
 * - Nada de regra de jogo aqui. Só transporte HTTP.
 * - Nunca enviamos `attributes`, `score` ou `ending` no body.
 */

import type {
  ApiErrorEnvelope,
  OptionId,
  PlayerProfileResponse,
  PlayerResponse,
  PlayerRunChoicesResponse,
  RankingResponse,
  SessionResponse,
} from './types'

const RAW_BASE = (import.meta.env.VITE_API_BASE_URL ?? '').trim()
const API_BASE = RAW_BASE.replace(/\/$/, '')

function url(path: string): string {
  return `${API_BASE}${path}`
}

export class ApiError extends Error {
  readonly status: number
  readonly code: string
  readonly details?: Record<string, unknown>

  constructor(status: number, envelope: ApiErrorEnvelope | null, fallback: string) {
    const code = envelope?.error?.code ?? `http_${status}`
    const message = envelope?.error?.message ?? fallback
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.details = envelope?.error?.details
  }
}

/** Converte corpo JSON de erro (envelope nosso ou `detail` padrão FastAPI/Starlette). */
function jsonBodyToEnvelope(status: number, raw: unknown): ApiErrorEnvelope | null {
  if (!raw || typeof raw !== 'object') return null
  const o = raw as Record<string, unknown>
  if (
    'error' in o &&
    o.error &&
    typeof o.error === 'object' &&
    o.error !== null &&
    'message' in (o.error as object)
  ) {
    return raw as ApiErrorEnvelope
  }
  if ('detail' in o) {
    const detail = o.detail
    let msg: string
    if (Array.isArray(detail)) {
      msg = detail
        .map((item) =>
          typeof item === 'object' && item !== null && 'msg' in item
            ? String((item as { msg: unknown }).msg)
            : String(item),
        )
        .join(' ')
    } else {
      msg = String(detail ?? '')
    }
    if (status === 404 && (msg === 'Not Found' || msg === '')) {
      return {
        error: {
          code: 'not_found',
          message:
            'Rota não encontrada no servidor (404). Pare e suba de novo o backend (uvicorn) com o código atual — é preciso expor GET /api/players/{id}/profile. Confira também http://localhost:8000/docs.',
        },
      }
    }
    return {
      error: {
        code: status === 422 ? 'validation_error' : `http_${status}`,
        message: msg || 'Erro na API',
      },
    }
  }
  return null
}

const JSON_HEADERS: HeadersInit = {
  'Content-Type': 'application/json',
  Accept: 'application/json',
}

async function request<T>(
  path: string,
  init: { method: 'GET' | 'POST'; body?: unknown } = { method: 'GET' },
): Promise<T> {
  const response = await fetch(url(path), {
    method: init.method,
    headers: JSON_HEADERS,
    body: init.body !== undefined ? JSON.stringify(init.body) : undefined,
  })

  if (!response.ok) {
    let envelope: ApiErrorEnvelope | null = null
    try {
      const raw = await response.json()
      envelope = jsonBodyToEnvelope(response.status, raw)
    } catch {
      // resposta não-JSON (ex.: 502 do proxy) — segue com envelope=null
    }
    throw new ApiError(response.status, envelope, response.statusText || 'Erro na API')
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}

export function createPlayer(name: string): Promise<PlayerResponse> {
  return request<PlayerResponse>('/api/players', {
    method: 'POST',
    body: { name },
  })
}

export function createSession(playerId: number): Promise<SessionResponse> {
  return request<SessionResponse>('/api/sessions', {
    method: 'POST',
    body: { player_id: playerId },
  })
}

export function getSession(sessionId: number): Promise<SessionResponse> {
  return request<SessionResponse>(`/api/sessions/${sessionId}`)
}

export function submitChoice(
  sessionId: number,
  eventId: string,
  optionId: OptionId,
): Promise<SessionResponse> {
  return request<SessionResponse>(`/api/sessions/${sessionId}/choices`, {
    method: 'POST',
    body: { event_id: eventId, option_id: optionId },
  })
}

export function getRanking(limit = 10): Promise<RankingResponse> {
  return request<RankingResponse>(`/api/ranking?limit=${limit}`)
}

export function getPlayerProfile(playerId: number): Promise<PlayerProfileResponse> {
  return request<PlayerProfileResponse>(`/api/players/${playerId}/profile`)
}

export function getPlayerRunChoices(
  playerId: number,
  rankingEntryId: number,
): Promise<PlayerRunChoicesResponse> {
  return request<PlayerRunChoicesResponse>(
    `/api/players/${playerId}/runs/${rankingEntryId}/choices`,
  )
}
