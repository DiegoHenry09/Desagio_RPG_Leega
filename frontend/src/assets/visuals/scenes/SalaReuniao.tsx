/**
 * Cena: sala-reuniao. scenes.md §"sala-reuniao".
 * Elementos: mesa oval grande, cadeiras, janela com luz, projetor lateral.
 */
export default function SalaReuniao() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 800 400"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      {/* Parede / fundo */}
      <rect x="0" y="0" width="800" height="280" fill="var(--bg-muted)" />
      {/* Chão */}
      <rect x="0" y="280" width="800" height="120" fill="#D8D2C5" />
      {/* Janela ao fundo com luz suave */}
      <rect x="540" y="40" width="220" height="140" rx="4" fill="#E8E4DD" stroke="#B5AFA1" strokeWidth="2" />
      <rect x="544" y="44" width="104" height="132" fill="#F5F2E8" opacity="0.85" />
      <rect x="652" y="44" width="104" height="132" fill="#F5F2E8" opacity="0.85" />
      <line x1="650" y1="44" x2="650" y2="176" stroke="#B5AFA1" strokeWidth="2" />
      <line x1="540" y1="110" x2="760" y2="110" stroke="#B5AFA1" strokeWidth="1.5" />
      {/* Luz entrando da janela */}
      <path d="M 540 180 L 760 180 L 700 280 L 580 280 Z" fill="#FFFFFF" opacity="0.12" />
      {/* Tela de projeção lateral esquerda */}
      <rect x="40" y="50" width="160" height="100" fill="#FFFFFF" stroke="#1F2937" strokeWidth="2" />
      <rect x="56" y="68" width="40" height="10" fill="var(--corp-blue-light)" />
      <rect x="56" y="86" width="80" height="6" fill="var(--bg-muted)" />
      <rect x="56" y="100" width="60" height="6" fill="var(--bg-muted)" />
      <rect x="56" y="114" width="70" height="6" fill="var(--bg-muted)" />
      {/* Mesa oval grande */}
      <ellipse cx="400" cy="320" rx="280" ry="60" fill="#9C8B6E" />
      <ellipse cx="400" cy="312" rx="280" ry="56" fill="#B59E78" />
      {/* Cadeiras sugeridas (backs) */}
      <rect x="170" y="296" width="32" height="40" rx="4" fill="#3B5B7C" opacity="0.85" />
      <rect x="240" y="290" width="32" height="44" rx="4" fill="#3B5B7C" opacity="0.85" />
      <rect x="528" y="290" width="32" height="44" rx="4" fill="#3B5B7C" opacity="0.85" />
      <rect x="598" y="296" width="32" height="40" rx="4" fill="#3B5B7C" opacity="0.85" />
      {/* Cadeira oposta visível (cabeceira) */}
      <rect x="380" y="266" width="40" height="38" rx="4" fill="#3B5B7C" opacity="0.7" />
    </svg>
  )
}
