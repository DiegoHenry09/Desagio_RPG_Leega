import type { OptionId, OptionPayload } from '../api/types'

import './ChoiceList.css'

interface Props {
  options: OptionPayload[]
  onChoose: (optionId: OptionId) => void
  disabled?: boolean
  selectedId?: OptionId | null
}

/**
 * Lista de opções de uma escolha.
 *
 * `OptionPayload` deliberadamente NÃO inclui `consequences` (api.md
 * §"Invariante de segurança"). O frontend só mostra `id + label`.
 */
export default function ChoiceList({ options, onChoose, disabled, selectedId }: Props) {
  return (
    <fieldset
      className="cs-choices"
      disabled={disabled}
      aria-label="Opções de escolha"
    >
      <legend className="cs-choices__legend">Sua escolha</legend>
      <ul className="cs-choices__list">
        {options.map((option) => {
          const isSelected = selectedId === option.id
          return (
            <li key={option.id}>
              <button
                type="button"
                className={[
                  'cs-choices__button',
                  isSelected ? 'cs-choices__button--selected' : '',
                ]
                  .filter(Boolean)
                  .join(' ')}
                onClick={() => onChoose(option.id)}
                aria-pressed={isSelected}
              >
                <span className="cs-choices__button-id" aria-hidden="true">
                  {option.id}
                </span>
                <span className="cs-choices__button-label">{option.label}</span>
              </button>
            </li>
          )
        })}
      </ul>
    </fieldset>
  )
}
