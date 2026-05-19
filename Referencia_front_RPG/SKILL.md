---
name: corporate-survivor-visuals
description: Padrão visual e catálogo de personas/cenários do Corporate Survivor. Use SEMPRE que estiver implementando qualquer tela do frontend que precise representar pessoas (gestor, RH, colega, gerente, sênior, líder), cenários (sala de reunião, copa, restaurante, bar, banheiro, mesa de trabalho) ou microanimações de feedback (resposta a escolhas, transições de evento). Use também ao adicionar novos eventos no JSON que mencionem personas/cenários novos, ao montar a tela de evento (GamePage), ao criar a tela inicial, a tela de final, ou ao decidir qualquer asset visual do jogo. Esta skill define o padrão técnico (SVG-first, Lottie para movimento, sem GIFs pesados), as personas catalogadas com IDs estáveis, os cenários catalogados, a paleta, a tipografia, regras de acessibilidade e o pipeline de criação de novos assets. Se você está mexendo em algo visual do Corporate Survivor, consulte esta skill primeiro.
---

# Corporate Survivor — Visuals & Personas

Skill de identidade visual e representação de personas do mini RPG corporativo. Define um sistema leve, performático e profissional para "personas no cenário" sem GIFs pesados.

---

## Quando usar

Consulte esta skill ao:

- Implementar `GamePage`, `HomePage`, `EndingPage` ou qualquer página do frontend.
- Renderizar um evento que envolva uma persona (gestor, gerente, sênior, colega, RH, líder externo).
- Renderizar um cenário (sala de reunião, copa, restaurante, bar, banheiro, mesa).
- Adicionar feedback visual após uma escolha (microanimação nas barras de atributo, reação da persona).
- Criar ou ajustar um evento novo em `events.json` que introduza persona/cena nova.
- Decidir tipografia, paleta, espaçamento.

Se você está editando código visual e ignora esta skill, o resultado vai ficar inconsistente com o resto do jogo. Sempre consulte.

---

## Princípios visuais inegociáveis

1. **Realismo corporativo brasileiro sem caricatura.** Personas representam pessoas reais de escritórios brasileiros. Sem vilão estereotipado. Sem RH carrancudo. Sem gestor de terno três peças. Diversidade real: gênero, etnia, idade.

2. **Leve por construção.** Asset individual ≤ 80KB. Página inteira do jogo ≤ 500KB de imagem/animação. Nada de GIF gigante. Sem dependência de CDN externo para asset crítico.

3. **SVG-first.** Toda persona e todo cenário é SVG. SVG escala, é editável, é pequeno, animável via CSS. GIF e WebP só para casos onde SVG não cabe (raro neste projeto).

4. **Movimento sutil e funcional.** Animação serve a comunicar estado, não a decorar. Loop curto (2-4s), fade suave, micro-respiração. Nada de bounce dramático, nada de partículas, nada de parallax.

5. **Acessibilidade não é negociável.** Toda imagem tem `alt`. Toda animação respeita `prefers-reduced-motion`. Contraste mínimo WCAG AA. Foco visível em interativos.

6. **Identificação imediata.** Cada persona é reconhecível em 1 segundo pelo papel (gestor vs colega vs RH). Não pela cor única, mas pela combinação de pose, ambientação e contexto da cena.

7. **Sem "Corporate Memphis".** Aquele estilo flat caricato de blob figures sem rosto (Alegria/Bro) é proibido. É exatamente o que o tom narrativo do jogo recusa.

---

## Arquitetura de assets

```
frontend/src/assets/visuals/
  personas/
    trainee.svg
    gestor.svg
    gerente.svg
    colega.svg
    rh.svg
    senior.svg
    lider-externo.svg
  scenes/
    sala-reuniao.svg
    copa.svg
    mesa-trabalho.svg
    restaurante.svg
    bar.svg
    banheiro.svg
    sala-apresentacao.svg
  animations/
    feedback-positive.json    # Lottie
    feedback-negative.json
    feedback-neutral.json
    breathing.json            # respiração sutil para personas
  icons/
    energia.svg
    reputacao.svg
    networking.svg
    ansiedade.svg
    produtividade.svg
    aprendizado.svg
```

Cada subpasta tem um `_index.ts` que exporta todos os assets com tipo:

```typescript
// personas/_index.ts
import trainee from './trainee.svg'
import gestor from './gestor.svg'
// ...

export const personas = {
  trainee, gestor, gerente, colega, rh, senior, 'lider-externo': liderExterno
} as const

export type PersonaId = keyof typeof personas
```

Mesma lógica para `scenes`, `animations`, `icons`.

---

## Mapeamento evento → cena → personas

Eventos do `events.json` ganham dois campos opcionais novos (consumidos pelo frontend, ignorados pela engine):

```json
{
  "id": "ev_day1_001",
  "scene": "...",
  "visuals": {
    "scene": "sala-reuniao",
    "personas": ["rh", "trainee"]
  }
}
```

A engine não valida `visuals` (não é regra de jogo). O frontend, ao montar a tela do evento, consulta `visuals` e renderiza:

- **Fundo:** ilustração SVG de `scenes/sala-reuniao.svg`
- **Personas:** SVGs sobrepostos em posições fixas (regra de layout abaixo)

Se `visuals` está ausente: usa um fundo neutro padrão (`scenes/_default.svg`) sem persona. Não é erro — só significa que aquele evento ainda não tem visual definido.

### Tabela de mapeamento (referência rápida)

Mapeamento sugerido para os 15 eventos principais + 2 secretos. Detalhado em `references/event-visuals-map.md`.

| Evento | Cena | Personas |
|---|---|---|
| ev_day1_001 (Onboarding RH) | sala-reuniao | rh, trainee |
| ev_day1_002 (Primeiro almoço) | restaurante | colega, trainee |
| ev_day1_003 (Setup pendente) | mesa-trabalho | trainee |
| ev_day2_001 (Tarefa escopo vago) | mesa-trabalho | gestor, trainee |
| ev_day2_002 (Duas urgências) | mesa-trabalho | colega, trainee |
| ev_day2_003 (Crítica em reunião) | sala-reuniao | senior, gestor, trainee |
| ev_day3_001 (Reunião sem pauta) | sala-reuniao | trainee, gestor, colega |
| ev_day3_002 (Happy hour) | bar | colega, trainee |
| ev_day3_003 (Pedido 18h) | mesa-trabalho | trainee |
| ev_day4_001 (Mentoria) | mesa-trabalho | senior, trainee |
| ev_day4_002 (Erro descoberto) | mesa-trabalho | trainee |
| ev_day4_003 (Pedido feedback) | sala-reuniao | gerente, trainee |
| ev_day5_001 (Apresentação) | sala-apresentacao | trainee |
| ev_day5_002 (Almoço com gerente) | restaurante | gerente, trainee |
| ev_day5_003 (Tarefa 17h45) | mesa-trabalho | trainee |
| ev_secret_001 (Projeto especial) | mesa-trabalho | lider-externo, trainee |
| ev_secret_002 (Crise no banheiro) | banheiro | trainee |

---

## Personas catalogadas (resumo)

Catálogo completo com descrição física, paleta de roupas, postura típica e variantes está em `references/personas.md`. Resumo:

| ID | Nome | Papel | Tom |
|---|---|---|---|
| `trainee` | (Você) | Protagonista | Neutro, postura aberta. Avatar levemente genérico para projeção do jogador |
| `gestor` | Rafael | Gestor direto | Profissional, gesto contido. Demanda + apoio em medidas equilibradas |
| `gerente` | Camila | Gerente da área | Sênior, postura calma, olhar atento |
| `colega` | Bruno/Marina | Par no time | Casual, postura relaxada, próxima |
| `rh` | Patrícia | Apresentadora RH | Profissional formal, mas acolhedora |
| `senior` | Eduardo | Mentor sênior | Postura experiente, vestimenta confortável |
| `lider-externo` | Ana | Líder de outra área | Confiante, energia de quem está propondo algo |

**Importante:** os nomes acima são opcionais — podem aparecer no texto narrativo se o evento referenciar diretamente, mas o jogo não força isso. As personas são representadas visualmente sem precisar de nome na tela.

---

## Cenários catalogados (resumo)

Catálogo completo em `references/scenes.md`. Resumo:

| ID | Cena | Elementos |
|---|---|---|
| `sala-reuniao` | Sala de reunião grande | Mesa oval, cadeiras, projetor, janela ao fundo |
| `mesa-trabalho` | Mesa de trabalho do trainee | Notebook, monitor, café, planta pequena |
| `copa` | Copa/cozinha do escritório | Bancada, máquina de café, geladeira |
| `restaurante` | Restaurante japonês | Mesa, hashi, ambiente clean |
| `bar` | Bar de happy hour | Balcão, luz amarelada, copos |
| `banheiro` | Banheiro do escritório | Pia, espelho, azulejo cinza |
| `sala-apresentacao` | Sala com projetor | Tela, fileiras de cadeiras, pódio pequeno |

---

## Padrão técnico

### SVG personas

- Viewbox padronizado: `0 0 200 320` (proporção 5:8, formato de personagem em pé)
- Estilo: flat illustration com sombras suaves (1-2 níveis de tom, sem gradient pesado)
- Paleta usa variáveis CSS para que personas se adaptem ao tema (dia/noite, se implementado):
  ```html
  <svg style="--skin: #D4A574; --shirt: #4A5568; --pants: #2D3748">
  ```
- Rosto neutro com expressão sutil; evitar feições extremas

### SVG cenas

- Viewbox padronizado: `0 0 800 400` (proporção 2:1, formato horizontal)
- Cenas são "vazias" (sem personas) — personas são sobrepostas em DOM separado
- 3 pontos de ancoragem definidos em cada cena para até 3 personas:
  ```typescript
  // scene-anchors.ts
  export const sceneAnchors = {
    'sala-reuniao': [
      { x: 0.25, y: 0.55 },
      { x: 0.50, y: 0.50 },
      { x: 0.75, y: 0.55 },
    ],
    // ...
  }
  ```

### Lottie microanimações

- Duração 2-4s
- Loop opcional dependendo do contexto
- Tamanho ≤ 30KB cada
- Renderizadas com `lottie-react`
- Sempre verificar `prefers-reduced-motion`:
  ```tsx
  const reduceMotion = useReducedMotion()
  return reduceMotion
    ? <StaticIcon />
    : <Lottie animationData={data} loop />
  ```

### Microanimações CSS de feedback

Para a animação das barras de atributo após uma escolha:

```css
@keyframes attr-up { from { box-shadow: 0 0 0 0 var(--accent-positive); } to { box-shadow: 0 0 0 6px transparent; } }
@keyframes attr-down { from { box-shadow: 0 0 0 0 var(--accent-negative); } to { box-shadow: 0 0 0 6px transparent; } }

@media (prefers-reduced-motion: reduce) {
  .attr-bar { animation: none !important; }
}
```

### Persona "breathing"

Microanimação opcional de respiração para personas em tela (não distrair):

```css
@keyframes breathe {
  0%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(1.005); }
}
.persona-svg { animation: breathe 4s ease-in-out infinite; transform-origin: bottom; }
@media (prefers-reduced-motion: reduce) { .persona-svg { animation: none; } }
```

---

## Paleta oficial

Definida em CSS variables em `frontend/src/styles/tokens.css` (consumido pelo Tailwind via `theme.extend`).

```css
:root {
  /* Fundos */
  --bg-base: #F5F4F0;          /* off-white levemente quente */
  --bg-surface: #FFFFFF;        /* cards */
  --bg-muted: #E8E4DD;          /* divisórias, fundos secundários */

  /* Texto */
  --text-primary: #1F2937;      /* cinza muito escuro */
  --text-secondary: #6B7280;
  --text-muted: #9CA3AF;

  /* Estrutura corporativa neutra */
  --corp-blue: #3B5B7C;         /* azul corporativo desbotado */
  --corp-blue-light: #D6DEE8;

  /* Acentos emocionais (atributos e feedback) */
  --accent-positive: #7FA47B;    /* verde sálvia — ganho */
  --accent-negative: #C97A6E;    /* terracota — perda */
  --accent-anxiety: #D4A95B;     /* amarelo mostarda — ansiedade */
  --accent-energy: #6BA8B0;      /* azul-petróleo claro — energia */
  --accent-rep: #A07AB8;         /* lilás — reputação */
  --accent-network: #C0875A;     /* caramelo — networking */
  --accent-prod: #3B5B7C;        /* corp-blue — produtividade */
  --accent-learn: #5E8F73;       /* verde musgo — aprendizado */
}
```

Cores não são "lindas" — são funcionais e neutras. Não tentar embelezar.

---

## Tipografia

Stack única, sem fontes web pesadas:

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
```

Carregar Inter via `@fontsource/inter` (subset latin) — peso 400, 500, 600, 700. Total ~80KB.

Escala (Tailwind defaults com pequeno ajuste):
- `text-xs` 12px — labels de atributos
- `text-sm` 14px — texto de UI
- `text-base` 16px — base
- `text-lg` 18px — cena do evento (legibilidade prioritária)
- `text-xl` 20px — títulos de evento
- `text-2xl` 24px — H1 da tela inicial / final

---

## Acessibilidade

Checklist obrigatório por tela:

- [ ] Toda imagem tem `alt` descritivo ou `alt=""` (decorativa).
- [ ] Animações respeitam `prefers-reduced-motion`.
- [ ] Contraste de texto ≥ 4.5:1 (WCAG AA).
- [ ] Foco visível em todos interativos (botões de opção, botões de navegação).
- [ ] Botões de opção navegáveis por teclado (Tab + Enter/Space).
- [ ] Heading hierarchy correto (`<h1>` único por tela).
- [ ] Tela inicial: landmark `<main>` definido.
- [ ] Cor não é único veículo de informação (ex.: atributos têm ícone + label, não só cor).

---

## Como adicionar uma persona nova

1. Criar SVG em `frontend/src/assets/visuals/personas/<id>.svg`.
2. Adicionar export em `personas/_index.ts`.
3. Atualizar `references/personas.md` com descrição da persona.
4. Atualizar `references/event-visuals-map.md` ligando persona aos eventos.
5. **Não** atualizar `events.json` apenas por mudança visual — eventos só ganham `visuals.personas` quando faz sentido narrativamente.

## Como adicionar uma cena nova

1. Criar SVG em `frontend/src/assets/visuals/scenes/<id>.svg` no viewbox `0 0 800 400`.
2. Adicionar export em `scenes/_index.ts`.
3. Adicionar pontos de ancoragem em `scene-anchors.ts` (3 pontos).
4. Atualizar `references/scenes.md`.

## Como adicionar uma microanimação nova

1. Exportar Lottie JSON ≤ 30KB para `frontend/src/assets/visuals/animations/<id>.json`.
2. Adicionar export em `animations/_index.ts`.
3. Garantir fallback estático para `prefers-reduced-motion`.

---

## Pipeline de criação de assets

Detalhado em `references/asset-pipeline.md`. Resumo:

- **Opção A — criação manual em Figma/Inkscape:** controle total, demora ~30min por persona. Recomendado para personas finais.
- **Opção B — geração por IA + ajuste manual:** Midjourney/Ideogram para gerar base flat illustration, depois converter para SVG via vetorização (Adobe Illustrator ou inkscape autotrace) ou redesenho. Acelera, mas exige edição para coerência.
- **Opção C — biblioteca aberta:** unDraw (CC0), Open Doodles, Storyset (atribuição). Limitado em personas brasileiras coerentes; usar com critério.
- **Opção D — placeholder durante Sprint 3:** iniciar com avatares minimalistas (silhuetas em SVG com paleta correta), substituir por ilustrações finais no Sprint 4.

Recomendação para o desafio (escopo curto): **Opção D no Sprint 3 + Opção B no Sprint 4** se sobrar tempo. Não bloqueie Sprint 3 esperando arte final.

---

## Anti-padrões (vão fazer o Auditor reprovar visual)

- Usar `.gif` real maior que 80KB.
- Usar emoji para representar persona (😎🧑‍💼).
- Avatares que parecem stock photo (rostos reais ou pseudo-reais).
- Corporate Memphis (blob figures sem rosto).
- Animação que distrai da leitura da cena.
- Personagem se movendo continuamente enquanto jogador lê texto.
- Ignorar `prefers-reduced-motion`.
- Cor como único veículo de informação.
- Persona com estereótipo (gestor de terno + relógio caro).

---

## Referências

Para detalhes profundos consulte:

- `references/personas.md` — catálogo completo de personas com descrição visual, paleta, postura, variantes.
- `references/scenes.md` — catálogo completo de cenários.
- `references/style-guide.md` — paleta detalhada, tipografia, espaçamento, motion design.
- `references/asset-pipeline.md` — como criar/buscar/otimizar assets, com prompts de IA recomendados.
- `references/event-visuals-map.md` — mapeamento explícito evento → cena → personas.

Leia o reference relevante antes de implementar uma feature visual nova. Não tente adivinhar — está documentado.
