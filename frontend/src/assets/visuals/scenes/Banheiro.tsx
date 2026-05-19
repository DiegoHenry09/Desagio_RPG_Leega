/**
 * Cena: banheiro. scenes.md §"banheiro" (tema sensível — sem dramatização).
 * Pia, espelho grande, azulejo cinza, iluminação fria. Tom introspectivo.
 */
export default function Banheiro() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 800 400"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      {/* Parede de azulejo cinza */}
      <rect x="0" y="0" width="800" height="400" fill="#C7CAD0" />
      {/* Grid de azulejo */}
      {Array.from({ length: 10 }).map((_, i) => (
        <line
          key={`v-${i}`}
          x1={i * 80}
          y1="0"
          x2={i * 80}
          y2="400"
          stroke="#A8ACB2"
          strokeWidth="1"
          opacity="0.6"
        />
      ))}
      {Array.from({ length: 6 }).map((_, i) => (
        <line
          key={`h-${i}`}
          x1="0"
          y1={i * 80}
          x2="800"
          y2={i * 80}
          stroke="#A8ACB2"
          strokeWidth="1"
          opacity="0.6"
        />
      ))}
      {/* Espelho grande */}
      <rect x="240" y="40" width="320" height="180" rx="2" fill="#D8DCE2" stroke="#7A7F87" strokeWidth="3" />
      <rect x="248" y="48" width="304" height="164" fill="#E0E4EA" opacity="0.6" />
      {/* Silhueta sugerida no espelho */}
      <path d="M 380 130 Q 400 110 420 130 L 416 200 L 384 200 Z" fill="#9CA3AF" opacity="0.35" />
      {/* Pia */}
      <rect x="200" y="240" width="400" height="50" rx="6" fill="#F5F4F0" stroke="#7A7F87" strokeWidth="2" />
      <ellipse cx="400" cy="270" rx="80" ry="14" fill="#D8DCE2" />
      {/* Torneira */}
      <rect x="394" y="218" width="12" height="22" fill="#7A7F87" />
      <rect x="386" y="218" width="28" height="6" rx="2" fill="#7A7F87" />
      {/* Sabonete */}
      <rect x="540" y="232" width="40" height="14" rx="6" fill="var(--accent-positive)" opacity="0.7" />
      {/* Bancada */}
      <rect x="100" y="288" width="600" height="14" fill="#7A7F87" />
      <rect x="100" y="302" width="600" height="98" fill="#D8DCE2" />
    </svg>
  )
}
