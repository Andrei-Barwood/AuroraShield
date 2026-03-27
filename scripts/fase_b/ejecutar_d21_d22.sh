#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
cd "$ROOT_DIR"

OUT_ROOT="artifacts/p01/fase_b/d21_d22/corpus"
mkdir -p "$OUT_ROOT"

echo "[INFO] D21: construir corpus semilla y clasificar por tipo"
python3 scripts/fase_b/p01_seccion1.py seed-corpus \
  --fixtures fixtures/p01 \
  --out "$OUT_ROOT" \
  --template-pack mensajeria

echo "[INFO] D22: normalizar corpus y eliminar duplicados de bajo valor"
python3 scripts/fase_b/p01_seccion1.py normalize-corpus \
  --corpus "$OUT_ROOT" \
  --out "$OUT_ROOT"

python3 - <<'PY'
import json
from datetime import datetime, timezone
from pathlib import Path

seed_path = Path("artifacts/p01/fase_b/d21_d22/corpus/clasificacion_semillas.json")
norm_path = Path("artifacts/p01/fase_b/d21_d22/corpus/normalizacion_reporte.json")
out_path = Path("infra/p01/fase_b/metricas_d21_d22.json")

seed = json.loads(seed_path.read_text(encoding="utf-8"))
norm = json.loads(norm_path.read_text(encoding="utf-8"))

total_input = int(norm.get("total_input", 0))
total_unique = int(norm.get("total_unique", 0))
exact_removed = int(norm.get("duplicates_removed_exact", 0))
low_removed = int(norm.get("duplicates_removed_low_value", 0))

reduction_pct = round(((total_input - total_unique) / total_input * 100.0), 2) if total_input else 0.0

metricas = {
    "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "contexto": {
        "fase": "Fase B",
        "seccion": "Seccion 1 (D19-D34)",
        "tramo": "D21-D22",
    },
    "d21": {
        "total_semillas": int(seed.get("total_semillas", 0)),
        "generated_semillas": int(seed.get("generated_semillas", 0)),
        "template_pack": seed.get("template_pack", "none"),
        "distribucion_schema": seed.get("distribucion_schema", {}),
        "distribucion_message_type": seed.get("distribucion_message_type", {}),
        "distribucion_group": seed.get("distribucion_group", {}),
    },
    "d22": {
        "total_input": total_input,
        "total_unique": total_unique,
        "duplicates_removed_exact": exact_removed,
        "duplicates_removed_low_value": low_removed,
        "reduction_pct": reduction_pct,
        "distribucion_before_message_type": norm.get("distribucion_before_message_type", {}),
        "distribucion_after_message_type": norm.get("distribucion_after_message_type", {}),
    },
    "status": {
        "clasificacion_multi_tipo": len(seed.get("distribucion_message_type", {})) >= 4,
        "deduplicacion_activa": (exact_removed + low_removed) > 0,
    },
}

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(metricas, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"OK: métricas D21-D22 en {out_path}")
PY

echo "OK: D21-D22 completado"
