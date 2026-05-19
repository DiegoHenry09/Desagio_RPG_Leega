# Personas — Catálogo detalhado

Catálogo completo das personas representadas visualmente no Corporate Survivor. Cada persona tem identidade visual estável que aparece em qualquer evento onde for referenciada.

**Princípios de representação:**

- Diversidade real de gênero, etnia e idade refletindo escritórios brasileiros.
- Sem caricatura, sem estereótipo.
- Vestimenta corporate-casual (não de terno, não de tênis sujo).
- Expressão facial sutil — nunca exagerada.
- Postura comunica papel mais que vestuário.

---

## `trainee` — O Protagonista (Você)

**Papel narrativo:** o jogador. Aparece em quase todos os eventos.

**Identidade visual:**
- Avatar levemente genérico para permitir projeção.
- Idade aparente: 22-28.
- Vestimenta: camisa social casual ou camiseta com camisa aberta por cima.
- Postura: aberta, atenta, levemente ansiosa nos primeiros dias.
- Acessório recorrente: notebook ou bloco de notas.

**Paleta sugerida (CSS vars no SVG):**
```
--skin: #D4A574 (variar entre 3 tons em variantes alt para diversidade)
--shirt: #6BA8B0 (azul-petróleo claro)
--pants: #2D3748
--hair: #2D2A28
```

**Variantes:** criar 3 versões (trainee-1, trainee-2, trainee-3) com tons de pele e cabelo diferentes. Frontend escolhe aleatoriamente na criação do player (`localStorage` salva a escolha).

**Expressão padrão:** neutra, atenta. Pode variar conforme contexto (ler texto da cena para decidir).

**Postura por cena:**
- Sala de reunião: sentado, postura levemente curvada para frente.
- Mesa de trabalho: sentado de frente para o notebook.
- Bar/restaurante: postura mais relaxada.
- Banheiro: em pé, frente ao espelho, postura tensa.

---

## `gestor` — Gestor direto (Rafael)

**Papel narrativo:** quem delega tarefas, dá feedback de curto prazo. Aparece em eventos de pedidos urgentes, escopo vago.

**Identidade visual:**
- Idade aparente: 38-45.
- Etnia: várias possíveis — proposta: pardo, cabelo curto grisalho nas têmporas.
- Vestimenta: camisa polo ou camisa social sem gravata. Calça social.
- Postura: gesticula levemente quando fala. Olhar direto sem ser intimidador.

**Paleta:**
```
--skin: #B98A6B
--shirt: #3B5B7C (corp-blue)
--pants: #2D3748
--hair: #4A3F3A com #999999 nas têmporas
```

**Acessório recorrente:** crachá pendurado, smartphone na mão.

**Expressão padrão:** atenta, profissional. Em eventos de cobrança: sobrancelha levemente elevada, sem severidade.

**Anti-padrão a evitar:** terno e gravata, relógio Rolex aparente, postura intimidadora. Não é Wolf of Wall Street.

---

## `gerente` — Gerente da área (Camila)

**Papel narrativo:** liderança sênior, dá feedback estratégico, conversa de carreira. Aparece em eventos de feedback formal, almoço de fim de semana.

**Identidade visual:**
- Idade aparente: 42-50.
- Etnia: várias — proposta: branca, cabelo castanho médio amarrado em rabo de cavalo baixo.
- Vestimenta: blusa lisa + calça social ou saia midi. Sem joia chamativa.
- Postura: confiante mas acessível. Sentada com braços relaxados quando ouve.

**Paleta:**
```
--skin: #E8C8A8
--shirt: #5E8F73 (verde musgo)
--pants: #4A4945
--hair: #6B5544
```

**Expressão padrão:** olhar atento, leve meio-sorriso. Não é "boazinha" caricata — é alguém que escuta.

---

## `colega` — Par no time (Bruno ou Marina)

**Papel narrativo:** colega de trabalho do mesmo nível. Convida para almoço, happy hour, pede favores.

**Identidade visual:** duas variantes intercambiáveis.

### Variante Bruno (masculino)
- Idade: 26-32.
- Vestimenta: camiseta + camisa aberta, jeans.
- Postura: relaxada.
```
--skin: #A06F4A
--shirt: #A07AB8 / shirt-open: #1F2937
--pants: #4A3F3A
```

### Variante Marina (feminino)
- Idade: 26-32.
- Vestimenta: blusa básica, jeans.
- Postura: relaxada, gesticula com a mão.
```
--skin: #D4A574
--shirt: #C97A6E
--pants: #2D3748
```

Frontend pode alternar entre as duas em eventos diferentes para dar variedade visual.

**Expressão padrão:** amigável sem ser invasiva.

---

## `rh` — Apresentadora do RH (Patrícia)

**Papel narrativo:** facilitadora do onboarding. Aparece principalmente no `ev_day1_001`.

**Identidade visual:**
- Idade: 32-40.
- Etnia: proposta: parda.
- Vestimenta: blusa cor sólida + calça social. Crachá visível com cor distinta.
- Postura: em pé na variante "apresentação", gesticula com slide ao fundo.

**Paleta:**
```
--skin: #C99878
--shirt: #C0875A (caramelo)
--pants: #2D3748
--hair: #2D2A28 cacheado solto
```

**Expressão padrão:** profissional, acolhedora. Não é a "tia do RH" caricata — é uma profissional sênior fazendo um trabalho.

---

## `senior` — Mentor sênior (Eduardo)

**Papel narrativo:** profissional veterano que oferece mentoria, faz crítica construtiva, dá perspectiva.

**Identidade visual:**
- Idade: 45-55.
- Etnia: várias — proposta: branco, cabelo grisalho curto, barba pequena também grisalha.
- Vestimenta: camisa lisa, manga curta ou enrolada. Calça cargo ou jeans escuro.
- Postura: tranquila, mãos no colo ou sobre a mesa. Não invade espaço.

**Paleta:**
```
--skin: #DDB69A
--shirt: #4A5568
--pants: #2D3748
--hair: #8A8580 (grisalho)
```

**Expressão padrão:** observadora, atenta. Quando fala em reunião (crítica pública no `ev_day2_003`): expressão neutra-séria, sem agressão.

**Anti-padrão:** não é "velho ranzinza" nem "gandalf corporativo". É um profissional que viu muita coisa e fala sem peso emocional.

---

## `lider-externo` — Líder de outra área (Ana)

**Papel narrativo:** aparece no evento secreto `ev_secret_001`, ofertando projeto especial.

**Identidade visual:**
- Idade: 38-46.
- Etnia: proposta: negra, cabelo natural curto ou trança presa.
- Vestimenta: blazer sobre blusa básica, calça social escura. Confiança vestida.
- Postura: em pé, postura aberta de quem está propondo algo.

**Paleta:**
```
--skin: #6B4533
--shirt: #1F2937 (blazer) sobre #F5F4F0 (blusa clara)
--pants: #1F2937
--hair: #2D2A28
```

**Expressão padrão:** energia genuína de quem viu potencial em alguém.

---

## Composição em cena

Cada cena tem 3 pontos de ancoragem onde personas podem ser colocadas (definidos em `scene-anchors.ts`). Regras:

- **trainee sempre presente:** posição varia por cena (centro em sala de reunião, lado direito em mesa de trabalho).
- **Persona principal do evento ocupa posição mais próxima do trainee** ou em foco da composição.
- **Personas de fundo (≥ 3 na cena):** desfocadas via filter SVG `<filter><feGaussianBlur stdDeviation="1.5"/></filter>` para não competir.

Exemplo `ev_day2_003` (Crítica em reunião):
- Posição 0 (esquerda): `senior` (quem fala a crítica)
- Posição 1 (centro): `trainee`
- Posição 2 (direita): `gestor` (silencioso, observando)

---

## Estados visuais por estado de jogo (opcional)

Se quiser sofisticação extra no Sprint 4: a persona `trainee` pode ter sutis variações visuais conforme atributos:

- Ansiedade ≥ 7: postura mais curvada, leve círculo escuro sob os olhos.
- Energia ≤ 3: ombros caídos.
- Reputação ≥ 8: postura mais ereta, sutil sorriso.

Implementar via classes CSS aplicadas ao SVG do trainee:
```tsx
<TraineeSVG className={`
  ${state.ansiedade >= 7 && 'persona-anxious'}
  ${state.energia <= 3 && 'persona-tired'}
  ${state.reputacao >= 8 && 'persona-confident'}
`} />
```

Cada classe ajusta `transform` e talvez `filter` no SVG. Mantém o asset base único.

**Não é obrigatório.** Implementar só se Sprint 4 sobrar tempo. ADR-009 cobre se ativado.
