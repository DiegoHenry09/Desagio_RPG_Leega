#!/usr/bin/env bash
# Auditoria leve de governanca — Sprint 0.1-D.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "== Corporate Survivor - audit.sh (governance 0.1-D) =="

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

required_files=(
  "README.md"
  "PROJECT_STATUS.md"
  "HANDOFF.md"
  ".gitignore"
  ".env.example"
  "docs/02-product/architecture.md"
  "docs/02-product/game-rules.md"
  "docs/02-product/api.md"
  "docs/01-governance/decisions.md"
  "docs/00-start/sprint-plan.md"
  "docs/01-governance/cursor-workflow.md"
  "docs/01-governance/agent-usage.md"
  "docs/00-start/project-structure.md"
  "docs/00-start/setup-company-env.md"
  ".cursor/rules/_dispatcher.mdc"
  ".cursor/rules/frontend.mdc"
  ".cursor/rules/backend.mdc"
  ".cursor/rules/game-engine.mdc"
  ".cursor/rules/docs-sync.mdc"
  "scripts/audit.sh"
  "scripts/audit.ps1"
)

for file in "${required_files[@]}"; do
  [[ -f "$file" ]] || fail "$file ausente"
done

shopt -s nullglob
preflight_dirs=(.preflight_*/)
if (( ${#preflight_dirs[@]} > 0 )); then
  fail "pastas temporarias encontradas: ${preflight_dirs[*]}"
fi

legacy_docs=(corporate-survivor-*.md corporate-survivor-plano.md)
if (( ${#legacy_docs[@]} > 0 )); then
  fail "Markdown legado solto na raiz: ${legacy_docs[*]}"
fi

echo "OK - governanca minima presente e raiz limpa."
echo "Nota: no Windows, scripts/audit.ps1 e o caminho principal."
echo "Nota: backend/frontend ainda nao sao exigidos nesta auditoria."
