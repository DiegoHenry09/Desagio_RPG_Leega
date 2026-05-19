/**
 * Líder Externo (Ana) — líder de outra área. personas.md §"lider-externo".
 * Paleta: pele #6B4533, blazer escuro sobre blusa clara, cabelo natural curto.
 */
interface Props {
  title?: string
}

export default function LiderExterno({ title }: Props) {
  const skin = '#6B4533'
  const blazer = '#1F2937'
  const blouse = '#F5F4F0'
  const pants = '#1F2937'
  const hair = '#1A1614'

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
      <rect x="76" y="204" width="48" height="96" rx="6" fill={pants} />
      {/* Blusa clara (parte interna) */}
      <path d="M 80 116 Q 100 112 120 116 L 120 200 Q 100 206 80 200 Z" fill={blouse} />
      {/* Blazer aberto (lateral) */}
      <path d="M 56 114 Q 80 110 80 130 L 80 212 Q 60 218 50 214 Z" fill={blazer} />
      <path d="M 144 114 Q 120 110 120 130 L 120 212 Q 140 218 150 214 Z" fill={blazer} />
      <rect x="92" y="80" width="16" height="18" fill={skin} />
      <circle cx="100" cy="58" r="28" fill={skin} />
      {/* Cabelo natural curto */}
      <path
        d="M 72 50 Q 78 30 100 28 Q 122 30 128 50 Q 130 60 128 64 Q 122 50 100 52 Q 78 50 72 64 Q 70 60 72 50 Z"
        fill={hair}
      />
      <circle cx="92" cy="60" r="2" fill="#1F2937" />
      <circle cx="108" cy="60" r="2" fill="#1F2937" />
      {/* Sorriso genuíno */}
      <path
        d="M 91 72 Q 100 78 109 72"
        stroke="#1F2937"
        strokeWidth="1.5"
        fill="none"
        strokeLinecap="round"
      />
    </svg>
  )
}
