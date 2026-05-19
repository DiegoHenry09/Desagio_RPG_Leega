/**
 * Senior (Eduardo) — mentor sênior. personas.md §"senior".
 * Paleta: pele #DDB69A, camisa cinza-azulado, cabelo grisalho, barba curta.
 */
interface Props {
  title?: string
}

export default function Senior({ title }: Props) {
  const skin = '#DDB69A'
  const shirt = '#4A5568'
  const pants = '#2D3748'
  const hair = '#8A8580'

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
      <ellipse cx="100" cy="310" rx="52" ry="6" fill="#000" opacity="0.08" />
      <rect x="72" y="202" width="56" height="98" rx="6" fill={pants} />
      <path
        d="M 54 114 Q 100 92 146 114 L 154 216 Q 100 226 46 216 Z"
        fill={shirt}
      />
      <rect x="92" y="80" width="16" height="18" fill={skin} />
      <circle cx="100" cy="58" r="28" fill={skin} />
      {/* Cabelo grisalho curto */}
      <path d="M 74 50 Q 100 32 126 50 L 126 62 Q 100 50 74 62 Z" fill={hair} />
      {/* Barba curta grisalha */}
      <path d="M 80 70 Q 100 86 120 70 Q 120 84 100 88 Q 80 84 80 70 Z" fill={hair} opacity="0.85" />
      <circle cx="92" cy="60" r="2" fill="#1F2937" />
      <circle cx="108" cy="60" r="2" fill="#1F2937" />
      {/* Boca neutra-séria */}
      <line x1="93" y1="76" x2="107" y2="76" stroke="#1F2937" strokeWidth="1.4" strokeLinecap="round" />
      {/* Linha de óculos sutil */}
      <circle cx="92" cy="60" r="6" fill="none" stroke="#1F2937" strokeWidth="1" opacity="0.6" />
      <circle cx="108" cy="60" r="6" fill="none" stroke="#1F2937" strokeWidth="1" opacity="0.6" />
      <line x1="98" y1="60" x2="102" y2="60" stroke="#1F2937" strokeWidth="1" opacity="0.6" />
    </svg>
  )
}
