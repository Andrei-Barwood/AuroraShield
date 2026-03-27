#!/usr/bin/env python3
"""
Valida formato unificado de logs P01 en JSONL.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = [
    "timestamp_utc",
    "run_id",
    "stage",
    "event_type",
    "reason_code",
    "severity",
    "fixture_id",
    "parser_route",
    "action",
    "sanitized",
    "details_hash",
]

SEVERITY = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
PARSER_ROUTE = {"legacy_v1", "actual_v2"}
ACTION = {"accept", "degrade", "reject"}


def validate_event(ev: dict, line_no: int) -> list[str]:
    errors = []

    for key in REQUIRED:
        if key not in ev:
            errors.append(f"L{line_no}: falta campo requerido '{key}'")

    if "severity" in ev and ev["severity"] not in SEVERITY:
        errors.append(f"L{line_no}: severity inválido '{ev['severity']}'")

    if "parser_route" in ev and ev["parser_route"] not in PARSER_ROUTE:
        errors.append(f"L{line_no}: parser_route inválido '{ev['parser_route']}'")

    if "action" in ev and ev["action"] not in ACTION:
        errors.append(f"L{line_no}: action inválido '{ev['action']}'")

    if "sanitized" in ev and not isinstance(ev["sanitized"], bool):
        errors.append(f"L{line_no}: sanitized debe ser boolean")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python3 scripts/validar_logs_unificados_p01.py <archivo.jsonl>")
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"No existe: {path}")
        return 1

    all_errors: list[str] = []
    with path.open("r", encoding="utf-8") as fh:
        for idx, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                event = json.loads(raw)
            except json.JSONDecodeError as e:
                all_errors.append(f"L{idx}: JSON inválido ({e})")
                continue
            all_errors.extend(validate_event(event, idx))

    if all_errors:
        print("Se encontraron errores:")
        for e in all_errors:
            print(f"- {e}")
        return 2

    print("OK: logs válidos según formato unificado P01")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
