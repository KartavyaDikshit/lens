# Contributing

Lens needs contributors who care about deterministic systems, provenance, and
small interfaces. The core rule is simple: keep the default path pure Python and
offline-testable.

## Useful First Contributions

- Add an adapter fixture for another graph or document export shape.
- Improve citation formatting without changing deterministic ranking.
- Add more provenance ranking tests against Pulse JSON-LD examples.
- Write a small optional integration wrapper for a vector store or graph store.
- Improve the GitHub Pages docs with examples and screenshots.

## Engineering Rules

- Do not add a required LLM, vector database, graph database, network, or cloud
  dependency to the base package.
- Scores and persisted metadata are integers. Do not introduce floats into
  ranking outputs.
- Every answer path must preserve citations to source id, URI, and CID or node id
  when available.
- Tests must pass offline with `python -m pytest`.
- Prefer explicit adapters over hidden global service clients.

## Pull Request Checklist

- Tests cover the changed behavior.
- New adapters include at least one deterministic fixture.
- Public types remain importable from `knitweb_lens`.
- README or docs are updated when user-facing behavior changes.

