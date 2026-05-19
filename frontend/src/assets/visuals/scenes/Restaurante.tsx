/**
 * Cena: restaurante (japonês). scenes.md §"restaurante".
 * Mesa de madeira clara, pratos, hashi sobre hashioki, copo, noren ao fundo.
 */
export default function Restaurante() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 800 400"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      {/* Parede e iluminação amarelada */}
      <rect x="0" y="0" width="800" height="240" fill="#E8DCC0" />
      <rect x="0" y="0" width="800" height="240" fill="#F5E6B8" opacity="0.18" />
      {/* Painel divisor de madeira */}
      <rect x="80" y="0" width="6" height="240" fill="#7A5A3A" />
      <rect x="200" y="0" width="6" height="240" fill="#7A5A3A" />
      <rect x="600" y="0" width="6" height="240" fill="#7A5A3A" />
      {/* Noren (cortina vermelha estilizada) */}
      <rect x="100" y="40" width="90" height="80" fill="#C97A6E" />
      <rect x="120" y="60" width="50" height="4" fill="#FFFFFF" opacity="0.7" />
      {/* Lanterna estilizada */}
      <ellipse cx="660" cy="80" rx="22" ry="32" fill="#C97A6E" />
      <line x1="660" y1="40" x2="660" y2="20" stroke="#1F2937" strokeWidth="1" />
      <line x1="660" y1="48" x2="660" y2="112" stroke="#1F2937" strokeWidth="1" opacity="0.4" />
      {/* Chão */}
      <rect x="0" y="240" width="800" height="160" fill="#C4A570" />
      {/* Mesa de madeira clara */}
      <rect x="80" y="280" width="640" height="80" fill="#D6B68A" />
      <rect x="80" y="280" width="640" height="8" fill="#A88654" />
      <line x1="80" y1="320" x2="720" y2="320" stroke="#A88654" strokeWidth="1" opacity="0.4" />
      {/* Pratos (2 pequenos) */}
      <ellipse cx="240" cy="324" rx="40" ry="10" fill="#FFFFFF" stroke="#9CA3AF" strokeWidth="1" />
      <ellipse cx="240" cy="320" rx="34" ry="8" fill="#F0EDE6" />
      <ellipse cx="560" cy="324" rx="40" ry="10" fill="#FFFFFF" stroke="#9CA3AF" strokeWidth="1" />
      <ellipse cx="560" cy="320" rx="34" ry="8" fill="#F0EDE6" />
      {/* Hashi sobre hashioki */}
      <rect x="310" y="316" width="60" height="3" rx="1" fill="#5C3A1A" transform="rotate(-3 340 318)" />
      <rect x="312" y="322" width="60" height="3" rx="1" fill="#5C3A1A" transform="rotate(-3 342 324)" />
      <rect x="334" y="328" width="16" height="4" rx="1" fill="#7A5A3A" />
      {/* Copo de chá */}
      <rect x="430" y="296" width="22" height="30" rx="2" fill="#E8E4DD" stroke="#9CA3AF" strokeWidth="1" />
      <ellipse cx="441" cy="296" rx="11" ry="3" fill="#5E8F73" opacity="0.7" />
    </svg>
  )
}
