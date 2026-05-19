import { useEffect, useState } from 'react'

import { ApiError, createPlayer, createSession, getSession } from '../api/client'
import type { SessionResponse } from '../api/types'
import {
  clearSessionId,
  getSessionId,
  setSessionId,
} from '../state/sessionStorage'

import './HomePage.css'

interface Props {
  onStarted: (session: SessionResponse) => void
  onResume: (session: SessionResponse) => void
  onShowEnding: (session: SessionResponse) => void
  onShowRanking: () => void
}

type LoadingState = 'idle' | 'checking' | 'starting'

export default function HomePage({
  onStarted,
  onResume,
  onShowEnding,
  onShowRanking,
}: Props) {
  const [name, setName] = useState('')
  // Inicializador lazy: se não há sessionId no mount, já começamos em 'idle'.
  // Evita set-state-in-effect só para refletir um estado conhecido em mount.
  const [loading, setLoading] = useState<LoadingState>(() =>
    getSessionId() !== null ? 'checking' : 'idle',
  )
  const [error, setError] = useState<string | null>(null)
  const [existing, setExisting] = useState<SessionResponse | null>(null)

  useEffect(() => {
    const sessionId = getSessionId()
    if (!sessionId) return
    let cancelled = false
    getSession(sessionId)
      .then((session) => {
        if (cancelled) return
        setExisting(session)
        setLoading('idle')
      })
      .catch((err) => {
        if (cancelled) return
        if (err instanceof ApiError && err.status === 404) {
          clearSessionId()
        }
        setExisting(null)
        setLoading('idle')
      })
    return () => {
      cancelled = true
    }
  }, [])

  function validateName(value: string): string | null {
    const trimmed = value.trim()
    if (trimmed.length < 1) return 'Informe um nome para iniciar a jornada.'
    if (trimmed.length > 64) return 'Use no máximo 64 caracteres.'
    return null
  }

  async function handleStart(event: React.FormEvent) {
    event.preventDefault()
    const validationError = validateName(name)
    if (validationError) {
      setError(validationError)
      return
    }
    setError(null)
    setLoading('starting')
    try {
      const player = await createPlayer(name.trim())
      const session = await createSession(player.id)
      setSessionId(session.id)
      onStarted(session)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Não foi possível iniciar a jornada. Verifique se o backend está rodando em :8000.')
      }
      setLoading('idle')
    }
  }

  function handleResume() {
    if (!existing) return
    if (existing.status === 'finished') {
      onShowEnding(existing)
    } else {
      onResume(existing)
    }
  }

  function handleDiscard() {
    clearSessionId()
    setExisting(null)
  }

  return (
    <div className="cs-home">
      <header className="cs-home__hero">
        <p className="cs-home__eyebrow">Mini RPG corporativo</p>
        <h1 className="cs-home__title">Corporate Survivor</h1>
        <p className="cs-home__subtitle">
          Sobreviva à sua primeira semana como trainee. Cinco dias, três eventos por dia,
          decisões que custam algo.
        </p>
      </header>

      {existing ? (
        <section
          className="cs-home__resume"
          aria-label="Sessão em andamento"
        >
          <div>
            <p className="cs-home__resume-eyebrow">
              {existing.status === 'finished'
                ? 'Sessão encerrada'
                : 'Você tem uma jornada em andamento'}
            </p>
            <p className="cs-home__resume-progress">
              {existing.status === 'finished'
                ? 'Veja o resultado da partida.'
                : `Dia ${existing.current_day} de 5 — sequência ${existing.current_sequence}.`}
            </p>
          </div>
          <div className="cs-home__resume-actions">
            <button
              type="button"
              className="cs-home__btn cs-home__btn--primary"
              onClick={handleResume}
            >
              {existing.status === 'finished' ? 'Ver final' : 'Continuar jornada'}
            </button>
            <button
              type="button"
              className="cs-home__btn cs-home__btn--ghost"
              onClick={handleDiscard}
            >
              Descartar
            </button>
          </div>
        </section>
      ) : null}

      <form className="cs-home__form" onSubmit={handleStart} noValidate>
        <label className="cs-home__label" htmlFor="cs-home-name">
          Como você quer ser chamado?
        </label>
        <input
          id="cs-home-name"
          type="text"
          className="cs-home__input"
          value={name}
          maxLength={64}
          minLength={1}
          required
          onChange={(event) => {
            setName(event.target.value)
            if (error) setError(null)
          }}
          placeholder="Seu nome"
          autoComplete="off"
          disabled={loading !== 'idle'}
        />
        {error ? (
          <p className="cs-home__error" role="alert">
            {error}
          </p>
        ) : null}
        <div className="cs-home__form-actions">
          <button
            type="submit"
            className="cs-home__btn cs-home__btn--primary"
            disabled={loading !== 'idle'}
          >
            {loading === 'starting' ? 'Iniciando...' : 'Iniciar nova jornada'}
          </button>
          <button
            type="button"
            className="cs-home__btn cs-home__btn--ghost"
            onClick={onShowRanking}
            disabled={loading === 'starting'}
          >
            Ver ranking global
          </button>
        </div>
      </form>
    </div>
  )
}
