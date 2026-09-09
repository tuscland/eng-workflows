---
name: implement-ticket
description: "Implement a tracked ticket with an independent local review/fix loop, then publish the verified result. Use for standalone or child implementation tickets."
---

# Implement Ticket

```text
/implement-ticket <ticket-or-local-run>
```

The calling agent is the author and coordinator; a separate agent reviews. Read [the local loop contract](references/local-review-loop.md) for handoffs, upstream skill composition, cycle counting, and publication conditions. This workflow explicitly requests review subagents.

1. Load repository conventions and the ticket's authoritative specification. Resolve its parent, blockers, declared implementation base, implementation branch, pull-request base, planning baseline, and artifacts. Fetch the base; required planning artifacts and completed blockers must be reachable from it. A standalone ticket may use its declared target branch without a planning baseline. Surface missing or ambiguous handoffs rather than choosing another base.
2. Reuse the ticket's existing local run and author worktree, preserving its phase and cycle count. For a new run, reuse the declared implementation branch and worktree when they already exist. This is the normal single-ticket case: the integration branch is also the implementation branch. Otherwise create the declared ticket branch and its worktree under `.worktrees/` from the fetched implementation base. Initialize the local run and specification snapshot; provision the repository-required isolated test environment.
3. Run `/implement` under the shared composition contract: implement, verify, and commit locally; the next step supplies its review. Record the candidate and check results. Reuse its commit rather than committing twice.
4. Spawn a reviewer without author conversation history. Supply [the reviewer instructions](references/review.md), local run path, candidate SHA, pinned base, specification, and prior reports/responses. Wait for its complete report and review subagents before editing again.
5. Follow the report:
   - `clean`: apply the shared publication conditions.
   - `findings`: reserve the next correction cycle and follow **Correct findings** below in this same author agent, then return to step 4. After the third correction's review still reports findings, stop as `limit-reached`.
   - `needs-human` or `blocked`: preserve the run and surface the decision or actual blocker.
6. After the publication conditions pass, normally push the reviewed commit history and create or update the ticket's draft pull request under repository conventions. Explicit invocation authorizes this final publication. Link the ticket, target its declared pull-request base, and append the review record defined by the local loop contract after the normal change and verification summary.
7. Verify the remote head and pull-request base/link. Record and report the commit, PR, checks, cycles used, and local report path. Retain the worktree and run.

Only this skill coordinates the loop and publishes. Never force-push, merge, close issues, or post intermediate review conversations.

## Correct findings

Before a new correction, require the author head to match the reviewed candidate. On resume, inspect the recorded phase and existing fixes; finish pending verification or the response without reapplying changes, recommitting, or reserving another cycle. Reconcile unaccounted changes first.

Verify each unresolved finding. Accept supported defects or rebut them with evidence; return required product decisions to the user. Give accepted findings and the original specification to `/implement` under the shared composition contract. If every finding is rebutted, skip code changes and the commit.

Record the resulting candidate and checks, then write the response covering every finding ID with its fix, rebuttal, or decision and evidence. Failed checks leave the cycle incomplete. Every response, including one with an unchanged SHA, returns to independent review; only the reviewer closes findings.
