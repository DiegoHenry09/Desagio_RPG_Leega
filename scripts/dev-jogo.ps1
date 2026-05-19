# Corporate Survivor — sobe backend + frontend em janelas separadas e abre o browser.
# Uso: .\scripts\dev-jogo.ps1   ou dê duplo clique em Abrir-Jogo.bat na raiz do repo.
param(
    [switch]$SkipBrowser,
    [int]$SecondsBeforeBrowser = 5
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Backend = Join-Path $RepoRoot "backend"
$Frontend = Join-Path $RepoRoot "frontend"

if (-not (Test-Path $Backend)) { throw "Pasta backend não encontrada: $Backend" }
if (-not (Test-Path $Frontend)) { throw "Pasta frontend não encontrada: $Frontend" }

function Start-DevCmd {
    param(
        [Parameter(Mandatory)][string]$Title,
        [Parameter(Mandatory)][string]$Command
    )
    Start-Process cmd.exe -ArgumentList @("/k", $Command) -WindowStyle Normal
}

# Backend :8000 — usa .venv se existir
$backendLine = @(
    "cd /d `"$Backend`""
    "title Corporate Survivor — Backend :8000"
    "echo."
    "echo Backend em http://127.0.0.1:8000  ^|  docs: http://127.0.0.1:8000/docs"
    "echo Pare com Ctrl+C quando quiser reiniciar."
    "echo."
    "if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat"
    "python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000"
) -join " && "

# Frontend :5173 — proxy /api para o backend (vite.config.ts)
$frontendLine = @(
    "cd /d `"$Frontend`""
    "title Corporate Survivor — Frontend :5173"
    "echo."
    "echo Frontend em http://127.0.0.1:5173/"
    "echo Pare com Ctrl+C quando quiser reiniciar."
    "echo."
    "npm run dev"
) -join " && "

Write-Host ""
Write-Host "Abrindo 2 janelas: Backend (8000) e Frontend (5173)..." -ForegroundColor Cyan
Write-Host "Feche cada janela ou use Ctrl+C para parar. Para atualizar o código, salve os arquivos (^reload no backend)." -ForegroundColor Gray
Write-Host ""

Start-DevCmd -Title "Backend" -Command $backendLine
Start-Sleep -Milliseconds 800
Start-DevCmd -Title "Frontend" -Command $frontendLine

if (-not $SkipBrowser) {
    Write-Host "Aguardando ${SecondsBeforeBrowser}s e abrindo o navegador..." -ForegroundColor Yellow
    Start-Sleep -Seconds $SecondsBeforeBrowser
    Start-Process "http://127.0.0.1:5173/"
}
