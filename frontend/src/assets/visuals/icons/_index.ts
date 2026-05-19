/**
 * Registry de ícones, labels e cores por atributo.
 *
 * Cor não é único veículo de informação (style-guide §1.4): cada barra do
 * AttributePanel mostra ícone + label + número + cor.
 */
import type { ComponentType, SVGProps } from 'react'

import type { AttributeId } from '../../../api/types'
import {
  AnsiedadeIcon,
  AprendizadoIcon,
  EnergiaIcon,
  NetworkingIcon,
  ProdutividadeIcon,
  ReputacaoIcon,
} from './AttributeIcons'

export type AttributeIconComponent = ComponentType<SVGProps<SVGSVGElement>>

export const attributeIcons: Record<AttributeId, AttributeIconComponent> = {
  energia: EnergiaIcon,
  reputacao: ReputacaoIcon,
  networking: NetworkingIcon,
  ansiedade: AnsiedadeIcon,
  produtividade: ProdutividadeIcon,
  aprendizado: AprendizadoIcon,
}

export const attributeLabels: Record<AttributeId, string> = {
  energia: 'Energia',
  reputacao: 'Reputação',
  networking: 'Networking',
  ansiedade: 'Ansiedade',
  produtividade: 'Produtividade',
  aprendizado: 'Aprendizado',
}

export const attributeColors: Record<AttributeId, string> = {
  energia: 'var(--accent-energy)',
  reputacao: 'var(--accent-rep)',
  networking: 'var(--accent-network)',
  ansiedade: 'var(--accent-anxiety)',
  produtividade: 'var(--accent-prod)',
  aprendizado: 'var(--accent-learn)',
}
