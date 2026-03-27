#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
cd "$ROOT_DIR"

FAIL_STRUCT="artifacts/p01/fase_b/d25_d26/fallas/estructural/fallas.jsonl"
FAIL_SEM="artifacts/p01/fase_b/d25_d26/fallas/semantico/fallas.jsonl"
CLUSTERS_ROOT="artifacts/p01/fase_b/d27_d28/clusters"
MIN_ROOT="artifacts/p01/fase_b/d27_d28/minimize"
REPRO_ROOT="artifacts/p01/fase_b/d27_d28/repro"
METRICAS_OUT="infra/p01/fase_b/metricas_d27_d28.json"

if [[ ! -f "$FAIL_STRUCT" || ! -f "$FAIL_SEM" ]]; then
  echo "[INFO] No existen fallas D25-D26, ejecutando tramo previo..."
  ./scripts/fase_b/ejecutar_d25_d26.sh
fi

if [[ ! -d "artifacts/p01/fase_b/d21_d22/corpus/raw" ]]; then
  echo "[INFO] No existe corpus raw de D21-D22, regenerando..."
  ./scripts/fase_b/ejecutar_d21_d22.sh
fi

mkdir -p "$CLUSTERS_ROOT" "$MIN_ROOT" "$REPRO_ROOT"

echo "[INFO] D27: deduplicacion por firma (estructural)"
python3 scripts/fase_b/p01_seccion1.py dedup-signatures \
  --failures "$FAIL_STRUCT" \
  --out "$CLUSTERS_ROOT/estructural.json"

echo "[INFO] D27: deduplicacion por firma (semantico)"
python3 scripts/fase_b/p01_seccion1.py dedup-signatures \
  --failures "$FAIL_SEM" \
  --out "$CLUSTERS_ROOT/semantico.json"

cat "$FAIL_STRUCT" "$FAIL_SEM" > "$CLUSTERS_ROOT/fallas_combinado.jsonl"

echo "[INFO] D27: deduplicacion por firma (combinado)"
python3 scripts/fase_b/p01_seccion1.py dedup-signatures \
  --failures "$CLUSTERS_ROOT/fallas_combinado.jsonl" \
  --out "$CLUSTERS_ROOT/combinado.json"

echo "[INFO] D28: minimizacion automatica (estructural)"
python3 scripts/fase_b/p01_seccion1.py minimize \
  --failures "$FAIL_STRUCT" \
  --fixtures-root artifacts/p01/fase_b/d21_d22/corpus/raw \
  --out "$MIN_ROOT/estructural"

echo "[INFO] D28: minimizacion automatica (semantico)"
python3 scripts/fase_b/p01_seccion1.py minimize \
  --failures "$FAIL_SEM" \
  --fixtures-root artifacts/p01/fase_b/d21_d22/corpus/raw \
  --out "$MIN_ROOT/semantico"

echo "[INFO] D28: minimizacion automatica (combinado)"
python3 scripts/fase_b/p01_seccion1.py minimize \
  --failures "$CLUSTERS_ROOT/fallas_combinado.jsonl" \
  --fixtures-root artifacts/p01/fase_b/d21_d22/corpus/raw \
  --out "$MIN_ROOT/combinado"

for ctx in estructural semantico combinado; do
  echo "[INFO] D28: repro run1 para $ctx"
  python3 scripts/fase_b/p01_seccion1.py harness \
    --fixtures "$MIN_ROOT/$ctx/fixtures" \
    --out "$REPRO_ROOT/$ctx/run1" \
    --run-id "d28-${ctx}-r1"

  echo "[INFO] D28: repro run2 para $ctx"
  python3 scripts/fase_b/p01_seccion1.py harness \
    --fixtures "$MIN_ROOT/$ctx/fixtures" \
    --out "$REPRO_ROOT/$ctx/run2" \
    --run-id "d28-${ctx}-r2"
done

python3 scripts/fase_b/validar_d27_d28.py \
  --clusters-root "$CLUSTERS_ROOT" \
  --min-root "$MIN_ROOT" \
  --repro-root "$REPRO_ROOT" \
  --out "$METRICAS_OUT"

echo "OK: D27-D28 completado"
