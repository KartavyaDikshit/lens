# Sync Pulse Issues To Knitweb Project 2

The Lens-enabling Pulse backlog issues already exist:

- https://github.com/Knitweb/pulse/issues/152
- https://github.com/Knitweb/pulse/issues/153
- https://github.com/Knitweb/pulse/issues/154
- https://github.com/Knitweb/pulse/issues/155
- https://github.com/Knitweb/pulse/issues/156
- https://github.com/Knitweb/pulse/issues/157
- https://github.com/Knitweb/pulse/issues/158

Adding them to `https://github.com/orgs/Knitweb/projects/2/views/1` requires a
GitHub token with Project V2 scope. Refresh the local GitHub CLI token:

```bash
gh auth refresh -h github.com -s read:project -s project
```

Then run:

```bash
python3 tools/add_pulse_issues_to_project.py --set-backlog-status
```

The helper is dependency-free and uses `gh auth token` plus GitHub GraphQL. It
adds the seven Pulse issues to Knitweb Project 2 and sets the `Status` field to
`Backlog` when that option exists.

