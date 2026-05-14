# Playthrough: run_demitido — Final antecipado `demitido`

**Objetivo:** demonstrar que o final antecipado `demitido` é alcançável com o catálogo Sprint 1.2.  
**Condição do final antecipado:** `reputacao <= 0` após clamp (ADR-010, prioridade 1)  
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

### ev_day1_003 — Setup pendente → **Opção C**
"Esperar a TI resolver. Aproveitar para descansar disfarçado."  
Delta: energia +2, reputacao -2, aprendizado -1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| energia    | 5     | +2    | 7      |
| reputacao  | 5     | -2    | 3      |
| aprendizado| 6     | -1    | 5      |

**Estado após Dia 1:** ene=7, rep=3, net=5, ans=3, pro=5, apr=5

---

## Dia 2 — Terça

### ev_day2_001 — Tarefa de escopo vago → **Opção C**
"Perguntar a um trainee mais antigo ou colega o que ele costuma entregar pro gestor."  
Delta: networking +1, aprendizado +1, reputacao -1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| networking | 5     | +1    | 6      |
| aprendizado| 5     | +1    | 6      |
| reputacao  | 3     | -1    | 2      |

### ev_day2_002 — Duas urgências → **Opção C**
"Tentar fazer os dois em paralelo, alternando entre as duas tarefas."  
Delta: produtividade -1, energia -2, ansiedade +3

| Atributo      | Antes | Delta | Depois |
|---------------|-------|-------|--------|
| produtividade | 5     | -1    | 4      |
| energia       | 7     | -2    | 5      |
| ansiedade     | 3     | +3    | 6      |

### ev_day2_003 — Crítica pública em reunião → **Opção C**
"Concordar em silêncio, agradecer e dizer que vai refazer."  
Delta: energia -1, reputacao -1, aprendizado +1

| Atributo   | Antes | Delta | Depois |
|------------|-------|-------|--------|
| energia    | 5     | -1    | 4      |
| reputacao  | 2     | -1    | 1      |
| aprendizado| 6     | +1    | 7      |

**Estado após Dia 2:** ene=4, rep=1, net=6, ans=6, pro=4, apr=7

---

## Dia 3 — Quarta

### ev_day3_001 — Reunião sem pauta → **Opção C**
"Levar trabalho paralelo discretamente para fazer durante a reunião."  
Delta: produtividade +1, reputacao -2

| Atributo      | Antes | Delta | Depois (clamp) |
|---------------|-------|-------|----------------|
| produtividade | 4     | +1    | 5              |
| reputacao     | 1     | -2    | **0 (clamped)**|

**→ CHECAGEM DE GATILHO ANTECIPADO:**  
`reputacao = 0 ≤ 0` → **gatilho `reputation_zero` disparado**  
**Final antecipado: `demitido`**

---

## Estado no momento do final antecipado

| Atributo      | Valor |
|---------------|-------|
| energia       | 4     |
| reputacao     | 0     |
| networking    | 6     |
| ansiedade     | 6     |
| produtividade | 5     |
| aprendizado   | 7     |

**dias_completed = 2** (Dias 1 e 2 com 3 eventos principais concluídos)

## Verificação do gatilho

Avaliação na ordem ADR-010 após clamp de ev_day3_001 C:

| Ordem | Condição          | Resultado           |
|-------|-------------------|---------------------|
| 1     | reputacao <= 0    | ✅ **DISPARADO**    |
| 2     | energia <= 0      | ❌ (não avaliado)   |
| 3     | ansiedade >= 10   | ❌ (não avaliado)   |

`trigger_name = "reputation_zero"` → `ending_id = "demitido"`

**Final: `demitido`** — "Sua presença foi prejuízo visível para o time."

## Score calculado

```
base = 0*12 + 5*10 + 7*9 + 6*8 + 4*5 + 6*(-7)
     = 0 + 50 + 63 + 48 + 20 - 42 = 139
bonus = -100 (demitido)
completion = 2 dias × 5 = 10
score = max(0, 139 - 100 + 10) = 49
```

## Secretos desbloqueados neste run

Nenhum: reputação e networking nunca atingiram o threshold de `ev_secret_001`, e ansiedade nunca chegou a 7 para `ev_secret_002`.
