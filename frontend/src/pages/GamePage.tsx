import { useEffect, useState } from 'react'

import { ApiError, getSession, submitChoice } from '../api/client'
import type { EventPayload, OptionId, SessionResponse } from '../api/types'
import { getEventVisual } from '../assets/visuals/eventVisualsMap'
import {
  dialogueSpeakerName,
  type PersonaId,
} from '../assets/visuals/personas/_index'
import AttributePanel from '../components/AttributePanel'
import ChoiceList from '../components/ChoiceList'
import EventStage from '../components/EventStage'
import SecretEventBanner from '../components/SecretEventBanner'
import { clearSessionId, getTraineeVariant } from '../state/sessionStorage'

import './GamePage.css'

interface Props {
  initialSession: SessionResponse
  onFinished: (session: SessionResponse) => void
  onBackHome: () => void
  onShowRanking: () => void
}

/** Primeira persona “falante” para o bloco de diálogo: prioriza quem não é o trainee se houver. */
function primaryDialoguePersona(personas: PersonaId[]): PersonaId {
  const nonTrainee = personas.find((p) => p !== 'trainee')
  return nonTrainee ?? personas[0] ?? 'trainee'
}

/**
 * GamePage orquestra:
 *   - exibe `current_event` da sessão
 *   - envia POST /api/sessions/{id}/choices ao escolher uma opção
 *   - se response.status === 'finished' → encerra para EndingPage
 *   - se response.inject_secret_event presente → mostra banner discreto
 *
 * Toda matemática (clamp, score, ending, consequence) é do backend.
 */
export default function GamePage({
  initialSession,
  onFinished,
  onBackHome,
  onShowRanking,
}: Props) {
  const [session, setSession] = useState<SessionResponse>(initialSession)
  const [selectedOption, setSelectedOption] = useState<OptionId | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [secretEvent, setSecretEvent] = useState<EventPayload | null>(initialSession.inject_secret_event)
  const traineeVariant = getTraineeVariant()

  useEffect(() => {
    if (initialSession.status === 'finished') {
      onFinished(initialSession)
    }
  }, [initialSession, onFinished])

  async function refreshSession() {
    try {
      const fresh = await getSession(session.id)
      setSession(fresh)
      if (fresh.status === 'finished') {
        onFinished(fresh)
      }
    } catch (err) {
      const message =
        err instanceof ApiError
          ? err.message
          : 'Falha ao atualizar a sessão. Verifique o backend.'
      setError(message)
    }
  }

  async function handleChoose(optionId: OptionId) {
    if (submitting) return
    if (!session.current_event) return
    if (session.status !== 'active') return
    setSelectedOption(optionId)
    setSubmitting(true)
    setError(null)
    try {
      const next = await submitChoice(session.id, session.current_event.id, optionId)
      setSession(next)
      if (next.inject_secret_event) {
        setSecretEvent(next.inject_secret_event)
      }
      if (next.status === 'finished') {
        onFinished(next)
      }
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
        if (err.status === 404) {
          clearSessionId()
        }
      } else {
        setError('Não foi possível registrar sua escolha. Tente novamente.')
      }
    } finally {
      setSubmitting(false)
      setSelectedOption(null)
    }
  }

  const currentEvent = session.current_event
  const eventVisual = currentEvent ? getEventVisual(currentEvent.id) : null
  const dialoguePersona = eventVisual
    ? primaryDialoguePersona(eventVisual.personas)
    : 'trainee'
  const dialogueLabel = dialogueSpeakerName(dialoguePersona, session.player_name)

  const weekdayFull = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-feira',
    'Sexta-feira',
  ] as const
  const weekdayShort = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'] as const
  const currentWeekdayIdx = Math.min(Math.max(session.current_day, 1), 5) - 1

  return (
    <div className="cs-game">
      <header className="cs-game__topbar">
        <div className="cs-game__progress-wrap">
          <div className="cs-game__progress">
            <span className="cs-game__progress-label">Dia</span>
            <span className="cs-game__progress-value">{session.current_day}</span>
            <span className="cs-game__progress-sep">/</span>
            <span className="cs-game__progress-total">5</span>
            <span className="cs-game__progress-weekday" title={weekdayFull[currentWeekdayIdx]}>
              {weekdayFull[currentWeekdayIdx]}
            </span>
            <span className="cs-game__progress-seq">
              Evento {session.current_sequence} de 3
            </span>
          </div>
          <ol className="cs-game__week-strip" aria-label="Dias úteis da semana (1 a 5)">
            {[1, 2, 3, 4, 5].map((day) => {
              const idx = day - 1
              const isCurrent = day === session.current_day
              return (
                <li
                  key={day}
                  className={
                    isCurrent
                      ? 'cs-game__week-day cs-game__week-day--current'
                      : 'cs-game__week-day'
                  }
                  aria-current={isCurrent ? 'step' : undefined}
                >
                  <span className="cs-game__week-day-short" title={weekdayFull[idx]}>
                    {weekdayShort[idx]}
                  </span>
                  <span className="cs-game__week-day-num">{day}</span>
                </li>
              )
            })}
          </ol>
        </div>
        <div className="cs-game__topbar-actions">
          <button
            type="button"
            className="cs-game__link"
            onClick={onShowRanking}
          >
            Ranking
          </button>
          <button
            type="button"
            className="cs-game__link"
            onClick={onBackHome}
          >
            Início
          </button>
        </div>
      </header>

      {secretEvent ? (
        <SecretEventBanner
          secretEventTitle={secretEvent.title}
          onDismiss={() => setSecretEvent(null)}
        />
      ) : null}

      {currentEvent ? (
        <div className="cs-game__layout">
          <EventStage event={currentEvent} traineeVariant={traineeVariant} />
          <article className="cs-game__event" aria-labelledby="cs-game-event-title">
            <h1 id="cs-game-event-title" className="cs-game__event-title">
              {currentEvent.title}
            </h1>
            <div className="cs-game__dialogue" role="region" aria-label="Cena e diálogo">
              <span className="cs-game__dialogue-badge" aria-hidden="true">
                Cena
              </span>
              <p className="cs-game__dialogue-speaker">{dialogueLabel}</p>
              <p className="cs-game__dialogue-scene">{currentEvent.scene}</p>
            </div>
            <p className="cs-game__event-bridge">
              E agora — <strong>o que você faz?</strong> Escolha abaixo.
            </p>
            <ChoiceList
              options={currentEvent.options}
              onChoose={handleChoose}
              disabled={submitting}
              selectedId={selectedOption}
            />
          </article>
          <aside className="cs-game__sidebar">
            <AttributePanel attributes={session.attributes} />
          </aside>
        </div>
      ) : (
        <div className="cs-game__empty">
          <p>Sessão sem evento ativo.</p>
          <button type="button" className="cs-game__link" onClick={refreshSession}>
            Recarregar
          </button>
        </div>
      )}

      {error ? (
        <p className="cs-game__error" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  )
}
