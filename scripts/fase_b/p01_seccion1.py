#!/usr/bin/env python3
"""
P01 - Fase B Sección 1 (D19-D34)
CLI unificada para instrumentación, corpus, mutación, campañas y triage.

Modo defensive-by-design:
- No ejecuta payloads ofensivos.
- Solo procesa fixtures sintéticos locales.
- Genera artefactos reproducibles y sanitizados.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ENTRYPOINTS_REFERENCIA = 8
REQUIRED_FIELDS = ["fixture_id", "schema_version", "message_type", "payload"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


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


def safe_parser_route(v: str) -> str:
    sv = str(v).strip()
    if sv in {"legacy_v1", "actual_v2"}:
        return sv
    return "actual_v2"


def stable_hash(data: Any) -> str:
    canon = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def iter_json_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.json"))


@dataclass
class Event:
    timestamp_utc: str
    run_id: str
    stage: str
    event_type: str
    reason_code: str
    severity: str
    fixture_id: str
    parser_route: str
    action: str
    sanitized: bool
    details_hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp_utc": self.timestamp_utc,
            "run_id": self.run_id,
            "stage": self.stage,
            "event_type": self.event_type,
            "reason_code": self.reason_code,
            "severity": self.severity,
            "fixture_id": self.fixture_id,
            "parser_route": self.parser_route,
            "action": self.action,
            "sanitized": self.sanitized,
            "details_hash": self.details_hash,
        }


def run_harness(fixtures: Path, out_dir: Path, run_id: str) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    events_path = out_dir / "events.jsonl"
    failures_path = out_dir / "failures.jsonl"
    summary_path = out_dir / "summary.json"

    fixture_files = iter_json_files(fixtures)
    events: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    unique_entry_classes = set()

    for f in fixture_files:
        raw = f.read_text(encoding="utf-8")
        fixture_id = f.stem
        parser_route = "actual_v2"
        action = "reject"
        reason_code = "HARN-JSON-INVALID"
        severity = "HIGH"

        try:
            data = json.loads(raw)
            fixture_id = str(data.get("fixture_id", fixture_id))
            parser_route = safe_parser_route(data.get("schema_version", "actual_v2"))

            missing = [k for k in REQUIRED_FIELDS if k not in data]
            if missing:
                action = "reject"
                reason_code = "HARN-MISSING-FIELDS"
                severity = "HIGH"
            elif not isinstance(data.get("payload"), dict):
                action = "reject"
                reason_code = "HARN-PAYLOAD-TYPE"
                severity = "HIGH"
            else:
                action = normalize_behavior(data.get("expected_behavior", "degrade"))
                reason_code = "HARN-BASELINE"
                severity = "LOW" if action == "accept" else "MEDIUM"

                mtype = str(data.get("message_type", "unknown"))
                unique_entry_classes.add((parser_route, mtype))

            details_hash = stable_hash(data)
        except Exception:
            details_hash = hashlib.sha256(raw.encode("utf-8", errors="ignore")).hexdigest()

        ev = Event(
            timestamp_utc=utc_now(),
            run_id=run_id,
            stage="Stage-2",
            event_type="harness_eval",
            reason_code=reason_code,
            severity=severity,
            fixture_id=fixture_id,
            parser_route=parser_route,
            action=action,
            sanitized=True,
            details_hash=details_hash,
        ).to_dict()

        events.append(ev)
        if action == "reject" or severity in {"HIGH", "CRITICAL"}:
            failures.append(ev)

    with events_path.open("w", encoding="utf-8") as fh:
        for ev in events:
            fh.write(json.dumps(ev, ensure_ascii=False) + "\n")

    with failures_path.open("w", encoding="utf-8") as fh:
        for ev in failures:
            fh.write(json.dumps(ev, ensure_ascii=False) + "\n")

    rejects = sum(1 for e in events if e["action"] == "reject")
    accepts = sum(1 for e in events if e["action"] == "accept")
    degrades = sum(1 for e in events if e["action"] == "degrade")

    summary = {
        "run_id": run_id,
        "fixtures_total": len(fixture_files),
        "events_total": len(events),
        "accepts": accepts,
        "degrades": degrades,
        "rejects": rejects,
        "failures_total": len(failures),
        "entrypoints_identificados": ENTRYPOINTS_REFERENCIA,
        "entrypoints_probados": min(ENTRYPOINTS_REFERENCIA, len(unique_entry_classes)),
        "coverage_base_pct": (
            min(ENTRYPOINTS_REFERENCIA, len(unique_entry_classes)) / ENTRYPOINTS_REFERENCIA * 100
            if ENTRYPOINTS_REFERENCIA
            else 0.0
        ),
        "outputs": {
            "events": str(events_path.as_posix()),
            "failures": str(failures_path.as_posix()),
        },
    }
    write_json(summary_path, summary)
    print(f"OK: harness ejecutado en {out_dir}")
    return 0


def cmd_coverage(summary_json: Path) -> int:
    if not summary_json.exists():
        print(f"No existe summary: {summary_json}")
        return 1
    s = json.loads(summary_json.read_text(encoding="utf-8"))
    coverage = float(s.get("coverage_base_pct", 0.0))
    rejects = int(s.get("rejects", 0))
    total = int(s.get("fixtures_total", 0))
    reject_rate = (rejects / total * 100.0) if total else 0.0

    print("Cobertura base")
    print(f"- Run ID: {s.get('run_id', '')}")
    print(f"- EntryPointCoverage: {coverage:.2f}%")
    print(f"- RejectRate: {reject_rate:.2f}%")
    print("- Meta sugerida inicial: >=95% cobertura, <=40% reject en baseline")
    return 0


def cmd_seed_corpus(fixtures: Path, out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = out_dir / "raw"
    idx_csv = out_dir / "index_semillas.csv"
    rows: list[dict[str, str]] = []

    for p in iter_json_files(fixtures):
        data = json.loads(p.read_text(encoding="utf-8"))
        fixture_id = str(data.get("fixture_id", p.stem))
        schema = safe_parser_route(data.get("schema_version", "actual_v2"))
        mtype = str(data.get("message_type", "unknown"))
        group = f"{schema}__{mtype}"

        dst = raw_dir / group / p.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)

        rows.append(
            {
                "fixture_id": fixture_id,
                "group": group,
                "source": str(p.as_posix()),
                "target": str(dst.as_posix()),
                "sha256": stable_hash(data),
            }
        )

    with idx_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["fixture_id", "group", "source", "target", "sha256"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"OK: corpus semilla construido en {out_dir}")
    return 0


def cmd_normalize_corpus(corpus_dir: Path, out_dir: Path) -> int:
    raw = corpus_dir / "raw"
    if not raw.exists():
        print(f"No existe corpus raw: {raw}")
        return 1

    normalized = out_dir / "normalized"
    normalized.mkdir(parents=True, exist_ok=True)

    seen: dict[str, Path] = {}
    duplicates = 0
    copied = 0

    for p in iter_json_files(raw):
        data = json.loads(p.read_text(encoding="utf-8"))
        h = stable_hash(data)
        if h in seen:
            duplicates += 1
            continue

        rel_group = p.parent.name
        dst = normalized / rel_group / p.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
        seen[h] = p
        copied += 1

    report = {
        "source": str(raw.as_posix()),
        "normalized_dir": str(normalized.as_posix()),
        "total_unique": copied,
        "duplicates_removed": duplicates,
    }
    write_json(out_dir / "normalizacion_reporte.json", report)
    print(f"OK: corpus normalizado en {normalized}")
    return 0


def _mutate_structural(data: dict[str, Any]) -> list[dict[str, Any]]:
    out = []

    a = dict(data)
    a.pop("payload", None)
    a["_mutation"] = "remove_payload"
    a["expected_behavior"] = "rechazar"
    out.append(a)

    b = dict(data)
    b["payload"] = "payload_invalido"
    b["_mutation"] = "payload_as_string"
    b["expected_behavior"] = "rechazar"
    out.append(b)

    c = dict(data)
    payload = dict(c.get("payload", {})) if isinstance(c.get("payload"), dict) else {}
    payload["subject"] = "X" * 512
    c["payload"] = payload
    c["_mutation"] = "oversized_subject"
    c["expected_behavior"] = "degradar"
    out.append(c)

    return out


def _mutate_semantic(data: dict[str, Any]) -> list[dict[str, Any]]:
    out = []

    a = dict(data)
    a["schema_version"] = "unsupported_v9"
    a["_mutation"] = "unsupported_schema"
    a["expected_behavior"] = "rechazar"
    out.append(a)

    b = dict(data)
    b["expected_behavior"] = "accion_invalida"
    b["_mutation"] = "invalid_expected_behavior"
    out.append(b)

    c = dict(data)
    payload = dict(c.get("payload", {})) if isinstance(c.get("payload"), dict) else {}
    payload["locale"] = "zz-ZZ"
    c["payload"] = payload
    c["_mutation"] = "semantic_locale_out_of_profile"
    c["expected_behavior"] = "degradar"
    out.append(c)

    return out


def _generate_mutations(normalized_dir: Path, out_dir: Path, mode: str) -> int:
    src = normalized_dir / "normalized"
    if not src.exists():
        print(f"No existe corpus normalizado: {src}")
        return 1

    mut_root = out_dir / mode
    mut_root.mkdir(parents=True, exist_ok=True)
    manifest = []

    for p in iter_json_files(src):
        data = json.loads(p.read_text(encoding="utf-8"))
        muts = _mutate_structural(data) if mode == "estructural" else _mutate_semantic(data)
        for idx, m in enumerate(muts, 1):
            fid = str(m.get("fixture_id", p.stem))
            out_name = f"{fid}__{mode}__{idx}.json"
            dst = mut_root / p.parent.name / out_name
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            manifest.append(
                {
                    "source": str(p.as_posix()),
                    "target": str(dst.as_posix()),
                    "mode": mode,
                    "mutation": m.get("_mutation", "unknown"),
                }
            )

    write_json(out_dir / f"manifest_{mode}.json", {"count": len(manifest), "items": manifest})
    print(f"OK: mutaciones {mode} generadas en {mut_root}")
    return 0


def cmd_plan_campaign(budget_json: Path, out_plan: Path) -> int:
    if budget_json.exists():
        budget = json.loads(budget_json.read_text(encoding="utf-8"))
    else:
        budget = {
            "campana_1": {"max_cases": 500, "max_minutes": 60},
            "campana_2": {"max_cases": 800, "max_minutes": 90},
        }

    plan = {
        "generated_at": utc_now(),
        "campaigns": [
            {
                "id": "long_1",
                "objetivo": "discovery inicial",
                "presupuesto": budget.get("campana_1", {}),
            },
            {
                "id": "long_2",
                "objetivo": "validacion de clusters nuevos",
                "presupuesto": budget.get("campana_2", {}),
            },
        ],
    }
    write_json(out_plan, plan)
    print(f"OK: plan de campañas creado en {out_plan}")
    return 0


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    out = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def cmd_capture_failures(events_jsonl: Path, out_dir: Path) -> int:
    events = _read_jsonl(events_jsonl)
    failures = [e for e in events if e.get("action") == "reject" or e.get("severity") in {"HIGH", "CRITICAL"}]

    out_dir.mkdir(parents=True, exist_ok=True)
    _write_jsonl(out_dir / "fallas.jsonl", failures)

    by_reason = defaultdict(int)
    for e in failures:
        by_reason[e.get("reason_code", "UNKNOWN")] += 1

    write_json(
        out_dir / "fallas_resumen.json",
        {"total_events": len(events), "total_failures": len(failures), "by_reason": dict(sorted(by_reason.items()))},
    )
    print(f"OK: captura de fallas en {out_dir}")
    return 0


def cmd_dedup_signatures(failures_jsonl: Path, out_clusters: Path) -> int:
    rows = _read_jsonl(failures_jsonl)
    clusters: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for r in rows:
        sig = "|".join(
            [
                str(r.get("stage", "?")),
                str(r.get("reason_code", "?")),
                str(r.get("parser_route", "?")),
            ]
        )
        clusters[sig].append(r)

    out = []
    for sig, items in sorted(clusters.items(), key=lambda kv: len(kv[1]), reverse=True):
        out.append(
            {
                "signature": sig,
                "count": len(items),
                "sample_fixture_id": items[0].get("fixture_id", ""),
                "severity_hint": items[0].get("severity", "MEDIUM"),
            }
        )

    write_json(out_clusters, {"clusters": out, "total_clusters": len(out), "total_failures": len(rows)})
    print(f"OK: deduplicación por firma en {out_clusters}")
    return 0


def cmd_minimize(failures_jsonl: Path, fixtures_root: Path, out_dir: Path) -> int:
    rows = _read_jsonl(failures_jsonl)
    fixture_index: dict[str, Path] = {}
    for p in iter_json_files(fixtures_root):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            fixture_index[str(data.get("fixture_id", p.stem))] = p
        except Exception:
            continue

    out_dir.mkdir(parents=True, exist_ok=True)
    report = []

    for r in rows:
        fid = str(r.get("fixture_id", ""))
        src = fixture_index.get(fid)
        if not src:
            continue

        data = json.loads(src.read_text(encoding="utf-8"))
        minimal = {
            "fixture_id": data.get("fixture_id", fid),
            "schema_version": data.get("schema_version", "actual_v2"),
            "message_type": data.get("message_type", "texto"),
            "payload": data.get("payload", {}),
            "expected_behavior": data.get("expected_behavior", "rechazar"),
            "_minimized_from": str(src.as_posix()),
        }

        dst = out_dir / f"{fid}__min.json"
        dst.write_text(json.dumps(minimal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        report.append({"fixture_id": fid, "source": str(src.as_posix()), "minimized": str(dst.as_posix())})

    write_json(out_dir / "reporte_minimizacion.json", {"total": len(report), "items": report})
    print(f"OK: minimización completada en {out_dir}")
    return 0


def cmd_repro(fixture: Path, out_file: Path) -> int:
    if not fixture.exists():
        print(f"No existe fixture: {fixture}")
        return 1
    data = json.loads(fixture.read_text(encoding="utf-8"))
    out = {
        "generated_at": utc_now(),
        "fixture_path": str(fixture.as_posix()),
        "fixture_id": data.get("fixture_id", fixture.stem),
        "schema_version": data.get("schema_version", "actual_v2"),
        "expected_behavior": normalize_behavior(data.get("expected_behavior", "degrade")),
        "command": f"python3 scripts/fase_b/p01_seccion1.py harness --fixtures {fixture.parent.as_posix()} --out artifacts/p01/fase_b/repro",
        "output_format": "jsonl+summary",
    }
    write_json(out_file, out)
    print(f"OK: script de repro estandarizado en {out_file}")
    return 0


def cmd_triage(clusters_json: Path, out_file: Path) -> int:
    if not clusters_json.exists():
        print(f"No existe clusters: {clusters_json}")
        return 1

    c = json.loads(clusters_json.read_text(encoding="utf-8")).get("clusters", [])
    triage = []

    for cl in c:
        count = int(cl.get("count", 0))
        sev_hint = str(cl.get("severity_hint", "MEDIUM"))
        base = 1
        if sev_hint == "CRITICAL":
            base = 4
        elif sev_hint == "HIGH":
            base = 3
        elif sev_hint == "MEDIUM":
            base = 2

        score = base * (1 + min(count, 20) / 10)
        triage.append(
            {
                "signature": cl.get("signature", ""),
                "count": count,
                "severity_preliminar": sev_hint,
                "score": round(score, 2),
                "prioridad": "P0" if score >= 6 else ("P1" if score >= 3 else "P2"),
            }
        )

    triage.sort(key=lambda x: x["score"], reverse=True)
    write_json(out_file, {"top_hallazgos": triage[:20], "total_clusters": len(triage)})
    print(f"OK: triage preliminar en {out_file}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="P01 Fase B Sección 1")
    sp = p.add_subparsers(dest="cmd", required=True)

    h = sp.add_parser("harness")
    h.add_argument("--fixtures", required=True)
    h.add_argument("--out", required=True)
    h.add_argument("--run-id", default=f"harness-{datetime.now().strftime('%Y%m%d%H%M%S')}")

    cov = sp.add_parser("coverage")
    cov.add_argument("--summary", required=True)

    seed = sp.add_parser("seed-corpus")
    seed.add_argument("--fixtures", required=True)
    seed.add_argument("--out", required=True)

    norm = sp.add_parser("normalize-corpus")
    norm.add_argument("--corpus", required=True)
    norm.add_argument("--out", required=True)

    ms = sp.add_parser("mutate-struct")
    ms.add_argument("--normalized", required=True)
    ms.add_argument("--out", required=True)

    mm = sp.add_parser("mutate-semantic")
    mm.add_argument("--normalized", required=True)
    mm.add_argument("--out", required=True)

    pc = sp.add_parser("plan-campaign")
    pc.add_argument("--budget", required=True)
    pc.add_argument("--out", required=True)

    cf = sp.add_parser("capture-failures")
    cf.add_argument("--events", required=True)
    cf.add_argument("--out", required=True)

    dd = sp.add_parser("dedup-signatures")
    dd.add_argument("--failures", required=True)
    dd.add_argument("--out", required=True)

    mn = sp.add_parser("minimize")
    mn.add_argument("--failures", required=True)
    mn.add_argument("--fixtures-root", required=True)
    mn.add_argument("--out", required=True)

    rp = sp.add_parser("repro")
    rp.add_argument("--fixture", required=True)
    rp.add_argument("--out", required=True)

    tr = sp.add_parser("triage")
    tr.add_argument("--clusters", required=True)
    tr.add_argument("--out", required=True)

    return p


def main() -> int:
    p = build_parser()
    args = p.parse_args()

    cmd = args.cmd
    if cmd == "harness":
        return run_harness(Path(args.fixtures), Path(args.out), args.run_id)
    if cmd == "coverage":
        return cmd_coverage(Path(args.summary))
    if cmd == "seed-corpus":
        return cmd_seed_corpus(Path(args.fixtures), Path(args.out))
    if cmd == "normalize-corpus":
        return cmd_normalize_corpus(Path(args.corpus), Path(args.out))
    if cmd == "mutate-struct":
        return _generate_mutations(Path(args.normalized), Path(args.out), "estructural")
    if cmd == "mutate-semantic":
        return _generate_mutations(Path(args.normalized), Path(args.out), "semantico")
    if cmd == "plan-campaign":
        return cmd_plan_campaign(Path(args.budget), Path(args.out))
    if cmd == "capture-failures":
        return cmd_capture_failures(Path(args.events), Path(args.out))
    if cmd == "dedup-signatures":
        return cmd_dedup_signatures(Path(args.failures), Path(args.out))
    if cmd == "minimize":
        return cmd_minimize(Path(args.failures), Path(args.fixtures_root), Path(args.out))
    if cmd == "repro":
        return cmd_repro(Path(args.fixture), Path(args.out))
    if cmd == "triage":
        return cmd_triage(Path(args.clusters), Path(args.out))

    print(f"Comando no soportado: {cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
