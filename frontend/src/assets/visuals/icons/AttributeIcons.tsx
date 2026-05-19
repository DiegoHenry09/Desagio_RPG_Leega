/**
 * Ícones SVG inline dos 6 atributos. style-guide.md §8.
 * Cada ícone usa currentColor para herdar a cor do contexto.
 * Sem dependência externa (sem lucide-react).
 */
import type { ReactNode, SVGProps } from 'react'

type IconProps = SVGProps<SVGSVGElement>

function Base({ children, ...rest }: IconProps & { children: ReactNode }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      width="20"
      height="20"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
      {...rest}
    >
      {children}
    </svg>
  )
}

export function EnergiaIcon(props: IconProps) {
  return (
    <Base {...props}>
      <path d="M13 3 L5 14 L11 14 L10 21 L19 10 L13 10 Z" />
    </Base>
  )
}

export function ReputacaoIcon(props: IconProps) {
  return (
    <Base {...props}>
      <path d="M12 3.5 L14.5 9 L20 9.5 L16 13.5 L17.2 19 L12 16.3 L6.8 19 L8 13.5 L4 9.5 L9.5 9 Z" />
    </Base>
  )
}

export function NetworkingIcon(props: IconProps) {
  return (
    <Base {...props}>
      <circle cx="8" cy="12" r="4" />
      <circle cx="16" cy="12" r="4" />
      <line x1="11.2" y1="12" x2="12.8" y2="12" />
    </Base>
  )
}

export function AnsiedadeIcon(props: IconProps) {
  return (
    <Base {...props}>
      <path d="M2 12 Q 5 8 8 12 T 14 12 T 20 12 T 22 12" />
      <path d="M2 16 Q 5 12 8 16 T 14 16 T 20 16 T 22 16" opacity="0.5" />
    </Base>
  )
}

export function ProdutividadeIcon(props: IconProps) {
  return (
    <Base {...props}>
      <rect x="4" y="4" width="16" height="16" rx="2" />
      <path d="M8 12 L11 15 L16 9" />
    </Base>
  )
}

export function AprendizadoIcon(props: IconProps) {
  return (
    <Base {...props}>
      <path d="M4 6 L12 4 L20 6 L20 18 L12 16 L4 18 Z" />
      <line x1="12" y1="4" x2="12" y2="16" />
    </Base>
  )
}
