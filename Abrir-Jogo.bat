@echo off
setlocal
cd /d "%~dp0"
echo.
echo Corporate Survivor — iniciando Backend + Frontend...
echo Dica: comandos para copiar/colar estao em COMO-RODAR.txt
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\dev-jogo.ps1"
if errorlevel 1 (
  echo.
  echo ERRO ao executar scripts\dev-jogo.ps1
  echo Verifique se PowerShell esta disponivel e se as pastas backend e frontend existem.
  pause
)
