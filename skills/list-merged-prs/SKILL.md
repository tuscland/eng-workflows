---
name: list-merged-prs
description: List PRs authored by the authenticated GitHub user and merged into main since the start of yesterday, ordered chronologically and grouped by coarse category as copy-ready Markdown for Slack. Use for daily updates, standups, and other requests for recently merged PRs.
---

# List Merged PRs

Use the authenticated `gh` CLI to search every repository visible to the current account. Unless the user supplies another author, resolve the author with `gh api user --jq .login`.

Interpret "since yesterday" as starting at yesterday's calendar date in the user's local timezone. Compute that date as `YYYY-MM-DD`, then run:

```sh
gh api graphql \
  -f query='query($searchQuery: String!) {
    search(query: $searchQuery, type: ISSUE, first: 100) {
      nodes { ... on PullRequest { number title url mergedAt } }
    }
  }' \
  -F searchQuery='author:LOGIN is:pr is:merged base:main merged:>=YYYY-MM-DD' \
  --jq '.data.search.nodes | sort_by(.mergedAt) | .[] | "[#\(.number)](\(.url)) - \(.title)"'
```

Keep the ascending merge order produced by the command within each category.

Replace `LOGIN` with the resolved account login. Honor a different author, date range, organization, repository, or base branch when the user supplies one. Otherwise use the authenticated login, `main`, and the cutoff above.

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
