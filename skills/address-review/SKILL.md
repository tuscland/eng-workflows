---
name: address-review
description: "Address actionable findings on a ticket's linked implementation, commit verified fixes locally, and prepare the push and reply for approval. Use from the author agent after /review-ticket."
---

# Address Review

Usage:

```text
/address-review <ticket>
```

The author agent usually retains the planning and implementation worktrees, but this workflow must remain reconstructible from remote state. The upstream `/implement` skill owns changes, tests, and its unpublished review preflight. This skill owns review interpretation, the local commit, and the push-and-reply approval gate.

1. Load the repository instructions and its issue-tracker, worktree, testing, and review conventions. Read the ticket and resolve exactly one active linked pull request. If none exists or several are plausible, ask the user which implementation to update.
2. Read the pull-request head, reviews, review comments, inline threads, commits, and diff. Select the substantive review being addressed and collect all of its unresolved findings. Use its visible `Reviewed commit: <SHA>` as the fixed point. Ask the user if the target review is ambiguous or the recorded commit is missing or not an ancestor of the current head.
3. Locate the implementation branch worktree. Reuse it when it matches the remote branch; otherwise create a branch worktree under the repository's `.worktrees/` directory from the current remote head. Never apply fixes in the detached review worktree.
4. Verify every finding independently:
   - accept it when the current code supports it;
   - prepare a concise rebuttal with code evidence when it does not;
   - ask the user when it requires a product or architectural decision.
5. When at least one finding is accepted, give the accepted findings to `/implement` as the specification, using the reviewed commit as the fixed point. Let `/implement` own the fixes, tests, and unpublished review preflight. When repository guidance requires an isolated stack or environment, provision one for this worktree before tests. If every finding is rebutted, skip implementation and prepare an evidence-backed reply.
6. After verification succeeds, inspect the final diff and commit only the files changed to address the review. Invoking `/address-review` authorizes this local commit without another approval gate. If verification failed or the commit scope is ambiguous, stop without committing. If no code changed, skip the commit.
7. Draft a complete reply mapping every finding identifier to its disposition, evidence, fix, or rebuttal. Show the diff and verification results, the local commit when one exists, and the complete draft reply. Wait for approval before pushing or posting.
8. Immediately before acting, fetch the remote branch and verify that its pull-request head still equals the pre-fix head inspected by this workflow. If it changed, report that and let the user decide.
9. Approval authorizes a normal push of the local commit, when one exists, and posting the complete reply. Push first, then verify that the remote pull-request head equals the local commit. Post the reply only after that verification succeeds. If no code changed, skip the push and post only after confirming the head is unchanged.

Never force-push, merge, close issues, or resolve review threads.
