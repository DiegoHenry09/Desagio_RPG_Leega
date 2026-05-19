# Cenários — Catálogo detalhado

Sete cenas cobrem todos os 15 eventos principais + 2 secretos. Cada cena é um SVG `0 0 800 400` (proporção 2:1), sem personas — personas são sobrepostas em DOM separado.

**Princípios:**
- Cenas são "palcos vazios". Personas entram em camada superior.
- Estilo flat illustration com 2-3 tons por elemento. Sem fotorrealismo.
- Iluminação implícita: leve gradient diagonal sutil para sugerir profundidade.
- Sem perspectiva forçada. Levemente isométrica funciona.
- Elementos identificadores do ambiente (cafeteira na copa, hashi no restaurante) ficam em segundo plano para reconhecimento rápido.

---

## `sala-reuniao` — Sala de reunião grande

**Eventos:** `ev_day1_001`, `ev_day2_003`, `ev_day3_001`, `ev_day4_003`

**Elementos visíveis:**
- Mesa oval grande ocupando 60% da cena, centralizada.
- 6-8 cadeiras em volta (algumas mais sugestivas em segundo plano).
- Janela ao fundo com luz suave (sem mostrar paisagem detalhada).
- Tela de projeção lateral, opcional com slide neutro abstrato.
- Parede de cor neutra (`--bg-muted`).

**Pontos de ancoragem:**
```
[
  { x: 0.20, y: 0.55 },  // esquerda da mesa
  { x: 0.50, y: 0.50 },  // cabeceira / centro
  { x: 0.80, y: 0.55 }   // direita da mesa
]
```

**Tom:** profissional, ligeiramente solene. Não fria, não acolhedora.

---

## `mesa-trabalho` — Mesa de trabalho do trainee

**Eventos:** `ev_day1_003`, `ev_day2_001`, `ev_day2_002`, `ev_day3_003`, `ev_day4_001`, `ev_day4_002`, `ev_day5_003`, `ev_secret_001`

(O mais usado — vale caprichar)

**Elementos visíveis:**
- Mesa frontal ocupando metade inferior.
- Notebook aberto centro-direita com tela ligada (luz azulada sutil).
- Monitor externo opcional à esquerda.
- Caneca de café com vapor estilizado.
- Bloco de notas + caneta.
- Planta pequena num canto.
- Fone de ouvido pendurado discretamente.
- Parede ao fundo com painel divisor de open office em segundo plano (sugestão, não detalhado).

**Pontos de ancoragem:**
```
[
  { x: 0.30, y: 0.60 },  // colega que se aproxima
  { x: 0.55, y: 0.65 },  // trainee na cadeira
  { x: 0.80, y: 0.55 }   // gestor parado ao lado
]
```

**Variante "vazia":** sem personas, só ambiente. Usar para eventos onde trainee está sozinho (`ev_day2_001` reflexão, `ev_day4_002` descobrindo erro).

**Tom:** familiar, controlado, levemente cluttered (real).

---

## `copa` — Copa/cozinha do escritório

**Eventos:** (reserva — pode ser usado em eventos futuros ou secretos extras)

**Elementos visíveis:**
- Bancada com máquina de café espresso.
- Geladeira ao fundo.
- Pia.
- Microondas.
- Banco alto opcional.
- Janela pequena ou painel com avisos.

**Pontos de ancoragem:**
```
[
  { x: 0.25, y: 0.65 },
  { x: 0.55, y: 0.60 },
  { x: 0.80, y: 0.65 }
]
```

**Tom:** mais casual que sala de reunião. Espaço social informal.

---

## `restaurante` — Restaurante japonês

**Eventos:** `ev_day1_002`, `ev_day5_002`

**Elementos visíveis:**
- Mesa de madeira clara em primeiro plano.
- Pratos pequenos, hashi sobre o hashioki.
- Copo de chá ou água.
- Parede lateral com elemento japonês discreto (noren, lanterna estilizada).
- Iluminação amarelada suave.

**Pontos de ancoragem:**
```
[
  { x: 0.30, y: 0.55 },
  { x: 0.70, y: 0.55 },
  { x: 0.50, y: 0.40 }   // fundo, opcional
]
```

**Tom:** acolhedor, levemente formal. Conversa importante.

---

## `bar` — Bar de happy hour

**Eventos:** `ev_day3_002`

**Elementos visíveis:**
- Balcão em primeiro plano com 2-3 copos (chopp, drink).
- Banquetas altas.
- Luz pendente amarelada acima do balcão.
- Parede de fundo com prateleira de garrafas (silhuetas, sem labels).
- Sutil indicação de barulho/ambiência: ondas leves saindo de personas.

**Pontos de ancoragem:**
```
[
  { x: 0.25, y: 0.50 },
  { x: 0.50, y: 0.55 },
  { x: 0.75, y: 0.50 }
]
```

**Tom:** descontraído sem ser caótico. Luz quente.

---

## `banheiro` — Banheiro do escritório

**Eventos:** `ev_secret_002`

**Elementos visíveis:**
- Pia ocupando primeiro plano centro-direito.
- Espelho retangular grande acima.
- Toalheiro/sabonete.
- Azulejo cinza neutro nas paredes.
- Luz fria implícita.
- Reflexo no espelho mostra silhueta sugerida (não detalhada).

**Pontos de ancoragem:**
```
[
  { x: 0.55, y: 0.55 }   // trainee em frente à pia/espelho
]
```

**Tom:** introspectivo. Esta cena é especificamente íntima — não há ninguém mais aqui.

**Cuidado especial:** o evento associado (`ev_secret_002` — crise emocional) trata de tema sensível. A ilustração deve transmitir calma e privacidade, não dramatização. Sem efeitos visuais de "crise" (sem distorção, sem cores intensas).

---

## `sala-apresentacao` — Sala com projetor

**Eventos:** `ev_day5_001`

**Elementos visíveis:**
- Tela de projeção no fundo centralizada.
- Slide neutro abstrato na tela (alguns retângulos, sem texto legível).
- Pódio pequeno ou apenas área aberta à frente.
- 8-10 cadeiras em fileiras parcialmente visíveis (algumas vazias, algumas ocupadas por silhuetas).
- Luz frontal da tela ilumina suavemente.

**Pontos de ancoragem:**
```
[
  { x: 0.50, y: 0.50 }   // trainee apresentando, posição central
]
```

**Tom:** expositivo, levemente tenso (apresentação em público).

---

## `_default` — Fundo neutro

**Para eventos sem `visuals.scene` definido.**

**Elementos:** apenas paleta de fundo (`--bg-base`) com sutil padrão de pontos ou linhas finas. Sem objetos.

**Pontos de ancoragem:**
```
[
  { x: 0.50, y: 0.50 }
]
```

**Uso:** placeholder até o evento ganhar visual próprio. Não é estado de erro.

---

## Composição: como personas e cena se sobrepõem

A página de evento renderiza assim:

```tsx
<div className="event-stage">
  <SceneSVG sceneId={event.visuals.scene} className="stage-bg" />
  {event.visuals.personas.map((personaId, idx) => (
    <PersonaSVG
      key={personaId}
      personaId={personaId}
      style={{
        position: 'absolute',
        left: `${sceneAnchors[event.visuals.scene][idx].x * 100}%`,
        top: `${sceneAnchors[event.visuals.scene][idx].y * 100}%`,
        transform: 'translate(-50%, -100%)',
      }}
    />
  ))}
</div>
```

CSS:
```css
.event-stage {
  position: relative;
  aspect-ratio: 2 / 1;
  max-width: 100%;
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg-muted);
}
.stage-bg { width: 100%; height: 100%; }
```

---

## Responsividade

Em telas estreitas (< 480px): cena ocupa largura total, altura proporcional. Personas escalam junto. Em telas largas: cena tem `max-width: 720px` e centraliza.

Não usar `background-image` para a cena — manter SVG inline para permitir personas serem posicionadas com porcentagens dos pontos de ancoragem, que escalam corretamente.

---

## Modo "reduced motion"

Cenas são estáticas por natureza, então pouca coisa muda. Mas:

- Vapor do café na `mesa-trabalho`: removido se `prefers-reduced-motion: reduce`.
- Luz pendente do `bar` com brilho pulsante: estática se reduced motion.
- Reflexo da tela no `sala-apresentacao`: estático.

CSS:
```css
@media (prefers-reduced-motion: reduce) {
  .scene-animated-element { animation: none !important; }
}
```
