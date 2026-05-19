/**
 * Cena: bar (happy hour). scenes.md §"bar".
 * Balcão em primeiro plano, copos, banquetas, prateleira de garrafas atrás,
 * luz pendente amarelada.
 */
export default function Bar() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 800 400"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      {/* Parede com tom quente */}
      <rect x="0" y="0" width="800" height="280" fill="#3D2E22" />
      {/* Iluminação ambiente */}
      <ellipse cx="400" cy="60" rx="240" ry="80" fill="#F5C97A" opacity="0.2" />
      {/* Prateleira de garrafas (silhuetas) */}
      <rect x="80" y="80" width="640" height="6" fill="#5C3A1A" />
      <rect x="80" y="160" width="640" height="6" fill="#5C3A1A" />
      {/* Garrafas atrás do balcão (silhuetas variadas) */}
      <rect x="120" y="92" width="14" height="64" fill="#5E8F73" opacity="0.85" />
      <rect x="148" y="98" width="14" height="58" fill="#A07AB8" opacity="0.85" />
      <rect x="176" y="92" width="14" height="64" fill="#C97A6E" opacity="0.85" />
      <rect x="204" y="100" width="14" height="56" fill="#3B5B7C" opacity="0.85" />
      <rect x="240" y="92" width="14" height="64" fill="#5E8F73" opacity="0.85" />
      <rect x="268" y="98" width="14" height="58" fill="#C0875A" opacity="0.85" />
      <rect x="540" y="92" width="14" height="64" fill="#5E8F73" opacity="0.85" />
      <rect x="568" y="100" width="14" height="56" fill="#A07AB8" opacity="0.85" />
      <rect x="596" y="92" width="14" height="64" fill="#C97A6E" opacity="0.85" />
      <rect x="624" y="98" width="14" height="58" fill="#3B5B7C" opacity="0.85" />
      <rect x="652" y="92" width="14" height="64" fill="#5E8F73" opacity="0.85" />
      <rect x="680" y="98" width="14" height="58" fill="#C0875A" opacity="0.85" />
      {/* Luz pendente */}
      <line x1="400" y1="0" x2="400" y2="40" stroke="#1F2937" strokeWidth="1.5" />
      <path d="M 380 40 L 420 40 L 414 70 L 386 70 Z" fill="#F5C97A" />
      <ellipse cx="400" cy="74" rx="22" ry="6" fill="#FCD97A" opacity="0.8" />
      {/* Balcão (chão de cor) */}
      <rect x="0" y="280" width="800" height="120" fill="#2A1E14" />
      <rect x="0" y="290" width="800" height="44" fill="#5C3A1A" />
      <rect x="0" y="290" width="800" height="6" fill="#7A5A3A" />
      {/* Copos no balcão */}
      <rect x="180" y="300" width="22" height="28" rx="1" fill="#F5C97A" opacity="0.85" stroke="#1F2937" strokeWidth="1" />
      <ellipse cx="191" cy="300" rx="11" ry="3" fill="#F5C97A" opacity="0.95" />
      <rect x="380" y="296" width="26" height="32" rx="3" fill="#3D2E22" opacity="0.7" stroke="#1F2937" strokeWidth="1" />
      <ellipse cx="393" cy="296" rx="13" ry="3" fill="#C97A6E" opacity="0.9" />
      <rect x="580" y="302" width="20" height="26" rx="1" fill="#F5C97A" opacity="0.85" stroke="#1F2937" strokeWidth="1" />
      <ellipse cx="590" cy="302" rx="10" ry="3" fill="#F5C97A" opacity="0.95" />
      {/* Banquetas (parte de cima visível) */}
      <ellipse cx="220" cy="340" rx="22" ry="4" fill="#1A1614" />
      <ellipse cx="420" cy="340" rx="22" ry="4" fill="#1A1614" />
      <ellipse cx="620" cy="340" rx="22" ry="4" fill="#1A1614" />
    </svg>
  )
}
