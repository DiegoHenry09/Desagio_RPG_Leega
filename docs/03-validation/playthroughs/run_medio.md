# Playthrough: run_medio — Final `sobrevivente`

**Objetivo:** demonstrar que o final fallback `sobrevivente` é alcançável com o catálogo Sprint 1.2.  
**Condição do final:** fallback — nenhum predicado de maior prioridade ativado  
**Gerado em:** 2026-05-14 — Sprint 1.2

---

## Estado inicial

| Atributo     | Valor |
|--------------|-------|
| energia      | 7     |
| reputacao    | 5     |
| networking   | 3     |
| ansiedade    | 2     |
| produtividade| 5     |
| aprendizado  | 4     |

---

## Dia 1 — Segunda

### ev_day1_001 — Onboarding com RH → **Opção A**
"Tomar notas detalhadas em um caderno."  
Delta: aprendizado +2, energia -1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| aprendizado| 4     | +2    | 6      |
| energia    | 7     | -1    | 6      |

### ev_day1_002 — O primeiro almoço → **Opção A**
"Aceitar o convite e ir junto."  
Delta: networking +2, energia -1, ansiedade +1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| networking | 3     | +2    | 5      |
| energia    | 6     | -1    | 5      |
| ansiedade  | 2     | +1    | 3      |

### ev_day1_003 — Setup pendente → **Opção A**
"Procurar a documentação interna no Confluence/Notion e começar a estudar."  
Delta: aprendizado +2, produtividade +1, energia -1

| Atributo      | Antes | Delta | Depois |
|---------------|-------|-------|--------|
| aprendizado   | 6     | +2    | 8      |
| produtividade | 5     | +1    | 6      |
| energia       | 5     | -1    | 4      |

**Estado após Dia 1:** ene=4, rep=5, net=5, ans=3, pro=6, apr=8

---

## Dia 2 — Terça

### ev_day2_001 — Tarefa de escopo vago → **Opção C**
"Perguntar a um trainee mais antigo ou colega o que ele costuma entregar pro gestor."  
Delta: networking +1, aprendizado +1, reputacao -1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| networking | 5     | +1    | 6      |
| aprendizado| 8     | +1    | 9      |
| reputacao  | 5     | -1    | 4      |

### ev_day2_002 — Duas urgências → **Opção B**
"Responder ao gestor: 'vou priorizar — me dá 1h' e cuidar dele primeiro."  
Delta: reputacao +1, networking -1, energia -1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| reputacao  | 4     | +1    | 5      |
| networking | 6     | -1    | 5      |
| energia    | 4     | -1    | 3      |

### ev_day2_003 — Crítica pública em reunião → **Opção B**
"Defender o trabalho explicando as restrições de tempo que você teve."  
Delta: reputacao +1, networking -1, ansiedade +1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| reputacao  | 5     | +1    | 6      |
| networking | 5     | -1    | 4      |
| ansiedade  | 3     | +1    | 4      |

**Estado após Dia 2:** ene=3, rep=6, net=4, ans=4, pro=6, apr=9

---

## Dia 3 — Quarta

### ev_day3_001 — Reunião sem pauta → **Opção A**
"Entrar com notebook fechado, prestar atenção e tomar notas."  
Delta: aprendizado +1, energia -1

| Atributo   | Antes | Delta | Depois (clamp) |
|------------|-------|-------|----------------|
| aprendizado| 9     | +1    | 10 (clamped)   |
| energia    | 3     | -1    | 2              |

### ev_day3_002 — Convite para happy hour → **Opção B**
"Recusar dizendo que já tem compromisso pessoal."  
Delta: energia +1, networking -2

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| energia    | 2     | +1    | 3      |
| networking | 4     | -2    | 2      |

### ev_day3_003 — Pedido de última hora → **Opção B**
"Responder 'consigo amanhã cedo com mais segurança, ok?'"  
Delta: reputacao +1, produtividade -1, ansiedade -1

| Atributo      | Antes | Delta | Depois |
|---------------|-------|-------|--------|
| reputacao     | 6     | +1    | 7      |
| produtividade | 6     | -1    | 5      |
| ansiedade     | 4     | -1    | 3      |

**Estado após Dia 3:** ene=3, rep=7, net=2, ans=3, pro=5, apr=10

---

## Dia 4 — Quinta

### ev_day4_001 — Mentoria oferecida → **Opção A**
"Aceitar e dedicar uma hora antes da reunião preparando perguntas concretas."  
Delta: aprendizado +3, networking +2, energia -2

| Atributo   | Antes | Delta | Depois (clamp) |
|------------|-------|-------|----------------|
| aprendizado| 10    | +3    | 10 (clamped)   |
| networking | 2     | +2    | 4              |
| energia    | 3     | -2    | 1              |

### ev_day4_002 — Erro descoberto → **Opção B**
"Corrigir em silêncio e torcer para ninguém perceber o original."  
Delta: ansiedade +2

| Atributo  | Antes | Delta | Depois |
|-----------|-------|-------|--------|
| ansiedade | 3     | +2    | 5      |

### ev_day4_003 — Pedido de feedback → **Opção C**
"Pedir tempo para pensar e mandar por escrito até sexta."  
Delta: reputacao +1, aprendizado +1, produtividade -1

| Atributo      | Antes | Delta | Depois (clamp) |
|---------------|-------|-------|----------------|
| reputacao     | 7     | +1    | 8              |
| aprendizado   | 10    | +1    | 10 (clamped)   |
| produtividade | 5     | -1    | 4              |

**Estado após Dia 4:** ene=1, rep=8, net=4, ans=5, pro=4, apr=10

---

## Dia 5 — Sexta

### ev_day5_001 — Apresentação para o time → **Opção C**
"Pedir para adiar a apresentação para a próxima semana."  
Delta: energia +2, reputacao -3

| Atributo  | Antes | Delta | Depois |
|-----------|-------|-------|--------|
| energia   | 1     | +2    | 3      |
| reputacao | 8     | -3    | 5      |

### ev_day5_002 — Almoço com a gerente → **Opção B**
"Manter a conversa cordial mas guardada, falar pouco de você."  
Delta: energia -1

| Atributo | Antes | Delta | Depois |
|----------|-------|-------|--------|
| energia  | 3     | -1    | 2      |

### ev_day5_003 — Tarefa final, 17h45 → **Opção C**
"Dizer honestamente: 'tô exausto, prefiro entregar bem feito na segunda cedo.'"  
Delta: energia +2, reputacao -1, aprendizado +1

| Atributo   | Antes | Delta | Depois (clamp) |
|------------|-------|-------|----------------|
| energia    | 2     | +2    | 4              |
| reputacao  | 5     | -1    | 4              |
| aprendizado| 10    | +1    | 10 (clamped)   |

---

## Estado final

| Atributo      | Valor |
|---------------|-------|
| energia       | 4     |
| reputacao     | 4     |
| networking    | 4     |
| ansiedade     | 5     |
| produtividade | 4     |
| aprendizado   | 10    |

## Verificação dos predicados (ordem de prioridade)

| Predicado          | Condição                                           | Resultado |
|--------------------|----------------------------------------------------|-----------|
| demitido (100)     | reputacao <= 1                                     | ❌ (rep=4)|
| burnout (95)       | energia <= 1 AND ansiedade >= 8                    | ❌        |
| risco_op (80)      | produtividade <= 2 AND reputacao <= 3              | ❌        |
| invisivel (60)     | networking <= 2 AND reputacao <= 4 AND apr <= 4    | ❌ (net=4)|
| trainee_lenda (50) | rep >= 8 AND net >= 7 AND apr >= 7 AND pro >= 7    | ❌        |
| promessa (40)      | rep >= 6 AND (apr >= 6 OR pro >= 7)                | ❌ (rep=4)|
| sobrevivente (0)   | True (fallback)                                    | ✅ **ATIVADO** |

**Final: `sobrevivente`** — "Você terminou a primeira semana. Não é pouco."

## Score calculado

```
base = 4*12 + 4*10 + 10*9 + 4*8 + 4*5 + 5*(-7)
     = 48 + 40 + 90 + 32 + 20 - 35 = 195
bonus = 60 (sobrevivente)
completion = 5 dias × 5 = 25
score = max(0, 195 + 60 + 25) = 280
```

## Secretos desbloqueados neste run

Nenhum: reputação e networking não atingiram threshold de `ev_secret_001`, e ansiedade nunca chegou a 7 para `ev_secret_002`.
