#!/usr/bin/env python3
"""
Valida D25-D26: scheduler de campañas y captura automatica de fallas.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(part: int, total: int) -> float:
    return round((part / total * 100.0), 2) if total else 0.0


def analyze_plan(plan_path: Path) -> dict[str, Any]:
    plan = read_json(plan_path)
    campaigns = list(plan.get("campaigns", []))

    budget_ok = 0
    scheduler_ok = 0

    total_cases = 0
    total_minutes = 0

    for c in campaigns:
        presupuesto = c.get("presupuesto", {})
        scheduler = c.get("scheduler", {})

        max_cases = int(presupuesto.get("max_cases", 0))
        max_minutes = int(presupuesto.get("max_minutes", 0))
        cadence = int(scheduler.get("cadence_minutes", 0))
        max_runs_daily = int(scheduler.get("max_runs_daily", 0))

        total_cases += max_cases
        total_minutes += max_minutes

        if max_cases > 0 and max_minutes > 0:
            budget_ok += 1
        if cadence > 0 and max_runs_daily > 0:
            scheduler_ok += 1

    total_campaigns = len(campaigns)
    return {
        "total_campaigns": total_campaigns,
        "budget_ok": budget_ok,
        "scheduler_ok": scheduler_ok,
        "budget_ok_pct": pct(budget_ok, total_campaigns),
        "scheduler_ok_pct": pct(scheduler_ok, total_campaigns),
        "total_max_cases": total_cases,
        "total_max_minutes": total_minutes,
        "scheduler_global": plan.get("scheduler_global", {}),
    }


def analyze_failures_root(fallas_root: Path) -> dict[str, Any]:
    if not fallas_root.exists():
        return {
            "contexts": 0,
            "contexts_with_runs": 0,
            "total_events": 0,
            "total_failures": 0,
            "runs_detected": 0,
            "artifact_files_total": 0,
            "by_context": {},
        }

    by_context: dict[str, Any] = {}
    total_events = 0
    total_failures = 0
    runs_detected = 0
    contexts_with_runs = 0
    artifact_files_total = 0

    for ctx in sorted([p for p in fallas_root.iterdir() if p.is_dir()]):
        resumen = ctx / "fallas_resumen.json"
        bundle = ctx / "artefactos_corrida.json"

        if not resumen.exists():
            continue

        r = read_json(resumen)
        total_events += int(r.get("total_events", 0))
        total_failures += int(r.get("total_failures", 0))

        run_count = 0
        if bundle.exists():
            b = read_json(bundle)
            runs = list(b.get("runs", []))
            run_count = len(runs)
            runs_detected += run_count
            artifact_files_total += 1  # bundle file
            artifact_files_total += sum(2 for _ in runs)  # fallas + resumen por run

        if run_count > 0:
            contexts_with_runs += 1

        by_context[ctx.name] = {
            "total_events": int(r.get("total_events", 0)),
            "total_failures": int(r.get("total_failures", 0)),
            "runs_detected": run_count,
            "has_bundle": bundle.exists(),
        }

    return {
        "contexts": len(by_context),
        "contexts_with_runs": contexts_with_runs,
        "total_events": total_events,
        "total_failures": total_failures,
        "runs_detected": runs_detected,
        "artifact_files_total": artifact_files_total,
        "by_context": by_context,
    }


def build_report(plan_path: Path, fallas_root: Path) -> dict[str, Any]:
    plan = analyze_plan(plan_path)
    cap = analyze_failures_root(fallas_root)

    d25_scheduler_ok = plan["total_campaigns"] >= 2 and plan["scheduler_ok_pct"] >= 100.0
    d25_budget_ok = plan["total_campaigns"] >= 2 and plan["budget_ok_pct"] >= 100.0

    d26_capture_ok = cap["contexts"] >= 2 and cap["total_failures"] > 0
    d26_artifacts_ok = cap["contexts"] >= 2 and cap["contexts_with_runs"] == cap["contexts"]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "contexto": {
            "fase": "Fase B",
            "seccion": "Seccion 1 (D19-D34)",
            "tramo": "D25-D26",
        },
        "d25": {
            "plan": plan,
            "criterios_validacion": {
                "campaigns_min": 2,
                "scheduler_ok_pct_min": 100.0,
                "budget_ok_pct_min": 100.0,
            },
            "estado": {
                "scheduler_definido": d25_scheduler_ok,
                "presupuesto_por_campana_definido": d25_budget_ok,
            },
        },
        "d26": {
            "captura": cap,
            "criterios_validacion": {
                "contexts_min": 2,
                "total_failures_min": 1,
                "contexts_with_runs_equals_contexts": True,
            },
            "estado": {
                "captura_automatica_integrada": d26_capture_ok,
                "artefactos_por_corrida_guardados": d26_artifacts_ok,
            },
        },
        "status": {
            "d25_cumplido": d25_scheduler_ok and d25_budget_ok,
            "d26_cumplido": d26_capture_ok and d26_artifacts_ok,
            "d25_d26_cumplido": (d25_scheduler_ok and d25_budget_ok and d26_capture_ok and d26_artifacts_ok),
        },
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validar D25-D26")
    p.add_argument("--plan", required=True)
    p.add_argument("--fallas-root", required=True)
    p.add_argument("--out", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()

    report = build_report(Path(args.plan), Path(args.fallas_root))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: validacion D25-D26 en {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
