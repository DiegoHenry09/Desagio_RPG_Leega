import { scenes, type SceneId } from '../assets/visuals/scenes/_index'

interface Props {
  sceneId: SceneId
}

export default function SceneSVG({ sceneId }: Props) {
  const Component = scenes[sceneId] ?? scenes._default
  return <Component />
}
