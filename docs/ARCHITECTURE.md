# Architecture

Lens v1 is an ephemeral interpret layer over content-addressed fabric data.

## Boundaries

- Pulse/Knitweb remains the fabric, transport, accounting, and provenance source.
- Lens reads exported Web data and source rows. It does not persist consensus
  state or mutate Pulse records.
- Live LLMs, graph databases, and vector stores are optional wrappers around the
  adapter protocol, not base dependencies.

## Flow

1. Source adapters normalize data into `Chunk` values.
2. `Retriever` ranks chunks with integer-only scoring.
3. `RLMHarness` creates an `InterpretSession`.
4. An `LLMAdapter` turns selected chunks into an answer.
5. `InterpretAnswer` returns text plus citations back to each `ChunkRef`.

## Lessons From Similar Systems

- Hyperon/MeTTa: represent knowledge as queryable atoms in a graph-like store,
  and let reasoning iterate over those atoms. Lens applies that pattern to
  Pulse chunks without embedding MeTTa as a storage dependency.
- LightRAG: graph relationships should be first-class retrieval signals, not
  an afterthought behind vector similarity.
- LlamaIndex and LangChain: connectors and retrievers need to be separable from
  generation so users can bring their own sources and models.
- IPFS/libp2p: content identity and provider discovery are separate concerns.
  Lens keeps source ids and CIDs explicit, then leaves p2p movement to Pulse.
- W3C DID/VC/Data Integrity: verifiable statements need identifiers, proofs,
  and tamper-evident representations. Lens keeps provenance and CIDs visible in
  every answer path.
- ClaudeClaw-style daemons: always-on agent systems should have clear isolation
  and auth boundaries. Lens core therefore stays library-first; the HTTP route
  is small, explicit, and stdlib-only.

## Non-Goals

- No base vector database.
- No base graph database.
- No required LLM API key.
- No durable writes to Pulse.
- No ranking floats in returned metadata.

