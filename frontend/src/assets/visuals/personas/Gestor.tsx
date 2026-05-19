/**
 * Gestor (Rafael) — gestor direto. personas.md §"gestor".
 * Paleta: pele #B98A6B, camisa corp-blue, cabelo escuro com têmporas grisalhas.
 */
interface Props {
  title?: string
}

export default function Gestor({ title }: Props) {
  const skin = '#B98A6B'
  const shirt = 'var(--corp-blue)'
  const pants = '#2D3748'
  const hair = '#4A3F3A'
  const grey = '#9A9590'

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
      <rect x="73" y="200" width="54" height="100" rx="6" fill={pants} />
      <path
        d="M 56 112 Q 100 90 144 112 L 152 216 Q 100 226 48 216 Z"
        fill={shirt}
      />
      {/* Crachá pendurado */}
      <line x1="100" y1="112" x2="100" y2="148" stroke="#1F2937" strokeWidth="1" />
      <rect x="92" y="148" width="16" height="22" rx="2" fill="#FFFFFF" stroke="#1F2937" strokeWidth="1" />
      <line x1="95" y1="156" x2="105" y2="156" stroke="#9CA3AF" strokeWidth="0.8" />
      <line x1="95" y1="161" x2="103" y2="161" stroke="#9CA3AF" strokeWidth="0.8" />

      <rect x="92" y="80" width="16" height="18" fill={skin} />
      <circle cx="100" cy="58" r="28" fill={skin} />
      {/* Cabelo curto com têmporas grisalhas */}
      <path d="M 74 50 Q 100 32 126 50 L 126 60 Q 100 50 74 60 Z" fill={hair} />
      <path d="M 74 56 Q 78 50 82 52 L 80 62 Q 76 62 74 60 Z" fill={grey} opacity="0.7" />
      <path d="M 126 56 Q 122 50 118 52 L 120 62 Q 124 62 126 60 Z" fill={grey} opacity="0.7" />
      <circle cx="92" cy="60" r="2" fill="#1F2937" />
      <circle cx="108" cy="60" r="2" fill="#1F2937" />
      <path
        d="M 88 54 Q 92 50 96 54"
        stroke="#1F2937"
        strokeWidth="1.4"
        fill="none"
        strokeLinecap="round"
      />
      <path
        d="M 104 54 Q 108 50 112 54"
        stroke="#1F2937"
        strokeWidth="1.4"
        fill="none"
        strokeLinecap="round"
      />
      <path
        d="M 94 72 L 106 72"
        stroke="#1F2937"
        strokeWidth="1.5"
        fill="none"
        strokeLinecap="round"
      />
    </svg>
  )
}
