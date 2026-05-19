/**
 * Registry de personas. Adicionar uma persona nova exige:
 *   1) Criar componente em assets/visuals/personas/<Nome>.tsx
 *   2) Adicionar entry aqui
 *   3) Atualizar Referencia_front_RPG/personas.md
 *   4) Atualizar event-visuals-map se aparecer em algum evento
 */
import type { ComponentType } from 'react'
import type { TraineeVariant } from '../../../state/sessionStorage'

import Colega from './Colega'
import Gerente from './Gerente'
import Gestor from './Gestor'
import LiderExterno from './LiderExterno'
import Rh from './Rh'
import Senior from './Senior'
import Trainee from './Trainee'

export type PersonaId =
  | 'trainee'
  | 'gestor'
  | 'gerente'
  | 'colega'
  | 'rh'
  | 'senior'
  | 'lider-externo'

export interface PersonaComponentProps {
  variant?: TraineeVariant
  title?: string
}

export const personas: Record<PersonaId, ComponentType<PersonaComponentProps>> = {
  trainee: Trainee,
  gestor: Gestor,
  gerente: Gerente,
  colega: Colega,
  rh: Rh,
  senior: Senior,
  'lider-externo': LiderExterno,
}

/**
 * Títulos acessíveis (SVG / leitor de tela). Nomes alinhados a
 * `Referencia_front_RPG/personas.md` e SKILL `corporate-survivor-visuals`.
 */
export const personaLabels: Record<PersonaId, string> = {
  trainee: 'Trainee (você)',
  gestor: 'Rafael — gestor direto',
  gerente: 'Camila — gerente da área',
  colega: 'Bruno ou Marina — colega de time',
  rh: 'Patrícia — RH',
  senior: 'Eduardo — mentor sênior',
  'lider-externo': 'Ana — líder de outra área',
}

/** Primeiro nome (ou rótulo curto) para falas na UI de evento. */
export const personaDialogueNames: Record<PersonaId, string> = {
  trainee: '',
  gestor: 'Rafael',
  gerente: 'Camila',
  colega: 'Bruno / Marina',
  rh: 'Patrícia',
  senior: 'Eduardo',
  'lider-externo': 'Ana',
}

/** Nome exibido no bloco de diálogo: jogador quando a fala é do trainee. */
export function dialogueSpeakerName(
  persona: PersonaId,
  playerName: string,
): string {
  if (persona === 'trainee') {
    const t = playerName.trim()
    return t.length > 0 ? t : 'Você'
  }
  return personaDialogueNames[persona]
}
