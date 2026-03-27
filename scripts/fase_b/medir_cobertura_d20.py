#!/usr/bin/env python3
"""
Analiza resultados de D19 y define objetivos D20 para Sección 1 de Fase B.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("Uso: python3 scripts/fase_b/medir_cobertura_d20.py <batch_resumen.json> <objetivos.json>")
        return 1

    batch_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    if not batch_path.exists():
        print(f"No existe: {batch_path}")
        return 1

    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    agg = batch.get("aggregate", {})

    cov_actual = float(agg.get("weighted_coverage_base_pct", 0.0))
    reject_actual = float(agg.get("reject_rate_pct", 0.0))

    cov_obj_d24 = max(60.0, round(cov_actual + 20.0, 2))
    cov_obj_d34 = max(95.0, round(cov_actual + 55.0, 2))

    objetivos = {
        "contexto": {
            "fase": "Fase B",
            "seccion": "Seccion 1 (D19-D34)",
            "origen": str(batch_path.as_posix()),
        },
        "baseline_d20": {
            "coverage_base_pct_actual": cov_actual,
            "reject_rate_pct_actual": reject_actual,
            "total_runs_batch": int(agg.get("total_runs", 0)),
            "total_fixtures_batch": int(agg.get("total_fixtures", 0)),
        },
        "objetivos": {
            "d24": {
                "entrypoint_coverage_base_pct_min": cov_obj_d24,
                "reject_rate_pct_rango": [20.0, 70.0],
                "artifacts_por_corrida_min": 3,
            },
            "d34": {
                "entrypoint_coverage_base_pct_min": cov_obj_d34,
                "dedup_precision_pct_min": 90.0,
                "repro_success_rate_pct_min": 95.0,
            },
        },
        "notas": [
            "Los objetivos se ajustan en D34 según evidencia de campañas largas.",
            "RejectRate fuera del rango esperado requiere revisar corpus y reglas de normalizacion.",
        ],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(objetivos, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: objetivos D20 guardados en {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
