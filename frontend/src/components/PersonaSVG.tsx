import { personaLabels, personas, type PersonaId } from '../assets/visuals/personas/_index'
import type { TraineeVariant } from '../state/sessionStorage'

interface Props {
  personaId: PersonaId
  variant?: TraineeVariant
  title?: string
}

export default function PersonaSVG({ personaId, variant, title }: Props) {
  const Component = personas[personaId]
  if (!Component) {
    return null
  }
  const accessibleTitle = title ?? personaLabels[personaId]
  return <Component variant={variant} title={accessibleTitle} />
}
