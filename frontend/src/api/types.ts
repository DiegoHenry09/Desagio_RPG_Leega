/**
 * Tipos da API HTTP — espelham EXATAMENTE o contrato definido em
 * `docs/02-product/api.md` e `backend/schemas/sessions.py`. Não inventar
 * campos aqui: se a API mudar, atualizar o doc primeiro, depois propagar.
 *
 * Invariantes críticas (frontend.mdc + api.md):
 * - `OptionPayload` NÃO tem `consequences` (backend nunca envia).
 * - `RankingItem` inclui `player_id` (perfil/histórico); NÃO expõe `session_id`.
 * - Score, ending e atributos vêm prontos da engine — frontend só renderiza.
 */

export type AttributeId =
  | 'energia'
  | 'reputacao'
  | 'networking'
  | 'ansiedade'
  | 'produtividade'
  | 'aprendizado'

export interface Attributes {
  energia: number
  reputacao: number
  networking: number
  ansiedade: number
  produtividade: number
  aprendizado: number
}

export type OptionId = 'A' | 'B' | 'C' | 'D'

export interface OptionPayload {
  id: OptionId
  label: string
}

export interface EventPayload {
  id: string
  title: string
  scene: string
  day: number | null
  sequence: number | null
  is_main: boolean
  options: OptionPayload[]
}

export type SessionStatus = 'active' | 'finished'

export interface SessionResponse {
  id: number
  player_id: number
  /** Nome do jogador (`Player.name`), espelhado pela API em todo snapshot de sessão. */
  player_name: string
  status: SessionStatus
  current_day: number
  current_sequence: number
  current_event_id: string | null
  ending_id: string | null
  score: number | null
  created_at: string
  updated_at: string
  finished_at: string | null
  attributes: Attributes
  current_event: EventPayload | null
  inject_secret_event: EventPayload | null
}

export interface PlayerResponse {
  id: number
  name: string
  created_at: string
}

export interface RankingItem {
  id: number
  player_id: number
  player_name: string
  score: number
  ending_id: string
  created_at: string
}

export interface RankingResponse {
  items: RankingItem[]
  limit: number
  count: number
}

export interface PlayerProfileStats {
  games_played: number
  best_score: number | null
  avg_score: number | null
}

export interface PlayerRunItem {
  ranking_entry_id: number
  score: number
  ending_id: string
  created_at: string
  choices_count: number
}

export interface PlayerProfileResponse {
  player_id: number
  player_name: string
  stats: PlayerProfileStats
  ending_counts: Record<string, number>
  runs: PlayerRunItem[]
}

export interface PlayerRunChoiceItem {
  event_id: string
  option_id: string
  day: number
  sequence: number
  created_at: string
}

export interface PlayerRunChoicesResponse {
  ranking_entry_id: number
  choices: PlayerRunChoiceItem[]
}

/** Envelope de erro padronizado pelo backend (api.md §"Convenção de erros"). */
export interface ApiErrorEnvelope {
  error: {
    code: string
    message: string
    details?: Record<string, unknown>
  }
}
