from knitweb_lens import Chunk, ChunkRef, Retriever


def test_retriever_is_deterministic_and_integer_scored():
    chunks = [
        Chunk(
            ChunkRef("s", cid="b"),
            title="Other",
            text="unrelated",
            priority=10,
        ),
        Chunk(
            ChunkRef("s", cid="a", relation_path=("derived-from->root",)),
            title="Pulse fabric",
            text="Lens preserves Pulse fabric citations.",
            priority=10,
        ),
    ]

    ranked1 = Retriever().retrieve("Pulse citations", chunks, limit=2)
    ranked2 = Retriever().retrieve("Pulse citations", reversed(chunks), limit=2)

    assert [item.chunk.ref.cid for item in ranked1] == ["a", "b"]
    assert [item.chunk.ref.cid for item in ranked2] == ["a", "b"]
    assert all(isinstance(item.score, int) for item in ranked1)


def test_retriever_tie_breaks_by_source_identity():
    chunks = [
        Chunk(ChunkRef("b", cid="2"), title="same", text="same text", priority=1),
        Chunk(ChunkRef("a", cid="1"), title="same", text="same text", priority=1),
    ]

    ranked = Retriever().retrieve("same", chunks, limit=2)

    assert [item.chunk.ref.source_id for item in ranked] == ["a", "b"]

