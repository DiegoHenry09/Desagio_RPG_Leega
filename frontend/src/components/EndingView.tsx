import type { SessionResponse } from '../api/types'
import { personas, type PersonaId } from '../assets/visuals/personas/_index'
import type { TraineeVariant } from '../state/sessionStorage'

import AttributePanel from './AttributePanel'

import './EndingView.css'

interface Props {
  session: SessionResponse
  traineeVariant?: TraineeVariant
  onViewRanking: () => void
  onNewJourney: () => void
}

const ENDING_TITLES: Record<string, string> = {
  trainee_lenda: 'Trainee Lenda',
  promessa: 'Promessa Corporativa',
  sobrevivente: 'Sobrevivente do Onboarding',
  invisivel: 'Funcionário Invisível',
  risco_op: 'Risco Operacional',
  burnout: 'Burnout em Tempo Recorde',
  demitido: 'Demitido no Período de Experiência',
}

const ENDING_DESCRIPTIONS: Record<string, string> = {
  trainee_lenda: 'Já estão falando que você não parece trainee.',
  promessa: 'Há expectativa real sobre você.',
  sobrevivente: 'Você terminou a primeira semana. Não é pouco.',
  invisivel: 'Cinco dias se passaram. Quase ninguém sabe seu nome.',
  risco_op: 'Você passou despercebido pelas pessoas certas e marcado pelas erradas.',
  burnout: 'Você não chegou à sexta inteiro. Seu corpo cobrou antes da empresa cobrar.',
  demitido: 'Sua presença foi prejuízo visível para o time.',
}

const POSITIVE_ENDINGS = new Set(['trainee_lenda', 'promessa'])
const NEGATIVE_ENDINGS = new Set(['burnout', 'demitido', 'risco_op'])

function endingTone(endingId: string | null): 'positive' | 'negative' | 'neutral' {
  if (!endingId) return 'neutral'
  if (POSITIVE_ENDINGS.has(endingId)) return 'positive'
  if (NEGATIVE_ENDINGS.has(endingId)) return 'negative'
  return 'neutral'
}

export default function EndingView({
  session,
  traineeVariant,
  onViewRanking,
  onNewJourney,
}: Props) {
  const tone = endingTone(session.ending_id)
  const title = session.ending_id ? ENDING_TITLES[session.ending_id] ?? session.ending_id : 'Sessão encerrada'
  const description = session.ending_id ? ENDING_DESCRIPTIONS[session.ending_id] ?? '' : ''
  const TraineeComponent = personas.trainee as (typeof personas)[PersonaId]

  return (
    <article className="cs-ending" data-tone={tone}>
      <div className="cs-ending__portrait" aria-hidden="true">
        <TraineeComponent variant={traineeVariant} />
      </div>
      <header className="cs-ending__header">
        <p className="cs-ending__eyebrow">Final</p>
        <h1 className="cs-ending__title">{title}</h1>
        {description ? <p className="cs-ending__desc">{description}</p> : null}
      </header>
      <div className="cs-ending__stats">
        <AttributePanel attributes={session.attributes} />
        <div className="cs-ending__score">
          <span className="cs-ending__score-label">Score</span>
          <span className="cs-ending__score-value">{session.score ?? '—'}</span>
        </div>
      </div>
      <div className="cs-ending__actions">
        <button
          type="button"
          className="cs-ending__btn cs-ending__btn--primary"
          onClick={onViewRanking}
        >
          Ver ranking global
        </button>
        <button
          type="button"
          className="cs-ending__btn cs-ending__btn--secondary"
          onClick={onNewJourney}
        >
          Nova jornada
        </button>
      </div>
    </article>
  )
}
