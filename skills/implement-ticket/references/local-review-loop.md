# Local review loop contract

Planning uses the tracker and pushed history. Implementation review uses local commits and reports; only the verified, independently cleared result is pushed.

## Ownership and upstream composition

The main agent is author/coordinator. A separate reviewer follows [the reviewer instructions](review.md) and runs `/code-review`'s parallel Standards and Spec agents. The author waits during review and handles every correction. This uses four active agents without a separate coordinator or author subagent.

Within this workflow, `/implement` owns implementation, TDD, verification, and local commits. The independent reviewer replaces its embedded review and runs after the candidate is committed. Pass this composition explicitly when invoking `/implement`; do not run duplicate reviews or commits. Corrections reuse `/implement` and return to the same loop.

## Local handoff

Resolve `git rev-parse --path-format=absolute --git-common-dir`. Store each run under `<git-common-dir>/ticket-workflows/<ticket-key>/<run-id>/`, shared across worktrees and outside tracked files. Print the absolute path and pass it to each agent. These agents need the same local repository; an unpublished candidate cannot be reviewed from remote Git history alone.

Keep:

- `run.md`: canonical ticket repository and issue number; ticket/spec source and revision; implementation base, implementation branch, pull-request base, and pinned review-base SHA (the planning baseline for planned work); planning references; author worktree and agent identity; initial remote implementation head or `absent`; candidate and verification evidence; correction attempts started; current phase/state; report paths; substantive human decision requests and resolutions; publication progress/URL and verified closing association.
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
3. A fresh fetch confirms the implementation base still contains the pinned planning baseline and the remote implementation branch matches its recorded state. Reconcile unexpected movement in the implementation or pull-request base and renew review whenever it changes the reviewed diff; never silently rebase or force-push.
4. No pending decision, blocker, or exhausted nonconverging loop remains.

Push the reviewed commit history normally, then create or update its draft PR under repository conventions. Do not squash or rewrite after review. Keep reports, responses, and coordination off the tracker and out of commits. Never merge or close issues directly.

Record publication progress. If the push succeeds but PR creation fails, verify that same remote head and resume only the missing publication step; reuse an existing PR rather than creating a duplicate.

## Pull request ticket association

Put the provider-native closing directive for the canonical ticket in the pull request body. For GitHub, use `Closes #<number>` when the issue and pull request share a repository, or `Closes <owner>/<repository>#<number>` when they do not. Preserve or restore it when updating an existing pull request. Place it immediately before the local review record so that record remains the final section.

After creating or updating the pull request, read back the remote body and provider relationship. On GitHub, when the pull request targets the default branch, verify that `closingIssuesReferences` contains the exact repository and issue number recorded in `run.md`; matching only a number is insufficient across repositories. For a non-default integration base, verify the issue cross-reference and the exact directive in the remote body, then record that automatic closure is deferred to the final integration pull request. A bare issue URL or textual mention does not satisfy either check.

GitHub closes an associated issue automatically only when the closing change reaches the repository's default branch. A child pull request targeting an integration branch still carries its own closing directive for traceability, but the eventual integration-to-default pull request must repeat the closing directives for every delivered child ticket. Do not report those tickets as auto-closing until that final pull request contains and verifies the associations.

## Pull request review record

Append a concise review record to the end of the pull request description without replacing the repository's normal template. Build it from the completed reports, responses, and decision history in the local run; do not rely on conversation memory or link local files.

Report both counts so the result is unambiguous:

- **Correction loops** is the number of completed correction/fix cycles. The initial review is not a correction loop, and incomplete or invalid review retries do not count.
- **Review passes** is the number of completed reviews, including review 0 and the review after each completed correction.

For each completed review pass, list every actionable finding in that report with its stable ID, concise summary, and status or disposition at that pass. Say `None` when the pass was clean. Preserve enough detail to explain what the loop discovered and how it converged, without copying full reports or internal discussion.

List every substantive product, architecture, scope, or implementation decision requested from a human during the run, together with the resulting decision. Exclude routine tool and publication permission prompts. Say `None` when no substantive decision was requested.

Use this shape:

```markdown
## Local review record

- Correction loops: <count>
- Review passes: <count>

### Review 0 — <outcome>

- `<finding ID>` — <finding summary>; <status or disposition>

### Review 1 — <outcome>

- None

### Human decisions requested

- <decision requested> — <resulting decision>
```
