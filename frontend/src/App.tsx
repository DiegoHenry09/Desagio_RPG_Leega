import { useState } from 'react'

import type { SessionResponse } from './api/types'
import EndingPage from './pages/EndingPage'
import GamePage from './pages/GamePage'
import HomePage from './pages/HomePage'
import PlayerProfilePage from './pages/PlayerProfilePage'
import RankingPage from './pages/RankingPage'

import './App.css'

type View =
  | { name: 'home' }
  | { name: 'game'; session: SessionResponse }
  | { name: 'ending'; session: SessionResponse }
  | { name: 'ranking' }
  | { name: 'player-profile'; playerId: number }

/**
 * Orquestrador de telas por estado (sem react-router por escolha explícita
 * da Sprint 3.0 — escopo mínimo, sem URL bookmarkable).
 *
 * Estados:
 *   home    → HomePage (entrada / continuar / ranking)
 *   game    → GamePage (loop principal de escolha)
 *   ending  → EndingPage (resultado da sessão)
 *   ranking        → RankingPage (leaderboard global)
 *   player-profile → histórico/estatísticas por jogador
 */
function App() {
  const [view, setView] = useState<View>({ name: 'home' })

  function goHome() {
    setView({ name: 'home' })
  }

  function goGame(session: SessionResponse) {
    if (session.status === 'finished') {
      setView({ name: 'ending', session })
    } else {
      setView({ name: 'game', session })
    }
  }

  function goEnding(session: SessionResponse) {
    setView({ name: 'ending', session })
  }

  function goRanking() {
    setView({ name: 'ranking' })
  }

  function goPlayerProfile(playerId: number) {
    setView({ name: 'player-profile', playerId })
  }

  return (
    <div className="app-shell">
      <header className="app-shell__header">
        <div className="app-shell__header-inner">
          <span className="app-shell__brand">Corporate Survivor</span>
          {view.name === 'game' || view.name === 'ending' ? (
            <span className="app-shell__player" title="Jogador">
              {view.session.player_name}
            </span>
          ) : null}
          <div className="app-shell__nav">
            <button type="button" onClick={goHome}>
              Início
            </button>
            <button type="button" onClick={goRanking}>
              Ranking
            </button>
          </div>
        </div>
      </header>
      <main className="app-shell__main">
        <div className="app-shell__main-inner">
          {view.name === 'home' ? (
            <HomePage
              onStarted={goGame}
              onResume={goGame}
              onShowEnding={goEnding}
              onShowRanking={goRanking}
            />
          ) : null}
          {view.name === 'game' ? (
            <GamePage
              initialSession={view.session}
              onFinished={goEnding}
              onBackHome={goHome}
              onShowRanking={goRanking}
            />
          ) : null}
          {view.name === 'ending' ? (
            <EndingPage
              session={view.session}
              onViewRanking={goRanking}
              onNewJourney={goHome}
            />
          ) : null}
          {view.name === 'ranking' ? (
            <RankingPage onBack={goHome} onOpenPlayer={goPlayerProfile} />
          ) : null}
          {view.name === 'player-profile' ? (
            <PlayerProfilePage
              playerId={view.playerId}
              onBack={goRanking}
              onHome={goHome}
            />
          ) : null}
        </div>
      </main>
      <footer className="app-shell__footer">
        Mini RPG corporativo — Sprint 3.0. Backend é fonte da verdade.
      </footer>
    </div>
  )
}

export default App
