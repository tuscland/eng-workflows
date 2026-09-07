---
name: eng-review-report
description: "Prepare a concise Markdown engineering-review report of pull requests authored by one person and merged directly into main during a recent window. Use for product-awareness and architecture-focused weekly updates."
---

# Eng Review Report

Produce a terse, evidence-backed update that can be pasted directly into Notion as raw Markdown.

## Defaults

- GitHub identity: the authenticated `gh` account. Resolve it with `gh api user --jq .login`; an explicitly supplied identity overrides it.
- Scope: all repositories visible to the authenticated `gh` account in which that identity has qualifying pull requests. If the request names repositories, use only those repositories. Do not infer repository-only scope from the current working directory.
- Base branch: `main`.
- Time zone: the user's or system's local time zone. An explicitly supplied time zone overrides it.
- Time window: from 00:00 on the most recent Saturday strictly before the run date through the current time. Explicit user-supplied dates or time zones override these defaults.
- Data source: read-only GitHub queries through `gh`. Do not mutate remote state while preparing the report.

## Select reportable pull requests

Report only pull requests that satisfy all of these conditions:

- authored by the selected identity;
- merged during the time window, using the actual `mergedAt` timestamp;
- targeted `main` when merged.

Exclude open, draft, closed-without-merge, and non-`main` pull requests. In particular, do not report intermediate ticket or stacked pull requests merged into integration or implementation branches.

Search across repositories and paginate until the result set is complete. If authentication, permissions, pagination, or rate limits make the result incomplete, do not guess; add a short Markdown blockquote explaining the limitation.

## Investigate each merged pull request

Inspect every reportable pull request individually. Read its description, linked issues, commits, changed files and diff, review discussion, and relevant surrounding code or documentation. Do not summarize from the title alone.

When a pull request merged to `main` is an integration or roll-up change, inspect its constituent commits, linked issues, and intermediate pull requests as evidence needed to understand what shipped. Do not list or link those intermediate pull requests in the report; the `main` pull request remains the sole reportable unit.

For every reportable pull request, explain what engineers need to know. Prioritize:

- the product capability or behavior that became available;
- important changes to system boundaries, APIs, data models, dependencies, infrastructure, or operational behavior;
- credible architecture drift, divergence from established patterns, or new coupling;
- non-obvious implementation constraints, tradeoffs, migrations, rollout concerns, testing challenges, or follow-up risks.

Include only dimensions supported by evidence and material to the project. Do not invent implementation difficulty or architecture drift, and do not add empty labels merely to say that a dimension was absent.

## Synthesis

- Give every reportable pull request its own linked heading and concise summary. Never collapse several pull requests into one reference line.
- Organize related pull requests under broad product or architecture themes when that improves comprehension. Use as few themes as the material warrants.
- State shipped outcomes rather than narrating commit history.
- Preserve important uncertainty and follow-up risk, but do not turn the report into a backlog or list unrelated open work.
- Use intermediate pull requests only as evidence and never identify them in the report. Mention linked issues, planning activity, review activity, or unfinished work only as unlinked context inside a qualifying pull request's summary when necessary to explain what reached `main`.
- Deduplicate each qualifying pull request and include it exactly once.

## Output

Return only the report Markdown: no fenced code block, methodology, query log, or prose before or after it.

Use this shape as a guide rather than a rigid section list:

```markdown
## Eng Review — <start date> to <end date>

### <product or architecture theme>

#### `<repository>` [#123](url) — <pull-request title>

<A compact summary of the shipped product outcome and the material engineering context, such as architecture impact, implementation constraints, migration concerns, or follow-up risk.>

#### `<repository>` [#456](url) — <pull-request title>

<Summary specific to this pull request.>
```

When the report covers only one repository, omit the repository label from pull-request headings. If no pull requests qualify, return the report heading followed by `No pull requests were merged into main during this period.`

Keep the complete result brief enough to read aloud in a meeting while still giving each pull request a useful engineering summary.
