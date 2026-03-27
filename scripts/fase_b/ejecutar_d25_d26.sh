#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
cd "$ROOT_DIR"

PLAN_OUT="artifacts/p01/fase_b/d25_d26/plan_campanas.json"
FALLAS_ROOT="artifacts/p01/fase_b/d25_d26/fallas"
METRICAS_OUT="infra/p01/fase_b/metricas_d25_d26.json"

if [[ ! -f "artifacts/p01/fase_b/d23_d24/harness/estructural/events.jsonl" || ! -f "artifacts/p01/fase_b/d23_d24/harness/semantico/events.jsonl" ]]; then
  echo "[INFO] No existen eventos D23-D24, ejecutando tramo previo..."
  ./scripts/fase_b/ejecutar_d23_d24.sh
fi

echo "[INFO] D25: generar plan de campanas con scheduler y presupuesto"
python3 scripts/fase_b/p01_seccion1.py plan-campaign \
  --budget infra/p01/fase_b/presupuesto_campanas.json \
  --out "$PLAN_OUT"

mkdir -p "$FALLAS_ROOT"

echo "[INFO] D26: capturar fallas de corrida estructural"
python3 scripts/fase_b/p01_seccion1.py capture-failures \
  --events artifacts/p01/fase_b/d23_d24/harness/estructural/events.jsonl \
  --out "$FALLAS_ROOT/estructural"

echo "[INFO] D26: capturar fallas de corrida semantica"
python3 scripts/fase_b/p01_seccion1.py capture-failures \
  --events artifacts/p01/fase_b/d23_d24/harness/semantico/events.jsonl \
  --out "$FALLAS_ROOT/semantico"

python3 scripts/fase_b/validar_d25_d26.py \
  --plan "$PLAN_OUT" \
  --fallas-root "$FALLAS_ROOT" \
  --out "$METRICAS_OUT"

echo "OK: D25-D26 completado"
