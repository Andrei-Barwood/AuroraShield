#!/usr/bin/env python3
"""
Genera un resumen rápido de KPIs para P01 desde metrics/p01/runs_template.csv.
Uso:
  python3 scripts/p01_kpi_summary.py metrics/p01/runs_template.csv
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path


def fnum(v: str) -> float:
    try:
        return float(v)
    except Exception:
        return 0.0


def pct(num: float, den: float) -> float:
    return (num / den * 100.0) if den else 0.0


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python3 scripts/p01_kpi_summary.py <csv>")
        return 1

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"No existe: {csv_path}")
        return 1

    rows = []
    with csv_path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    if not rows:
        print("CSV sin filas de datos.")
        return 0

    r = rows[-1]

    a1 = pct(fnum(r["entrypoints_probados"]), fnum(r["entrypoints_identificados"]))
    a2 = pct(fnum(r["malformed_rechazados_pre_limiteB"]), fnum(r["malformed_total"]))
    a3 = pct(fnum(r["intentos_esc_priv_exitosos"]), fnum(r["intentos_esc_priv_totales"]))

    b2 = pct(fnum(r["bypass_limiteC_confirmados"]), fnum(r["intentos_bypass_limiteC"]))

    r1 = pct(fnum(r["repros_exitosos"]), fnum(r["repros_totales"]))
    r4 = pct(fnum(r["replay_deterministicos"]), fnum(r["replay_totales"]))
    r5 = pct(fnum(r["artifacts_completos"]), fnum(r["artifacts_totales"]))

    m3 = pct(fnum(r["tests_regresion_ok"]), fnum(r["tests_regresion_totales"]))

    print("P01 KPI summary (última corrida)")
    print(f"- Run ID: {r.get('run_id', '')}")
    print(f"- Variante: {r.get('variant', '')}")
    print(f"- A1 EntryPointCoverage: {a1:.2f}%")
    print(f"- A2 BoundaryRejectRate: {a2:.2f}%")
    print(f"- A3 PrivEscAttemptSuccess: {a3:.2f}%")
    print(f"- B2 KernelBoundaryBypassRate: {b2:.2f}%")
    print(f"- R1 ReproSuccessRate: {r1:.2f}%")
    print(f"- R4 DeterministicReplayRate: {r4:.2f}%")
    print(f"- R5 ArtifactCompleteness: {r5:.2f}%")
    print(f"- M3 RegressionPassRate: {m3:.2f}%")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
