---
name: list-merged-prs
description: List PRs authored by the authenticated GitHub user and merged into main since the start of yesterday, ordered chronologically and grouped by coarse category as copy-ready Markdown for Slack. Use for daily updates, standups, and other requests for recently merged PRs.
---

# List Merged PRs

Use Python 3.9+ and the authenticated `gh` CLI to search every repository visible to the current account. The [retrieval helper](scripts/list_merged_prs.py) resolves the current author, paginates GitHub results, filters exact merge timestamps, and returns chronological JSON without changing remote state.

Interpret "since yesterday" as yesterday at local midnight through the current time. Run the helper from its installed skill directory; pass the user's IANA timezone when known, otherwise it uses the system's local timezone:

```sh
python3 <skill-dir>/scripts/list_merged_prs.py --timezone Europe/Paris
```

The timezone above is an example. Honor supplied overrides using `--author`, `--base`, repeatable `--repo owner/name` or `--org name`, and `--since`/`--until`. Dates mean midnight in the selected timezone; timestamps must contain an offset or `Z`. The interval includes `--since` and excludes `--until`; for an inclusive final calendar day, use the following day's midnight as `--until`. Without overrides, use the authenticated author, `main`, all accessible repositories, and yesterday's cutoff.

The helper emits results only after complete retrieval. If the query exceeds GitHub's 1,000-result search cap, split the window or repository scope, complete every partition, deduplicate by PR ID, and sort the combined results by `mergedAt`. For changing search results, retry once. If authentication, permissions, pagination, or other failures prevent completeness, return a concise limitation instead of a partial list or `No PRs found.` Keep ascending merge order within each category.

Group results under these coarse categories, omitting empty categories:

- `*Features*`: `feat`
- `*Fixes*`: `fix`
- `*Documentation*`: `docs`
- `*Maintenance*`: `chore`, `build`, `ci`, `refactor`, `test`, `perf`, and `style`

Determine the category from the Conventional Commit type at the start of each title, allowing an optional scope and `!`. For a title without a recognized type, infer the closest category from its substance; default to Maintenance when unclear.

Return only the grouped Markdown, with no introduction, code fence, or closing note:

```markdown
*Features*

[#123](https://github.com/owner/repository/pull/123) - PR title
```

Preserve each title exactly. If there are no results, say `No PRs found.`
