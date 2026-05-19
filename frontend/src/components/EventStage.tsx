import { getEventVisual } from '../assets/visuals/eventVisualsMap'
import { getAnchorsFor } from '../assets/visuals/sceneAnchors'
import type { EventPayload } from '../api/types'
import type { TraineeVariant } from '../state/sessionStorage'

import PersonaSVG from './PersonaSVG'
import SceneSVG from './SceneSVG'
import './EventStage.css'

interface Props {
  event: EventPayload
  traineeVariant?: TraineeVariant
}

export default function EventStage({ event, traineeVariant }: Props) {
  const visual = getEventVisual(event.id)
  const anchors = getAnchorsFor(visual.scene)
  const visiblePersonas = visual.personas.slice(0, anchors.length)
  const altDescription = `Cena: ${visual.scene.replace(/-/g, ' ')}. ${event.title}.`

  return (
    <div
      className="cs-event-stage"
      role="img"
      aria-label={altDescription}
      data-scene={visual.scene}
    >
      <div className="cs-event-stage__scene">
        <SceneSVG sceneId={visual.scene} />
      </div>
      {visiblePersonas.map((personaId, idx) => {
        const anchor = anchors[idx]
        return (
          <div
            key={`${event.id}-${personaId}-${idx}`}
            className="cs-event-stage__persona"
            style={{ left: `${anchor.x * 100}%`, top: `${anchor.y * 100}%` }}
          >
            <PersonaSVG
              personaId={personaId}
              variant={personaId === 'trainee' ? traineeVariant : undefined}
            />
          </div>
        )
      })}
    </div>
  )
}
