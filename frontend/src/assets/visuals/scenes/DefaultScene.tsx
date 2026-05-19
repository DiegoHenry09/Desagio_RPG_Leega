/**
 * Cena: _default. scenes.md §"_default".
 * Fundo neutro com padrão sutil de pontos. Usado quando o event_id é
 * desconhecido ou ainda não tem visual mapeado.
 */
export default function DefaultScene() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 800 400"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <rect x="0" y="0" width="800" height="400" fill="var(--bg-base)" />
      <pattern id="cs-dots" x="0" y="0" width="32" height="32" patternUnits="userSpaceOnUse">
        <circle cx="16" cy="16" r="1.5" fill="#C2BDB3" opacity="0.55" />
      </pattern>
      <rect x="0" y="0" width="800" height="400" fill="url(#cs-dots)" />
      <rect x="0" y="300" width="800" height="100" fill="var(--bg-muted)" opacity="0.45" />
    </svg>
  )
}
