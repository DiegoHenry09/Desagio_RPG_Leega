#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB_PATH="$ROOT/backend/data/corporate_survivor.db"

echo "Corporate Survivor — reset_db.sh"
echo "Caminho do banco esperado: $DB_PATH"

read -r -p "Apagar este arquivo SQLite? [y/N] " confirm
if [[ "${confirm,,}" != "y" ]]; then
  echo "Cancelado."
  exit 0
fi

rm -f "$DB_PATH"
echo "Removido (se existia). Reinicie o backend para recriar via migrations ou create_all."
