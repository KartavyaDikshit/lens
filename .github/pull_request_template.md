## Summary

## Verification

- [ ] `python -m pytest`
- [ ] `python -m build` when packaging or public imports changed

## Review Policy

- [ ] This PR deletes no more than two files.
- [ ] This PR does not touch control surfaces.
- [ ] Reviewer feedback was given, even if the PR is mergeable as-is.

Control surfaces include CI, package metadata, release/versioning, auth/project
scripts, governance docs, service boundary code, and changes that weaken
citations, integer-only scoring, or offline-testability.

