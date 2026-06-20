# Top 10 Feedback Targets

Use public GitHub issues, discussions, or project contact channels. Do not treat
this list as endorsement; it is a prioritized feedback map for Lens.

## 1. Ben Goertzel / OpenCog Hyperon

- Public anchor: https://hyperon.opencog.org/
- Why: Hyperon and MeTTa are the closest conceptual match for symbolic reasoning
  over graph-like atoms.
- Ask: Does Lens preserve enough structure for an RLM-like loop without adopting
  MeTTa as a storage dependency?

## 2. Alexey Potapov / OpenCog Hyperon

- Public anchor: https://arxiv.org/abs/2310.18318
- Why: Hyperon architecture and MeTTa semantics can stress-test the Lens
  distinction between chunks, atoms, and durable fabric records.
- Ask: Which minimal atom/path metadata would make Lens useful for symbolic
  reasoning experiments?

## 3. Daniel.y / @danielaskdd

- Public anchor: https://github.com/danielaskdd
- Project: https://github.com/HKUDS/LightRAG
- Why: Leading public contributor signal on LightRAG, a directly relevant graph
  RAG implementation.
- Ask: Are Lens relation paths and graph-row adapters enough for graph-enhanced
  retrieval without forcing a graph database dependency?

## 4. Jerry Liu / @jerryjliu

- Public anchor: https://github.com/jerryjliu
- Project: https://github.com/run-llama/llama_index
- Why: LlamaIndex is a major reference for data connectors, indexing, and
  retrieval interfaces.
- Ask: Is the SourceAdapter and Chunk contract clear enough for third-party data
  connectors?

## 5. Logan Markewich / @logan-markewich

- Public anchor: https://github.com/logan-markewich
- Project: https://github.com/run-llama/llama_index
- Why: High-volume LlamaIndex maintainer experience is useful for adapter
  ergonomics and test fixtures.
- Ask: What would make Lens adapters easy to test and contribute?

## 6. Harrison Chase / @hwchase17

- Public anchor: https://github.com/hwchase17
- Project: https://github.com/langchain-ai/langchain
- Why: LangChain is a major reference for agent/retriever composition and
  integration boundaries.
- Ask: Should Lens keep generation behind a tiny LLMAdapter protocol, or expose
  a richer tool loop?

## 7. Andrey Vasnetsov / @generall

- Public anchor: https://github.com/generall
- Project: https://github.com/qdrant/qdrant
- Why: Qdrant expertise can help with vector result metadata, filtering, and
  quantized score handling.
- Ask: Is integer quantization of external vector scores acceptable at the Lens
  boundary, and what metadata should be preserved?

## 8. David Dias / @daviddias

- Public anchor: https://github.com/daviddias
- Project: https://github.com/libp2p/specs
- Why: IPFS/libp2p/IPLD experience is relevant to content addressing, provider
  discovery, and keeping transport separate from interpretation.
- Ask: Are Lens source references compatible with future p2p provider discovery
  without smuggling transport concerns into the interpret layer?

## 9. Manu Sporny / @msporny

- Public anchor: https://github.com/msporny
- Specs: https://www.w3.org/TR/vc-data-model-2.0/ and
  https://w3c.github.io/vc-data-integrity/
- Why: W3C verifiable credentials and data integrity work directly inform
  tamper-evident citations and proof-preserving export.
- Ask: What should a provenance-cited answer expose so linked-data proofs remain
  independently verifiable?

## 10. moazbuilds / ClaudeClaw

- Public anchor: https://github.com/moazbuilds
- Project: https://github.com/moazbuilds/claudeclaw
- Why: ClaudeClaw is a useful reference for keeping agent daemons lightweight,
  isolated, and contributor-friendly.
- Ask: What service/auth boundaries should Lens keep before adding any always-on
  daemon or channel integration?

