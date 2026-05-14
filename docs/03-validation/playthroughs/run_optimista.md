# Playthrough: run_optimista — Final `trainee_lenda`

**Objetivo:** demonstrar que o final `trainee_lenda` é alcançável com o catálogo Sprint 1.2.  
**Condição do final:** `reputacao >= 8 AND networking >= 7 AND aprendizado >= 7 AND produtividade >= 7`  
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

### ev_day1_001 — Onboarding com RH → **Opção B**
"Aproveitar as pausas para conversar com os outros trainees."  
Delta: networking +2, ansiedade +1, aprendizado -1

| Atributo     | Antes | Delta | Depois |
|--------------|-------|-------|--------|
| networking   | 3     | +2    | 5      |
| ansiedade    | 2     | +1    | 3      |
| aprendizado  | 4     | -1    | 3      |

### ev_day1_002 — O primeiro almoço → **Opção A**
"Aceitar o convite e ir junto."  
Delta: networking +2, energia -1, ansiedade +1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| networking | 5     | +2    | 7      |
| energia    | 7     | -1    | 6      |
| ansiedade  | 3     | +1    | 4      |

### ev_day1_003 — Setup pendente → **Opção B**
"Mandar uma mensagem objetiva para o gestor avisando dos bloqueios."  
Delta: reputacao +2, ansiedade +1, energia -1

| Atributo  | Antes | Delta | Depois |
|-----------|-------|-------|--------|
| reputacao | 5     | +2    | 7      |
| ansiedade | 4     | +1    | 5      |
| energia   | 6     | -1    | 5      |

**Estado após Dia 1:** ene=5, rep=7, net=7, ans=5, pro=5, apr=3

---

## Dia 2 — Terça

### ev_day2_001 — Tarefa de escopo vago → **Opção A**
"Pedir 15 minutos de alinhamento para entender o público e o nível de detalhe esperado."  
Delta: reputacao +2, produtividade +1, energia -1

| Atributo      | Antes | Delta | Depois |
|---------------|-------|-------|--------|
| reputacao     | 7     | +2    | 9      |
| produtividade | 5     | +1    | 6      |
| energia       | 5     | -1    | 4      |

### ev_day2_002 — Duas urgências → **Opção B**
"Responder ao gestor: 'vou priorizar — me dá 1h' e cuidar dele primeiro."  
Delta: reputacao +1, networking -1, energia -1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| reputacao  | 9     | +1    | 10     |
| networking | 7     | -1    | 6      |
| energia    | 4     | -1    | 3      |

### ev_day2_003 — Crítica pública em reunião → **Opção A**
"Reconhecer publicamente, perguntar quais pontos especificamente faltaram e anotar."  
Delta: aprendizado +3, reputacao +2, ansiedade +2

| Atributo   | Antes | Delta | Depois (clamp) |
|------------|-------|-------|----------------|
| aprendizado| 3     | +3    | 6              |
| reputacao  | 10    | +2    | 10 (clamped)   |
| ansiedade  | 5     | +2    | 7              |

**→ ansiedade = 7 ≥ 7: `ev_secret_002` elegível!**

### SECRETO: ev_secret_002 — Crise emocional no banheiro → **Opção A**
"Mandar uma mensagem para alguém em quem confia."  
Delta: ansiedade -3, networking +1, reputacao -1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| ansiedade  | 7     | -3    | 4      |
| networking | 6     | +1    | 7      |
| reputacao  | 10    | -1    | 9      |

**Estado após Dia 2 + secreto:** ene=3, rep=9, net=7, ans=4, pro=6, apr=6

---

## Dia 3 — Quarta

### ev_day3_001 — Reunião sem pauta → **Opção A**
"Entrar com notebook fechado, prestar atenção e tomar notas."  
Delta: aprendizado +1, energia -1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| aprendizado| 6     | +1    | 7      |
| energia    | 3     | -1    | 2      |

### ev_day3_002 — Convite para happy hour → **Opção C**
"Aceitar mas avisar que sai antes das 22h."  
Delta: networking +1, energia -1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| networking | 7     | +1    | 8      |
| energia    | 2     | -1    | 1      |

### ev_day3_003 — Pedido de última hora → **Opção C**
"Pedir mais contexto antes de aceitar: 'qual o escopo exato e até que hora vc precisa?'"  
Delta: aprendizado +2, reputacao +1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| aprendizado| 7     | +2    | 9      |
| reputacao  | 9     | +1    | 10     |

**→ rep=10 ≥ 7 e net=8 ≥ 5 e current_day=3 ≥ 3: `ev_secret_001` elegível!**

### SECRETO: ev_secret_001 — Convite para projeto especial → **Opção B**
"Pedir um dia para pensar e conversar com sua gerente direta antes."  
Delta: reputacao +2, aprendizado +1

| Atributo   | Antes | Delta | Depois (clamp) |
|------------|-------|-------|----------------|
| reputacao  | 10    | +2    | 10 (clamped)   |
| aprendizado| 9     | +1    | 10 (clamped)   |

**Estado após Dia 3 + secreto:** ene=1, rep=10, net=8, ans=4, pro=6, apr=10

---

## Dia 4 — Quinta

### ev_day4_001 — Mentoria oferecida → **Opção B**
"Aceitar mas chegar sem se preparar; deixar a conversa fluir."  
Delta: aprendizado +1, networking +1, reputacao -1

| Atributo   | Antes | Delta | Depois (clamp) |
|------------|-------|-------|----------------|
| aprendizado| 10    | +1    | 10 (clamped)   |
| networking | 8     | +1    | 9              |
| reputacao  | 10    | -1    | 9              |

### ev_day4_002 — Erro descoberto → **Opção A**
"Avisar o gestor proativamente, mostrar o problema e já trazer a correção."  
Delta: reputacao +3, ansiedade +1, aprendizado +1

| Atributo   | Antes | Delta | Depois (clamp) |
|------------|-------|-------|----------------|
| reputacao  | 9     | +3    | 10 (clamped)   |
| ansiedade  | 4     | +1    | 5              |
| aprendizado| 10    | +1    | 10 (clamped)   |

### ev_day4_003 — Pedido de feedback → **Opção A**
"Dar feedback estruturado com dois pontos positivos e dois pontos a melhorar."  
Delta: reputacao +2, networking +1, aprendizado +1, ansiedade +1

| Atributo   | Antes | Delta | Depois (clamp) |
|------------|-------|-------|----------------|
| reputacao  | 10    | +2    | 10 (clamped)   |
| networking | 9     | +1    | 10 (clamped)   |
| aprendizado| 10    | +1    | 10 (clamped)   |
| ansiedade  | 5     | +1    | 6              |

**Estado após Dia 4:** ene=1, rep=10, net=10, ans=6, pro=6, apr=10

---

## Dia 5 — Sexta

### ev_day5_001 — Apresentação para o time → **Opção C**
"Pedir para adiar a apresentação para a próxima semana."  
Delta: energia +2, reputacao -3

| Atributo  | Antes | Delta | Depois |
|-----------|-------|-------|--------|
| energia   | 1     | +2    | 3      |
| reputacao | 10    | -3    | 7      |

> Nota: Opção C escolhida para recuperar energia crítica. Perde reputação mas mantém viabilidade do final.

### ev_day5_002 — Almoço com a gerente → **Opção A**
"Compartilhar abertamente o que você aprendeu, dúvidas reais e expectativas de carreira."  
Delta: reputacao +2, networking +2, aprendizado +1, ansiedade +1

| Atributo   | Antes | Delta | Depois (clamp) |
|------------|-------|-------|----------------|
| reputacao  | 7     | +2    | 9              |
| networking | 10    | +2    | 10 (clamped)   |
| aprendizado| 10    | +1    | 10 (clamped)   |
| ansiedade  | 6     | +1    | 7              |

### ev_day5_003 — Tarefa final, 17h45 → **Opção B**
"Pedir o escopo, avaliar, dar um prazo realista para segunda de manhã."  
Delta: produtividade +1, reputacao +2, aprendizado +1

| Atributo      | Antes | Delta | Depois (clamp) |
|---------------|-------|-------|----------------|
| produtividade | 6     | +1    | 7              |
| reputacao     | 9     | +2    | 10 (clamped)   |
| aprendizado   | 10    | +1    | 10 (clamped)   |

---

## Estado final

| Atributo      | Valor |
|---------------|-------|
| energia       | 3     |
| reputacao     | 10    |
| networking    | 10    |
| ansiedade     | 7     |
| produtividade | 7     |
| aprendizado   | 10    |

## Verificação dos predicados (ordem de prioridade)

| Predicado      | Condição                                        | Resultado |
|----------------|-------------------------------------------------|-----------|
| demitido (100) | reputacao <= 1                                  | ❌ (rep=10)|
| burnout (95)   | energia <= 1 AND ansiedade >= 8                 | ❌ (ene=3) |
| risco_op (80)  | produtividade <= 2 AND reputacao <= 3           | ❌        |
| invisivel (60) | networking <= 2 AND reputacao <= 4 AND apr <= 4 | ❌        |
| trainee_lenda (50) | rep >= 8 AND net >= 7 AND apr >= 7 AND pro >= 7 | ✅ **ATIVADO** |

**Final: `trainee_lenda`** — "Já estão falando que você não parece trainee."

## Score calculado

```
base = 10*12 + 7*10 + 10*9 + 10*8 + 3*5 + 7*(-7)
     = 120 + 70 + 90 + 80 + 15 - 49 = 326
bonus = 200 (trainee_lenda)
completion = 5 dias × 5 = 25
score = max(0, 326 + 200 + 25) = 551
```

## Secretos desbloqueados neste run

- `ev_secret_002` (após ev_day2_003 — ansiedade atingiu 7)
- `ev_secret_001` (após ev_day3_003 — rep ≥ 7 e net ≥ 5 a partir do dia 3)
