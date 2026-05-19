/**
 * Pontos de ancoragem de personas em cada cena.
 * Fonte: Referencia_front_RPG/scenes.md — uma entrada por cena.
 *
 * Valores em fração [0..1] de width/height da cena (viewBox 800x400).
 * O <PersonaSVG> usa translate(-50%, -100%) para que o ponto seja o "pé"
 * da persona. Esses anchors NÃO são regra de jogo — só posicionamento visual.
 */
import type { SceneId } from './scenes/_index'

export interface Anchor {
  x: number
  y: number
}

const FALLBACK: Anchor[] = [{ x: 0.5, y: 0.82 }]

export const sceneAnchors: Record<SceneId, Anchor[]> = {
  'sala-reuniao': [
    { x: 0.22, y: 0.86 },
    { x: 0.5, y: 0.78 },
    { x: 0.78, y: 0.86 },
  ],
  'mesa-trabalho': [
    { x: 0.3, y: 0.94 },
    { x: 0.55, y: 0.94 },
    { x: 0.8, y: 0.86 },
  ],
  restaurante: [
    { x: 0.3, y: 0.78 },
    { x: 0.7, y: 0.78 },
    { x: 0.5, y: 0.62 },
  ],
  bar: [
    { x: 0.27, y: 0.92 },
    { x: 0.52, y: 0.92 },
    { x: 0.76, y: 0.92 },
  ],
  banheiro: [{ x: 0.55, y: 0.92 }],
  'sala-apresentacao': [{ x: 0.5, y: 0.86 }],
  copa: [
    { x: 0.32, y: 0.92 },
    { x: 0.56, y: 0.9 },
    { x: 0.8, y: 0.92 },
  ],
  _default: [{ x: 0.5, y: 0.86 }],
}

export function getAnchorsFor(sceneId: SceneId): Anchor[] {
  return sceneAnchors[sceneId] ?? FALLBACK
}
