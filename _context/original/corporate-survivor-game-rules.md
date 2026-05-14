# Corporate Survivor — Game Rules & Catálogo de Eventos

Documento de referência narrativo e técnico do jogo. Fonte da verdade para o Agent Engine/Content.

---

## 1. Atributos

Seis atributos. Range inteiro 0..10 com clamp nos extremos.

| Atributo | Inicial | Sentido | Descrição |
|---|---|---|---|
| Energia | 7 | Alto é bom | Capacidade física e mental do jogador no momento. Esgota com escolhas demandantes. Recupera com escolhas mais leves. |
| Reputação | 5 | Alto é bom | Como o jogador é percebido por gestores e pares. Cresce com entregas e postura; cai com falhas visíveis. |
| Networking | 3 | Alto é bom | Qualidade dos vínculos profissionais formados na semana. Cresce com interação social; cai com isolamento. |
| Ansiedade | 2 | **Alto é ruim** | Carga emocional acumulada. Cresce com estresse e exposição; cai com pausas e clareza. |
| Produtividade | 5 | Alto é bom | Output efetivo entregue pelo jogador. Sobe com foco e execução; cai com dispersão. |
| Aprendizado | 4 | Alto é bom | Quanto o jogador absorveu sobre a empresa, processo, e a si mesmo. Sobe com curiosidade ativa. |

**Por que esses valores iniciais:**
- Energia 7: jogador chega descansado.
- Reputação 5: neutra, ainda não construiu nem destruiu.
- Networking 3: baixo porque é o primeiro dia; quase ninguém conhece.
- Ansiedade 2: existe (é primeira semana) mas não é problema ainda.
- Produtividade 5: neutra, ainda sem entrega real.
- Aprendizado 4: começa baixo porque ainda não conhece o ambiente.

**Soma inicial: 22 sobre máximo de 60 (sem ansiedade) — espaço claro para crescer ou cair.**

---

## 2. Schema final do `events.json`

```json
{
  "schemaVersion": "1.0",
  "events": [ Event, Event, ... ]
}
```

### Tipo `Event`

```typescript
{
  "id": string,              // único; convenção: ev_dayN_NNN (principal) ou ev_secret_NNN (secreto)
  "isMain": boolean,         // true = evento principal de um dia
  "day": 1 | 2 | 3 | 4 | 5 | null,  // obrigatório se isMain=true; null se secreto
  "sequence": 1 | 2 | 3 | null,      // obrigatório se isMain=true: ordem dentro do dia
  "title": string,           // exibido na tela
  "scene": string,           // texto narrativo (1-3 parágrafos)
  "feedback"?: string,       // opcional, narrativa pós-escolha curta
  "tags": string[],          // ex: ["social", "entrega", "pressao"]
  "unlock"?: UnlockCondition, // só faz sentido em secretos; ignorado se isMain=true
  "options": Option[]        // entre 2 e 4
}
```

### Tipo `Option`

```typescript
{
  "id": "A" | "B" | "C" | "D",
  "label": string,                 // texto da escolha
  "consequences": Consequences,    // delta por atributo
  "requires"?: OptionRequirement,  // condições para a opção aparecer
  "unlocks"?: string[],            // event_ids de secretos que esta escolha habilita
  "blocks"?: string[]              // event_ids de secretos que esta escolha desabilita
}
```

### Tipo `Consequences`

```typescript
{
  "energia"?: number,        // delta inteiro, tipicamente -3 a +3
  "reputacao"?: number,
  "networking"?: number,
  "ansiedade"?: number,
  "produtividade"?: number,
  "aprendizado"?: number
}
```

Soma absoluta dos deltas de uma opção: ≤ 7. Isso evita escolhas "milagrosas" (todos positivos altos) ou "catastróficas" (todos negativos altos).

### Tipo `UnlockCondition` (só para secretos)

```typescript
{
  "requires_all"?: string[],         // todos esses event_ids precisam ter sido vivenciados
  "requires_any"?: string[],         // pelo menos um
  "blocked_by"?: string[],           // se algum desses foi vivenciado, este NÃO aparece
  "min_attrs"?: Partial<Attributes>, // ex: {"reputacao": 7}
  "max_attrs"?: Partial<Attributes>, // ex: {"ansiedade": 4}
  "after_day"?: number,              // só aparece a partir desse dia
  "before_day"?: number              // só aparece até esse dia
}
```

### Tipo `OptionRequirement`

Mesma forma de `UnlockCondition`. Aplicado a opções individuais — se o requisito não é atendido, a opção não aparece na UI.

---

## 3. Finais (registry de predicados)

Definidos em `backend/engine/endings.py` com decorator `@register_ending`. Avaliados ao fim do dia 5 (15 eventos principais concluídos) em ordem de prioridade decrescente. Primeiro predicado que retorna `True` define o final.

| ID | Nome | Prioridade | Predicado (em pseudo-código) | Descrição |
|---|---|---|---|---|
| `demitido` | Demitido no Período de Experiência | 100 | `reputacao <= 1` | Sua presença foi prejuízo visível para o time. |
| `burnout` | Burnout em Tempo Recorde | 95 | `energia <= 1 AND ansiedade >= 8` | Você não chegou à sexta inteiro. Seu corpo cobrou antes da empresa cobrar. |
| `risco_op` | Risco Operacional | 80 | `produtividade <= 2 AND reputacao <= 3` | Você passou despercebido pelas pessoas certas e marcado pelas erradas. |
| `invisivel` | Funcionário Invisível | 60 | `networking <= 2 AND reputacao <= 4 AND aprendizado <= 4` | Cinco dias se passaram. Quase ninguém sabe seu nome. |
| `trainee_lenda` | Trainee Lenda | 50 | `reputacao >= 8 AND networking >= 7 AND aprendizado >= 7 AND produtividade >= 7` | Já estão falando que você não parece trainee. |
| `promessa` | Promessa Corporativa | 40 | `reputacao >= 6 AND (aprendizado >= 6 OR produtividade >= 7)` | Há expectativa real sobre você. |
| `sobrevivente` | Sobrevivente do Onboarding | 0 | `True` (fallback) | Você terminou a primeira semana. Não é pouco. |

**Por que a ordem importa:** finais negativos têm prioridade alta para "capturar" estados ruins antes que predicados positivos os reivindiquem. Ex.: um jogador com reputação 1 mas produtividade 8 cai em `demitido`, não em `promessa`.

**Estados ambíguos:** se nenhum predicado positivo bate mas nenhum negativo também, cai em `sobrevivente`. Isso é o estado-médio.

**Sete finais cobrem o desafio:** o desafio cita exemplos com 7 finais — todos cobertos.

---

## 4. Regra de progressão (5 dias × 3 eventos)

### 4.1 Fluxo da sessão

```
Estado inicial: day=1, sequence=1, atributos iniciais.

Loop principal:
  evento_atual = catálogo.principal(day=current_day, sequence=current_sequence)
  apresentar evento_atual ao jogador
  jogador escolhe opção X
  aplicar consequências de X
  registrar em choices_log
  verificar secretos elegíveis (ver 4.2)
  se houve secreto elegível:
    apresentar secreto
    jogador escolhe
    aplicar consequências
    registrar
  avançar:
    se current_sequence < 3:
      current_sequence += 1
    senão se current_day < 5:
      current_day += 1
      current_sequence = 1
    senão:
      → resolver final
```

### 4.2 Elegibilidade de secretos

Após cada escolha em um evento principal, a engine verifica todos os secretos do catálogo:

```python
for secreto in catalogo.secretos():
    if já_foi_vivenciado(secreto, state.history):
        continue
    if not condicao_atendida(secreto.unlock, state):
        continue
    return secreto  # primeiro elegível
return None
```

No máximo um secreto entre dois principais. Se múltiplos elegíveis, escolha o de menor `id` lexicograficamente (determinístico).

### 4.3 Invariantes verificados em `validate_events()`

1. `schemaVersion == "1.0"`.
2. Para cada `day` em 1..5: existem exatamente 3 eventos com `isMain: true` e `day: day`.
3. Para cada principal: `sequence` é 1, 2 ou 3, e os 3 valores aparecem uma vez por dia.
4. Para cada secreto: `isMain: false`, `day: null`, `unlock` presente com ao menos uma condição.
5. Todo `event_id` em `unlocks`/`blocks`/`requires_all`/`requires_any`/`blocked_by` existe.
6. Toda `option` tem 1-4 opções e cada opção tem ID único entre A, B, C, D.
7. Soma absoluta dos deltas de cada opção ≤ 7.
8. Atributos referenciados em consequências e unlocks pertencem aos 6 atributos válidos.
9. Nenhum evento referencia a si mesmo.

Validação acontece no boot do FastAPI. Falha = boot falha.

### 4.4 Final antecipado: **não há** (decisão ADR-007)

Mesmo se o jogador chegar a energia 0 e ansiedade 10 no dia 2, o jogo continua. O final é resolvido sempre no fim do dia 5. Isso simplifica engine, UI e testes. Final `burnout` ou `demitido` é interpretação narrativa do estado final, não interrupção mecânica.

Trade-off honesto: o desafio menciona "fim de jogo se atributo chega a zero". Estamos optando por uma interpretação que mantém o loop uniforme. ADR-007 registra essa interpretação.

---

## 5. Os 15 eventos principais

Tom: corporativo brasileiro realista. Sem vilões. Sem heróis. Cada opção é defensável em algum contexto e tem custo em outro. Quem joga deve sentir que escolhe entre trade-offs, não entre certo e errado.

### Dia 1 — Segunda — Chegada

#### `ev_day1_001` — Onboarding com RH (sequence 1)

**Cena:** O RH reservou a sala de reunião grande para a apresentação de boas-vindas. São oito trainees novos sentados em volta da mesa oval. A apresentadora projeta o slide de cultura da empresa. A apresentação está marcada para durar duas horas e quinze minutos.

**Opções:**
- **A — Tomar notas detalhadas em um caderno.**
  - aprendizado +2, energia -1
- **B — Aproveitar as pausas para conversar com os outros trainees.**
  - networking +2, ansiedade +1, aprendizado -1
- **C — Levantar a mão quando abrem espaço para perguntar sobre benefícios e horário flexível.**
  - reputação +1, networking -1, ansiedade +1

#### `ev_day1_002` — O primeiro almoço (sequence 2)

**Cena:** Meio-dia. Três pessoas do seu time direto aparecem na sua mesa. "Vamos almoçar? Tem um japonês legal aqui perto, é mais caro mas vale." Você não conhece ninguém ainda. O almoço cabe no seu orçamento, mas com aperto.

**Opções:**
- **A — Aceitar o convite e ir junto.**
  - networking +2, energia -1, ansiedade +1
- **B — Agradecer e dizer que precisa resolver algo, vai sozinho a algo mais simples.**
  - energia +1, networking -2
- **C — Ir junto mas pedir só uma entrada para gastar menos.**
  - networking +1, ansiedade +2

#### `ev_day1_003` — Setup pendente (sequence 3)

**Cena:** A TI ainda não liberou seus acessos críticos. Você tem três horas até o fim do expediente sem conseguir fazer nada do que foi previsto. Seu gestor está em reunião e não pode te atender agora.

**Opções:**
- **A — Procurar a documentação interna no Confluence/Notion e começar a estudar.**
  - aprendizado +2, produtividade +1, energia -1
- **B — Mandar uma mensagem objetiva para o gestor avisando dos bloqueios e o que vai fazer enquanto isso.**
  - reputação +2, ansiedade +1, energia -1
- **C — Esperar a TI resolver. Aproveitar para descansar disfarçado.**
  - energia +2, reputação -2, aprendizado -1

---

### Dia 2 — Terça — Primeiras entregas

#### `ev_day2_001` — Tarefa de escopo vago (sequence 1)

**Cena:** Seu gestor te chama: "Toma, dá uma estudada nesse caso e me devolve um resumo executivo até amanhã." Ele te encaminha um documento de 40 páginas sem dizer o que considera um bom resumo, nem quem é o público.

**Opções:**
- **A — Pedir 15 minutos de alinhamento para entender o público e o nível de detalhe esperado.**
  - reputação +2, produtividade +1, energia -1
- **B — Começar a ler e fazer um resumo bem-feito que cobre tudo, deduzindo o escopo.**
  - produtividade +2, energia -2, ansiedade +1
- **C — Perguntar a um trainee mais antigo ou colega o que ele costuma entregar pro gestor.**
  - networking +1, aprendizado +1, reputação -1

#### `ev_day2_002` — Duas urgências (sequence 2)

**Cena:** 14h30. Sua colega de outro time vem na sua mesa e pede um favor "rapidinho" que vai tomar uma hora sua. Cinco minutos depois, seu gestor manda mensagem pedindo um ajuste em algo que você já entregou. Os dois estão te olhando.

**Opções:**
- **A — Avisar a colega que você vai priorizar a demanda do gestor e refazer o ajuste primeiro.**
  - reputação +1, networking -2
- **B — Responder ao gestor: "vou priorizar — me dá 1h" e cuidar dele primeiro.**
  - reputação +1, networking -1, energia -1
- **C — Tentar fazer os dois em paralelo, alternando entre as duas tarefas.**
  - produtividade -1, energia -2, ansiedade +3

#### `ev_day2_003` — Crítica pública em reunião (sequence 3)

**Cena:** Na daily, alguém sênior comenta em voz alta sobre o documento que você entregou: "tá bem cru, dá pra ver que faltou contexto." A sala fica em silêncio. As pessoas estão te olhando.

**Opções:**
- **A — Reconhecer publicamente, perguntar quais pontos especificamente faltaram e anotar.**
  - aprendizado +3, reputação +2, ansiedade +2
- **B — Defender o trabalho explicando as restrições de tempo que você teve.**
  - reputação +1, networking -1, ansiedade +1
- **C — Concordar em silêncio, agradecer e dizer que vai refazer.**
  - energia -1, reputação -1, aprendizado +1

---

### Dia 3 — Quarta — Pressão real

#### `ev_day3_001` — Reunião sem pauta (sequence 1)

**Cena:** Convite no calendário: "Alinhamento — 1h". Sem agenda, sem descrição, sem documento prévio. Onze participantes. Começa em cinco minutos.

**Opções:**
- **A — Entrar com notebook fechado, prestar atenção e tomar notas.**
  - aprendizado +1, energia -1
- **B — Logo no início, perguntar educadamente qual é o objetivo da reunião e o que se espera dela.**
  - reputação +2, networking -1, ansiedade +1
- **C — Levar trabalho paralelo discretamente para fazer durante a reunião.**
  - produtividade +1, reputação -2

#### `ev_day3_002` — Convite para happy hour (sequence 2)

**Cena:** Final do dia. "Galera vai no bar de sempre amanhã depois do trabalho, vem com a gente?" É um momento informal real do time. Você está cansado e tem que acordar cedo na sexta.

**Opções:**
- **A — Aceitar e ir junto.**
  - networking +3, energia -2, ansiedade +1
- **B — Recusar dizendo que já tem compromisso pessoal.**
  - energia +1, networking -2
- **C — Aceitar mas avisar que sai antes das 22h.**
  - networking +1, energia -1
- **D — (Requer reputação ≥ 6) Aceitar e oferecer carona para quem mora do seu lado.**
  - networking +3, reputação +1, energia -2

#### `ev_day3_003` — Pedido de última hora (sequence 3)

**Cena:** 18h02. Mensagem do gestor: "Rapidinho, consegue subir isso hoje?" Você já está saindo. Não está claro o tamanho do "isso". Sua família te espera para jantar.

**Opções:**
- **A — Responder "claro, pode deixar comigo" e ficar até resolver.**
  - produtividade +2, energia -3, ansiedade +1, reputação +1
- **B — Responder "consigo amanhã cedo com mais segurança, ok?"**
  - reputação +1, produtividade -1, ansiedade -1
- **C — Pedir mais contexto antes de aceitar: "qual o escopo exato e até que hora vc precisa?"**
  - aprendizado +2, reputação +1
- **D — Não responder agora e responder amanhã de manhã.**
  - energia +1, reputação -3

---

### Dia 4 — Quinta — Cansaço e oportunidade

#### `ev_day4_001` — Mentoria oferecida (sequence 1)

**Cena:** Uma pessoa sênior do time, com quase 10 anos de empresa, te chama e oferece 30 minutos no fim do dia "se você quiser tirar dúvidas, eu lembro como é começar aqui."

**Opções:**
- **A — Aceitar e dedicar uma hora antes da reunião preparando perguntas concretas.**
  - aprendizado +3, networking +2, energia -2
- **B — Aceitar mas chegar sem se preparar; deixar a conversa fluir.**
  - aprendizado +1, networking +1, reputação -1
- **C — Agradecer mas recusar dizendo que está cheio de coisa essa semana.**
  - energia +1, networking -2, aprendizado -1

#### `ev_day4_002` — Erro descoberto (sequence 2)

**Cena:** Você descobre que aquela entrega de terça tinha um erro factual. Ninguém percebeu ainda, mas alguém pode perceber a qualquer momento. O erro é seu.

**Opções:**
- **A — Avisar o gestor proativamente, mostrar o problema e já trazer a correção.**
  - reputação +3, ansiedade +1, aprendizado +1
- **B — Corrigir em silêncio e torcer para ninguém perceber o original.**
  - ansiedade +2, reputação 0
- **C — Esperar para ver se alguém aponta antes de agir.**
  - ansiedade +3, reputação -2 (se descoberto: -4)

#### `ev_day4_003` — Pedido de feedback (sequence 3)

**Cena:** Sua gerente direta te chama: "Como você tá vendo a semana? Quero feedback honesto do onboarding — o que tá funcionando e o que tá ruim."

**Opções:**
- **A — Dar feedback estruturado com dois pontos positivos e dois pontos a melhorar.**
  - reputação +2, networking +1, aprendizado +1, ansiedade +1
- **B — Dar feedback genérico positivo: "tá tudo bem, gostando muito."**
  - energia +1, reputação -2
- **C — Pedir tempo para pensar e mandar por escrito até sexta.**
  - reputação +1, aprendizado +1, produtividade -1

---

### Dia 5 — Sexta — Encerramento

#### `ev_day5_001` — Apresentação para o time (sequence 1)

**Cena:** Você precisa fazer uma apresentação de 10 minutos para o time inteiro (uns 15 pessoas) sobre o que aprendeu na semana. Marcada para depois do almoço.

**Opções:**
- **A — Preparar slides estruturados na manhã, com problemas que você identificou.**
  - reputação +3, produtividade +2, energia -2, ansiedade +2
- **B — Apresentar sem slides, falando livremente sobre as experiências.**
  - networking +2, reputação +1, ansiedade +3
- **C — Pedir para adiar a apresentação para a próxima semana, alegando que ainda tem coisa a digerir.**
  - energia +2, reputação -3

#### `ev_day5_002` — Almoço com a gerente (sequence 2)

**Cena:** Sua gerente convida para almoçar só vocês dois. "Quero bater um papo mais aberto sobre como você tá vendo a empresa." O restaurante é tranquilo.

**Opções:**
- **A — Compartilhar abertamente o que você aprendeu, dúvidas reais e expectativas de carreira.**
  - reputação +2, networking +2, aprendizado +1, ansiedade +1
- **B — Manter a conversa cordial mas guardada, falar pouco de você.**
  - reputação 0, energia -1
- **C — Recusar dizendo que precisa terminar coisa pendente para sexta.**
  - produtividade +1, reputação -2, networking -2

#### `ev_day5_003` — Tarefa final, 17h45 (sequence 3)

**Cena:** Faltam 15 minutos para o fim da semana. Mensagem da gerente: "Surgiu uma coisa de última hora, dá pra resolver hoje? Não é trivial mas não é absurdo."

**Opções:**
- **A — Aceitar e ficar o tempo que for necessário até entregar.**
  - produtividade +2, reputação +2, energia -3, ansiedade +1
- **B — Pedir o escopo, avaliar, dar um prazo realista para segunda de manhã.**
  - produtividade +1, reputação +2, aprendizado +1
- **C — Dizer honestamente: "tô exausto, prefiro entregar bem feito na segunda cedo."**
  - energia +2, reputação -1, aprendizado +1
- **D — (Requer ansiedade ≥ 7) Recusar dizendo que não tem condição agora.**
  - energia +2, ansiedade -2, reputação -3

---

## 6. Eventos secretos opcionais (2)

#### `ev_secret_001` — Convite para projeto especial

**Unlock:**
```json
{
  "min_attrs": { "reputacao": 7, "networking": 5 },
  "after_day": 3
}
```

**Cena:** Um líder de outra área que você nem conhece bem para na sua mesa: "Soube que você está mandando bem. Tô montando um time pequeno para um projeto interno que vai começar mês que vem. Topa entrar?"

**Opções:**
- **A — Aceitar imediatamente.**
  - networking +3, reputação +1, energia -1, ansiedade +1
- **B — Pedir um dia para pensar e conversar com sua gerente direta antes.**
  - reputação +2, aprendizado +1
- **C — Agradecer mas recusar dizendo que ainda está se ambientando.**
  - reputação -1, ansiedade -1

#### `ev_secret_002` — Crise emocional no banheiro

**Unlock:**
```json
{
  "min_attrs": { "ansiedade": 7 }
}
```

**Cena:** Você entra no banheiro do andar e percebe que está respirando rápido demais. A mão está suando. Você não está bem.

**Opções:**
- **A — Mandar uma mensagem para alguém em quem confia (amigo, terapeuta, RH).**
  - ansiedade -3, networking +1, reputação -1
- **B — Esperar passar sozinho, lavar o rosto, voltar para mesa.**
  - ansiedade -1, energia -2
- **C — Avisar a gerente que precisa sair mais cedo hoje.**
  - ansiedade -2, energia +1, reputação -2

---

## 7. Tabela de tensão por dia

Mostra qual atributo cada dia mais estressa. Garante que a semana não seja monótona — cada dia toca dimensões diferentes.

| Dia | Atributos mais pressionados | Atributos mais favorecidos |
|---|---|---|
| 1 | Networking (criar do zero), Energia | Aprendizado (muito a absorver) |
| 2 | Reputação (primeiras entregas), Ansiedade | Produtividade, Aprendizado |
| 3 | Energia, Ansiedade (semana acumulando) | Networking, Produtividade |
| 4 | Reputação (julgamento se forma), Aprendizado | Aprendizado, Networking |
| 5 | Ansiedade (encerramento), Energia | Reputação (chance de fechar bem) |

**Padrão narrativo:** começa social (dia 1), vira entrega (dia 2-3), confronta erro (dia 4), exige síntese (dia 5).

---

## 8. Score final

```python
ATTR_WEIGHTS = {
    "reputacao": 12,
    "produtividade": 10,
    "aprendizado": 9,
    "networking": 8,
    "energia": 5,
    "ansiedade": -7,  # penaliza
}

ENDING_BONUS = {
    "trainee_lenda": 200,
    "promessa": 120,
    "sobrevivente": 60,
    "invisivel": 20,
    "risco_op": 0,
    "burnout": -50,
    "demitido": -100,
}

def compute_score(state, ending_id):
    base = sum(getattr(state.attributes, a) * w for a, w in ATTR_WEIGHTS.items())
    bonus = ENDING_BONUS[ending_id]
    # bônus por completar a semana (cada dia tem peso pequeno)
    completion = state.days_completed * 5
    return max(0, base + bonus + completion)
```

Range esperado: ~0 a ~500. Médio: ~200.

---

## 9. Validação obrigatória do catálogo

Script `python -m engine.validate_events` confere:

1. Schema version `"1.0"`.
2. Exatamente 3 principais por dia × 5 dias = 15 principais.
3. Para cada dia, `sequence` cobre {1, 2, 3} sem repetição.
4. Secretos têm `isMain: false`, `day: null`, e ao menos uma condição de unlock.
5. Toda referência de ID (em unlocks/blocks/requires_*) aponta para evento existente.
6. Cada opção tem 1-4 opções com IDs únicos em {A, B, C, D}.
7. Soma absoluta de deltas por opção ≤ 7.
8. Atributos referenciados são os 6 oficiais.
9. Nenhum evento referencia a si mesmo.
10. Cada opção tem `label` não-vazio.

Falha = exit 1 = boot do FastAPI não conclui.

---

## 10. Checklist de balanceamento (após produzir todos os eventos)

Antes de fechar a Sprint 1, verificar manualmente:

- [ ] Cada um dos 7 finais é alcançável em pelo menos um playthrough simulado.
- [ ] Não há opção dominante em nenhum evento (sempre puxa um atributo e fragiliza outro).
- [ ] Soma dos deltas máximos possíveis em 15 eventos cobre o range 0..10 com folga em ambas as direções para cada atributo.
- [ ] Nenhum dia tem 3 eventos focados no mesmo atributo (variedade).
- [ ] Eventos secretos não são óbvios de unlockar (caso contrário, viram principais).

Documentar 3 playthroughs em `docs/playthroughs/`:
- `run_optimista.md` — caminho que alcança `trainee_lenda`
- `run_demitido.md` — caminho que alcança `demitido`
- `run_medio.md` — caminho que alcança `sobrevivente`

Esses playthroughs servem de teste de regressão narrativa e prova manual de que o jogo "funciona como jogo".
