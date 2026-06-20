# Pulse Backlog Extraction For Lens

These are the Pulse-enabling backlog items requested for
`https://github.com/orgs/Knitweb/projects/2/views/1`. They are intentionally
limited to Pulse core/export work. Lens-specific backlog can live in the Lens
repo or a separate project later.

Project write status: the current `gh` token is authenticated but lacks the
GitHub Project V2 scopes required to read or write Project 2.

## Items

### 1. Pulse: stable read-only export boundary for Lens

Document the supported external imports: canonical CID, Web, JSON-LD
export/import, provenance traversal, attestation verification, and domain record
shape checks.

### 2. Pulse: deterministic Web snapshot API

Add a read-only API returning state root, node count, edge count, records, and
JSON-LD export without mutating fabric state.

### 3. Pulse: reusable provenance query contract

Stabilize ancestry, origins, relation-filter outputs, and dangling-reference
visibility so Lens can cite and rank by provenance paths.

### 4. Pulse: signed record verification helper

Add a single helper for CID recomputation, author-field validation, attestation
verification, and float-free canonical encoding checks.

### 5. Pulse: integer attention metadata records

Add optional CID-linked metadata records for confidence, usefulness, deploy/debug
score, source priority, and relation weight. All values stay integer-only.

### 6. Pulse: gateway `/interpret` delegation hook

Add a read-only gateway hook that forwards interpret requests to a Lens
service/module, without adding LLM/vector dependencies to Pulse.

### 7. Pulse docs: Lens/RLM contract

Specify that Lens is an ephemeral interpret layer over content-addressed fabric
chunks, not a persistence or consensus layer.

