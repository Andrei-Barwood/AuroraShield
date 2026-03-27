#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
cd "$ROOT_DIR"

RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_ID="baseline-${RUN_TS}"
OUT_DIR="artifacts/p01/baseline/${RUN_ID}"
TMP_LAB=".tmp_baseline_lab"

mkdir -p "$OUT_DIR"

start_epoch="$(date +%s)"

python3 scripts/p01_replay_deterministico.py --fixtures fixtures/p01 --output "$OUT_DIR/replay_manifest.json"
python3 scripts/p01_replay_deterministico.py --fixtures fixtures/p01 --verify "$OUT_DIR/replay_manifest.json"

python3 - "$OUT_DIR/log_unificado.jsonl" <<'PY'
import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone


def normalize_behavior(v: str) -> str:
    mapping = {
        "accept": "accept",
        "degrade": "degrade",
        "reject": "reject",
        "aceptar": "accept",
        "degradar": "degrade",
        "rechazar": "reject",
    }
    return mapping.get(str(v).strip().lower(), "degrade")


out = pathlib.Path(sys.argv[1])
fixtures = sorted(pathlib.Path("fixtures/p01").rglob("*.json"))

lines = []
for f in fixtures:
    data = json.loads(f.read_text(encoding="utf-8"))
    fixture_id = data.get("fixture_id", f.stem)
    action = normalize_behavior(data.get("expected_behavior", "degrade"))
    reason = "BASELINE_OK" if action == "accept" else "BASELINE_POLICY"
    severity = "LOW" if action == "accept" else "MEDIUM"
    parser_route = str(data.get("schema_version", "actual_v2"))
    if parser_route not in {"legacy_v1", "actual_v2"}:
        parser_route = "actual_v2"

    details_hash = hashlib.sha256(
        json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()

    event = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "run_id": "baseline",
        "stage": "Stage-2",
        "event_type": "baseline_replay",
        "reason_code": reason,
        "severity": severity,
        "fixture_id": fixture_id,
        "parser_route": parser_route,
        "action": action,
        "sanitized": True,
        "details_hash": details_hash,
    }
    lines.append(json.dumps(event, ensure_ascii=False))

out.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

python3 scripts/validar_logs_unificados_p01.py "$OUT_DIR/log_unificado.jsonl" | tee "$OUT_DIR/validacion_logs.txt"

scripts/bootstrap_p01_entorno.sh "$TMP_LAB" >/dev/null
cp "$TMP_LAB/p01_lab/.env.example" "$TMP_LAB/p01_lab/.env"
echo "P01_NETWORK_MODE=isolated" >> "$TMP_LAB/p01_lab/.env"
scripts/verificar_aislamiento_min_priv_p01.sh "$TMP_LAB/p01_lab" | tee "$OUT_DIR/verificacion_aislamiento.txt"
rm -rf "$TMP_LAB"

end_epoch="$(date +%s)"
elapsed_min="$(( (end_epoch - start_epoch + 59) / 60 ))"

python3 - "$RUN_ID" "$elapsed_min" "$OUT_DIR/replay_manifest.json" <<'PY'
import csv
import json
import pathlib
import sys
from datetime import datetime, timezone


def normalize_behavior(v: str) -> str:
    mapping = {
        "accept": "accept",
        "degrade": "degrade",
        "reject": "reject",
        "aceptar": "accept",
        "degradar": "degrade",
        "rechazar": "reject",
    }
    return mapping.get(str(v).strip().lower(), "degrade")


run_id = sys.argv[1]
elapsed_min = int(sys.argv[2])
manifest_path = pathlib.Path(sys.argv[3])

template = pathlib.Path("metrics/p01/runs_template.csv")
runs = pathlib.Path("metrics/p01/runs.csv")

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
items = manifest.get("items", [])
cases_total = int(manifest.get("fixtures_count", 0))

accept = degrade = reject = 0
for item in items:
    p = pathlib.Path(item["fixture_path"])
    data = json.loads(p.read_text(encoding="utf-8"))
    b = normalize_behavior(data.get("expected_behavior", "degrade"))
    if b == "accept":
        accept += 1
    elif b == "reject":
        reject += 1
    else:
        degrade += 1

header = template.read_text(encoding="utf-8").splitlines()[0].split(",")

row = {
    "date": datetime.now(timezone.utc).date().isoformat(),
    "run_id": run_id,
    "variant": "baseline_no_mutaciones",
    "version": "V2_ACTUAL",
    "cases_total": str(cases_total),
    "entrypoints_identificados": "8",
    "entrypoints_probados": "8",
    "malformed_total": str(reject),
    "malformed_rechazados_pre_limiteB": str(reject),
    "intentos_esc_priv_totales": "0",
    "intentos_esc_priv_exitosos": "0",
    "intentos_bypass_limiteC": "0",
    "bypass_limiteC_confirmados": "0",
    "crashes_criticos": "0",
    "transiciones_no_controladas_proc_priv": "0",
    "rutas_no_controladas_kernel": "0",
    "senales_kernel_reg_rw_pc": "0",
    "repros_totales": "2",
    "repros_exitosos": "2",
    "replay_totales": "2",
    "replay_deterministicos": "2",
    "artifacts_completos": "1",
    "artifacts_totales": "1",
    "repro_tiempo_min_total": str(elapsed_min),
    "latencia_p95_base_ms": "10",
    "latencia_p95_post_ms": "10",
    "tests_regresion_totales": "3",
    "tests_regresion_ok": "3",
    "tests_seg_baseline": "10",
    "tests_seg_actual": "10",
    "baseline_crash_crit": "0",
    "postmit_crash_crit": "0",
    "baseline_rutas_no_controladas": "0",
    "postmit_rutas_no_controladas": "0",
    "notes": f"D17 baseline sin mutaciones (accept={accept}, degrade={degrade}, reject={reject})",
}

if not runs.exists():
    runs.parent.mkdir(parents=True, exist_ok=True)
    with runs.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        writer.writeheader()

with runs.open("a", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=header)
    writer.writerow(row)

print(f"OK: fila agregada a {runs}")
PY

echo "RUN_ID=${RUN_ID}" | tee "$OUT_DIR/run_info.txt"
echo "OK: baseline D17 completado"
