/**
 * Cena: copa. scenes.md §"copa" (reserva para eventos futuros / secretos).
 * Bancada, máquina de café, geladeira, microondas, painel de avisos.
 */
export default function Copa() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 800 400"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <rect x="0" y="0" width="800" height="260" fill="var(--bg-muted-soft)" />
      <rect x="0" y="260" width="800" height="140" fill="#D8D2C5" />
      {/* Geladeira ao fundo */}
      <rect x="80" y="40" width="120" height="280" rx="4" fill="#E8E4DD" stroke="#7A7F87" strokeWidth="2" />
      <line x1="80" y1="160" x2="200" y2="160" stroke="#7A7F87" strokeWidth="2" />
      <rect x="186" y="66" width="6" height="20" fill="#7A7F87" />
      <rect x="186" y="172" width="6" height="60" fill="#7A7F87" />
      {/* Bancada */}
      <rect x="240" y="200" width="500" height="20" fill="#9C8B6E" />
      <rect x="240" y="220" width="500" height="100" fill="#B59E78" />
      {/* Máquina de café */}
      <rect x="280" y="120" width="80" height="80" rx="4" fill="#1F2937" />
      <rect x="290" y="132" width="60" height="20" rx="2" fill="#3B5B7C" />
      <rect x="306" y="166" width="28" height="18" rx="2" fill="#FFFFFF" stroke="#9CA3AF" strokeWidth="1" />
      <ellipse cx="320" cy="166" rx="14" ry="3" fill="#4A3220" />
      {/* Microondas */}
      <rect x="420" y="140" width="120" height="60" rx="4" fill="#E8E4DD" stroke="#7A7F87" strokeWidth="2" />
      <rect x="430" y="150" width="80" height="40" rx="2" fill="#3B5B7C" opacity="0.3" />
      <rect x="516" y="156" width="18" height="6" fill="#7A7F87" />
      <rect x="516" y="166" width="18" height="6" fill="#7A7F87" />
      <rect x="516" y="176" width="18" height="6" fill="#7A7F87" />
      {/* Painel de avisos */}
      <rect x="600" y="80" width="140" height="100" rx="3" fill="#F5C97A" opacity="0.3" stroke="#9CA3AF" strokeWidth="2" />
      <rect x="612" y="92" width="40" height="28" fill="#FFFFFF" stroke="#9CA3AF" strokeWidth="1" />
      <rect x="660" y="98" width="60" height="14" fill="#FFFFFF" stroke="#9CA3AF" strokeWidth="1" />
      <rect x="620" y="130" width="100" height="20" fill="#FFFFFF" stroke="#9CA3AF" strokeWidth="1" />
      {/* Pia */}
      <rect x="600" y="200" width="120" height="20" fill="#9C8B6E" />
      <ellipse cx="660" cy="218" rx="40" ry="6" fill="#D8DCE2" />
    </svg>
  )
}
