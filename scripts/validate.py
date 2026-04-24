#!/usr/bin/env python3
"""Validate every models/*.yaml file against schema/model.schema.json.

Extra checks on top of JSON Schema:
  - Filename stem must match the model_id field.
  - release_date must be a real calendar date.
  - supersedes, if set, must reference an existing model_id in the repo.
  - sources must not contain the placeholder "..." pattern.
  - model_id must be unique across the repo.

Exits 0 on success, 1 on failure. Prints a summary either way.
"""

from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.exit("error: pyyaml not installed. Run: pip install pyyaml jsonschema")

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("error: jsonschema not installed. Run: pip install pyyaml jsonschema")


ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "models"
SCHEMA_PATH = ROOT / "schema" / "model.schema.json"


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text())


def _normalize(data: Any) -> Any:
    """Coerce YAML-native types (dates, datetimes) to JSON-compatible strings
    so the JSON Schema validator sees them as their documented string form."""
    if isinstance(data, dict):
        return {k: _normalize(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_normalize(v) for v in data]
    if isinstance(data, dt.datetime):
        return data.date().isoformat()
    if isinstance(data, dt.date):
        return data.isoformat()
    return data


def load_entries() -> list[tuple[Path, dict[str, Any]]]:
    entries = []
    for path in sorted(MODELS_DIR.glob("*.yaml")):
        if path.name == "TEMPLATE.yaml":
            continue
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError as exc:
            raise SystemExit(f"{path}: YAML parse error: {exc}")
        if not isinstance(data, dict):
            raise SystemExit(f"{path}: top-level must be a mapping")
        entries.append((path, _normalize(data)))
    return entries


def check_filename(path: Path, data: dict[str, Any]) -> list[str]:
    model_id = data.get("model_id")
    if not isinstance(model_id, str):
        return []  # schema will catch
    if path.stem != model_id:
        return [f"filename stem {path.stem!r} does not match model_id {model_id!r}"]
    return []


def check_date(data: dict[str, Any]) -> list[str]:
    raw = data.get("release_date")
    if not isinstance(raw, (str, dt.date)):
        return []
    if isinstance(raw, dt.date):
        return []  # yaml may parse it already
    try:
        dt.date.fromisoformat(raw)
    except ValueError as exc:
        return [f"release_date {raw!r}: {exc}"]
    return []


def check_sources(data: dict[str, Any]) -> list[str]:
    errors = []
    for url in data.get("sources") or []:
        if not isinstance(url, str):
            continue
        if url.rstrip().endswith("...") or url.endswith("/..."):
            errors.append(f"source {url!r} looks like a placeholder")
    return errors


def check_supersedes(
    data: dict[str, Any], known_ids: set[str]
) -> list[str]:
    target = data.get("supersedes")
    if target is None:
        return []
    if not isinstance(target, str):
        return []
    if target not in known_ids:
        return [
            f"supersedes {target!r} does not reference a model in this repo"
            " (add it or set supersedes: null)"
        ]
    return []


def main() -> int:
    schema = load_schema()
    validator = Draft202012Validator(schema)
    entries = load_entries()

    known_ids = {data.get("model_id") for _, data in entries if isinstance(data.get("model_id"), str)}

    total_errors = 0
    seen_ids: dict[str, Path] = {}

    for path, data in entries:
        rel = path.relative_to(ROOT)
        errors: list[str] = []

        for err in sorted(validator.iter_errors(data), key=lambda e: e.path):
            loc = ".".join(str(p) for p in err.absolute_path) or "<root>"
            errors.append(f"schema: {loc}: {err.message}")

        errors.extend(check_filename(path, data))
        errors.extend(check_date(data))
        errors.extend(check_sources(data))
        errors.extend(check_supersedes(data, known_ids))

        mid = data.get("model_id")
        if isinstance(mid, str):
            if mid in seen_ids and seen_ids[mid] != path:
                errors.append(f"duplicate model_id (also in {seen_ids[mid].relative_to(ROOT)})")
            seen_ids[mid] = path

        if errors:
            print(f"FAIL {rel}")
            for e in errors:
                print(f"  - {e}")
            total_errors += len(errors)
        else:
            print(f"ok   {rel}")

    print()
    if total_errors:
        print(f"{total_errors} error(s) across {len(entries)} file(s)")
        return 1
    print(f"validated {len(entries)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
