# Asset Pipeline — Como criar, otimizar e versionar assets visuais

Documenta as quatro opções de criação de assets, com vantagens, custos, prompts de IA testados e checklist de otimização.

---

## Decisão por sprint

| Sprint | Estratégia | Justificativa |
|---|---|---|
| Sprint 3 | Opção D — placeholders SVG geométricos com paleta correta | Não bloquear a entrega da UX por causa de arte |
| Sprint 4 | Opção B — geração por IA + ajuste manual em SVG | Eleva qualidade visual; aceita o custo de tempo |

Se Sprint 4 não der tempo: ficar com placeholders melhorados (Opção D refinada). Não é falha — é trade-off honesto.

---

## Opção A — Criação manual em Figma/Inkscape

### Quando usar

- Quando o asset final precisa ser exatamente como planejado.
- Quando há tempo (~30 min por persona, ~45 min por cena).

### Ferramentas

- **Figma** (web, conta gratuita): boa para layouts e ilustração simples. Exporta SVG.
- **Inkscape** (desktop, gratuito): mais poderoso para SVG técnico.
- **Illustrator** (pago): padrão profissional.

### Workflow

1. Criar viewbox correto (`0 0 200 320` para persona, `0 0 800 400` para cena).
2. Trabalhar em camadas nomeadas (`skin`, `shirt`, `pants`, `hair`).
3. Usar cor `currentColor` ou variáveis CSS no SVG final (manual).
4. Exportar como SVG otimizado (sem metadata, sem comentários).
5. Rodar SVGO (`npx svgo file.svg`) para minificar.

### Estimativa

- Persona base + 2 variantes: 90 min.
- Cena: 45 min.
- Total para projeto completo: ~10-12 horas. Inviável para o desafio.

---

## Opção B — Geração por IA + ajuste manual

### Quando usar

- Recomendado para o desafio se tempo permitir no Sprint 4.
- Acelera 5-10x em relação ao manual.

### Ferramentas

- **Midjourney** (pago, ~$10/mês): melhor qualidade flat illustration.
- **Ideogram** (free tier): bom para flat illustration, controle de estilo.
- **DALL-E 3 via ChatGPT Plus** (pago): qualidade média, fácil de prompts.

### Workflow

1. Gerar imagem PNG com IA usando prompt cuidadoso (templates abaixo).
2. Vetorizar:
   - **Adobe Illustrator** → Image Trace → Limited Color (4-8 cores).
   - **Inkscape** → Path → Trace Bitmap → Multiple scans (color quantization).
   - **Vector Magic** (web, freemium): boa qualidade automática.
3. Limpar SVG: remover paths supérfluos, agrupar camadas.
4. Substituir cores hardcoded por variáveis CSS.
5. SVGO para minificar.

### Prompts testados para personas

Base template:
```
flat vector illustration, single person, Brazilian corporate worker,
[idade] years old, [gênero], [etnia], [vestimenta],
[postura], neutral expression, soft skin tone,
muted color palette, no background, full body or upper body,
clean lines, no harsh shadows, no gradient, no photorealism,
isolated on white background, professional and respectful representation,
non-stereotypical, realistic body proportions
```

**Exemplo `trainee`:**
```
flat vector illustration, single person, Brazilian young professional,
25 years old, neutral gender expression, light brown skin,
wearing teal casual button-up shirt and dark pants,
seated posture leaning slightly forward, attentive expression,
holding a small notebook, muted color palette,
no background, isolated on white, clean flat lines,
no gradient, no photorealism, respectful representation
```

**Exemplo `gerente` (Camila):**
```
flat vector illustration, single woman, Brazilian senior professional,
45 years old, light skin, brown hair tied in low ponytail,
wearing soft green blouse and dark pants, standing posture,
relaxed shoulders, attentive caring expression, holding a coffee mug,
muted color palette, no background, clean flat lines,
no stereotypes, realistic body proportions, professional attire,
no jewelry, no makeup exaggeration
```

**Exemplo `lider-externo` (Ana):**
```
flat vector illustration, single woman, Brazilian senior leader,
42 years old, dark brown skin, natural short hair,
wearing dark blazer over light blouse, dark pants,
confident standing posture, open hand gesture as if proposing,
genuine warm expression, no exaggeration,
muted color palette, no background, clean flat lines,
respectful diverse representation, professional
```

### Prompts testados para cenas

Base template:
```
flat vector illustration, empty [tipo de ambiente] interior,
horizontal wide composition 2:1 aspect ratio,
soft warm lighting from [direção], muted neutral color palette,
[elementos específicos do ambiente],
clean flat lines, no people, no characters,
isolated style, no harsh shadows, no photorealism,
soft pastel feel without being childish, professional environment
```

**Exemplo `sala-reuniao`:**
```
flat vector illustration, empty corporate meeting room interior,
horizontal wide composition 2:1 ratio,
large oval table in center, 6-8 office chairs around,
projection screen on side wall, large window in background with soft daylight,
muted neutral palette of beige, soft blue, warm gray,
clean flat lines, no people, no characters,
no harsh shadows, professional minimalist style
```

**Exemplo `bar`:**
```
flat vector illustration, empty modern bar interior,
horizontal wide composition 2:1 ratio,
wooden bar counter in foreground, high stools,
shelf of bottle silhouettes behind bar, warm pendant light hanging,
soft amber lighting, muted palette with warm accents,
clean flat lines, no people, late afternoon atmosphere,
professional minimalist style, no logos
```

### Pegadinhas comuns

- IA insiste em colocar texto em placas/computadores. Remover na edição vetorial.
- IA pode gerar pessoas estereotipadas (gestor sempre branco e de terno). Iterar prompts com instruções específicas de diversidade. Rejeitar e regenerar quando não atender.
- IA confunde "flat illustration" com "minimal blob figures" (Corporate Memphis). Adicionar "with facial features, realistic proportions, not abstract" para forçar feições.
- Cores podem sair fora da paleta — ajustar manualmente no SVG depois.

---

## Opção C — Biblioteca aberta

### Quando usar

- Para ícones (Lucide já é padrão).
- Excepcionalmente para personas se nenhuma outra opção rolar.

### Recursos

- **unDraw** (https://undraw.co): CC0, sem atribuição, personas estilo minimalista. Limitação: personas são muito genéricas, sem brasilianidade.
- **Open Doodles** (https://www.opendoodles.com): doodle style, leve, gratuito. Não combina com estilo flat proposto.
- **Storyset** (https://storyset.com): atribuição requerida, qualidade média.
- **Humaaans** (https://humaaans.com): personagens componíveis, MIT license. **Provavelmente a melhor opção open para este projeto** se Opção B não rolar.

### Workflow Humaaans (recomendado se for usar opção C)

1. Acessar https://humaaans.com.
2. Compor cada persona escolhendo head, top, bottom, pose.
3. Customizar cores para bater com paleta.
4. Exportar SVG.
5. Minificar com SVGO.

Limitação: estilo Humaaans é levemente caricato — vai bater com regra "sem caricatura"? Avaliar antes de adotar. Se a equipe aceita o estilo, é o caminho mais rápido com qualidade aceitável.

---

## Opção D — Placeholders geométricos (Sprint 3)

### O quê

SVGs simples representando personas como silhuetas estilizadas com paleta correta. Reconhecíveis pelo papel via cor + posição na cena, não pelos detalhes.

### Vantagem

- Cria em ~5 min por persona.
- Não bloqueia Sprint 3.
- Pode ser substituído sem mudar API/markup.

### Estrutura

Cada placeholder tem:
- Cabeça redonda com cor de pele variando por persona.
- Tronco trapezoidal com cor de "camisa" da paleta da persona.
- Sem rosto detalhado (círculos pequenos para olhos, sem boca).
- Postura sugerida via proporção (sentado vs em pé).

### Exemplo SVG placeholder `trainee`:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 320">
  <!-- Sombra base -->
  <ellipse cx="100" cy="310" rx="50" ry="6" fill="#000" opacity="0.08"/>
  <!-- Pernas -->
  <rect x="75" y="200" width="50" height="100" rx="6" fill="#2D3748"/>
  <!-- Tronco -->
  <path d="M 60 110 Q 100 90 140 110 L 145 210 Q 100 220 55 210 Z" fill="#6BA8B0"/>
  <!-- Pescoço -->
  <rect x="92" y="80" width="16" height="20" fill="#D4A574"/>
  <!-- Cabeça -->
  <circle cx="100" cy="60" r="28" fill="#D4A574"/>
  <!-- Cabelo -->
  <path d="M 75 50 Q 100 30 125 50 L 125 60 Q 100 50 75 60 Z" fill="#2D2A28"/>
  <!-- Olhos -->
  <circle cx="92" cy="62" r="2" fill="#1F2937"/>
  <circle cx="108" cy="62" r="2" fill="#1F2937"/>
</svg>
```

Adapt para outras personas mudando paleta. Mantém viewbox e proporções iguais para todos.

### Quando substituir

Quando o asset final (Opção B) está pronto e revisado.

---

## Otimização de SVG (qualquer opção)

### SVGO

```bash
npm install -g svgo
svgo --multipass file.svg
```

Configuração recomendada (`.svgo.config.js`):

```js
module.exports = {
  multipass: true,
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          removeViewBox: false,
          cleanupIds: { minify: false },
          inlineStyles: { onlyMatchedOnce: false },
        },
      },
    },
    'removeDimensions',
  ],
}
```

### Verificação de tamanho

```bash
# Listar tamanhos
ls -lh frontend/src/assets/visuals/personas/*.svg

# Target: cada arquivo ≤ 20KB
# Cena: ≤ 30KB
# Total da pasta visuals/: ≤ 500KB
```

### Verificação de validez

```bash
# Renderizar todos os SVGs num HTML simples e abrir no browser para sanity check
ls frontend/src/assets/visuals/personas/*.svg | while read f; do
  echo "<div><h3>$(basename $f)</h3><img src=\"$f\" width=\"100\"></div>"
done > /tmp/preview.html
```

---

## Lottie microanimações

### Quando usar

- Feedback de escolha (pulse positivo/negativo nas barras).
- Microanimação opcional no botão "Continuar" da Home.

### Onde obter

- **LottieFiles** (https://lottiefiles.com): biblioteca gigante, vários gratuitos.
- **After Effects + Bodymovin**: criar do zero. Inviável no escopo.

### Filtrar busca por

- License: free for commercial use ou CC0.
- Frames ≤ 60 (loop curto).
- File size ≤ 30KB.

### Sugestões para o jogo

Buscar termos como:
- "pulse positive" → para feedback positivo.
- "pulse error" → para feedback negativo.
- "loading dots" → para estados de carregamento (alternativa a CSS).

### Importação

```bash
npm install lottie-react
```

```tsx
import Lottie from 'lottie-react'
import positiveFeedback from '@/assets/visuals/animations/feedback-positive.json'

<Lottie animationData={positiveFeedback} loop={false} style={{ width: 48 }} />
```

---

## Versionamento de assets

- Assets ficam no repositório (não em CDN externo).
- Em PR/commit que adiciona asset: incluir screenshot na descrição.
- `references/personas.md` e `references/scenes.md` listam os assets canônicos. Auditor verifica que arquivos em disco batem com referência.

---

## Checklist de revisão de asset

Antes de mergear um asset novo:

- [ ] Viewbox correto (`0 0 200 320` persona / `0 0 800 400` cena).
- [ ] Tamanho final ≤ limite (20KB persona, 30KB cena, 30KB Lottie).
- [ ] Cores usam paleta oficial.
- [ ] SVGO rodado, multipass.
- [ ] Renderiza corretamente em Chromium, Firefox, WebKit.
- [ ] Não há texto hardcoded em paths (precisa ser editável via i18n se for o caso).
- [ ] Sem identifiers genéricos (`id="Layer_1"`) que conflitam quando múltiplos SVGs estão na mesma página — usar prefix por arquivo.
- [ ] Alt text definido no componente que renderiza.

---

## Anti-padrões no pipeline

- **Não baixar de stock photo** — vai entregar realista que conflita com flat illustration.
- **Não usar emoji ou unicode** como persona — visualmente inconsistente, falha em alguns sistemas.
- **Não embedar `<image>` raster dentro de SVG** — perde escalabilidade.
- **Não usar fontes externas dentro do SVG** — quebra fora do browser.
- **Não confiar em IA para gerar SVG diretamente** — IA gera código SVG inválido frequentemente. Sempre gerar raster e vetorizar manualmente.
