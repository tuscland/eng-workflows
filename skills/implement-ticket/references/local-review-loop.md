# Local review loop contract

Planning uses the tracker and pushed history. Implementation and parent finalization use local commits and reports; newly authored implementation, cleanup, and correction commits are pushed only after independent clearance and verification. `finalize-parent` may first open a draft PR from already-published integration history.

## Ownership and upstream composition

The main agent is author/coordinator. A separate reviewer follows [the reviewer instructions](review.md). The author waits during review and handles every correction. Select and record the review mode before delegation:

- **Single reviewer:** for a bounded ticket whose behavior, affected callers, and verification fit one coherent review, one independent agent applies `/code-review`'s Standards and Spec criteria itself and reports both axes separately. Explicitly replace the upstream skill's fan-out with this composition; do not run a second embedded review.
- **Specialist reviewers:** for parent finalization, changes spanning interacting subsystems, security or compatibility-sensitive work, migrations, or uncertain scope, the independent reviewer coordinates `/code-review`'s separate Standards and Spec agents. This uses four active agents including the author. Use this mode when repository instructions require it or the single reviewer discovers complexity that needs separate analyses.

Both modes require the same evidence and clearance. Record mode changes without resetting the correction budget. If independent delegation or the selected mode's required capacity is unavailable, preserve the run and surface the blocker; author self-review cannot replace it.

Within this workflow, `/implement` owns implementation, TDD, verification, and local commits. The independent reviewer replaces its embedded review and runs after the candidate is committed. Pass this composition explicitly when invoking `/implement`; do not run duplicate reviews or commits. Corrections reuse `/implement` and return to the same loop.

## Local handoff

Resolve `git rev-parse --path-format=absolute --git-common-dir`. Store each run under `<git-common-dir>/ticket-workflows/<ticket-key>/<run-id>/`, shared across worktrees and outside tracked files. Print the absolute path and pass it to each agent. These agents need the same local repository; an unpublished candidate cannot be reviewed from remote Git history alone.

Keep:

- `run.md`: workflow kind; canonical ticket repository, issue number, and node ID; ticket/spec source and revision; project URL/ID, item ID, status field/option IDs, previous status, and verified tracker setup when applicable; implementation base, implementation branch, pull-request base, planning baseline, and pinned review-base SHA with its provenance; planning references; author worktree and agent identity; review mode and rationale; initial remote implementation head or `absent`; candidate and verification evidence; correction attempts started; current phase/state; report paths; substantive human decision requests and resolutions; publication progress/URL and verified native ticket association; prioritized cleanup opportunities.
- `spec.md`: a snapshot of the specification, acceptance criteria, and required parent context, with source revision or content hash. Review uses this explicit snapshot instead of rediscovering a spec from commit messages.
- `review-<cycle>-<attempt>.md`: complete reviewer report, with a distinct filename for each retry so prior reports survive.
- `response-<cycle>.md`: the author's dispositions, evidence, input/resulting SHAs, and checks for that correction.

The author owns run state and responses; the reviewer owns reports. Write outputs before returning their paths. Record the pending phase before delegation and the resulting commit before preparing a response. On interruption, inspect existing commits and outputs to finish the pending phase without repeating work.

Each review records the candidate SHA, pinned base, spec identity, cycle, and outcome (`clean`, `findings`, `needs-human`, or `blocked`). Preserve separate Standards and Spec sections, stable IDs such as `STD-001`/`SPEC-001`, and every prior finding's `open`, `partial`, or `closed` status with evidence. Only the reviewer closes findings. `clean` requires both axes complete and no unresolved actionable finding or decision.

Every pass reviews the full ticket diff from the pinned base and rechecks prior findings. A changed candidate or specification invalidates an earlier clean report. A rebuttal-only response still needs review, even at the same SHA.

## Review base and planning baseline

The planning baseline proves that required planning artifacts are available. Verify it remains reachable from the implementation base and candidate when supplied; it does not generally identify the start of a ticket's diff.

- For a new child branch, pin the fetched integration revision from which that branch is created. Earlier delivered siblings are context, not part of this ticket's diff.
- For a single planned ticket using the integration branch itself, pin its pre-implementation planning baseline.
- For a standalone ticket, pin the fetched target revision from which implementation starts.
- For parent finalization, pin the merge base of the fetched target and integration candidate, so review includes planning documents and the entire delivered feature.

Record the base before authoring. Reuse an existing run's pin. If a branch already contains implementation but has no run, recover its actual starting revision from the handoff and history; do not pin its current head or a newer base that would omit existing work. Resolve genuinely ambiguous provenance before clearance. Correcting a legacy planning-baseline pin requires evidence of the ticket's starting revision, preservation of prior reports, and renewed full review without resetting the cycle count.

Keep the pin across corrections. Reconcile later base movement under the publication conditions; changing a pin or reviewed diff invalidates clearance. Still inspect relevant callers and interactions outside the diff when assessing consequences.

## Decisions requiring human input

Use `needs-human` for unresolved decisions that materially change accepted scope, behavior, compatibility, or architecture, or require authority the workflow does not have. Resolve ordinary implementation choices using the specification and repository conventions. Honor recorded decisions; disagreement with a supported implementation choice alone is not a new product decision. Continue independent authorized work while a required decision is pending, preserving the run's phase and budget.

## Ticket project and status

At implementation startup, resolve the intended project from the explicit request or repository/ticket handoff. Otherwise use the ticket's existing project or its parent's project when that identifies one unambiguous project. Inspect repository-linked projects when needed; do not choose among multiple plausible projects by name similarity. Associate the implementation ticket itself, even when its parent already belongs to the project. Preserve other project memberships.

On GitHub Projects v2:

1. Resolve the canonical issue node ID, project ID, and the project's actual Status field and In progress option IDs (or the equivalent active-work option declared by repository conventions). The issue's open/closed state and a label are not the project status.
2. Find the issue's existing project item, following pagination. If absent, call `addProjectV2ItemById` with an input containing the project ID and the issue node ID as `contentId`. Retain the returned item ID; do not create a draft issue or duplicate item.
3. If needed, use `updateProjectV2ItemFieldValue` with that project ID, item ID, Status field ID, and `value: {singleSelectOptionId: <in-progress-option-id>}`. Read back the issue's project membership and the item's Status; record the actual verified values in `run.md`.

On resume, finish only incomplete setup. Re-read remote state before a mutation; do not reset a later review/done status while resuming review or publication. If a project or status mapping is ambiguous, or access prevents the update, record the missing decision or permission and continue independent local work. Do not invent a project/status option or claim startup tracking is complete. Invocation authorizes these specific metadata updates without another approval checkpoint; it does not authorize changing unrelated project fields.

## Six-cycle limit

Review 0 examines the initial implementation. Allow at most six corrections, each followed by review; the usual maximum is seven review passes.

| Result | Next action |
| --- | --- |
| Clean review and passing candidate checks | Check publication conditions |
| Findings and fewer than six corrections started | Reserve correction N, address it, review N |
| Findings after correction 6 and review | Stop `limit-reached`; do not publish new commits |
| Required human decision | Stop `needs-human` with the decision and evidence |
| Failed checks, stale input, incomplete review, or unavailable tools | Record the blocked phase and resolve or surface the blocker |

Reserve a correction before beginning it; complete the cycle after its review. Rebuttal-only corrections count. Always review correction 6; never begin correction 7 without explicit human authorization.

Resume the existing run and pending attempt. Compaction, interruptions, and repeated invocations do not reset the budget. Retrying an incomplete or invalidated review does not allocate a correction or permit an extra fix. Reconcile changed inputs, record any changed specification, and preserve superseded reports. After `limit-reached`, a human must authorize another budget.

## Publication conditions

Only the calling delivery skill (`implement-ticket` or `finalize-parent`) publishes reviewed commits, when:

1. The latest complete review is clean for the exact current commit and spec snapshot.
2. Required checks passed for that candidate, the author worktree is clean, and commits contain only ticket-related work.
3. A fresh fetch confirms the implementation base still contains the planning baseline when one is required, the candidate contains the pinned review base, and the remote implementation branch matches its recorded state. Reconcile unexpected movement in the implementation or pull-request base and renew review whenever it changes the reviewed diff; never silently rebase or force-push.
4. No pending decision, blocker, or exhausted nonconverging loop remains.

For `finalize-parent`, end-to-end evidence may include earlier executions whose applicability to the current candidate is verified under its report reference's reuse policy. This does not waive required PR checks on the published SHA or independent review of the current candidate.

Push the reviewed commit history normally, then create or update its draft PR under repository conventions. Do not squash or rewrite after review. Keep raw review reports, responses, and coordination off the tracker and out of commits. The user-facing HTML delivery report from `finalize-parent` follows that skill's artifact-delivery rules. Never merge or close issues directly.

Record publication progress. If the push succeeds but PR creation fails, verify that same remote head and resume only the missing publication step; reuse an existing PR rather than creating a duplicate.

## Pull request ticket association

Put the provider-native closing directive for the canonical ticket in the pull request body. For GitHub, use `Closes #<number>` when the issue and pull request share a repository, or `Closes <owner>/<repository>#<number>` when they do not. Preserve or restore it when updating an existing pull request. Place it immediately before the local review record so that record remains the final section.

GitHub [interprets closing keywords only for pull requests targeting the default branch](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue). On an integration branch, `Closes #123` creates no native link. A mention or timeline cross-reference is not the relationship shown in the issue's Development section.

After creating or updating the pull request, read back its body and `closingIssuesReferences`, following pagination. Require the exact issue node ID, repository, and number recorded for the ticket. If missing, resolve the canonical issue and pull request node IDs and add a manual native relationship with GitHub's GraphQL mutation:

```graphql
mutation LinkTicket($issueId: ID!, $pullRequestId: ID!) {
  addCloseIssueReferences(input: {
    issueId: $issueId,
    pullRequestIds: [$pullRequestId]
  }) {
    issue { id }
  }
}
```

This operation associates the PR with the issue; it does not close the issue immediately. Preserve existing links. Use the same operation for a cross-repository ticket, resolving each node in its own repository. Check API errors, then independently re-read `closingIssuesReferences` and require the canonical ticket for **every** base branch. `Issue.closedByPullRequestsReferences(userLinkedOnly: true)` can also confirm the manual link from the ticket side. A successful mutation response or retained directive alone is insufficient.

If the relationship remains missing after the write and a bounded read-back retry, or the provider lacks the operation or required access, record publication as incomplete with the exact blocker and existing PR URL. Preserve the reviewed work and retry only the missing association after resolving the blocker; do not create another PR, change its declared base, or substitute a comment. Keep the closing directive immediately before the final review record when editing the body.

GitHub closes an associated issue automatically only when the closing change reaches the repository's default branch. A child pull request targeting an integration branch still carries its own closing directive for traceability, but the eventual integration-to-default pull request must repeat the closing directives for every delivered child ticket. Do not report those tickets as auto-closing until that final pull request contains and verifies the associations.

## Completion and cleanup opportunities

After implementation and review, inspect the final diff and nearby code already encountered for useful follow-up cleanup, dead code removal, or debt reduction. Record the opportunities in `run.md`, publish a concise **Cleanup opportunities** section in the ticket PR body, and include them in the final user-facing handoff alongside the project/status, commit, PR, verified native ticket link, checks, correction/review counts, and local report path. Put the cleanup section before the closing directives and final local review record. Keep enough code evidence, impact, and cost in the PR for `finalize-parent` to assess it without local files or conversation history.

Use a short ranked table with opportunity and code evidence, expected impact, estimated cost, and priority rationale. Express impact concretely (for example, a removed failure mode, less maintenance, or reduced runtime/bundle cost); estimate effort as small/medium/large with a brief explanation of scope and risk. Favor high-impact, low-cost work, explaining any different ordering due to dependencies or risk. Check callers, exports, configuration, and dynamic use before calling code dead; label uncertain candidates as requiring verification. Say when no worthwhile opportunity was found rather than inventing recommendations.

For `implement-ticket`, these are follow-up recommendations, not additional implementation or newly filed tickets. `finalize-parent` selects and executes supported cleanup under its own scope and final review loop. Required correctness fixes still belong in the review/fix loop. Do not alter the reviewed candidate to implement optional cleanup after a clean review; doing so requires renewed verification and review.

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
