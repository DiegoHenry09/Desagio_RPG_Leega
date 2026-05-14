$ErrorActionPreference = "Stop"

Write-Host "== Corporate Survivor - audit.ps1 (governance 0.1-D) =="

function Fail($Message) {
    Write-Error "FAIL: $Message"
    exit 1
}

function Require-File($Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        Fail "$Path ausente"
    }
}

$requiredFiles = @(
    "README.md",
    "PROJECT_STATUS.md",
    "HANDOFF.md",
    ".gitignore",
    ".env.example",
    "docs/02-product/architecture.md",
    "docs/02-product/game-rules.md",
    "docs/02-product/api.md",
    "docs/01-governance/decisions.md",
    "docs/00-start/sprint-plan.md",
    "docs/01-governance/cursor-workflow.md",
    "docs/01-governance/agent-usage.md",
    "docs/00-start/project-structure.md",
    "docs/00-start/setup-company-env.md",
    ".cursor/rules/_dispatcher.mdc",
    ".cursor/rules/frontend.mdc",
    ".cursor/rules/backend.mdc",
    ".cursor/rules/game-engine.mdc",
    ".cursor/rules/docs-sync.mdc",
    "scripts/audit.sh",
    "scripts/audit.ps1"
)

foreach ($file in $requiredFiles) {
    Require-File $file
}

$preflightDirs = Get-ChildItem -Force -Directory -Filter ".preflight_*"
if ($preflightDirs.Count -gt 0) {
    Fail ("Pastas temporarias encontradas: " + (($preflightDirs | ForEach-Object { $_.Name }) -join ", "))
}

$legacyDocs = Get-ChildItem -Force -File | Where-Object {
    $_.Name -like "corporate-survivor-*.md" -or $_.Name -eq "corporate-survivor-plano.md"
}
if ($legacyDocs.Count -gt 0) {
    Fail ("Markdown legado solto na raiz: " + (($legacyDocs | ForEach-Object { $_.Name }) -join ", "))
}

Write-Host "OK - governanca minima presente e raiz limpa."
Write-Host "Nota: backend/frontend ainda nao sao exigidos nesta auditoria."
