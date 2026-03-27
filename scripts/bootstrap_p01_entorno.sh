#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
P01_DIR="$ROOT_DIR/p01_lab"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "[ERROR] Falta dependencia: $1" >&2
    exit 1
  }
}

echo "[INFO] Validando dependencias mínimas..."
require_cmd bash
require_cmd python3
require_cmd git

echo "[INFO] Creando estructura de laboratorio en: $P01_DIR"
mkdir -p "$P01_DIR"/{artifacts,logs,tmp,results,configs}
mkdir -p "$P01_DIR/fixtures"/base
mkdir -p "$P01_DIR/fixtures/escenarios"/{legacy_v1,actual_v2}

ENV_EXAMPLE="$P01_DIR/.env.example"
if [[ ! -f "$ENV_EXAMPLE" ]]; then
  cat > "$ENV_EXAMPLE" <<'ENV'
# Configuración local de laboratorio P01
P01_MODE=defensive
P01_LOG_LEVEL=INFO
P01_RESULTS_DIR=./results
P01_FIXTURES_DIR=./fixtures
ENV
fi

chmod 700 "$P01_DIR/tmp"
chmod 750 "$P01_DIR/logs" "$P01_DIR/artifacts"

echo "[INFO] Bootstrap completado."
echo "[INFO] Estructura lista para corridas reproducibles."
