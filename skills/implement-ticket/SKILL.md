---
name: implement-ticket
description: "Implement one tracked ticket in an isolated worktree by validating its planning handoff, delegating to /implement, and opening a draft pull request. Use for standalone or child implementation tickets."
---

# Implement Ticket

Usage:

```text
/implement-ticket <ticket>
```

The upstream `/implement` skill owns TDD, implementation, verification, and its unpublished review preflight. This skill owns ticket readiness, branch and worktree isolation, the durable planning handoff, and pull-request publication.

1. Load the repository instructions and its issue-tracker, branch, worktree, testing, and pull-request conventions. Read the ticket and its comments, treating its authoritative agent brief as the specification when one exists.
2. Resolve the ticket's parent, blockers, acceptance criteria, implementation base, planning baseline, and declared planning artifacts. A standalone ticket may use its declared target branch without a planning baseline. A child ticket must inherit a published integration branch and baseline from its parent.
3. Fetch the remote implementation base. For a child ticket, verify that the branch exists remotely, the planning baseline is reachable from it, and every declared planning artifact exists at that baseline. Confirm that completed blockers have landed on the remote integration branch. If any invariant is missing, stop and direct the user to `/plan-issue-tree`; do not repair the planning handoff or fall back to another base.
4. Give the ticket its own branch and worktree, starting from the fetched remote base. Put the worktree under the repository's `.worktrees/` directory. Never implement directly in the integration worktree or another ticket's worktree.
5. When repository guidance requires an isolated stack or environment for the relevant tests, provision one for this worktree before implementation. Never run a full suite against a shared mutable stack.
6. Run `/implement` with the ticket or authoritative agent brief as its specification and the resolved base commit as the fixed point. Do not duplicate or override its implementation, testing, or review workflow.
7. After `/implement` succeeds, inspect the final diff and prepare the commit and draft pull-request metadata. Invoking `/implement-ticket` authorizes committing only the files belonging to the ticket, pushing the branch normally, and opening the draft pull request without another approval gate. Follow the repository's pull-request-opening guidance. Target the resolved implementation base and link the ticket using the repository's convention.
8. Verify that the remote branch head equals the created commit and that the draft pull request has the intended base and ticket link. Keep the implementation worktree so the author agent can later address review findings.
9. Report what changed, verification performed, remaining caveats, the commit, and the draft pull-request title, URL, and base.

Never force-push, merge, close the ticket, or bypass a missing planning handoff.
