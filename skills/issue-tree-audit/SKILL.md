---
name: issue-tree-audit
description: "Audit a GitHub issue tree against the current codebase, identify obsolete, completed, duplicate, overlapping, over-scoped, or mis-prioritized work, and propose phased cleanup. Use when reviewing a backlog or an author's related issues before changing the tracker."
---

# Issue Tree Audit

Reconcile the issue tracker with the product that exists now. Treat every issue as a claim to verify, not as current truth. Produce a manageable, evidence-backed cleanup plan before changing the tracker.

## Establish the audit scope

1. Load the repository instructions and its issue-tracker and label conventions.
2. Resolve the repository and requested issue set. When the user says “my issues,” use the authenticated GitHub identity as the author unless the context identifies another person.
3. Recover the native tree: parents, sub-issues, blockers, linked pull requests, labels, assignees, project fields, and relevant comments. Include neighboring issues only when they affect overlap, status, or ownership.
4. For a large tree, select a small first batch with the highest expected impact. Prefer root trackers, active or near-term work, and nodes whose cleanup will clarify several descendants. State the selection rule.
5. Record the working-tree status before auditing. Repository inspection is read-only in this workflow.

## Test each issue against current reality

Read the issue and its discussion, then inspect the relevant code, tests, documentation, schemas, and merged history. Determine:

- what capability exists today;
- what user-visible work genuinely remains;
- which assumptions, paths, examples, or implementation plans are stale;
- whether another issue already owns the same outcome;
- whether the parent and child relationships still describe the work;
- whether another person is actively responsible for it.

Age alone is not evidence that an issue is obsolete. Distinguish a stale implementation proposal from a product need that is still valid.

Classify each issue as one of: keep, close as completed, close as not planned or superseded, mark duplicate, simplify or rescope, split, repair hierarchy, correct labels or priority, or request a product decision.

For every recommendation, provide the issue link, the proposed action, the codebase evidence, why the action is appropriate now, and any remaining work or risk. Keep the explanation concise but sufficient for the user to challenge the conclusion.

## Organize remediation into phases

Order phases by impact, dependency, confidence, and mutation risk. A useful default is:

1. High-confidence cleanup that immediately improves the tree: completed or obsolete issues, clear duplicates, exact label corrections, obvious hierarchy repairs, and concise root trackers.
2. Active scope shaping: refresh important live specifications, split independently deliverable work, and remove stale implementation detail.
3. Portfolio decisions: uncertain product choices, broad reprioritization, and long-term ideas that need owner input.

Adapt the boundaries to the tree. Do not change everything at once. Present the audit and a detailed plan for the first phase before performing any write.

## Preserve the approval boundary

Issue discovery and codebase inspection are read-only. Do not edit, comment on, relabel, reparent, or close anything until the user approves the phase or the named actions.

Approval for one phase authorizes only that phase. Re-read every target immediately before mutation and stop on material concurrent changes. Preserve active work owned by someone else; recommend changes or a status comment instead unless the user explicitly authorizes more.

Tracker cleanup does not authorize repository edits, commits, pull requests, or code changes.

## Execute an approved phase

Make the smallest approved mutation to each issue.

- Prefer short bodies that state the outcome, current delivery state, essential decisions or constraints, and completion condition.
- Use native parent and sub-issue relationships as the delivery source of truth. Avoid duplicating child status in prose unless sequencing needs explanation.
- Remove stale paths, historical narration, speculative implementation detail, and already-delivered examples. Preserve still-valid product decisions and acceptance criteria.
- When splitting work, keep each child independently deliverable and make the tracker explain only shared context and ordering.
- Change only the requested label axis or field; preserve unrelated metadata.
- For another owner's active issue, leave its scope intact unless approved. A concise informational comment may record what has landed and suggest a split.

Before closing any issue, post a concise justification comment. State the evidence, where remaining work lives, and the superseding issue when applicable. Only then close it with the accurate reason: completed, not planned, or duplicate.

## Verify and report

Re-read every issue touched and verify the exact bodies, labels, state reasons, parent and child relationships, and comments. For closures, confirm the justification comment predates the close event. Compare the final working-tree status with the initial snapshot.

Report the completed phase with issue links, note any deviation or partial failure, and explicitly confirm whether repository files remained untouched.
