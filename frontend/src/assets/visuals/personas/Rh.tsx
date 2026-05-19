/**
 * RH (Patrícia) — apresentadora do onboarding. personas.md §"rh".
 * Paleta: pele #C99878, camisa caramelo, cabelo escuro cacheado, crachá visível.
 */
interface Props {
  title?: string
}

export default function Rh({ title }: Props) {
  const skin = '#C99878'
  const shirt = 'var(--accent-network)'
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
      <rect x="76" y="202" width="48" height="98" rx="6" fill={pants} />
      <path
        d="M 60 112 Q 100 92 140 112 L 148 214 Q 100 224 52 214 Z"
        fill={shirt}
      />
      {/* Crachá visível com fita */}
      <line x1="100" y1="112" x2="100" y2="144" stroke="var(--corp-blue)" strokeWidth="2" />
      <rect x="91" y="144" width="18" height="24" rx="2" fill="#FFFFFF" stroke="var(--corp-blue)" strokeWidth="1.5" />
      <rect x="94" y="148" width="12" height="3" fill="var(--corp-blue-light)" />
      <line x1="94" y1="155" x2="106" y2="155" stroke="#9CA3AF" strokeWidth="0.8" />
      <line x1="94" y1="160" x2="103" y2="160" stroke="#9CA3AF" strokeWidth="0.8" />

      <rect x="92" y="80" width="16" height="18" fill={skin} />
      <circle cx="100" cy="58" r="28" fill={skin} />
      {/* Cabelo cacheado solto */}
      <path
        d="M 68 50 Q 78 24 100 28 Q 122 24 132 50 Q 134 68 128 74 Q 124 64 120 70 Q 118 60 112 66 Q 110 56 100 60 Q 90 56 88 66 Q 82 60 80 70 Q 76 64 72 74 Q 66 68 68 50 Z"
        fill={hair}
      />
      <circle cx="92" cy="60" r="2" fill="#1F2937" />
      <circle cx="108" cy="60" r="2" fill="#1F2937" />
      <path
        d="M 92 72 Q 100 76 108 72"
        stroke="#1F2937"
        strokeWidth="1.5"
        fill="none"
        strokeLinecap="round"
      />
    </svg>
  )
}
