"""Deterministic integer-scored retrieval."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from .types import Chunk, RankedChunk
from .util import tokenize, unique_tokens


class Retriever:
    """Rank chunks by lexical match, source priority, provenance, and weight."""

    def __init__(self, *, phrase_bonus: int = 40) -> None:
        self.phrase_bonus = phrase_bonus

    def score(self, query: str, chunk: Chunk) -> RankedChunk:
        q_terms = tuple(term for term in tokenize(query) if len(term) > 1)
        if not q_terms:
            q_terms = tokenize(query)
        text = f"{chunk.title}\n{chunk.text}"
        doc_terms = Counter(tokenize(text))
        title_terms = unique_tokens(chunk.title)

        lexical = 0
        for term in q_terms:
            lexical += doc_terms.get(term, 0) * 10
            if term in title_terms:
                lexical += 20
        if query.casefold().strip() and query.casefold().strip() in text.casefold():
            lexical += self.phrase_bonus

        priority_score = chunk.priority * 100
        weight_score = max(chunk.weight, 0) * 10
        provenance_score = max(0, 100 - max(chunk.distance, 0) * 20)
        provenance_score += len(chunk.ref.relation_path) * 5
        score = lexical + priority_score + weight_score + provenance_score
        return RankedChunk(
            chunk=chunk,
            score=score,
            lexical_score=lexical,
            provenance_score=provenance_score,
            priority_score=priority_score,
            weight_score=weight_score,
        )

    def rank(self, query: str, chunks: Iterable[Chunk]) -> tuple[RankedChunk, ...]:
        ranked = [self.score(query, chunk) for chunk in chunks]
        ranked.sort(
            key=lambda item: (
                -item.score,
                item.chunk.ref.source_id,
                item.chunk.ref.source_uri,
                item.chunk.ref.cid or "",
                item.chunk.ref.node_id or "",
                item.chunk.title,
                item.chunk.text,
            )
        )
        return tuple(ranked)

    def retrieve(self, query: str, chunks: Iterable[Chunk], *, limit: int = 8) -> tuple[RankedChunk, ...]:
        if limit < 0:
            raise ValueError("limit must be non-negative")
        return self.rank(query, chunks)[:limit]

