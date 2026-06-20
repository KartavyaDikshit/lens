# Review Policy

Lens keeps review lightweight, but the maintainer norm is explicit: trusted
contributors should get useful feedback every time, including when their change
is accepted quickly.

## Trusted Extra Developer Rule

A trusted extra developer may merge small changes when both conditions are true:

- The pull request deletes no more than two files.
- The pull request does not change control surfaces.

Control surfaces include:

- `.github/workflows/` and repository automation.
- `pyproject.toml`, package entry points, versioning, and release metadata.
- auth, GitHub Project, deployment, or maintainer scripts under `tools/`.
- `LICENSE`, `CONTRIBUTING.md`, `docs/REVIEW_POLICY.md`, and governance docs.
- HTTP/service boundary code such as `src/knitweb_lens/server.py`.
- Any change that weakens citation preservation, integer-only scoring, or
  offline-testability.

If a pull request touches a control surface or deletes more than two files, it
needs normal maintainer review before merge.

## Always Give Feedback

Every pull request from the trusted extra developer should receive feedback,
even if the final decision is "merge as-is." Feedback should be specific enough
to help her build stronger future changes:

- Name what is correct or useful.
- Point to the exact file, behavior, or test that matters.
- State any risk or missing test plainly.
- Give one concrete next step when a change is requested.

## Comment Response Style

Use respectful technical tact in review replies. The desired style is polite,
direct, and precise:

- Acknowledge the comment before disagreeing or redirecting.
- Avoid blame, sarcasm, and vague praise.
- Prefer evidence: file paths, tests, commands, API contracts, and examples.
- Keep the relationship warm while keeping the technical bar clear.
- When accepting feedback, say what changed.
- When declining feedback, explain the tradeoff and offer a narrower path.

Useful reply shapes:

```text
Thanks, this is a valid concern. I changed the adapter test to cover the Pulse
JSON-LD path directly in tests/test_adapters.py.
```

```text
I agree with the direction, but I do not want this in the base package because
it adds a live service dependency. A small optional adapter wrapper would fit.
```

```text
Good catch. The current change deletes one fixture and does not touch control
surfaces, so it is mergeable after the test run passes.
```

