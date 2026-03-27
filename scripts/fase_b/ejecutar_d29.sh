#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
cd "$ROOT_DIR"

MIN_ROOT="artifacts/p01/fase_b/d27_d28/minimize"
D29_ROOT="artifacts/p01/fase_b/d29"
SPECS_ROOT="$D29_ROOT/specs"
SMOKE_OUT="$D29_ROOT/smoke_repro.json"
INDEX_JSON="$D29_ROOT/index_specs.json"
INDEX_JSONL="$D29_ROOT/index_specs.jsonl"
METRICAS_OUT="infra/p01/fase_b/metricas_d29.json"

if [[ ! -d "$MIN_ROOT/estructural/fixtures" || ! -d "$MIN_ROOT/semantico/fixtures" || ! -d "$MIN_ROOT/combinado/fixtures" ]]; then
  echo "[INFO] No existe minimizacion D27-D28, ejecutando tramo previo..."
  ./scripts/fase_b/ejecutar_d27_d28.sh
fi

rm -rf "$SPECS_ROOT"
mkdir -p "$SPECS_ROOT"

for ctx in estructural semantico combinado; do
  fixtures_dir="$MIN_ROOT/$ctx/fixtures"
  out_ctx="$SPECS_ROOT/$ctx"
  mkdir -p "$out_ctx"

  count=0
  while IFS= read -r fixture; do
    fixture_name="$(basename "$fixture" .json)"
    out_spec="$out_ctx/${fixture_name}__repro.json"

    python3 scripts/fase_b/p01_seccion1.py repro \
      --fixture "$fixture" \
      --out "$out_spec"
    count=$((count + 1))
  done < <(find "$fixtures_dir" -type f -name "*.json" | sort)

  echo "[INFO] D29: specs generados en '$ctx': $count"
done

python3 - "$SPECS_ROOT" "$INDEX_JSON" "$INDEX_JSONL" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

contexts = ["estructural", "semantico", "combinado"]
specs_root = Path(sys.argv[1])
index_json = Path(sys.argv[2])
index_jsonl = Path(sys.argv[3])

rows = []
by_context = {}
for ctx in contexts:
    files = sorted((specs_root / ctx).glob("*.json"))
    by_context[ctx] = len(files)
    for spec in files:
        data = json.loads(spec.read_text(encoding="utf-8"))
        rows.append(
            {
                "context": ctx,
                "spec_path": spec.as_posix(),
                "repro_id": data.get("repro_id"),
                "fixture_id": data.get("fixture", {}).get("fixture_id"),
                "run_id": data.get("execution", {}).get("run_id"),
                "format_version": data.get("format_version"),
            }
        )

index_payload = {
    "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "format": "d29-index-v1",
    "specs_root": specs_root.as_posix(),
    "total_specs": len(rows),
    "by_context": by_context,
    "items": rows,
}

index_json.parent.mkdir(parents=True, exist_ok=True)
index_json.write_text(json.dumps(index_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

with index_jsonl.open("w", encoding="utf-8") as fh:
    for row in rows:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
PY

python3 - "$ROOT_DIR" "$SPECS_ROOT" "$SMOKE_OUT" <<'PY'
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

repo_root = Path(sys.argv[1]).resolve()
specs_root = Path(sys.argv[2]).resolve()
smoke_out = Path(sys.argv[3]).resolve()
contexts = ["estructural", "semantico", "combinado"]

def run_shell(cmd: str) -> dict:
    proc = subprocess.run(
        cmd,
        shell=True,
        cwd=repo_root,
        text=True,
        capture_output=True,
    )
    return {
        "returncode": proc.returncode,
        "stdout_tail": (proc.stdout or "")[-600:],
        "stderr_tail": (proc.stderr or "")[-600:],
    }

by_context = {}
for ctx in contexts:
    files = sorted((specs_root / ctx).glob("*.json"))
    if not files:
        by_context[ctx] = {"ok": False, "reason": "sin_specs"}
        continue

    spec_path = files[0]
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    prepare_cmd = str(spec.get("execution", {}).get("prepare_command", ""))
    run_cmd = str(spec.get("execution", {}).get("run_command", ""))
    harness_out = Path(str(spec.get("output_contract", {}).get("harness_out", "")))

    prep_res = run_shell(prepare_cmd) if prepare_cmd else {"returncode": 1, "stderr_tail": "prepare vacio", "stdout_tail": ""}
    run_res = run_shell(run_cmd) if run_cmd else {"returncode": 1, "stderr_tail": "run vacio", "stdout_tail": ""}

    required_files = ["events.jsonl", "failures.jsonl", "summary.json"]
    missing_required = []
    for rf in required_files:
        target = (repo_root / harness_out / rf).resolve()
        if not target.exists():
            missing_required.append(rf)

    ok = prep_res["returncode"] == 0 and run_res["returncode"] == 0 and not missing_required

    by_context[ctx] = {
        "ok": ok,
        "spec_path": spec_path.as_posix(),
        "repro_id": spec.get("repro_id"),
        "prepare_returncode": prep_res["returncode"],
        "run_returncode": run_res["returncode"],
        "missing_required_files": missing_required,
        "prepare_stderr_tail": prep_res["stderr_tail"],
        "run_stderr_tail": run_res["stderr_tail"],
    }

payload = {
    "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "format": "d29-smoke-v1",
    "by_context": by_context,
}

smoke_out.parent.mkdir(parents=True, exist_ok=True)
smoke_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PY

python3 scripts/fase_b/validar_d29.py \
  --specs-root "$SPECS_ROOT" \
  --smoke "$SMOKE_OUT" \
  --out "$METRICAS_OUT"

echo "OK: D29 completado"
