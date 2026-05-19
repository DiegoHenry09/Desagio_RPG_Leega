/**
 * Gerente (Camila) — liderança sênior. personas.md §"gerente".
 * Paleta: pele #E8C8A8, blusa verde musgo, cabelo castanho em rabo baixo.
 */
interface Props {
  title?: string
}

export default function Gerente({ title }: Props) {
  const skin = '#E8C8A8'
  const shirt = 'var(--accent-learn)'
  const pants = '#4A4945'
  const hair = '#6B5544'

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
      <ellipse cx="100" cy="310" rx="50" ry="6" fill="#000" opacity="0.08" />
      <rect x="76" y="202" width="48" height="98" rx="6" fill={pants} />
      <path
        d="M 58 112 Q 100 92 142 112 L 150 214 Q 100 224 50 214 Z"
        fill={shirt}
      />
      <rect x="92" y="80" width="16" height="18" fill={skin} />
      <circle cx="100" cy="58" r="28" fill={skin} />
      {/* Cabelo puxado para trás com rabo baixo */}
      <path d="M 72 50 Q 100 26 128 50 L 128 64 Q 100 50 72 64 Z" fill={hair} />
      <path d="M 100 86 Q 108 88 110 102 L 100 100 Z" fill={hair} />
      <circle cx="92" cy="60" r="2" fill="#1F2937" />
      <circle cx="108" cy="60" r="2" fill="#1F2937" />
      {/* Sorriso sutil */}
      <path
        d="M 92 72 Q 100 76 108 72"
        stroke="#1F2937"
        strokeWidth="1.5"
        fill="none"
        strokeLinecap="round"
      />
      {/* Caneca de café (acessório opcional do prompt) */}
      <rect x="116" y="174" width="22" height="20" rx="2" fill="#FFFFFF" stroke="#1F2937" strokeWidth="1.2" />
      <path d="M 138 178 Q 144 182 138 188" stroke="#1F2937" strokeWidth="1.2" fill="none" />
      <ellipse cx="127" cy="174" rx="11" ry="2" fill="#4A3220" />
    </svg>
  )
}
