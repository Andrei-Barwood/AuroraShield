#!/usr/bin/env python3
"""
Replay determinístico de fixtures P01.

Uso:
  python3 scripts/p01_replay_deterministico.py --fixtures fixtures/p01 --output artifacts/replay_manifest.json
  python3 scripts/p01_replay_deterministico.py --fixtures fixtures/p01 --verify artifacts/replay_manifest.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def canonical_hash(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_manifest(fixtures_dir: Path) -> dict:
    items = []
    for p in sorted(fixtures_dir.rglob("*.json")):
        items.append(
            {
                "fixture_path": str(p.as_posix()),
                "sha256": canonical_hash(p),
            }
        )
    return {
        "manifest_version": 1,
        "fixtures_count": len(items),
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", required=True, help="Directorio con fixtures JSON")
    parser.add_argument("--output", help="Ruta de salida del manifiesto")
    parser.add_argument("--verify", help="Ruta de manifiesto existente para verificar")
    args = parser.parse_args()

    fixtures = Path(args.fixtures)
    if not fixtures.exists():
        print(f"ERROR: no existe {fixtures}")
        return 1

    manifest = build_manifest(fixtures)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"OK: manifiesto generado en {out}")

    if args.verify:
        ref = Path(args.verify)
        if not ref.exists():
            print(f"ERROR: no existe manifiesto de referencia {ref}")
            return 1
        existing = json.loads(ref.read_text(encoding="utf-8"))
        if existing == manifest:
            print("OK: replay determinístico (sin drift)")
            return 0
        print("ERROR: drift detectado entre manifiesto actual y referencia")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
