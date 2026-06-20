# Evals

Lens has a small offline eval harness for reliability work. It is intentionally
plain JSON and pure Python: no model service, vector database, or graph database
is required.

## Run

```bash
lens eval path/to/eval.json --base-dir .
```

## Fixture Shape

```json
{
  "cases": [
    {
      "name": "grounded provenance query",
      "query": "What preserves provenance citations?",
      "paths": ["tests/fixtures/example.md"],
      "should_abstain": false,
      "must_cite": ["example.md"]
    },
    {
      "name": "unsupported query",
      "query": "quantum weather banana",
      "paths": ["tests/fixtures/example.md"],
      "should_abstain": true
    }
  ]
}
```

`must_cite` entries are substring checks over citation source ids, source URIs,
CIDs, and node ids. The result report is integer-only and includes:

- total / passed / failed;
- true, false, and missed abstentions;
- citation failure count;
- integer average confidence;
- per-case confidence and missing citation fragments.

Use this before changing confidence thresholds, retriever scoring, or source
trust weighting.

