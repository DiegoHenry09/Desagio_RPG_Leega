# Architecture Decision Records — Corporate Survivor

Formato sugerido por ADR:

```
## ADR-XXX — <título curto>

- Status: Proposta | Aceita | Substituída
- Data: YYYY-MM-DD
- Contexto: ...
- Decisão: ...
- Consequências: ...
```

Registre decisões relevantes antes de mudanças estruturais ou quando houver trade-off importante.

---

## ADR-006 — Alembic vs `create_all` no SQLite

- **Status:** Proposta  
- **Contexto:** Ambiente corporativo pode impedir Alembic ou adicionar fricção na Sprint 0 executável.  
- **Decisão:** Tentar Alembic primeiro; se inviável, usar `Base.metadata.create_all(engine)` no startup do FastAPI para SQLite deste projeto.  
- **Consequências:** Menos histórico formal de schema; aceitável para escopo local/demo se documentado em `docs/00-start/setup-company-env.md`.

---

## ADR-007 — Sem final antecipado por atributo zerado

- **Status:** **Substituída por ADR-010 (2026-05-14)**  
- **Contexto (histórico):** Alguns desafios pedem "game over" ao zerar atributo; aumenta ramificações na UX e na engine.  
- **Decisão (histórica):** Ficou pendente. A auditoria da Sprint 0.1 apontou conflito potencial com o enunciado, que cita fim de jogo por atributo zerado, burnout e demissão.  
- **Resolução:** Sprint 1.0 fechou a decisão em ADR-010 — ver abaixo.  
- **Consequências:** Substituída integralmente; nenhum efeito ativo sobre a engine ou sprints futuras a partir desta data.

---

## ADR-008 — Node.js portátil (WinGet bloqueado)

- **Status:** Registro factual — Ambiente empresa  
- **Contexto:** `winget install OpenJS.NodeJS.20 --scope user` falhou com **acesso negado** ao diretório `WinGet\Packages`. Node 20 LTS foi instalado via ZIP portátil em `%LOCALAPPDATA%\CorporateSurvivorTools\...` + PATH usuário.  
- **Decisão:** Prosseguir sem chamado TI até travar onboarding ou atualização de toolchain; documentar em `docs/00-start/setup-company-env.md` e `PROJECT_STATUS.md`.  
- **Consequências:** Repetibilidade depende do mesmo layout PATH; onboarding externo deve seguir documentação atualizada.

---

## ADR-009 — Critério de aceite para outputs de LLM

- **Status:** Aceita  
- **Data:** 2026-05-14  
- **Contexto:** A auditoria apontou que havia governança, mas faltava matriz clara de aceitar/rejeitar output de LLM.  
- **Decisão:** Nenhum output de LLM será aceito sem checkpoint, escopo, evidência, handoff e respeito ao agente/sprint.  
- **Consequências:** Reduz achismo, aumenta rastreabilidade, pode deixar o processo um pouco mais lento e evita implementação fora do tema/desafio.

---

## ADR-010 — Final antecipado por atributo crítico (substitui ADR-007)

- **Status:** Aceita  
- **Data:** 2026-05-14  
- **Sprint:** 1.0 — Regras críticas do jogo e contrato da engine  
- **Substitui:** ADR-007  
- **Contexto:**
  - O enunciado em [`desafio_trainees_cursor_v3.pdf`](../../desafio_trainees_cursor_v3.pdf) lista entre as **Condições de fim de jogo**: "a semana termina (sexta-feira); algum atributo chega a zero; o personagem é demitido; o personagem entra em burnout; o personagem se torna destaque da equipe; o personagem sobrevive normalmente ao onboarding".
  - A Sprint 0.1 deixou em aberto se a engine deveria interromper a sessão antes do dia 5 quando uma condição crítica ocorresse, ou se tudo seria resolvido apenas ao fim do dia 5.
  - A Sprint 1.1 (engine skeleton) **não pode começar** sem regra unívoca: o validador, os tipos de estado e o fluxo da engine dependem de saber se existe ou não saída antecipada.

- **Decisão:**
  Sim, existe **final antecipado**. A engine encerra a sessão imediatamente após uma escolha (principal ou secreta) cujo efeito, **após clamp**, atinge um dos seguintes limiares — avaliados nesta ordem de prioridade:

  1. `reputacao <= 0` → final aplicado: `demitido`.
  2. `energia <= 0` → final aplicado: `burnout` (esgotamento físico).
  3. `ansiedade >= 10` → final aplicado: `burnout` (esgotamento psicológico).

  Os atributos `produtividade`, `aprendizado` e `networking` **não** disparam final antecipado; eles influenciam o final ao fim do dia 5 (predicados em [`docs/02-product/game-rules.md`](../02-product/game-rules.md) §3, ex.: `risco_op`, `invisivel`) e o `compute_score` (§8).

  Detalhes operacionais (ordem de avaliação, momento da checagem, score, ranking) ficam em [`docs/02-product/game-rules.md`](../02-product/game-rules.md) §4.4 — fonte da verdade para a engine.

- **Justificativa interpretativa do requisito "algum atributo chega a zero":**
  O enunciado fala genericamente em "atributo chega a zero", mas precisa ser interpretado à luz dos demais itens da mesma lista ("demitido", "burnout"), que indicam **estados narrativos críticos**, não baixa performance circunstancial.
  - **`energia <= 0` encerra:** energia zero é o canal narrativo direto de **burnout físico** — o personagem não consegue mais entregar nem se recompor dentro da semana.
  - **`reputacao <= 0` encerra:** reputação zero é o canal narrativo direto de **demissão** — o personagem perdeu a posição no período de experiência. É a única perda **objetivamente contratual** entre os atributos.
  - **`ansiedade >= 10` encerra (teto crítico, não chão):** ansiedade tem sentido invertido (alto é ruim). O equivalente narrativo de "chegar ao fundo" para ansiedade é **chegar ao topo do range**. Por isso o gatilho é `>= 10`, não `<= 0`. É o canal narrativo direto de **burnout psicológico**.
  - **`produtividade <= 0`, `aprendizado <= 0`, `networking <= 0` NÃO encerram imediatamente, mas impactam finais e score:** esses três atributos são de **construção** da semana (entregar bem, aprender, fazer rede), não de **sobrevivência**. Um trainee com `produtividade = 0` ainda está empregado, ainda tem chefia, ainda entra na sexta-feira; o efeito desse zero aparece via predicados de fim de semana (`risco_op`: `produtividade <= 2 AND reputacao <= 3`; `invisivel`: `networking <= 2 AND reputacao <= 4 AND aprendizado <= 4`) e via penalidade no `compute_score`. Tratar esses três como gatilhos antecipados criaria **múltiplas saídas pequenas** sem ganho narrativo, frustraria o jogador no meio da semana e contrariaria a leitura conjunta do enunciado, que combina "atributo zerado" com "demitido"/"burnout" como sinônimos do mesmo tipo de colapso.

- **Justificativa da prioridade dos gatilhos:**
  Quando, num mesmo passo, mais de uma condição dispara, a engine resolve na ordem 1 → 2 → 3 abaixo. A ordem reflete **gravidade narrativa decrescente** e **independência das demais**:

  1. **`reputacao <= 0` primeiro — demissão / perda objetiva da posição.** A demissão **interrompe a relação contratual**: uma vez demitido, o personagem não está mais na empresa, então qualquer outro colapso (físico ou psicológico) que ocorreria nas próximas escolhas perde contexto. É a única condição que envolve **terceiros tomando uma decisão sobre o jogador**, e por isso tem precedência: o jogo registra "Demitido" no lugar de "Burnout" se ambos ocorrerem na mesma escolha.
  2. **`energia <= 0` depois — esgotamento físico.** Energia zerada significa que o personagem **deixa de entregar** (e fisicamente colapsa: sai mais cedo, falta, adoece). É grave, mas a relação contratual ainda existe — por isso vem depois da demissão. É um colapso do **corpo do personagem**, anterior à manifestação psicológica plena.
  3. **`ansiedade >= 10` por último — burnout psicológico.** Ansiedade no teto é o canal **mais volátil** do jogo (sobe e desce muito entre escolhas) e é o último canal de colapso a se materializar como saída da semana. Vem por último porque, em termos narrativos, o burnout psicológico costuma se manifestar como **consequência** ou **acompanhamento** de esgotamento físico ou pressão por reputação, não como causa primária — quando os outros dois não dispararam, ele captura especificamente o caso de quem sobrecarregou o emocional sem destruir corpo nem reputação.

  Importante: ordens 2 e 3 mapeiam para o mesmo final (`burnout`); a ordem só importa para **diagnóstico/log narrativo** ("trigger: energy_zero" vs "trigger: anxiety_max") e para coerência semântica do final exibido.

- **Consequências:**
  - Engine deve checar gatilhos imediatamente após `clamp`, antes de avançar `sequence/day`, e re-checar após aplicação de evento secreto.
  - Ranking armazena **toda** sessão finalizada (incluindo antecipada), conforme `compute_score` em [`docs/02-product/game-rules.md`](../02-product/game-rules.md) §8.
  - Validador `validate_events()` precisa garantir que os IDs `demitido` e `burnout` existem no registry de finais.
  - UX precisa preparar telas de "final antecipado" (sprint futura de UX completa).
  - Os atributos não-críticos não exigem variação no fluxo principal — apenas predicados de fim de semana já existentes.

---

## Pendências de ADR

- Deploy intranet / domínios CORS definitivos.  
- Política de logs e retenção de PII (apenas nome do jogador em logs — ver plano).
