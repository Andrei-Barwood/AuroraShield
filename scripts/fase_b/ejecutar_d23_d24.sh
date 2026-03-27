#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
cd "$ROOT_DIR"

CORPUS_ROOT="artifacts/p01/fase_b/d21_d22/corpus"
MUT_ROOT="artifacts/p01/fase_b/d23_d24/mutations"
HARNESS_ROOT="artifacts/p01/fase_b/d23_d24/harness"
METRICAS_OUT="infra/p01/fase_b/metricas_d23_d24.json"

if [[ ! -d "$CORPUS_ROOT/normalized" ]]; then
  echo "[INFO] No hay corpus normalizado D21-D22, ejecutando bootstrap del tramo..."
  ./scripts/fase_b/ejecutar_d21_d22.sh
fi

echo "[INFO] D23: generar mutaciones estructurales"
python3 scripts/fase_b/p01_seccion1.py mutate-struct \
  --normalized "$CORPUS_ROOT" \
  --out "$MUT_ROOT"

echo "[INFO] D24: generar mutaciones semanticas"
python3 scripts/fase_b/p01_seccion1.py mutate-semantic \
  --normalized "$CORPUS_ROOT" \
  --out "$MUT_ROOT"

mkdir -p "$HARNESS_ROOT"

echo "[INFO] D23: validar mutaciones estructurales con harness"
python3 scripts/fase_b/p01_seccion1.py harness \
  --fixtures "$MUT_ROOT/estructural" \
  --out "$HARNESS_ROOT/estructural" \
  --run-id d23-struct

echo "[INFO] D24: validar mutaciones semanticas con harness"
python3 scripts/fase_b/p01_seccion1.py harness \
  --fixtures "$MUT_ROOT/semantico" \
  --out "$HARNESS_ROOT/semantico" \
  --run-id d24-semantic

python3 scripts/fase_b/validar_mutaciones_d23_d24.py \
  --manifest-struct "$MUT_ROOT/manifest_estructural.json" \
  --manifest-semantic "$MUT_ROOT/manifest_semantico.json" \
  --summary-struct "$HARNESS_ROOT/estructural/summary.json" \
  --summary-semantic "$HARNESS_ROOT/semantico/summary.json" \
  --out "$METRICAS_OUT"

echo "OK: D23-D24 completado"
