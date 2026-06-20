"""Lens: pure-Python interpret sessions over Knitweb fabric data."""

from .adapters import (
    FabricWebAdapter,
    JsonLdAdapter,
    LocalFilesAdapter,
    MappingRowsAdapter,
    RdfJsonLdAdapter,
    SourceAdapter,
    VectorResultsAdapter,
)
from .context import (
    CONTEXT_FORMAT,
    CONTEXT_VERSION,
    answer_from_context,
    answer_markdown,
    citation_lines,
    citations_markdown,
    context_bundle,
    session_from_context,
    session_markdown,
)
from .retriever import Retriever
from .rlm import LLMAdapter, OfflineLLMAdapter, RLMHarness
from .types import Chunk, ChunkRef, InterpretAnswer, InterpretSession, RankedChunk

__all__ = [
    "Chunk",
    "ChunkRef",
    "CONTEXT_FORMAT",
    "CONTEXT_VERSION",
    "FabricWebAdapter",
    "InterpretAnswer",
    "InterpretSession",
    "JsonLdAdapter",
    "LLMAdapter",
    "LocalFilesAdapter",
    "MappingRowsAdapter",
    "OfflineLLMAdapter",
    "RdfJsonLdAdapter",
    "Retriever",
    "RLMHarness",
    "RankedChunk",
    "SourceAdapter",
    "VectorResultsAdapter",
    "answer_from_context",
    "answer_markdown",
    "citation_lines",
    "citations_markdown",
    "context_bundle",
    "session_from_context",
    "session_markdown",
]

__version__ = "0.1.0"
