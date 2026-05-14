# Cursor workflow — Corporate Survivor

## Princípio

Antes de editar código ou docs sensíveis ao domínio, **declare o agente** e **carregue** as rules/docs indicadas na tabela do `_dispatcher.mdc`.

Ordem recomendada para tarefas multi-domínio: **Engine → Backend → Frontend**, parando para confirmação humana entre domínios.

O humano não aceita output de LLM sem checkpoint inicial. O checkpoint mínimo e os critérios de aceite/rejeição ficam em `docs/01-governance/agent-usage.md`.

Se a LLM sair do agente declarado, tocar arquivo proibido ou tentar iniciar sprint seguinte sem evidência, o humano interrompe a execução e reabre a tarefa com escopo menor.

## HANDOFF obrigatório

Ao encerrar uma sessão que alterou arquivos, atualize **`HANDOFF.md`** na raiz com:

```markdown
## HANDOFF — <ISO data/hora> — Agent <Nome>

### Declaração
- Atuei como: ...
- Sprint / escopo: ...
- Rules consultadas: ...
- Arquivos tocados: ...
- Não toquei: ...

### O que fiz
- ...

### O que falta / próximo agente
- ...

### Evidências
- comandos, paths, ou screenshots quando aplicável
```

O Auditor cruza esta declaração com o diff e com a auditoria mínima. No Windows, o caminho principal é:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/audit.ps1
```

`scripts/audit.sh` espelha os checks para Git Bash/WSL, mas não é o caminho principal no ambiente atual.

## Templates de prompt (ambíguos)

Quando globs não decidirem o agente sozinho:

1. Copie um bloco explícito no início do chat: “Atue como Agent X…”  
2. Liste paths de rules em `.cursor/rules/` e docs em `docs/`.  
3. Defina Definition of Done da micro-tarefa.

Referência de papéis: `docs/01-governance/agent-usage.md`.

## Fechamento de sprint

Uma sprint só começa depois de:

1. `HANDOFF.md` atualizado pela sessão anterior.
2. Auditoria mínima executada e evidência registrada.
3. Pendências bloqueantes explicitadas ou resolvidas.
4. Humano confirmar que o próximo agente pode assumir.

## Documentação

- Mudanças de contrato HTTP → `docs/02-product/api.md`  
- Mudanças de regra de jogo / schema JSON → `docs/02-product/game-rules.md` + engine  
- Decisões novas → `docs/01-governance/decisions.md`  
