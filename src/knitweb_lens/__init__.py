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
from .retriever import Retriever
from .rlm import LLMAdapter, OfflineLLMAdapter, RLMHarness
from .types import Chunk, ChunkRef, InterpretAnswer, InterpretSession, RankedChunk

__all__ = [
    "Chunk",
    "ChunkRef",
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
]

__version__ = "0.1.0"

