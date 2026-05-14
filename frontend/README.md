# Corporate Survivor Frontend

Frontend minimo da Sprint 0.3 para validar Vite + React + TypeScript no ambiente da empresa.

## Rodar localmente

```powershell
npm install
npm run dev
```

Abrir `http://localhost:5173`.

## Healthcheck

A tela inicial mostra `Corporate Survivor` e consulta `/api/health` pelo proxy de desenvolvimento do Vite, apontando para `http://localhost:8000/api/health`.

Este frontend permanece como thin client: nao calcula score, nao decide final, nao aplica consequencias e nao hardcoda eventos.
