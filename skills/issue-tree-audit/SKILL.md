---
name: issue-tree-audit
description: "Audit a GitHub issue tree against the current codebase and propose factual cleanup of stale, completed, duplicate, or overlapping issues and relationships. Preserve product intent and open specification questions. Use before changing the tracker."
---

# Issue Tree Audit

Reconcile issue facts and delivery status with the current codebase. Produce a manageable, evidence-backed cleanup plan before changing the tracker.

## Keep product decisions in specification work

Correct stale facts, duplication, status, and relationships while preserving the intended outcome. Do not decide future product behavior, invent acceptance criteria, drop requirements, or set roadmap priorities during an audit. Apply product decisions only when they are already recorded or explicitly supplied by the user.

Unknowns are valid issue content: retain unresolved questions for specification work. Do not require answers or start a product interview to finish independent cleanup. When a proposed edit depends on an unresolved product choice, leave that part intact and note the question briefly.

## Establish the audit scope

1. Load the repository instructions and its issue-tracker and label conventions.
2. Resolve the repository and requested issue set. When the user says “my issues,” use the authenticated GitHub identity as the author unless the context identifies another person.
3. Recover the native tree: parents, sub-issues, blockers, linked pull requests, labels, assignees, project fields, and relevant comments. Include neighboring issues only when they affect overlap, status, or ownership.
4. For a large tree, select a small first batch with the highest expected impact. Prefer root trackers, active or near-term work, and nodes whose cleanup will clarify several descendants. State the selection rule.
5. Record the working-tree status before auditing. Repository inspection is read-only in this workflow.

## Test each issue against current reality

Read the issue and its discussion, then inspect the relevant code, tests, documentation, schemas, and merged history. Determine:

- what capability exists today;
- which stated outcomes are delivered, remain unimplemented, or need specification;
- which assumptions, paths, examples, or implementation plans are stale;
- whether another issue already owns the same outcome;
- whether the parent and child relationships still describe the work;
- whether another person is actively responsible for it.

Age alone is not evidence that an issue is obsolete. Missing code shows an outcome is unimplemented, not that it is unwanted. A stale implementation proposal does not invalidate the product need.

Recommend only supported cleanup: keep (including open specification questions), close as completed, mark duplicate, record an already-decided cancellation or supersession, correct stale facts, or repair hierarchy/metadata. Consolidate or split already-defined work only when its outcomes and constraints remain intact. Correct priority only to match a recorded decision or an explicit repository rule.

For every recommendation, provide the issue link, the proposed action, the codebase evidence, why the action is appropriate now, and any remaining work or risk. Keep the explanation concise but sufficient for the user to challenge the conclusion.

## Organize remediation into phases

Order phases by impact, dependency, confidence, and mutation risk. A useful default is:

1. High-confidence status and metadata cleanup: completed issues, recorded cancellations or supersessions, clear duplicates, exact label corrections, and obvious hierarchy repairs.
2. Factual body updates: correct stale references, record delivered work, and simplify duplicated context while preserving intended outcomes, constraints, and unanswered questions.

Keep specification and roadmap decisions outside these phases. Present the audit and a concise plan for the first phase before performing any write.

## Preserve the approval boundary

Issue discovery and codebase inspection are read-only. Do not edit, comment on, relabel, reparent, or close anything until the user approves the phase or the named actions.

Approval for one phase authorizes only that cleanup, not product decisions. Re-read every target immediately before mutation and stop on material concurrent changes. Preserve active work owned by someone else; recommend changes or a status comment instead unless the user explicitly authorizes more.

Tracker cleanup does not authorize repository edits, commits, pull requests, or code changes.

## Execute an approved phase

Make the smallest approved mutation to each issue.

- Prefer short bodies that preserve the stated outcome, known delivery state, agreed constraints and completion criteria, and open specification questions. Leave unspecified criteria unresolved.
- Use native parent and sub-issue relationships as the delivery source of truth. Avoid duplicating child status in prose unless sequencing needs explanation.
- Remove demonstrably stale paths, redundant history, and obsolete implementation detail. Preserve product intent, acceptance criteria, and useful hypotheses or questions for specification work.
- When splitting already-defined work, preserve its requirements and known dependencies without inventing new scope or ordering.
- Change only the requested label axis or field; preserve unrelated metadata.
- For another owner's active issue, leave its scope intact unless approved. A concise informational comment may record what has landed and suggest a split.

Before closing any issue, post a concise justification comment. State the evidence, where remaining work lives, and the superseding issue when applicable. Only then close it with the accurate reason: completed, not planned, or duplicate. Use not planned only for an already-recorded or explicitly supplied cancellation; unanswered product questions are not a closure reason.

## Verify and report

Re-read every issue touched and verify the exact bodies, labels, state reasons, parent and child relationships, and comments. For closures, confirm the justification comment predates the close event. Compare the final working-tree status with the initial snapshot.

Report the completed phase with issue links, note any deviation or partial failure, and explicitly confirm whether repository files remained untouched.
