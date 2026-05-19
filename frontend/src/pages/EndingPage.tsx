import type { SessionResponse } from '../api/types'
import EndingView from '../components/EndingView'
import { clearSessionId, getTraineeVariant } from '../state/sessionStorage'

interface Props {
  session: SessionResponse
  onViewRanking: () => void
  onNewJourney: () => void
}

export default function EndingPage({ session, onViewRanking, onNewJourney }: Props) {
  const traineeVariant = getTraineeVariant()
  return (
    <EndingView
      session={session}
      traineeVariant={traineeVariant}
      onViewRanking={onViewRanking}
      onNewJourney={() => {
        clearSessionId()
        onNewJourney()
      }}
    />
  )
}
