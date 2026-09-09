# Local review loop contract

Planning uses the tracker and pushed history. Implementation review uses local commits and reports; only the verified, independently cleared result is pushed.

## Ownership and upstream composition

The main agent is author/coordinator. A separate reviewer follows [the reviewer instructions](review.md) and runs `/code-review`'s parallel Standards and Spec agents. The author waits during review and handles every correction. This uses four active agents without a separate coordinator or author subagent.

Within this workflow, `/implement` owns implementation, TDD, verification, and local commits. The independent reviewer replaces its embedded review and runs after the candidate is committed. Pass this composition explicitly when invoking `/implement`; do not run duplicate reviews or commits. Corrections reuse `/implement` and return to the same loop.

## Local handoff

Resolve `git rev-parse --path-format=absolute --git-common-dir`. Store each run under `<git-common-dir>/ticket-workflows/<ticket-key>/<run-id>/`, shared across worktrees and outside tracked files. Print the absolute path and pass it to each agent. These agents need the same local repository; an unpublished candidate cannot be reviewed from remote Git history alone.

Keep:

- `run.md`: ticket/spec source and revision; target branch and pinned base SHA; planning references; author branch/worktree and agent identity; initial remote implementation head or `absent`; candidate and verification evidence; correction attempts started; current phase/state; report paths; publication progress/URL.
- `spec.md`: a snapshot of the specification, acceptance criteria, and required parent context, with source revision or content hash. Review uses this explicit snapshot instead of rediscovering a spec from commit messages.
- `review-<cycle>-<attempt>.md`: complete reviewer report, with a distinct filename for each retry so prior reports survive.
- `response-<cycle>.md`: the author's dispositions, evidence, input/resulting SHAs, and checks for that correction.

The author owns run state and responses; the reviewer owns reports. Write outputs before returning their paths. Record the pending phase before delegation and the resulting commit before preparing a response. On interruption, inspect existing commits and outputs to finish the pending phase without repeating work.

Each review records the candidate SHA, pinned base, spec identity, cycle, and outcome (`clean`, `findings`, `needs-human`, or `blocked`). Preserve separate Standards and Spec sections, stable IDs such as `STD-001`/`SPEC-001`, and every prior finding's `open`, `partial`, or `closed` status with evidence. Only the reviewer closes findings. `clean` requires both axes complete and no unresolved actionable finding or decision.

Every pass reviews the full ticket diff from the pinned base and rechecks prior findings. A changed candidate or specification invalidates an earlier clean report. A rebuttal-only response still needs review, even at the same SHA.

## Three-cycle limit

Review 0 examines the initial implementation. Allow at most three corrections, each followed by review; the usual maximum is four review passes.

| Result | Next action |
| --- | --- |
| Clean review and passing candidate checks | Check publication conditions |
| Findings and fewer than three corrections started | Reserve correction N, address it, review N |
| Findings after correction 3 and review | Stop `limit-reached`, unpublished |
| Required human decision | Stop `needs-human` with the decision and evidence |
| Failed checks, stale input, incomplete review, or unavailable tools | Record the blocked phase and resolve or surface the blocker |

Reserve a correction before beginning it; complete the cycle after its review. Rebuttal-only corrections count. Always review correction 3; never begin correction 4 without explicit human authorization.

Resume the existing run and pending attempt. Compaction, interruptions, and repeated invocations do not reset the budget. Retrying an incomplete or invalidated review does not allocate a correction or permit an extra fix. Reconcile changed inputs, record any changed specification, and preserve superseded reports. After `limit-reached`, a human must authorize another budget.

## Publication conditions

Only `implement-ticket` publishes, when:

1. The latest complete review is clean for the exact current commit and spec snapshot.
2. Required checks passed for that candidate, the author worktree is clean, and commits contain only ticket-related work.
3. A fresh fetch confirms the target still matches the pinned base and the remote implementation branch matches its recorded state. Unexpected movement requires reconciliation and renewed review, not a silent rebase or force-push.
4. No pending decision, blocker, or exhausted nonconverging loop remains.

Push the reviewed commit history normally, then create or update its draft PR under repository conventions. Do not squash or rewrite after review. Keep reports, responses, and coordination off the tracker and out of commits. Never merge or close issues.

Record publication progress. If the push succeeds but PR creation fails, verify that same remote head and resume only the missing publication step; reuse an existing PR rather than creating a duplicate.
