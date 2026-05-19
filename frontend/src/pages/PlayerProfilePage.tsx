import { useCallback, useEffect, useState } from 'react'

import { ApiError, getPlayerProfile, getPlayerRunChoices } from '../api/client'
import type {
  PlayerProfileResponse,
  PlayerRunChoiceItem,
  PlayerRunItem,
} from '../api/types'

import './PlayerProfilePage.css'

const ENDING_LABELS: Record<string, string> = {
  trainee_lenda: 'Trainee Lenda',
  promessa: 'Promessa Corporativa',
  sobrevivente: 'Sobrevivente do Onboarding',
  invisivel: 'Funcionário Invisível',
  risco_op: 'Risco Operacional',
  burnout: 'Burnout em Tempo Recorde',
  demitido: 'Demitido no Período de Experiência',
}

function endingLabel(id: string): string {
  return ENDING_LABELS[id] ?? id
}

function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString('pt-BR')
  } catch {
    return iso.slice(0, 10)
  }
}

interface Props {
  playerId: number
  onBack: () => void
  onHome: () => void
}

type LoadingState = 'loading' | 'ready' | 'error'

export default function PlayerProfilePage({ playerId, onBack, onHome }: Props) {
  const [state, setState] = useState<LoadingState>('loading')
  const [profile, setProfile] = useState<PlayerProfileResponse | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [expandedRunId, setExpandedRunId] = useState<number | null>(null)
  const [choicesByRun, setChoicesByRun] = useState<
    Record<number, PlayerRunChoiceItem[] | 'loading' | 'error'>
  >({})

  useEffect(() => {
    let cancelled = false
    setState('loading')
    setErrorMessage(null)
    getPlayerProfile(playerId)
      .then((response) => {
        if (cancelled) return
        setProfile(response)
        setState('ready')
      })
      .catch((err) => {
        if (cancelled) return
        const message =
          err instanceof ApiError
            ? err.message
            : 'Não foi possível carregar o perfil. Verifique se o backend está rodando.'
        setErrorMessage(message)
        setState('error')
      })
    return () => {
      cancelled = true
    }
  }, [playerId])

  const toggleChoices = useCallback(
    async (run: PlayerRunItem) => {
      const rid = run.ranking_entry_id
      if (expandedRunId === rid) {
        setExpandedRunId(null)
        return
      }
      setExpandedRunId(rid)
      setChoicesByRun((prev) => ({ ...prev, [rid]: 'loading' }))
      try {
        const payload = await getPlayerRunChoices(playerId, rid)
        setChoicesByRun((prev) => ({ ...prev, [rid]: payload.choices }))
      } catch {
        setChoicesByRun((prev) => ({ ...prev, [rid]: 'error' }))
      }
    },
    [expandedRunId, playerId],
  )

  return (
    <div className="cs-player-profile">
      <div className="cs-player-profile__toolbar">
        <button type="button" className="cs-player-profile__back" onClick={onBack}>
          ← Ranking
        </button>
        <button type="button" className="cs-player-profile__home" onClick={onHome}>
          Início
        </button>
      </div>

      {state === 'loading' ? (
        <p className="cs-player-profile__status">Carregando perfil...</p>
      ) : null}
      {state === 'error' ? (
        <p className="cs-player-profile__status cs-player-profile__status--error" role="alert">
          {errorMessage}
        </p>
      ) : null}

      {state === 'ready' && profile ? (
        <>
          <header className="cs-player-profile__header">
            <h2 className="cs-player-profile__title">{profile.player_name}</h2>
            <p className="cs-player-profile__subtitle">Histórico e estatísticas</p>
          </header>

          <section className="cs-player-profile__stats" aria-label="Estatísticas">
            <div className="cs-player-profile__stat-card">
              <span className="cs-player-profile__stat-label">Partidas no ranking</span>
              <span className="cs-player-profile__stat-value">{profile.stats.games_played}</span>
            </div>
            <div className="cs-player-profile__stat-card">
              <span className="cs-player-profile__stat-label">Melhor score</span>
              <span className="cs-player-profile__stat-value">
                {profile.stats.best_score ?? '—'}
              </span>
            </div>
            <div className="cs-player-profile__stat-card">
              <span className="cs-player-profile__stat-label">Média de score</span>
              <span className="cs-player-profile__stat-value">
                {profile.stats.avg_score ?? '—'}
              </span>
            </div>
          </section>

          {Object.keys(profile.ending_counts).length > 0 ? (
            <section className="cs-player-profile__endings" aria-label="Finais alcançados">
              <h3>Finais</h3>
              <ul className="cs-player-profile__ending-list">
                {Object.entries(profile.ending_counts).map(([eid, count]) => (
                  <li key={eid}>
                    <span>{endingLabel(eid)}</span>
                    <span className="cs-player-profile__ending-count">×{count}</span>
                  </li>
                ))}
              </ul>
            </section>
          ) : null}

          <section className="cs-player-profile__runs" aria-label="Partidas">
            <h3>Partidas</h3>
            {profile.runs.length === 0 ? (
              <p className="cs-player-profile__empty">
                Nenhuma partida finalizada registrada no ranking para este jogador.
              </p>
            ) : (
              <ul className="cs-player-profile__run-list">
                {profile.runs.map((run) => (
                  <li key={run.ranking_entry_id} className="cs-player-profile__run">
                    <div className="cs-player-profile__run-summary">
                      <div>
                        <strong>{run.score}</strong>{' '}
                        <span className="cs-player-profile__run-ending">
                          {endingLabel(run.ending_id)}
                        </span>
                      </div>
                      <div className="cs-player-profile__run-meta">
                        <span>{formatDate(run.created_at)}</span>
                        <span className="cs-player-profile__run-choices-count">
                          {run.choices_count}{' '}
                          {run.choices_count === 1 ? 'escolha' : 'escolhas'}
                        </span>
                      </div>
                      <button
                        type="button"
                        className="cs-player-profile__toggle"
                        onClick={() => toggleChoices(run)}
                        aria-expanded={expandedRunId === run.ranking_entry_id}
                      >
                        {expandedRunId === run.ranking_entry_id
                          ? 'Ocultar escolhas'
                          : 'Ver escolhas'}
                      </button>
                    </div>
                    {expandedRunId === run.ranking_entry_id ? (
                      <RunChoicesPanel state={choicesByRun[run.ranking_entry_id]} />
                    ) : null}
                  </li>
                ))}
              </ul>
            )}
          </section>
        </>
      ) : null}
    </div>
  )
}

function RunChoicesPanel({
  state,
}: {
  state: PlayerRunChoiceItem[] | 'loading' | 'error' | undefined
}) {
  if (state === undefined || state === 'loading') {
    return <p className="cs-player-profile__choices-status">Carregando escolhas...</p>
  }
  if (state === 'error') {
    return (
      <p className="cs-player-profile__choices-status cs-player-profile__choices-status--error">
        Não foi possível carregar as escolhas.
      </p>
    )
  }
  if (state.length === 0) {
    return (
      <p className="cs-player-profile__choices-status">Nenhuma escolha registrada nesta partida.</p>
    )
  }
  return (
    <ol className="cs-player-profile__choices">
      {state.map((c, i) => (
        <li key={`${c.event_id}-${c.sequence}-${i}`}>
          <span className="cs-player-profile__choice-idx">{i + 1}.</span>
          <code className="cs-player-profile__choice-ev">{c.event_id}</code>
          <span className="cs-player-profile__choice-opt">Opção {c.option_id}</span>
          <span className="cs-player-profile__choice-day">
            Dia {c.day}, seq. {c.sequence}
          </span>
        </li>
      ))}
    </ol>
  )
}
