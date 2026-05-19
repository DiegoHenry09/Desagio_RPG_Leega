/**
 * Acesso ao localStorage do navegador.
 *
 * Política (frontend.mdc): persistimos APENAS `sessionId` e (opcional)
 * `traineeVariant`. Nada além disso. Qualquer outro estado é responsabilidade
 * do backend (fonte da verdade).
 *
 * Robustez: funções não-quebráveis em ambiente sem localStorage (SSR teórico
 * ou navegador com storage desabilitado).
 */

const SESSION_KEY = 'cs.sessionId'
const VARIANT_KEY = 'cs.traineeVariant'

export type TraineeVariant = 1 | 2 | 3

function safeStorage(): Storage | null {
  try {
    return typeof window !== 'undefined' ? window.localStorage : null
  } catch {
    return null
  }
}

export function getSessionId(): number | null {
  const storage = safeStorage()
  if (!storage) return null
  const raw = storage.getItem(SESSION_KEY)
  if (!raw) return null
  const parsed = Number.parseInt(raw, 10)
  return Number.isFinite(parsed) && parsed > 0 ? parsed : null
}

export function setSessionId(id: number): void {
  const storage = safeStorage()
  if (!storage) return
  storage.setItem(SESSION_KEY, String(id))
}

export function clearSessionId(): void {
  const storage = safeStorage()
  if (!storage) return
  storage.removeItem(SESSION_KEY)
}

export function getTraineeVariant(): TraineeVariant {
  const storage = safeStorage()
  if (!storage) return 1
  const raw = storage.getItem(VARIANT_KEY)
  const parsed = raw ? Number.parseInt(raw, 10) : NaN
  if (parsed === 1 || parsed === 2 || parsed === 3) return parsed
  const fresh: TraineeVariant = (Math.floor(Math.random() * 3) + 1) as TraineeVariant
  storage.setItem(VARIANT_KEY, String(fresh))
  return fresh
}
