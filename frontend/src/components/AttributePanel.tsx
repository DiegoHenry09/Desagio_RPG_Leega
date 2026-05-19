import { useEffect, useState } from 'react'

import type { AttributeId, Attributes } from '../api/types'
import {
  attributeColors,
  attributeIcons,
  attributeLabels,
} from '../assets/visuals/icons/_index'

import './AttributePanel.css'

interface Props {
  attributes: Attributes
}

const ATTRIBUTE_ORDER: AttributeId[] = [
  'energia',
  'reputacao',
  'networking',
  'ansiedade',
  'produtividade',
  'aprendizado',
]

const PULSE_MS = 700

type Pulse = 'up' | 'down'
type PulseMap = Partial<Record<AttributeId, Pulse>>

function attributesEqual(a: Attributes, b: Attributes): boolean {
  for (const key of ATTRIBUTE_ORDER) {
    if (a[key] !== b[key]) return false
  }
  return true
}

function diffPulses(prev: Attributes, next: Attributes): PulseMap {
  const result: PulseMap = {}
  for (const key of ATTRIBUTE_ORDER) {
    const delta = next[key] - prev[key]
    if (delta === 0) continue
    const isPositive = key === 'ansiedade' ? delta < 0 : delta > 0
    result[key] = isPositive ? 'up' : 'down'
  }
  return result
}

/**
 * Painel de atributos.
 *
 * IMPORTANTE: o "delta" exibido visualmente NÃO é regra de jogo. É apenas
 * a diferença entre o último snapshot recebido do backend e o atual, capturada
 * pelo próprio componente para disparar uma microanimação CSS. Score, ending
 * e consequence continuam exclusivos do backend.
 */
export default function AttributePanel({ attributes }: Props) {
  const [lastSeen, setLastSeen] = useState<Attributes>(attributes)
  const [pulses, setPulses] = useState<PulseMap>({})

  // Update during render: detectamos a mudança ANTES do efeito para evitar
  // set-state-in-effect cascading. Padrão recomendado pela React docs em
  // "Storing information from previous renders".
  if (!attributesEqual(lastSeen, attributes)) {
    const computed = diffPulses(lastSeen, attributes)
    setLastSeen(attributes)
    setPulses(computed)
  }

  useEffect(() => {
    if (Object.keys(pulses).length === 0) return
    const timer = setTimeout(() => setPulses({}), PULSE_MS)
    return () => clearTimeout(timer)
  }, [pulses])

  return (
    <section className="cs-attr-panel" aria-label="Painel de atributos">
      <h2 className="cs-attr-panel__title">Atributos</h2>
      <ul className="cs-attr-panel__list">
        {ATTRIBUTE_ORDER.map((id) => {
          const Icon = attributeIcons[id]
          const value = attributes[id]
          const pulse = pulses[id]
          const inverted = id === 'ansiedade'
          const percent = Math.max(0, Math.min(100, (value / 10) * 100))
          return (
            <li
              key={id}
              className={[
                'cs-attr-panel__row',
                pulse ? `cs-attr-panel__row--${pulse}` : '',
              ]
                .filter(Boolean)
                .join(' ')}
              style={{ color: attributeColors[id] }}
            >
              <span className="cs-attr-panel__icon" aria-hidden="true">
                <Icon />
              </span>
              <span className="cs-attr-panel__label">{attributeLabels[id]}</span>
              <span
                className="cs-attr-panel__bar"
                role="progressbar"
                aria-label={`${attributeLabels[id]} ${value} de 10`}
                aria-valuemin={0}
                aria-valuemax={10}
                aria-valuenow={value}
              >
                <span
                  className="cs-attr-panel__bar-fill"
                  style={{ width: `${percent}%`, background: attributeColors[id] }}
                />
              </span>
              <span className="cs-attr-panel__value">
                {value}
                {inverted ? (
                  <span className="cs-attr-panel__hint" aria-label="alto é ruim">
                    !
                  </span>
                ) : null}
              </span>
            </li>
          )
        })}
      </ul>
    </section>
  )
}
