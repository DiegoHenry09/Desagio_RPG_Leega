/**
 * Cena: sala-apresentacao. scenes.md §"sala-apresentacao".
 * Tela de projeção centralizada, slide neutro, fileiras de cadeiras parciais.
 * Plateia em ~15 silhuetas (alinhado ao texto do evento ev_day5_001 no catálogo).
 */
const AUDIENCE_COUNT = 15

export default function SalaApresentacao() {
  const seatW = 20
  const gap = 5
  const totalW = AUDIENCE_COUNT * seatW + (AUDIENCE_COUNT - 1) * gap
  const startX = (800 - totalW) / 2
  const baseY = 322

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 800 400"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <rect x="0" y="0" width="800" height="280" fill="var(--bg-muted)" />
      <rect x="0" y="280" width="800" height="120" fill="#D8D2C5" />
      {/* Tela de projeção grande */}
      <rect x="200" y="40" width="400" height="200" rx="2" fill="#FFFFFF" stroke="#1F2937" strokeWidth="3" />
      {/* Slide neutro (retângulos abstratos) */}
      <rect x="232" y="80" width="160" height="20" fill="var(--corp-blue-light)" />
      <rect x="232" y="120" width="240" height="10" fill="var(--bg-muted)" />
      <rect x="232" y="140" width="200" height="10" fill="var(--bg-muted)" />
      <rect x="232" y="170" width="80" height="40" fill="var(--accent-energy)" opacity="0.5" />
      <rect x="324" y="170" width="80" height="40" fill="var(--accent-rep)" opacity="0.5" />
      <rect x="416" y="170" width="80" height="40" fill="var(--accent-learn)" opacity="0.5" />
      {/* Luz frontal da tela */}
      <path d="M 200 240 L 600 240 L 700 360 L 100 360 Z" fill="#FFFFFF" opacity="0.1" />
      {/* Fileira de plateia (~15 lugares, vista de costas) */}
      {Array.from({ length: AUDIENCE_COUNT }, (_, i) => {
        const x = startX + i * (seatW + gap)
        const opacity = 0.48 + (i % 4) * 0.06
        return (
          <rect
            key={i}
            x={x}
            y={baseY}
            width={seatW}
            height={32}
            rx={3}
            fill="#3B5B7C"
            opacity={opacity}
          />
        )
      })}
    </svg>
  )
}
