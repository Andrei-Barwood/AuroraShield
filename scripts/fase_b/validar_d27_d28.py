#!/usr/bin/env python3
"""
Valida D27-D28: deduplicacion por firma y minimizacion reproducible.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONTEXTS = ["estructural", "semantico", "combinado"]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(part: int, total: int) -> float:
    return round((part / total * 100.0), 2) if total else 0.0


def analyze_clusters(clusters_root: Path) -> dict[str, Any]:
    by_context: dict[str, Any] = {}

    total_failures = 0
    total_clusters = 0

    for ctx in CONTEXTS:
        p = clusters_root / f"{ctx}.json"
        if not p.exists():
            by_context[ctx] = {
                "exists": False,
                "total_failures": 0,
                "total_clusters": 0,
                "top_cluster_count": 0,
                "cluster_reduction_pct": 0.0,
            }
            continue

        d = read_json(p)
        clusters = list(d.get("clusters", []))
        failures = int(d.get("total_failures", 0))
        n_clusters = int(d.get("total_clusters", len(clusters)))
        top_count = int(clusters[0].get("count", 0)) if clusters else 0
        reduction = round((1.0 - (n_clusters / failures)) * 100.0, 2) if failures else 0.0

        by_context[ctx] = {
            "exists": True,
            "total_failures": failures,
            "total_clusters": n_clusters,
            "top_cluster_count": top_count,
            "cluster_reduction_pct": reduction,
        }

        total_failures += failures
        total_clusters += n_clusters

    combinado = by_context.get("combinado", {})
    reduction_combined = float(combinado.get("cluster_reduction_pct", 0.0))

    return {
        "by_context": by_context,
        "aggregate": {
            "total_failures_sum": total_failures,
            "total_clusters_sum": total_clusters,
            "combined_reduction_pct": reduction_combined,
        },
    }


def summarize_run(summary_path: Path) -> dict[str, Any]:
    if not summary_path.exists():
        return {
            "exists": False,
            "fixtures_total": 0,
            "accepts": 0,
            "degrades": 0,
            "rejects": 0,
            "failures_total": 0,
            "coverage_base_pct": 0.0,
        }

    s = read_json(summary_path)
    return {
        "exists": True,
        "fixtures_total": int(s.get("fixtures_total", 0)),
        "accepts": int(s.get("accepts", 0)),
        "degrades": int(s.get("degrades", 0)),
        "rejects": int(s.get("rejects", 0)),
        "failures_total": int(s.get("failures_total", 0)),
        "coverage_base_pct": round(float(s.get("coverage_base_pct", 0.0)), 2),
    }


def same_summary(a: dict[str, Any], b: dict[str, Any]) -> bool:
    keys = ["fixtures_total", "accepts", "degrades", "rejects", "failures_total", "coverage_base_pct"]
    return all(a.get(k) == b.get(k) for k in keys)


def analyze_minimize_repro(min_root: Path, repro_root: Path) -> dict[str, Any]:
    by_context: dict[str, Any] = {}

    deterministic_ok = 0
    contexts_with_output = 0

    total_minimized = 0

    for ctx in CONTEXTS:
        rep_path = min_root / ctx / "reporte_minimizacion.json"
        rep = read_json(rep_path) if rep_path.exists() else {}

        minimized_total = int(rep.get("total", 0))
        missing_count = int(rep.get("missing_fixtures_count", 0))
        total_minimized += minimized_total

        r1 = summarize_run(repro_root / ctx / "run1" / "summary.json")
        r2 = summarize_run(repro_root / ctx / "run2" / "summary.json")
        deterministic = r1.get("exists") and r2.get("exists") and same_summary(r1, r2)

        if minimized_total > 0:
            contexts_with_output += 1
        if deterministic:
            deterministic_ok += 1

        by_context[ctx] = {
            "minimized_total": minimized_total,
            "missing_fixtures_count": missing_count,
            "repro_run1": r1,
            "repro_run2": r2,
            "deterministic": bool(deterministic),
        }

    contexts_total = len(CONTEXTS)

    return {
        "by_context": by_context,
        "aggregate": {
            "contexts_total": contexts_total,
            "contexts_with_output": contexts_with_output,
            "deterministic_ok": deterministic_ok,
            "repro_success_pct": pct(deterministic_ok, contexts_total),
            "total_minimized": total_minimized,
        },
    }


def build_report(clusters_root: Path, min_root: Path, repro_root: Path) -> dict[str, Any]:
    d27 = analyze_clusters(clusters_root)
    d28 = analyze_minimize_repro(min_root, repro_root)

    combined = d27["by_context"].get("combinado", {})
    d27_ok = (
        bool(d27["by_context"].get("estructural", {}).get("exists"))
        and bool(d27["by_context"].get("semantico", {}).get("exists"))
        and bool(combined.get("exists"))
        and int(combined.get("total_clusters", 0)) > 0
        and float(combined.get("cluster_reduction_pct", 0.0)) >= 70.0
    )

    d28_agg = d28["aggregate"]
    d28_ok = (
        int(d28_agg.get("contexts_with_output", 0)) == int(d28_agg.get("contexts_total", 0))
        and float(d28_agg.get("repro_success_pct", 0.0)) >= 95.0
        and int(d28_agg.get("total_minimized", 0)) > 0
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "contexto": {
            "fase": "Fase B",
            "seccion": "Seccion 1 (D19-D34)",
            "tramo": "D27-D28",
        },
        "d27": {
            "clusters": d27,
            "criterios_validacion": {
                "combined_cluster_reduction_pct_min": 70.0,
                "contexts_required": ["estructural", "semantico", "combinado"],
            },
            "estado": {
                "deduplicacion_por_firma_validada": d27_ok,
            },
        },
        "d28": {
            "minimizacion_repro": d28,
            "criterios_validacion": {
                "repro_success_pct_min": 95.0,
                "contexts_with_output_equals_total": True,
                "total_minimized_min": 1,
            },
            "estado": {
                "minimizacion_automatica_activa": int(d28_agg.get("total_minimized", 0)) > 0,
                "reproducibilidad_verificada": float(d28_agg.get("repro_success_pct", 0.0)) >= 95.0,
            },
        },
        "status": {
            "d27_cumplido": d27_ok,
            "d28_cumplido": d28_ok,
            "d27_d28_cumplido": d27_ok and d28_ok,
        },
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validar D27-D28")
    p.add_argument("--clusters-root", required=True)
    p.add_argument("--min-root", required=True)
    p.add_argument("--repro-root", required=True)
    p.add_argument("--out", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()

    report = build_report(Path(args.clusters_root), Path(args.min_root), Path(args.repro_root))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: validacion D27-D28 en {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
