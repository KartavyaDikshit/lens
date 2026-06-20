"""Small deterministic utilities shared by Lens modules."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

TOKEN_RE = re.compile(r"[a-z0-9]+")


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def stable_id(prefix: str, value: Any) -> str:
    digest = hashlib.sha256(stable_json(value).encode("utf-8")).hexdigest()
    return f"{prefix}:{digest}"


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def tokenize(text: str) -> tuple[str, ...]:
    return tuple(TOKEN_RE.findall(text.casefold()))


def unique_tokens(text: str) -> set[str]:
    return set(tokenize(text))


def record_to_text(record: Any) -> str:
    if isinstance(record, str):
        return record
    if not isinstance(record, dict):
        return stable_json(record)
    parts: list[str] = []
    for key in ("title", "name", "label", "summary", "description", "body", "text", "content"):
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
    if parts:
        return "\n\n".join(parts)
    return stable_json(record)


def record_title(record: Any, fallback: str = "") -> str:
    if isinstance(record, dict):
        for key in ("title", "name", "label", "kind", "id"):
            value = record.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return fallback


def chunk_text(text: str, *, size: int = 1200, overlap: int = 120) -> tuple[str, ...]:
    """Split text into deterministic character windows on whitespace."""
    cleaned = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    if not cleaned:
        return ()
    if len(cleaned) <= size:
        return (cleaned,)
    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + size)
        if end < len(cleaned):
            boundary = cleaned.rfind(" ", start, end)
            if boundary > start + size // 2:
                end = boundary
        part = cleaned[start:end].strip()
        if part:
            chunks.append(part)
        if end >= len(cleaned):
            break
        next_start = max(end - overlap, start + 1)
        while (
            next_start < len(cleaned)
            and next_start > 0
            and cleaned[next_start].isalnum()
            and cleaned[next_start - 1].isalnum()
        ):
            next_start += 1
        start = next_start
    return tuple(chunks)


def json_lines(values: Iterable[dict[str, Any]]) -> str:
    return "\n".join(stable_json(value) for value in values)
