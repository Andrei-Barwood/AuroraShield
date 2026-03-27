#!/usr/bin/env python3
"""
Valida D29: scripts de repro automáticos y salida estandarizada.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONTEXTS = ["estructural", "semantico", "combinado"]
REQUIRED_TOP = {"format_version", "repro_id", "fixture", "execution", "output_contract"}
REQUIRED_FIXTURE = {"fixture_path", "fixture_id", "schema_version", "expected_behavior"}
REQUIRED_EXEC = {"prepare_command", "run_command", "run_id", "isolated_input_dir"}
REQUIRED_OUTPUT = {"format", "harness_out", "required_files", "summary_required_fields"}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(part: int, total: int) -> float:
    return round((part / total * 100.0), 2) if total else 0.0


def analyze_specs(specs_root: Path) -> dict[str, Any]:
    specs = sorted(specs_root.rglob("*.json"))

    valid_top = 0
    valid_contract = 0
    format_ok = 0
    by_context: dict[str, int] = {c: 0 for c in CONTEXTS}
    ids: list[str] = []

    for p in specs:
        d = read_json(p)
        keys = set(d.keys())
        if REQUIRED_TOP.issubset(keys):
            valid_top += 1

        fixture = d.get("fixture", {}) if isinstance(d.get("fixture"), dict) else {}
        exec_block = d.get("execution", {}) if isinstance(d.get("execution"), dict) else {}
        out_block = d.get("output_contract", {}) if isinstance(d.get("output_contract"), dict) else {}

        if REQUIRED_FIXTURE.issubset(set(fixture.keys())) and REQUIRED_EXEC.issubset(set(exec_block.keys())) and REQUIRED_OUTPUT.issubset(set(out_block.keys())):
            valid_contract += 1

        if d.get("format_version") == "d29-repro-v1":
            format_ok += 1

        rid = str(d.get("repro_id", ""))
        if rid:
            ids.append(rid)

        parts = p.parts
        for ctx in CONTEXTS:
            if ctx in parts:
                by_context[ctx] += 1
                break

    unique_ids = len(set(ids))
    total = len(specs)

    return {
        "total_specs": total,
        "valid_top": valid_top,
        "valid_top_pct": pct(valid_top, total),
        "valid_contract": valid_contract,
        "valid_contract_pct": pct(valid_contract, total),
        "format_ok": format_ok,
        "format_ok_pct": pct(format_ok, total),
        "unique_repro_ids": unique_ids,
        "unique_repro_ids_pct": pct(unique_ids, total),
        "by_context": by_context,
    }


def analyze_smoke(smoke_path: Path) -> dict[str, Any]:
    if not smoke_path.exists():
        return {
            "exists": False,
            "contexts_total": 0,
            "contexts_ok": 0,
            "contexts_ok_pct": 0.0,
            "by_context": {},
        }

    smoke = read_json(smoke_path)
    by_context = smoke.get("by_context", {}) if isinstance(smoke.get("by_context"), dict) else {}

    total = len(by_context)
    ok = sum(1 for _, v in by_context.items() if bool(v.get("ok", False)))

    return {
        "exists": True,
        "contexts_total": total,
        "contexts_ok": ok,
        "contexts_ok_pct": pct(ok, total),
        "by_context": by_context,
    }


def build_report(specs_root: Path, smoke_path: Path) -> dict[str, Any]:
    spec_stats = analyze_specs(specs_root)
    smoke_stats = analyze_smoke(smoke_path)

    contexts_covered = all(int(spec_stats["by_context"].get(ctx, 0)) > 0 for ctx in CONTEXTS)
    d29_ok = (
        int(spec_stats.get("total_specs", 0)) >= 30
        and float(spec_stats.get("valid_contract_pct", 0.0)) >= 100.0
        and float(spec_stats.get("unique_repro_ids_pct", 0.0)) >= 100.0
        and contexts_covered
        and bool(smoke_stats.get("exists", False))
        and float(smoke_stats.get("contexts_ok_pct", 0.0)) >= 100.0
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "contexto": {
            "fase": "Fase B",
            "seccion": "Seccion 1 (D19-D34)",
            "tramo": "D29",
        },
        "d29": {
            "specs": spec_stats,
            "smoke": smoke_stats,
            "criterios_validacion": {
                "total_specs_min": 30,
                "valid_contract_pct_min": 100.0,
                "unique_repro_ids_pct_min": 100.0,
                "contexts_required": CONTEXTS,
                "smoke_contexts_ok_pct_min": 100.0,
            },
            "estado": {
                "scripts_repro_generados": int(spec_stats.get("total_specs", 0)) > 0,
                "salida_repro_estandarizada": float(spec_stats.get("valid_contract_pct", 0.0)) >= 100.0,
                "smoke_repro_ok": float(smoke_stats.get("contexts_ok_pct", 0.0)) >= 100.0,
            },
        },
        "status": {
            "d29_cumplido": d29_ok,
        },
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validar D29")
    p.add_argument("--specs-root", required=True)
    p.add_argument("--smoke", required=True)
    p.add_argument("--out", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()

    report = build_report(Path(args.specs_root), Path(args.smoke))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: validacion D29 en {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
