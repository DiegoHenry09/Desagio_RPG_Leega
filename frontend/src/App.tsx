import { useEffect, useState } from 'react'
import './App.css'

type ApiState = 'checking' | 'ok' | 'error'

const HEALTHCHECK_PATH = '/api/health'
const HEALTHCHECK_TARGET = 'http://localhost:8000/api/health'

function App() {
  const [apiState, setApiState] = useState<ApiState>('checking')

  useEffect(() => {
    let isMounted = true

    async function checkApi() {
      try {
        const response = await fetch(HEALTHCHECK_PATH)
        const payload = (await response.json()) as { status?: string }

        if (isMounted) {
          setApiState(response.ok && payload.status === 'ok' ? 'ok' : 'error')
        }
      } catch {
        if (isMounted) {
          setApiState('error')
        }
      }
    }

    void checkApi()

    return () => {
      isMounted = false
    }
  }, [])

  return (
    <main className="app-shell">
      <section className="hero-card" aria-labelledby="app-title">
        <p className="eyebrow">Sprint 0.3</p>
        <h1 id="app-title">Corporate Survivor</h1>
        <p className="subtitle">
          Frontend healthcheck minimo com Vite, React e TypeScript.
        </p>
        <p className={`api-status api-status--${apiState}`} aria-live="polite">
          API:{' '}
          {apiState === 'checking' && 'verificando'}
          {apiState === 'ok' && 'ok'}
          {apiState === 'error' && 'indisponivel'}
        </p>
        <p className="api-url">GET {HEALTHCHECK_TARGET}</p>
      </section>
    </main>
  )
}

export default App
