import { useEffect, useState } from 'react'

import { ApiError, getRanking } from '../api/client'
import type { RankingItem } from '../api/types'
import RankingPanel from '../components/RankingPanel'

import './RankingPage.css'

interface Props {
  onBack: () => void
  onOpenPlayer: (playerId: number) => void
}

type LoadingState = 'loading' | 'ready' | 'error'

export default function RankingPage({ onBack, onOpenPlayer }: Props) {
  const [state, setState] = useState<LoadingState>('loading')
  const [items, setItems] = useState<RankingItem[]>([])
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    getRanking(10)
      .then((response) => {
        if (cancelled) return
        setItems(response.items)
        setState('ready')
      })
      .catch((err) => {
        if (cancelled) return
        const message =
          err instanceof ApiError
            ? err.message
            : 'Não foi possível carregar o ranking. Verifique se o backend está rodando.'
        setErrorMessage(message)
        setState('error')
      })
    return () => {
      cancelled = true
    }
  }, [])

  return (
    <div className="cs-ranking-page">
      <button
        type="button"
        className="cs-ranking-page__back"
        onClick={onBack}
      >
        ← Voltar
      </button>
      {state === 'loading' ? (
        <p className="cs-ranking-page__status">Carregando ranking...</p>
      ) : null}
      {state === 'error' ? (
        <p className="cs-ranking-page__status cs-ranking-page__status--error" role="alert">
          {errorMessage}
        </p>
      ) : null}
      {state === 'ready' ? (
        <RankingPanel items={items} onOpenPlayer={onOpenPlayer} />
      ) : null}
    </div>
  )
}
