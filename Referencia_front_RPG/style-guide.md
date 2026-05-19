# Style Guide — Corporate Survivor

Sistema visual completo: paleta, tipografia, espaçamento, motion, elevation, formas.

---

## 1. Paleta

### Fundos (base neutra)

| Variável | Hex | Uso |
|---|---|---|
| `--bg-base` | `#F5F4F0` | Fundo principal da aplicação. Off-white levemente quente, evita branco puro estridente |
| `--bg-surface` | `#FFFFFF` | Cards, modais, áreas elevadas |
| `--bg-muted` | `#E8E4DD` | Divisórias, fundos secundários, skeleton loading |
| `--bg-dark` | `#1F2937` | Eventual "modo noturno" — não usar agora |

### Texto

| Variável | Hex | Uso | Contraste em `--bg-base` |
|---|---|---|---|
| `--text-primary` | `#1F2937` | Texto principal, títulos | 13.4:1 (AAA) |
| `--text-secondary` | `#6B7280` | Texto secundário, labels | 4.8:1 (AA) |
| `--text-muted` | `#9CA3AF` | Placeholders, dicas | 2.6:1 (não usar em texto longo) |

### Cor estrutural corporativa

| Variável | Hex | Uso |
|---|---|---|
| `--corp-blue` | `#3B5B7C` | Botão primário, links principais, headers de seção |
| `--corp-blue-hover` | `#2D4763` | Estado hover do azul corporativo |
| `--corp-blue-light` | `#D6DEE8` | Backgrounds claros associados (badge, tag) |

### Acentos emocionais (atributos)

| Variável | Hex | Atributo associado | Notas |
|---|---|---|---|
| `--accent-energy` | `#6BA8B0` | Energia | Azul-petróleo, sugere vitalidade calma |
| `--accent-rep` | `#A07AB8` | Reputação | Lilás, sugere influência sem grandiosidade |
| `--accent-network` | `#C0875A` | Networking | Caramelo, sugere calor humano |
| `--accent-anxiety` | `#D4A95B` | Ansiedade | Amarelo mostarda — único atributo onde alto é ruim. Cor escolhida para evocar tensão sem alarme |
| `--accent-prod` | `#3B5B7C` | Produtividade | Mesmo `--corp-blue`, sugere foco |
| `--accent-learn` | `#5E8F73` | Aprendizado | Verde musgo, sugere crescimento orgânico |

**Importante:** cor não é único veículo de informação. Cada atributo tem ícone + label + cor. Pessoa daltônica deve conseguir identificar atributo só pelo ícone.

### Feedback (resposta a escolhas)

| Variável | Hex | Uso |
|---|---|---|
| `--accent-positive` | `#7FA47B` | Delta positivo em atributo, sucesso |
| `--accent-negative` | `#C97A6E` | Delta negativo, erro |
| `--accent-neutral` | `#9CA3AF` | Delta zero ou neutro |

---

## 2. Tipografia

### Stack

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
```

Carregamento via `@fontsource/inter` (apenas subset latin + pesos necessários):

```ts
import '@fontsource/inter/400.css'
import '@fontsource/inter/500.css'
import '@fontsource/inter/600.css'
import '@fontsource/inter/700.css'
```

Total ~80KB. Sem fontes externas via CDN.

### Escala

| Token Tailwind | Tamanho | Line height | Peso | Uso |
|---|---|---|---|---|
| `text-xs` | 12px | 16px | 500 | Labels de atributo, badges |
| `text-sm` | 14px | 20px | 400 | UI secundária, captions |
| `text-base` | 16px | 24px | 400 | Texto corpo padrão |
| `text-lg` | 18px | 28px | 400 | **Cena do evento (legibilidade prioritária)** |
| `text-xl` | 20px | 28px | 600 | Título do evento |
| `text-2xl` | 24px | 32px | 700 | H1 das telas (Home, Final, Ranking) |
| `text-3xl` | 30px | 36px | 700 | Reservar para tela de Final |

### Regras

- Linha máxima de texto: 65 caracteres (~620px no tamanho base).
- `text-lg` para o `scene` do evento — esse é o texto mais importante do jogo, prioriza leitura.
- Botões de opção em `text-base` 500.
- Sem itálico para ênfase narrativa — usa **bold** com moderação ou aspas.

---

## 3. Espaçamento

Sistema baseado em múltiplos de 4px (Tailwind default).

### Componentes-chave

| Elemento | Padding | Gap | Notas |
|---|---|---|---|
| Card de evento | `p-6` (24px) | — | Card principal |
| Botão de opção | `px-4 py-3` (16/12px) | — | Toque generoso para mobile |
| Lista de opções | — | `gap-3` (12px) | Entre botões |
| Painel de atributos | `p-4` | `gap-2` | Compacto mas legível |
| Barra de atributo | `py-1` | `gap-2` | Label + barra + número |

### Layout

```
Container máximo: 1024px (max-w-5xl)
Mobile padding: 16px laterais
Desktop padding: 32px laterais
Vertical rhythm entre seções: 32px
```

---

## 4. Bordas e radius

| Token | Valor | Uso |
|---|---|---|
| `rounded` | 4px | Tags pequenas |
| `rounded-md` | 6px | Botões, inputs |
| `rounded-lg` | 8px | Cards, scene container |
| `rounded-xl` | 12px | Modais |
| `rounded-full` | 9999px | Barras de progresso, badges circulares |

Sem `rounded-2xl` ou maior — visual fica "soft" demais.

---

## 5. Elevação (sombras)

Usar com extrema parcimônia. Hierarquia plana é a regra.

| Token | Valor | Uso |
|---|---|---|
| `shadow-sm` | sutil | Card de evento (apenas) |
| `shadow-md` | médio | Modal de confirmação |
| `shadow-lg` | forte | Nunca usar |

```css
--shadow-sm: 0 1px 2px 0 rgba(0,0,0,0.04);
--shadow-md: 0 4px 8px -2px rgba(0,0,0,0.08);
```

---

## 6. Estados interativos

### Botão primário (continuar, iniciar)

```
default: bg-corp-blue text-white
hover:   bg-corp-blue-hover
focus:   outline 2px corp-blue offset 2px
active:  scale-98 (sutil)
disabled: bg-muted text-muted-foreground cursor-not-allowed
```

### Botão de opção (escolha do jogador)

```
default: bg-surface border-2 border-muted text-primary
hover:   border-corp-blue bg-corp-blue-light
focus:   outline 2px corp-blue offset 2px
active:  bg-corp-blue text-white border-corp-blue (durante click)
selected (após escolha): bg-corp-blue text-white (estado momentâneo antes de transição)
disabled (opção bloqueada por requisito): hidden — não mostra
```

**Importante:** opções bloqueadas por `requires` não ficam grayed-out — somem completamente. Informação que o jogador não merece.

---

## 7. Motion design

### Princípios

- Duração curta: 120-300ms para UI, até 800ms para transições de cena.
- Easing: `ease-out` por padrão. `ease-in-out` para idle/loop.
- Sem bounce. Sem spring. Sem overshoot.
- Animação serve a comunicar estado, não a entreter.

### Transições padronizadas

```css
:root {
  --transition-fast: 120ms ease-out;
  --transition-base: 200ms ease-out;
  --transition-slow: 320ms ease-out;
}
```

### Microanimações específicas

**Mudança de atributo após escolha:**
- Pulse de cor na barra: 600ms, ease-out.
- Número incrementa/decrementa em ~400ms.
- Pequeno glow na cor `--accent-positive` ou `--accent-negative` ao redor da barra (8px box-shadow que esmaece).

**Transição entre eventos:**
- Fade out da cena atual: 200ms.
- 100ms de buffer (cena em branco).
- Fade in da próxima cena: 300ms.
- Total: ~600ms.

**Entrada da tela de final:**
- Score conta de 0 até valor real em ~1.2s (ease-out, tipo contador estilo "stat number").
- Sem confete. Sem fireworks. Esta não é uma vitória — é o resultado.

### `prefers-reduced-motion`

Toda animação tem fallback:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 8. Ícones de atributo

SVG simples 24x24, traços de 2px, cor `currentColor` (herda do contexto).

| Atributo | Ícone sugerido | Comentário |
|---|---|---|
| Energia | bateria meia / raio | Não usar bateria cheia (parece full sempre) |
| Reputação | estrela contorno | Não preencher — implica julgamento |
| Networking | dois círculos conectados | Não usar handshake (estereotipado) |
| Ansiedade | onda / círculo concêntrico | Evitar coração agitado |
| Produtividade | checkmark em quadrado | Simples e claro |
| Aprendizado | livro aberto / lâmpada | Cuidado com lâmpada (clichê) |

Recomendação: usar **Lucide Icons** (open source, MIT, lightweight). Stack já tem `lucide-react` provavelmente disponível.

---

## 9. Sombras e estados de carregamento

### Skeleton

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--bg-muted) 25%,
    #F0EDE6 50%,
    var(--bg-muted) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}

@keyframes skeleton-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; background: var(--bg-muted); }
}
```

### Estado vazio

Texto centralizado em `--text-secondary`, sem ilustração. Mensagem direta:

> "Nenhuma partida em andamento."

Sem "oops!", sem emoji, sem ilustração espaçonave.

### Estado de erro

Ícone de alerta simples + mensagem em `--accent-negative` + botão de retry. Sem dramatização.

---

## 10. Responsividade

### Breakpoints (Tailwind padrão)

| Token | Mínimo | Uso |
|---|---|---|
| `sm:` | 640px | Tablet retrato |
| `md:` | 768px | Tablet paisagem |
| `lg:` | 1024px | Desktop |
| `xl:` | 1280px | Desktop largo |

### Layout por tamanho

**Mobile (< 640px):**
- Coluna única.
- Cena ocupa 100% largura.
- Painel de atributos colapsa em barra horizontal acima da cena (ícones + número, sem labels).
- Opções em coluna full-width.

**Tablet (640-1024px):**
- Cena ocupa largura completa.
- Painel de atributos lateral em coluna estreita à esquerda.
- Opções em coluna no centro.

**Desktop (≥ 1024px):**
- Cena com `max-width: 720px` centralizada.
- Painel de atributos lateral fixo à esquerda.
- Opções abaixo da cena.

---

## 11. Tela inicial (Home)

Composição específica:

```
┌─────────────────────────────────────┐
│  Corporate Survivor       (título)  │
│                                     │
│  Sobreviva à sua primeira semana    │
│  como trainee.       (subtítulo)    │
│                                     │
│  [SVG ilustrativa pequena]          │
│  scene: mesa-trabalho (variante     │
│  vazia, sem personas)               │
│                                     │
│  [ Começar nova jornada ]  primário │
│   Ver ranking global       link     │
└─────────────────────────────────────┘
```

Se há sessão salva, card aparece acima dos botões:

```
┌─────────────────────────────────────┐
│ ⏵ Você tem uma jornada em andamento│
│   Dia 3 de 5                        │
│   [ Continuar ]                     │
└─────────────────────────────────────┘
```

---

## 12. Tela de final

Layout específico:

```
┌─────────────────────────────────────┐
│   [SVG da persona trainee em        │
│   estado correspondente ao final]   │
│                                     │
│   Final                             │
│   Trainee Lenda      (text-3xl)     │
│                                     │
│   Já estão falando que você não     │
│   parece trainee.                   │
│                                     │
│   Estado final:                     │
│   [Painel de atributos com valores] │
│                                     │
│   Score: 387                        │
│   Top 18% do ranking                │
│                                     │
│   [ Ver ranking completo ]          │
│   [ Jogar novamente ]               │
└─────────────────────────────────────┘
```

Cor do "Final" varia conforme tipo:
- Finais bons (`trainee_lenda`, `promessa`): `--accent-positive`
- Finais neutros (`sobrevivente`): `--text-primary`
- Finais ruins (`demitido`, `burnout`, `risco_op`): `--accent-negative`
- `invisivel`: `--text-secondary` (apropriado)

---

## 13. Ranking

Tabela simples:

```
┌──────────────────────────────────────────┐
│ Ranking Global                           │
│                                          │
│ # │ Jogador  │ Final           │ Score   │
│ ──┼──────────┼─────────────────┼──────── │
│ 1 │ Diego    │ Trainee Lenda   │ 412     │
│ 2 │ ...                                  │
│                                          │
│ Sua posição: 7 (destacada)               │
└──────────────────────────────────────────┘
```

Linha do jogador atual destacada com `background: var(--corp-blue-light)`.

---

## 14. Checklist de revisão visual por tela

Antes de declarar uma tela pronta, conferir:

- [ ] Paleta usa apenas variáveis CSS definidas (sem hex hardcoded).
- [ ] Tipografia segue escala (sem font-size custom).
- [ ] Espaçamento múltiplo de 4px.
- [ ] Animações respeitam reduced-motion.
- [ ] Contraste validado em ferramenta (Lighthouse / axe).
- [ ] Layout testado em 360px, 768px, 1280px.
- [ ] Foco visível em todos interativos via Tab.
- [ ] Heading hierarchy correta.
- [ ] Ícones têm `aria-hidden="true"` se decorativos.
- [ ] Imagens têm alt descritivo ou vazio.

---

## 15. Pequeno guia para o Cursor / LLM

Ao implementar um componente novo:

1. Não invente cor. Use as variáveis. Se precisar de cor nova, propor adição ao style guide via ADR.
2. Não invente tamanho de fonte. Use a escala.
3. Não invente animação dramática. Releia a seção Motion.
4. Não use `<img src="*.gif">`. Use SVG ou Lottie.
5. Em dúvida, leia este arquivo de novo.
