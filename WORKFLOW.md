# Tracked Delivery Workflow

## Purpose

This workflow carries a substantial tracked change from discovery through implementation and independent review without losing planning context between agents.

It composes existing planning, implementation, and code-review skills. Those skills own the quality of their specialist work. The four workflow skills in this repository own the surrounding lifecycle:

- durable planning artifacts;
- issue-tree and blocker state;
- integration and implementation branches;
- isolated worktrees and test environments;
- cross-agent handoffs;
- commit, push, and publication approval boundaries.

The central invariant is:

> No implementation worktree may be created until every required planning artifact is committed to and reachable from the remote branch used as that worktree's base.

## Roles

The author agent normally performs planning, implementation, and review response. It may retain its integration and implementation worktrees across those phases.

The reviewer agent is separate and may run in a different environment. It receives no conversation memory or filesystem state from the author. It reconstructs the review from pushed commits, issues, pull-request data, and published reviews.

Local state is a convenience within one agent. Remote Git history and tracker data are the contract between agents.

## Commands

| Command | Responsibility | Specialist skill |
| --- | --- | --- |
| `/plan-issue-tree` | Create the integration branch, plan the change, publish planning artifacts, and establish the issue tree | `/grill-with-docs`, `/to-spec`, `/to-ticket` |
| `/implement-ticket` | Validate one ticket's handoff, implement it in an isolated worktree, and open a draft pull request | `/implement` |
| `/review-ticket` | Independently review the implementation linked to a ticket | `/code-review` |
| `/address-review` | Verify findings, implement accepted fixes, commit locally, and prepare a reply | `/implement` |

## Durable state

The workflow does not use a private manifest or hidden marker. State lives in artifacts every participating agent can retrieve:

- The integration branch contains ADRs, research notes, specifications, and other shared planning documents.
- The parent issue records the integration branch, planning baseline commit, and planning artifact paths.
- Native parent, child, and blocker relationships describe the implementation graph.
- Each child ticket contains its acceptance criteria, implementation base, and planning baseline.
- Each implementation pull request links its ticket and targets the ticket's declared base.
- Each published review includes `Reviewed commit: <SHA>` and stable finding identifiers.
- Each response maps those identifiers to fixes, rebuttals, or requested decisions.

A parent handoff uses this visible shape:

```text
Implementation base: integration/<parent>
Planning baseline: <commit SHA>
Planning artifacts:
- docs/adr/<file>
- docs/research/<file>
```

Repository conventions may choose different branch names or paths. The fields and reachability invariant remain the same.

## Branch and worktree model

For a multi-ticket change:

```text
target branch
`-- integration branch and planning worktree
    |-- ticket branch and implementation worktree
    |-- ticket branch and implementation worktree
    `-- ticket branch and implementation worktree
```

The integration branch exists before planning begins. Planning artifacts are created inside its worktree and pushed before implementation starts.

Each child branch starts from the fetched remote integration branch. Child pull requests target the integration branch. A later integration pull request may target the original target branch, but these workflow skills never merge it automatically.

A standalone ticket may branch directly from its declared target branch and does not require an integration branch or planning baseline.

All repository worktrees live under the repository's `.worktrees/` directory:

- The planning worktree is retained by the author through delivery.
- Each ticket has its own implementation worktree, retained for review response.
- The reviewer uses a detached worktree at the exact pull-request head.
- Review fixes are never made in the detached review worktree.

## Phase 1: plan the issue tree

`/plan-issue-tree` creates the integration branch and worktree before invoking the planning skills. This ensures every ADR and research note is created in the branch that will become the common ancestor of the implementation tickets.

The author runs discovery, specification, and ticket decomposition without starting implementation. Before publication, the workflow shows the user:

- planning artifacts;
- the proposed issue tree;
- acceptance criteria and blockers;
- the integration branch;
- intended tracker mutations.

After approval, the workflow commits and pushes the planning artifacts, publishes or updates the issue tree, records the final planning baseline, and verifies the remote state. If issue identifiers are backfilled into planning files, the resulting follow-up commit becomes the baseline.

A ticket is ready only when its base exists remotely, its baseline is reachable from that base, its planning artifacts exist at that baseline, and its blockers are represented in the tracker.

## Phase 2: implement a ticket

`/implement-ticket` starts from the ticket rather than an assumed local checkout. It resolves and verifies the ticket's declared base before creating a branch or worktree.

For child tickets, a missing integration branch, baseline, or planning artifact is a planning failure. The implementation workflow stops rather than repairing it or falling back to the target branch.

Once ready, the workflow delegates the actual implementation to `/implement`. After successful verification it commits, pushes, and opens the draft pull request automatically. The explicit invocation authorizes those publication steps, so there is no second approval gate at the end of implementation.

## Phase 3: review a ticket

`/review-ticket` is designed for an independent reviewer with no author-side context. The ticket is the canonical input; the workflow resolves its linked implementation pull request and asks when none or several are plausible.

The reviewer checks out the exact pushed head in a detached worktree and delegates detailed analysis to `/code-review`. A first review compares the full implementation with its actual pull-request base. A later review uses the commit recorded by the previous review as its fixed point and rechecks every prior finding.

The review is drafted locally and shown to the user. Nothing is posted until approval. Immediately before posting, the workflow verifies that the pull-request head is still the reviewed commit.

## Phase 4: address a review

`/address-review` returns to the author-side implementation branch. It reuses the implementation worktree when possible and can reconstruct it from the remote branch when necessary.

The workflow gathers the selected review and all associated unresolved findings. It verifies each finding rather than treating the review as infallible. Accepted findings become the specification passed to `/implement`; unsupported findings receive evidence-backed rebuttals; product or architecture decisions return to the user.

Verified fixes are committed locally without another approval gate. The workflow then presents the commit and complete reply and waits. Approval authorizes both the normal push and publication of the reply.

The push always happens first. The reply is posted only after the remote pull-request head is verified to equal the local fix commit. A failed or stale push therefore cannot produce a reply claiming unavailable fixes.

## Approval boundaries

| Phase | Automatic | Requires approval |
| --- | --- | --- |
| Plan | Local branch/worktree creation and planning | Commit and push planning artifacts; create or update tracker items |
| Implement | Commit, normal push, and draft pull-request creation after successful verification | Product or architecture decisions; ambiguous or missing handoff state |
| Review | Read-only inspection and draft preparation | Posting the review |
| Address review | Verified fixes and local commit | Pushing the fix commit and posting the reply |

Approval is scoped to the named actions and current remote heads. It never authorizes force-pushing, merging, closing issues, resolving threads, or unrelated changes.

## Failure rules

Stop rather than guessing when:

- the parent, ticket, linked pull request, target review, branch base, or commit scope is ambiguous;
- an integration branch or planning baseline is missing;
- a planning artifact is not present at the recorded baseline;
- a blocker has not landed on the implementation base;
- verification fails;
- the pull-request head changes after inspection;
- a push fails or the remote head does not match the expected commit.

These stops protect the durable handoff. They are not invitations to create a replacement branch, copy an unpublished file between agents, or silently change the ticket's base.
