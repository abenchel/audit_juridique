"""Génère packages/shared-types/src/generated.ts depuis les modèles Pydantic.

Utilise pydantic-to-typescript-like via datamodel-code-generator (qui sait faire
JSON Schema → TS) en passant par un export JSON Schema intermédiaire.

Usage : python -m scripts.generate_ts_types
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from pydantic import BaseModel

from models.audit import (
    AuditCreateRequest,
    AuditCreateResponse,
    AuditReport,
    ErrorFile,
    ExpectedDocument,
    FoundFile,
    JalonReport,
    UnclassifiedFile,
)
from models.document import ClassificationResult, FileMetadata
from models.project import ProjectOut, ProjectSummary

OUT_PATH = Path(__file__).resolve().parents[2] / "packages" / "shared-types" / "src" / "generated.ts"

EXPORTS: list[type[BaseModel]] = [
    AuditCreateRequest,
    AuditCreateResponse,
    AuditReport,
    JalonReport,
    ExpectedDocument,
    FoundFile,
    UnclassifiedFile,
    ErrorFile,
    ClassificationResult,
    FileMetadata,
    ProjectOut,
    ProjectSummary,
]


def _py_to_ts(py_type: str) -> str:
    """Mapping simple JSON Schema → TS pour types primitifs."""
    mapping = {
        "string": "string",
        "integer": "number",
        "number": "number",
        "boolean": "boolean",
        "null": "null",
    }
    return mapping.get(py_type, "unknown")


def _convert_property(prop: dict) -> str:
    if "$ref" in prop:
        ref = prop["$ref"].split("/")[-1]
        return ref
    if "enum" in prop:
        return " | ".join(f'"{e}"' for e in prop["enum"])
    if prop.get("type") == "array":
        item = _convert_property(prop["items"])
        return f"{item}[]"
    if "anyOf" in prop:
        parts = [_convert_property(p) for p in prop["anyOf"]]
        return " | ".join(parts)
    return _py_to_ts(prop.get("type", "unknown"))


def _model_to_ts(model: type[BaseModel]) -> str:
    schema = model.model_json_schema(ref_template="#/$defs/{model}")
    lines: list[str] = []

    # Émet d'abord les définitions imbriquées ($defs)
    defs = schema.get("$defs", {})
    for def_name, def_schema in defs.items():
        lines.append(_schema_to_interface(def_name, def_schema))

    lines.append(_schema_to_interface(model.__name__, schema))
    return "\n\n".join(lines)


def _schema_to_interface(name: str, schema: dict) -> str:
    if schema.get("enum"):
        values = " | ".join(f'"{v}"' for v in schema["enum"])
        return f"export type {name} = {values};"
    if "anyOf" in schema and "properties" not in schema:
        parts = [_convert_property(p) for p in schema["anyOf"]]
        return f"export type {name} = {' | '.join(parts)};"

    required = set(schema.get("required", []))
    props = schema.get("properties", {})
    lines = [f"export interface {name} {{"]
    for prop_name, prop_schema in props.items():
        ts_type = _convert_property(prop_schema)
        optional = "" if prop_name in required else "?"
        nullable = " | null" if prop_schema.get("anyOf") and any(
            p.get("type") == "null" for p in prop_schema["anyOf"]
        ) else ""
        lines.append(f"  {prop_name}{optional}: {ts_type}{nullable};")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    header = """// ============================================================
// AUTO-GENERATED — ne pas éditer à la main
// Source : apps/api/models/*.py (Pydantic v2)
// Régénérer : python -m scripts.generate_ts_types
// ============================================================

"""

    seen: set[str] = set()
    blocks: list[str] = []
    for model in EXPORTS:
        if model.__name__ in seen:
            continue
        seen.add(model.__name__)
        block = _model_to_ts(model)
        # Dédup interfaces déjà émises via $defs
        for line in block.split("\n\n"):
            m = re.match(r"export (interface|type) (\w+)", line)
            if m and m.group(2) in seen and line not in blocks:
                continue
            seen.add(m.group(2)) if m else None
            blocks.append(line)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(header + "\n\n".join(blocks) + "\n", encoding="utf-8")
    print(f"✓ {len(blocks)} types écrits dans {OUT_PATH}")


if __name__ == "__main__":
    main()
