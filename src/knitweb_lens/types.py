"""Core immutable Lens value types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

Scalar = str | int | None
Metadata = tuple[tuple[str, Scalar], ...]


def _require_str(name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be str")


def _require_int(name: str, value: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be int")


def _normalize_metadata(metadata: dict[str, Scalar] | Metadata | None) -> Metadata:
    if metadata is None:
        return ()
    if isinstance(metadata, tuple):
        items = metadata
    else:
        items = tuple(metadata.items())
    normalized: list[tuple[str, Scalar]] = []
    for key, value in items:
        _require_str("metadata key", key)
        if isinstance(value, bool) or isinstance(value, float):
            raise TypeError("metadata values must be str, int, or None")
        if value is not None and not isinstance(value, (str, int)):
            raise TypeError("metadata values must be str, int, or None")
        normalized.append((key, value))
    return tuple(sorted(normalized, key=lambda item: item[0]))


@dataclass(frozen=True)
class ChunkRef:
    """Stable reference back to the source record or chunk."""

    source_id: str
    source_uri: str = ""
    cid: str | None = None
    node_id: str | None = None
    relation_path: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _require_str("source_id", self.source_id)
        _require_str("source_uri", self.source_uri)
        if self.cid is not None:
            _require_str("cid", self.cid)
        if self.node_id is not None:
            _require_str("node_id", self.node_id)
        for rel in self.relation_path:
            _require_str("relation_path item", rel)

    def stable_key(self) -> tuple[str, str, str, str, tuple[str, ...]]:
        return (
            self.source_id,
            self.source_uri,
            self.cid or "",
            self.node_id or "",
            self.relation_path,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_uri": self.source_uri,
            "cid": self.cid,
            "node_id": self.node_id,
            "relation_path": list(self.relation_path),
        }


@dataclass(frozen=True)
class Chunk:
    """Normalized text plus source/provenance metadata."""

    ref: ChunkRef
    text: str
    title: str = ""
    record: dict[str, Any] | None = None
    priority: int = 50
    weight: int = 1
    distance: int = 0
    metadata: Metadata = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _require_str("text", self.text)
        _require_str("title", self.title)
        _require_int("priority", self.priority)
        _require_int("weight", self.weight)
        _require_int("distance", self.distance)
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))

    def stable_key(self) -> tuple[Any, ...]:
        return self.ref.stable_key() + (self.title, self.text)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ref": self.ref.to_dict(),
            "title": self.title,
            "text": self.text,
            "record": self.record,
            "priority": self.priority,
            "weight": self.weight,
            "distance": self.distance,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class RankedChunk:
    """A chunk with deterministic integer ranking details."""

    chunk: Chunk
    score: int
    lexical_score: int
    provenance_score: int
    priority_score: int
    weight_score: int

    def __post_init__(self) -> None:
        _require_int("score", self.score)
        _require_int("lexical_score", self.lexical_score)
        _require_int("provenance_score", self.provenance_score)
        _require_int("priority_score", self.priority_score)
        _require_int("weight_score", self.weight_score)

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunk": self.chunk.to_dict(),
            "score": self.score,
            "lexical_score": self.lexical_score,
            "provenance_score": self.provenance_score,
            "priority_score": self.priority_score,
            "weight_score": self.weight_score,
        }


@dataclass(frozen=True)
class InterpretSession:
    """Ephemeral interpret session after retrieval and budget pruning."""

    query: str
    session_id: str
    ranked_chunks: tuple[RankedChunk, ...]
    budget_chars: int
    max_chunks: int

    def __post_init__(self) -> None:
        _require_str("query", self.query)
        _require_str("session_id", self.session_id)
        _require_int("budget_chars", self.budget_chars)
        _require_int("max_chunks", self.max_chunks)

    @property
    def used_chars(self) -> int:
        return sum(len(item.chunk.text) for item in self.ranked_chunks)

    @property
    def citations(self) -> tuple[ChunkRef, ...]:
        return tuple(item.chunk.ref for item in self.ranked_chunks)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "session_id": self.session_id,
            "budget_chars": self.budget_chars,
            "max_chunks": self.max_chunks,
            "used_chars": self.used_chars,
            "ranked_chunks": [item.to_dict() for item in self.ranked_chunks],
        }


@dataclass(frozen=True)
class InterpretAnswer:
    """Grounded answer plus the session and citations used to produce it."""

    query: str
    text: str
    session: InterpretSession
    reliability: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        _require_str("query", self.query)
        _require_str("text", self.text)

    @property
    def citations(self) -> tuple[ChunkRef, ...]:
        return self.session.citations

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "text": self.text,
            "session": self.session.to_dict(),
            "citations": [ref.to_dict() for ref in self.citations],
            "reliability": self.reliability,
        }
