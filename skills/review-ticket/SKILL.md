---
name: review-ticket
description: "Independently review the implementation linked to a ticket against its specification and prepare an actionable review for approval. Use from a reviewer agent with no author-side context."
---

# Review Ticket

Usage:

```text
/review-ticket <ticket>
```

The reviewer is independent from the author agent and must reconstruct the review entirely from pushed commits, the issue tracker, and pull-request data. The upstream `/code-review` skill owns detailed standards and specification analysis. This skill owns review scope, isolation, durable findings, and the publication gate.

1. Load the repository instructions and its issue-tracker, worktree, and review conventions. Read the ticket, its parent and planning handoff when present, acceptance criteria, comments, and linked pull requests.
2. Resolve exactly one active pull request implementing the ticket. If none exists or several are plausible, show the ambiguity and ask the user which implementation to review.
3. Read the pull-request description, comments, inline threads, prior reviews, commits, actual base, current head, and full diff. Do not ask the user to reproduce remote context.
4. Create an isolated detached worktree at the current head under the repository's `.worktrees/` directory. This workflow never edits code, commits, pushes, changes pull-request metadata, or resolves threads.
5. Determine whether this workflow previously reviewed the implementation. Every published review from this workflow must visibly include `Reviewed commit: <SHA>`. Use the recorded commit as the later review's fixed point only when it is an ancestor of the current head; ask the user when the relevant prior review or fixed point is ambiguous.
6. On the first review, inspect the full diff from the pull-request base to its head. On a later review, discover findings in changes since the recorded commit while reading surrounding code as needed. Recheck every prior finding against the current code and classify it as `closed`, `partial`, or `open`.
7. Run `/code-review` with the chosen fixed point and the ticket as the specification. Preserve its independent standards and specification passes. Treat their reports as evidence rather than final review wording.
8. Retain only findings the author should act on before merge. Each finding must provide evidence, the concrete consequence if shipped, and the smallest useful resolution direction. Exclude nits, tooling-enforced matters, speculative concerns, and smells without a credible failure mode. A missing test is a finding only when risky behavior remains materially unverifiable.
9. Ask the user when an outcome depends on a product or architectural choice rather than a defect.
10. Draft a concise review containing the reviewed commit, stable visible finding identifiers, and prior-finding statuses when applicable. Show the complete draft and wait for approval before posting it.
11. Immediately before posting, compare the current pull-request head with the reviewed head. If it changed, report that and let the user decide. Once approved and unchanged, publish the draft as a review comment.
