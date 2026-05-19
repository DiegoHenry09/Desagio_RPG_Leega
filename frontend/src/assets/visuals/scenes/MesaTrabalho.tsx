/**
 * Cena: mesa-trabalho. scenes.md §"mesa-trabalho" (cena mais usada).
 * Elementos: mesa frontal, notebook aberto, monitor, caneca de café, planta,
 * bloco de notas, fone, painel divisor de open office ao fundo.
 */
export default function MesaTrabalho() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 800 400"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <rect x="0" y="0" width="800" height="220" fill="var(--bg-muted)" />
      <rect x="0" y="220" width="800" height="180" fill="#E0DAC8" />
      {/* Painel divisor de open office (fundo) */}
      <rect x="40" y="60" width="720" height="140" fill="#D5CDB5" />
      <line x1="280" y1="60" x2="280" y2="200" stroke="#B5AFA1" strokeWidth="2" />
      <line x1="520" y1="60" x2="520" y2="200" stroke="#B5AFA1" strokeWidth="2" />
      {/* Mesa principal */}
      <rect x="40" y="220" width="720" height="20" fill="#9C8B6E" />
      <rect x="40" y="240" width="720" height="10" fill="#7A6B52" />
      {/* Monitor externo */}
      <rect x="100" y="130" width="140" height="90" rx="4" fill="#1F2937" />
      <rect x="108" y="138" width="124" height="74" fill="#3B5B7C" />
      <rect x="118" y="146" width="40" height="6" fill="var(--corp-blue-light)" opacity="0.7" />
      <rect x="118" y="158" width="80" height="4" fill="var(--bg-muted)" opacity="0.6" />
      <rect x="118" y="168" width="60" height="4" fill="var(--bg-muted)" opacity="0.6" />
      <rect x="118" y="178" width="70" height="4" fill="var(--bg-muted)" opacity="0.6" />
      <rect x="158" y="220" width="24" height="6" fill="#4A4945" />
      {/* Notebook aberto centro */}
      <path d="M 310 220 L 330 156 L 470 156 L 490 220 Z" fill="#2D3748" />
      <rect x="335" y="160" width="130" height="56" fill="var(--corp-blue)" />
      <rect x="343" y="168" width="36" height="6" fill="#FFFFFF" opacity="0.8" />
      <rect x="343" y="180" width="60" height="4" fill="#FFFFFF" opacity="0.5" />
      <rect x="343" y="190" width="50" height="4" fill="#FFFFFF" opacity="0.5" />
      <rect x="343" y="200" width="70" height="4" fill="#FFFFFF" opacity="0.5" />
      {/* Caneca de café */}
      <rect x="540" y="194" width="34" height="30" rx="3" fill="#FFFFFF" stroke="#1F2937" strokeWidth="1.2" />
      <path d="M 574 200 Q 584 208 574 218" stroke="#1F2937" strokeWidth="1.2" fill="none" />
      <ellipse cx="557" cy="194" rx="17" ry="3" fill="#4A3220" />
      {/* Vapor estilizado da caneca */}
      <path
        className="cs-scene-steam"
        d="M 548 184 Q 552 174 548 168"
        stroke="#9CA3AF"
        strokeWidth="1.5"
        fill="none"
        strokeLinecap="round"
        opacity="0.6"
      />
      <path
        className="cs-scene-steam"
        d="M 560 180 Q 564 168 560 158"
        stroke="#9CA3AF"
        strokeWidth="1.5"
        fill="none"
        strokeLinecap="round"
        opacity="0.6"
      />
      {/* Bloco de notas + caneta */}
      <rect x="600" y="212" width="60" height="14" rx="1" fill="#F5F4F0" stroke="#9CA3AF" strokeWidth="1" />
      <line x1="608" y1="218" x2="650" y2="218" stroke="#9CA3AF" strokeWidth="0.8" />
      <line x1="608" y1="222" x2="640" y2="222" stroke="#9CA3AF" strokeWidth="0.8" />
      <rect x="640" y="200" width="32" height="3" rx="1" fill="var(--accent-network)" transform="rotate(-25 656 201)" />
      {/* Planta pequena */}
      <rect x="690" y="186" width="40" height="34" rx="2" fill="#B59E78" />
      <path d="M 710 186 L 700 162 L 712 168 L 720 156 L 718 174 L 728 168 L 720 186 Z" fill="var(--accent-learn)" />
    </svg>
  )
}
