/**
 * Colega (Bruno/Marina) — par no time. personas.md §"colega".
 * Implementamos a variante Marina (camiseta básica, postura relaxada).
 * Frontend pode alternar variante por evento em sprint futura.
 */
interface Props {
  title?: string
}

export default function Colega({ title }: Props) {
  const skin = '#D4A574'
  const shirt = 'var(--accent-negative)'
  const pants = '#2D3748'
  const hair = '#2D2A28'

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 200 320"
      role={title ? 'img' : undefined}
      aria-hidden={title ? undefined : true}
      aria-label={title}
      preserveAspectRatio="xMidYMax meet"
    >
      {title ? <title>{title}</title> : null}
      <ellipse cx="100" cy="310" rx="48" ry="6" fill="#000" opacity="0.08" />
      <rect x="78" y="202" width="44" height="98" rx="6" fill={pants} />
      <path
        d="M 62 112 Q 100 94 138 112 L 144 214 Q 100 224 56 214 Z"
        fill={shirt}
      />
      <rect x="92" y="80" width="16" height="18" fill={skin} />
      <circle cx="100" cy="58" r="28" fill={skin} />
      {/* Cabelo médio com volume */}
      <path d="M 70 50 Q 100 26 130 50 L 132 76 Q 124 70 124 80 L 118 78 L 116 70 L 100 66 L 84 70 L 82 78 L 76 80 Q 76 70 68 76 Z" fill={hair} />
      <circle cx="92" cy="60" r="2" fill="#1F2937" />
      <circle cx="108" cy="60" r="2" fill="#1F2937" />
      <path
        d="M 92 72 Q 100 77 108 72"
        stroke="#1F2937"
        strokeWidth="1.5"
        fill="none"
        strokeLinecap="round"
      />
    </svg>
  )
}
