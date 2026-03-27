#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
cd "$ROOT_DIR"

OUT_ROOT="artifacts/p01/fase_b/d19_d20/batch_harness"
mkdir -p "$OUT_ROOT"

run_harness() {
  local run_id="$1"
  local fixtures_dir="$2"
  local out_dir="$OUT_ROOT/$run_id"
  echo "[INFO] Ejecutando harness run_id=$run_id fixtures=$fixtures_dir"
  python3 scripts/fase_b/p01_seccion1.py harness --fixtures "$fixtures_dir" --out "$out_dir" --run-id "$run_id"
}

run_harness "d19-base" "fixtures/p01/base"
run_harness "d19-legacy" "fixtures/p01/escenarios/legacy_v1"
run_harness "d19-actual" "fixtures/p01/escenarios/actual_v2"
run_harness "d19-all" "fixtures/p01"

python3 - <<'PY'
import json
from pathlib import Path

out_root = Path("artifacts/p01/fase_b/d19_d20/batch_harness")
rows = []

for summary in sorted(out_root.glob("*/summary.json")):
    s = json.loads(summary.read_text(encoding="utf-8"))
    rows.append(
        {
            "run_id": s.get("run_id"),
            "fixtures_total": int(s.get("fixtures_total", 0)),
            "accepts": int(s.get("accepts", 0)),
            "degrades": int(s.get("degrades", 0)),
            "rejects": int(s.get("rejects", 0)),
            "coverage_base_pct": float(s.get("coverage_base_pct", 0.0)),
        }
    )

total_fixtures = sum(r["fixtures_total"] for r in rows)
total_rejects = sum(r["rejects"] for r in rows)
weighted_cov = (
    sum(r["coverage_base_pct"] * r["fixtures_total"] for r in rows) / total_fixtures
    if total_fixtures else 0.0
)
reject_rate = (total_rejects / total_fixtures * 100.0) if total_fixtures else 0.0

out = {
    "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    "runs": rows,
    "aggregate": {
        "total_runs": len(rows),
        "total_fixtures": total_fixtures,
        "weighted_coverage_base_pct": round(weighted_cov, 2),
        "reject_rate_pct": round(reject_rate, 2),
    },
}

out_path = out_root / "batch_resumen.json"
out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"OK: resumen batch en {out_path}")
PY

echo "OK: D19 batch completado"
