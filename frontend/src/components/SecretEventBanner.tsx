import './SecretEventBanner.css'

interface Props {
  secretEventTitle: string
  onDismiss: () => void
}

/**
 * Aviso discreto quando o backend devolve `inject_secret_event`.
 *
 * Sprint 3.0: NÃO implementamos fluxo completo de escolha secreta. Apenas
 * sinalizamos para o jogador que algo especial aconteceu. A engine ainda
 * não expõe `apply_secret_choice` (backlog) — quando expuser, o frontend
 * apresentará a opção real aqui em sprint futura.
 */
export default function SecretEventBanner({ secretEventTitle, onDismiss }: Props) {
  return (
    <aside className="cs-secret-banner" role="status" aria-live="polite">
      <div className="cs-secret-banner__body">
        <strong className="cs-secret-banner__title">Evento especial desbloqueado</strong>
        <p className="cs-secret-banner__text">
          {secretEventTitle}. O fluxo completo deste evento será tratado em uma sprint futura.
        </p>
      </div>
      <button
        type="button"
        className="cs-secret-banner__dismiss"
        onClick={onDismiss}
        aria-label="Fechar aviso de evento especial"
      >
        Entendi
      </button>
    </aside>
  )
}
