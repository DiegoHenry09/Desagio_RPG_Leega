# Event Visuals Map — Mapeamento explícito evento ↔ visual

Para cada um dos 15 eventos principais + 2 secretos, define qual cena e quais personas aparecem.

Este arquivo é a fonte da verdade para o campo `visuals` no `events.json`. Quando uma persona/cena é adicionada ou alterada, atualizar este mapa primeiro.

---

## Notação

```
EVENTO_ID — Título curto
  scene: <scene-id>
  personas: [<persona-id>, ...]  # ordem importa: define posição na cena via anchors
  nota: comentário opcional
```

---

## Dia 1 — Segunda — Chegada

### `ev_day1_001` — Onboarding com RH
- scene: `sala-reuniao`
- personas: `[rh, trainee]`
- nota: RH em pé na cabeceira (posição central), trainee sentado à mesa (posição direita)

### `ev_day1_002` — O primeiro almoço
- scene: `restaurante`
- personas: `[colega, trainee]`
- nota: usar variante Marina ou Bruno aleatoriamente; trainee à direita

### `ev_day1_003` — Setup pendente
- scene: `mesa-trabalho`
- personas: `[trainee]`
- nota: trainee sozinho, postura levemente frustrada

---

## Dia 2 — Terça — Primeiras entregas

### `ev_day2_001` — Tarefa de escopo vago
- scene: `mesa-trabalho`
- personas: `[gestor, trainee]`
- nota: gestor em pé ao lado da mesa (esquerda), trainee sentado (centro)

### `ev_day2_002` — Duas urgências
- scene: `mesa-trabalho`
- personas: `[colega, trainee]`
- nota: colega aproximando da mesa, expressão de pedido

### `ev_day2_003` — Crítica em reunião
- scene: `sala-reuniao`
- personas: `[senior, trainee, gestor]`
- nota: senior à esquerda (quem fala), trainee centro (foco), gestor à direita (observando)

---

## Dia 3 — Quarta — Pressão real

### `ev_day3_001` — Reunião sem pauta
- scene: `sala-reuniao`
- personas: `[gestor, trainee, colega]`
- nota: composição mais cheia — pode adicionar silhuetas desfocadas extras se desejar

### `ev_day3_002` — Convite para happy hour
- scene: `bar`
- personas: `[colega, trainee]`
- nota: cena ainda sem trainee no bar — opcional renderizar trainee chegando

### `ev_day3_003` — Pedido de última hora (18h)
- scene: `mesa-trabalho`
- personas: `[trainee]`
- nota: trainee sozinho, notebook aberto, telefone na mão (notification recebida)

---

## Dia 4 — Quinta — Cansaço e oportunidade

### `ev_day4_001` — Mentoria oferecida
- scene: `mesa-trabalho`
- personas: `[senior, trainee]`
- nota: senior puxa cadeira ao lado da mesa do trainee — composição íntima

### `ev_day4_002` — Erro descoberto
- scene: `mesa-trabalho`
- personas: `[trainee]`
- nota: trainee sozinho, postura tensa, olhando a tela

### `ev_day4_003` — Pedido de feedback
- scene: `sala-reuniao`
- personas: `[gerente, trainee]`
- nota: gerente à esquerda, trainee à direita, mesa entre eles. Composição 1-on-1

---

## Dia 5 — Sexta — Encerramento

### `ev_day5_001` — Apresentação para o time
- scene: `sala-apresentacao`
- personas: `[trainee]`
- nota: trainee no centro, em pé. Slide neutro atrás. Silhuetas vazias da plateia opcionais

### `ev_day5_002` — Almoço com a gerente
- scene: `restaurante`
- personas: `[gerente, trainee]`
- nota: similar ao `ev_day1_002` mas com gerente em vez de colega — escolha visual diferente da persona

### `ev_day5_003` — Tarefa final, 17h45
- scene: `mesa-trabalho`
- personas: `[trainee]`
- nota: trainee sozinho, escritório vazio implícito (sem outras silhuetas)

---

## Eventos secretos

### `ev_secret_001` — Convite para projeto especial
- scene: `mesa-trabalho`
- personas: `[lider-externo, trainee]`
- nota: lider-externo em pé ao lado da mesa, postura aberta convidativa

### `ev_secret_002` — Crise emocional no banheiro
- scene: `banheiro`
- personas: `[trainee]`
- nota: cena íntima, apenas trainee em frente ao espelho. Tratar com cuidado visual — sem dramatização. Iluminação calma, não cores intensas.

---

## Estatísticas do mapeamento

| Cena | Eventos que usam |
|---|---|
| `mesa-trabalho` | 8 (mais usada — vale caprichar) |
| `sala-reuniao` | 4 |
| `restaurante` | 2 |
| `bar` | 1 |
| `sala-apresentacao` | 1 |
| `banheiro` | 1 (secreto) |
| `copa` | 0 (reserva para eventos futuros) |

| Persona | Eventos onde aparece |
|---|---|
| `trainee` | 17 (todos) |
| `gestor` | 3 (`day2_001`, `day2_003`, `day3_001`) |
| `gerente` | 2 (`day4_003`, `day5_002`) |
| `colega` | 4 (`day1_002`, `day2_002`, `day3_001`, `day3_002`) |
| `senior` | 2 (`day2_003`, `day4_001`) |
| `rh` | 1 (`day1_001`) |
| `lider-externo` | 1 (`secret_001`) |

Cobertura razoável: cada persona aparece em pelo menos um evento, todas têm pelo menos 1 ocorrência de "foco" (não só fundo).

---

## Como o backend e o frontend usam este mapa

### Backend

Backend **não usa** este mapa. O campo `visuals` no `events.json` é opaco para a engine — passa transparente do JSON para o DTO de saída da API.

### Frontend

O frontend usa o mapa indiretamente, via `events.json`. Cada evento já tem o `visuals` declarado. O componente `EventStage`:

```tsx
function EventStage({ event }) {
  const { scene, personas } = event.visuals || { scene: '_default', personas: [] }
  const anchors = sceneAnchors[scene]

  return (
    <div className="event-stage">
      <SceneSVG sceneId={scene} />
      {personas.map((personaId, idx) => (
        <PersonaSVG
          key={personaId}
          personaId={personaId}
          anchor={anchors[idx]}
        />
      ))}
    </div>
  )
}
```

Se persona ou cena referenciada não existe no `_index.ts`, fallback para placeholder. Logar warning no console em dev.

---

## Atualizando o mapa

Ao adicionar evento novo no `events.json`:

1. Decidir cena (reusar das 7 ou propor nova em `scenes.md`).
2. Decidir personas envolvidas.
3. Atualizar este arquivo com a nova entrada.
4. Adicionar `visuals` no JSON do evento.
5. Se persona ou cena nova: criar assets antes de mergear.

---

## Conferência final (Sprint 4)

Antes de fechar Sprint 4, validar manualmente:

- [ ] Todos os 17 eventos renderizam corretamente no GamePage.
- [ ] Nenhum console warning sobre asset não encontrado.
- [ ] Cada persona aparece em pelo menos 1 evento com posicionamento correto.
- [ ] Mobile (360px) e desktop (1280px) renderizam consistentemente.
- [ ] Modo reduced-motion: tudo estático e legível.
