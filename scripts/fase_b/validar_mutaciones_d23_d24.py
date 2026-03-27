#!/usr/bin/env python3
"""
Valida D23-D24: calidad de mutaciones estructurales y utilidad de mutaciones semanticas.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_FIELDS_BASE = ["fixture_id", "schema_version"]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(part: int, total: int) -> float:
    return round((part / total * 100.0), 2) if total else 0.0


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


def analyze_manifest(manifest_json: Path) -> dict[str, Any]:
    manifest = read_json(manifest_json)
    items = list(manifest.get("items", []))

    parseable = 0
    with_mutation_tag = 0
    with_required_base = 0
    by_mutation: dict[str, int] = {}
    by_expected: dict[str, int] = {}

    samples_invalid: list[dict[str, str]] = []

    for item in items:
        target = Path(str(item.get("target", "")))
        mutation_name = str(item.get("mutation", "unknown"))
        by_mutation[mutation_name] = by_mutation.get(mutation_name, 0) + 1

        expected = normalize_behavior(str(item.get("expected_behavior", "degrade")))
        by_expected[expected] = by_expected.get(expected, 0) + 1

        try:
            data = json.loads(target.read_text(encoding="utf-8"))
            parseable += 1

            if "_mutation" in data:
                with_mutation_tag += 1

            if all(k in data for k in REQUIRED_FIELDS_BASE):
                with_required_base += 1
            else:
                if len(samples_invalid) < 5:
                    missing = [k for k in REQUIRED_FIELDS_BASE if k not in data]
                    samples_invalid.append(
                        {
                            "target": str(target.as_posix()),
                            "missing_required": ",".join(missing),
                        }
                    )
        except Exception:
            if len(samples_invalid) < 5:
                samples_invalid.append(
                    {
                        "target": str(target.as_posix()),
                        "missing_required": "json_parse_error",
                    }
                )

    total = len(items)
    return {
        "total": total,
        "parseable": parseable,
        "parseable_pct": pct(parseable, total),
        "with_mutation_tag": with_mutation_tag,
        "with_mutation_tag_pct": pct(with_mutation_tag, total),
        "with_required_base": with_required_base,
        "with_required_base_pct": pct(with_required_base, total),
        "mutations_by_type": dict(sorted(by_mutation.items())),
        "expected_behavior_distribution": dict(sorted(by_expected.items())),
        "samples_invalid": samples_invalid,
    }


def analyze_harness(summary_json: Path) -> dict[str, Any]:
    s = read_json(summary_json)
    total = int(s.get("fixtures_total", 0))
    accepts = int(s.get("accepts", 0))
    degrades = int(s.get("degrades", 0))
    rejects = int(s.get("rejects", 0))

    non_accept = rejects + degrades
    return {
        "run_id": s.get("run_id", ""),
        "fixtures_total": total,
        "accepts": accepts,
        "degrades": degrades,
        "rejects": rejects,
        "failures_total": int(s.get("failures_total", 0)),
        "coverage_base_pct": round(float(s.get("coverage_base_pct", 0.0)), 2),
        "reject_rate_pct": pct(rejects, total),
        "non_accept_rate_pct": pct(non_accept, total),
    }


def build_report(
    manifest_struct: Path,
    manifest_semantic: Path,
    summary_struct: Path,
    summary_semantic: Path,
) -> dict[str, Any]:
    m_struct = analyze_manifest(manifest_struct)
    m_sem = analyze_manifest(manifest_semantic)

    h_struct = analyze_harness(summary_struct)
    h_sem = analyze_harness(summary_semantic)

    d23_valid = (
        m_struct["parseable_pct"] >= 99.0
        and m_struct["with_mutation_tag_pct"] >= 99.0
        and h_struct["reject_rate_pct"] >= 50.0
    )
    d24_useful = (
        m_sem["parseable_pct"] >= 99.0
        and h_sem["non_accept_rate_pct"] >= 85.0
        and h_sem["failures_total"] > 0
    )

    coverage_gate_d24 = min(h_struct["coverage_base_pct"], h_sem["coverage_base_pct"]) >= 60.0

    return {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "contexto": {
            "fase": "Fase B",
            "seccion": "Seccion 1 (D19-D34)",
            "tramo": "D23-D24",
        },
        "d23": {
            "manifest": m_struct,
            "harness": h_struct,
            "criterios_validacion": {
                "parseable_pct_min": 99.0,
                "mutation_tag_pct_min": 99.0,
                "reject_rate_pct_min": 50.0,
            },
            "estado": {
                "mutaciones_estructurales_validas": d23_valid,
            },
        },
        "d24": {
            "manifest": m_sem,
            "harness": h_sem,
            "criterios_validacion": {
                "parseable_pct_min": 99.0,
                "non_accept_rate_pct_min": 85.0,
                "failures_total_min": 1,
            },
            "estado": {
                "mutaciones_semanticas_invalidas_utiles": d24_useful,
            },
        },
        "objetivo_d24": {
            "entrypoint_coverage_base_pct_min": 60.0,
            "coverage_gate_cumplido": coverage_gate_d24,
            "coverage_structural_pct": h_struct["coverage_base_pct"],
            "coverage_semantico_pct": h_sem["coverage_base_pct"],
        },
        "status": {
            "d23_cumplido": d23_valid,
            "d24_cumplido": d24_useful,
            "d23_d24_cumplido": d23_valid and d24_useful and coverage_gate_d24,
        },
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validar D23-D24")
    p.add_argument("--manifest-struct", required=True)
    p.add_argument("--manifest-semantic", required=True)
    p.add_argument("--summary-struct", required=True)
    p.add_argument("--summary-semantic", required=True)
    p.add_argument("--out", required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()

    report = build_report(
        Path(args.manifest_struct),
        Path(args.manifest_semantic),
        Path(args.summary_struct),
        Path(args.summary_semantic),
    )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: validacion D23-D24 en {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
