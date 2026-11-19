# Example release notes (invented)

Style for the notes file passed to `gh release create --notes-file`: one bullet per theme,
a bold label, one or two user-facing sentences, no internal bug or decision IDs.

```markdown
## 0.7.1 (2026-01-15)

- **Tested against third-party servers:** the MQTT reader and the OPC UA reader, against a
  public broker and an independent test server; and `exampletool run` end to end over them
  (opt-in, `EXAMPLETOOL_REALSERVER=1`).
- **Fixed (MQTT):** a negative 16-bit value now reads correctly, and a device's disconnect
  marks its channels offline.
- **State:** a saved state now carries queued items and a running maximum wait. A state taken
  from a live system is still refused when it holds an item whose position is unknown.
  Invalid state files are now refused by name, such as a timer with nothing waiting.
```

Note the last bullet states a known limit where a reader would assume more.

# Lessons for a repo-specific release file

Once a repo has been released a few times, write `references/<repo>.md` with what the generic
steps do not cover:

- The full list of files that carry the version, and any that a test cross-checks.
- Which workflow fires the publish (a release, or a tag push), and that tagging is safe when
  only a published release deploys.
- Push the version commit and wait for its CI to pass before the tag and the release.
- A public changelog may take no internal bug IDs: strip them when copying lines from an
  internal one.
- A changelog may hold an old `## Unreleased` far down: replace only the top one.
- A minor release also updates the "what's new" page; a patch release leaves it alone.
- After publishing, install the released version in a clean virtual environment and run one
  example. The package index may take a minute to show the new version: retry, do not rebuild.
- Any known test failures that are local only (for example optional GUI dependencies), so they
  are not mistaken for release blockers.
