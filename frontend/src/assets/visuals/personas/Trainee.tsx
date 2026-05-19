/**
 * Trainee — placeholder geométrico do protagonista.
 *
 * Três variantes (1, 2, 3) variam pele e cabelo para projeção do jogador,
 * conforme personas.md §"trainee". A variante é sorteada uma vez por player
 * e persistida em localStorage (state/sessionStorage.ts).
 *
 * Viewbox 0 0 200 320 conforme SKILL.md e asset-pipeline.md §"Opção D".
 */
import type { TraineeVariant } from '../../../state/sessionStorage'

interface Props {
  variant?: TraineeVariant
  title?: string
}

const SKIN: Record<TraineeVariant, string> = {
  1: '#D4A574',
  2: '#A86F4A',
  3: '#E8C8A8',
}

const HAIR: Record<TraineeVariant, string> = {
  1: '#2D2A28',
  2: '#1A1614',
  3: '#6B5544',
}

export default function Trainee({ variant = 1, title }: Props) {
  const skin = SKIN[variant]
  const hair = HAIR[variant]
  const shirt = 'var(--accent-energy)'
  const pants = '#2D3748'

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
      <rect x="75" y="200" width="50" height="100" rx="6" fill={pants} />
      <path
        d="M 60 110 Q 100 92 140 110 L 148 212 Q 100 222 52 212 Z"
        fill={shirt}
      />
      <rect x="92" y="80" width="16" height="18" fill={skin} />
      <circle cx="100" cy="60" r="28" fill={skin} />
      <path d="M 75 50 Q 100 28 125 50 L 125 64 Q 100 50 75 64 Z" fill={hair} />
      <circle cx="92" cy="62" r="2" fill="#1F2937" />
      <circle cx="108" cy="62" r="2" fill="#1F2937" />
      <path
        d="M 94 72 Q 100 75 106 72"
        stroke="#1F2937"
        strokeWidth="1.5"
        fill="none"
        strokeLinecap="round"
      />
      {/* Caderno (acessório recorrente) */}
      <rect x="110" y="170" width="22" height="30" rx="2" fill="#FFFFFF" stroke="#1F2937" strokeWidth="1" />
      <line x1="113" y1="178" x2="129" y2="178" stroke="#9CA3AF" strokeWidth="0.8" />
      <line x1="113" y1="184" x2="129" y2="184" stroke="#9CA3AF" strokeWidth="0.8" />
      <line x1="113" y1="190" x2="125" y2="190" stroke="#9CA3AF" strokeWidth="0.8" />
    </svg>
  )
}
