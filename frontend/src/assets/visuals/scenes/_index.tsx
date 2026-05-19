/**
 * Registry de cenas. Para adicionar nova cena:
 *   1) Criar componente em assets/visuals/scenes/<Nome>.tsx (viewBox 800x400)
 *   2) Adicionar entry aqui
 *   3) Adicionar anchors em sceneAnchors.ts
 *   4) Atualizar Referencia_front_RPG/scenes.md
 */
import type { ComponentType } from 'react'

import Bar from './Bar'
import Banheiro from './Banheiro'
import Copa from './Copa'
import DefaultScene from './DefaultScene'
import MesaTrabalho from './MesaTrabalho'
import Restaurante from './Restaurante'
import SalaApresentacao from './SalaApresentacao'
import SalaReuniao from './SalaReuniao'

export type SceneId =
  | 'sala-reuniao'
  | 'mesa-trabalho'
  | 'restaurante'
  | 'bar'
  | 'banheiro'
  | 'sala-apresentacao'
  | 'copa'
  | '_default'

export const scenes: Record<SceneId, ComponentType> = {
  'sala-reuniao': SalaReuniao,
  'mesa-trabalho': MesaTrabalho,
  restaurante: Restaurante,
  bar: Bar,
  banheiro: Banheiro,
  'sala-apresentacao': SalaApresentacao,
  copa: Copa,
  _default: DefaultScene,
}
