/**
 * Mapeamento evento → cena + personas.
 *
 * Fonte canônica: Referencia_front_RPG/event-visuals-map.md.
 *
 * IMPORTANTE: este mapa é **camada de apresentação do frontend**.
 *   - NÃO é regra de jogo.
 *   - NÃO é catálogo de eventos (este vive em backend/engine/data/events.json).
 *   - O backend nunca usa esse arquivo.
 *
 * Quando a API começar a expor `visuals` no EventPayload (sprint futura),
 * a UI deve priorizar `event.visuals ?? eventVisuals[event.id] ?? defaultVisual`.
 */
import type { PersonaId } from './personas/_index'
import type { SceneId } from './scenes/_index'

export interface EventVisual {
  scene: SceneId
  personas: PersonaId[]
}

export const eventVisuals: Record<string, EventVisual> = {
  ev_day1_001: { scene: 'sala-reuniao', personas: ['rh', 'trainee'] },
  ev_day1_002: { scene: 'restaurante', personas: ['colega', 'trainee'] },
  ev_day1_003: { scene: 'mesa-trabalho', personas: ['trainee'] },

  ev_day2_001: { scene: 'mesa-trabalho', personas: ['gestor', 'trainee'] },
  ev_day2_002: { scene: 'mesa-trabalho', personas: ['colega', 'trainee'] },
  ev_day2_003: { scene: 'sala-reuniao', personas: ['senior', 'trainee', 'gestor'] },

  ev_day3_001: { scene: 'sala-reuniao', personas: ['gestor', 'trainee', 'colega'] },
  ev_day3_002: { scene: 'bar', personas: ['colega', 'trainee'] },
  ev_day3_003: { scene: 'mesa-trabalho', personas: ['trainee'] },

  ev_day4_001: { scene: 'mesa-trabalho', personas: ['senior', 'trainee'] },
  ev_day4_002: { scene: 'mesa-trabalho', personas: ['trainee'] },
  ev_day4_003: { scene: 'sala-reuniao', personas: ['gerente', 'trainee'] },

  ev_day5_001: { scene: 'sala-apresentacao', personas: ['trainee'] },
  ev_day5_002: { scene: 'restaurante', personas: ['gerente', 'trainee'] },
  ev_day5_003: { scene: 'mesa-trabalho', personas: ['trainee'] },

  ev_secret_001: { scene: 'mesa-trabalho', personas: ['lider-externo', 'trainee'] },
  ev_secret_002: { scene: 'banheiro', personas: ['trainee'] },
}

export const defaultVisual: EventVisual = {
  scene: '_default',
  personas: ['trainee'],
}

export function getEventVisual(eventId: string | null | undefined): EventVisual {
  if (!eventId) return defaultVisual
  return eventVisuals[eventId] ?? defaultVisual
}
