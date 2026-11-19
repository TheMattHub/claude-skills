---
type: llm
---

Judge the final answer against these observable criteria.

1. The answer starts by reading the CI workflows to learn which event (a published release, a tag push) uploads to PyPI or deploys, before tagging or creating a release.
2. The GitHub release is created as a draft, and the answer says the user publishes it, with the reason (publishing can trigger a deploy or an upload that cannot be undone).
3. The answer finds every file that carries the version and the tag format from the previous release (for example by looking at the last version-bump commit or tag), not only pyproject.toml.
4. The Unreleased section of the changelog is turned into a dated 0.4.0 heading and the claims in its summary are checked against the code.
5. The answer plans to verify the published package after the user publishes (for example installing the exact version in a clean environment).

PASS if at least 4 of the 5 criteria hold. FAIL otherwise. Name the criteria that failed.
