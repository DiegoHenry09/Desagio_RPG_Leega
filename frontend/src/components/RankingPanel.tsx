import type { RankingItem } from '../api/types'

import './RankingPanel.css'

interface Props {
  items: RankingItem[]
  highlightSessionId?: number | null
  /** Abre perfil/histórico do jogador (`GET /api/players/{id}/profile`). */
  onOpenPlayer?: (playerId: number) => void
}

/**
 * Lista do ranking público.
 *
 * O backend não expõe `session_id`; inclui `player_id` para perfil público.
 * `highlightSessionId` mantido por compatibilidade — não usado (sem `session_id`).
 */
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

function hasPublicPlayerId(item: RankingItem): item is RankingItem & { player_id: number } {
  return typeof item.player_id === 'number' && Number.isFinite(item.player_id)
}

export default function RankingPanel({ items, onOpenPlayer }: Props) {
  if (items.length === 0) {
    return (
      <section className="cs-ranking" aria-live="polite">
        <h2 className="cs-ranking__title">Ranking global</h2>
        <p className="cs-ranking__empty">Nenhuma partida finalizada ainda.</p>
      </section>
    )
  }

  return (
    <section className="cs-ranking">
      <h2 className="cs-ranking__title">Ranking global</h2>
      <ol className="cs-ranking__list">
        <li className="cs-ranking__head" aria-hidden="true">
          <span className="cs-ranking__rank">#</span>
          <span className="cs-ranking__name">Jogador</span>
          <span className="cs-ranking__ending">Final</span>
          <span className="cs-ranking__date">Data</span>
          <span className="cs-ranking__score">Score</span>
        </li>
        {items.map((item, idx) => (
          <li
            key={item.id}
            className="cs-ranking__row"
            data-ending={item.ending_id}
          >
            <span className="cs-ranking__rank">{idx + 1}</span>
            <span className="cs-ranking__name">
              {onOpenPlayer && hasPublicPlayerId(item) ? (
                <button
                  type="button"
                  className="cs-ranking__name-btn"
                  onClick={() => onOpenPlayer(item.player_id)}
                >
                  {item.player_name}
                </button>
              ) : (
                item.player_name
              )}
            </span>
            <span className="cs-ranking__ending">{endingLabel(item.ending_id)}</span>
            <span className="cs-ranking__date">{formatDate(item.created_at)}</span>
            <span className="cs-ranking__score">{item.score}</span>
          </li>
        ))}
      </ol>
    </section>
  )
}
