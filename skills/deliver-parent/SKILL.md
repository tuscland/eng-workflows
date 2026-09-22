---
name: deliver-parent
description: "Implement every ticket in a fully planned parent issue, assemble reviewed ticket branches locally into an integration branch, and defer signing and GitHub publication until the user explicitly requests the final handoff."
---

# Deliver Parent

```text
/deliver-parent <parent-issue-or-local-run>
```

This skill coordinates `$issue-tree-audit`, `$implement-ticket`, and `$finalize-parent`; read all three skills and their routed references before acting. This workflow explicitly authorizes their review subagents.

The delivery phase is local-only. Invocation authorizes local worktrees, one local branch per ticket, unsigned commits, local merges into the declared integration branch, verification, review, cleanup, end-to-end evidence, and the HTML delivery report. It does not authorize SSH, Git remote operations, commit signing, GitHub writes, pull-request creation, or publication. These local-only rules replace the delegated skills' tracker setup, publication, pull-request, remote-check, and merge steps for this invocation.

## Local-only contract

- Pass `publication_mode=deferred-local` and this contract to every delegated skill and agent. Keep all authoring, review, correction, and finalization state usable without a remote branch or pull request.
- Use the planning handoff, existing local objects and refs, and read-only GitHub API calls over HTTPS. Run no `ssh`, `git fetch`, `git pull`, `git push`, `git clone`, `git ls-remote`, or other command that contacts a Git remote.
- Create every ticket on its declared local ticket branch from the current local integration tip. Even a single-ticket parent uses a distinct ticket branch.
- Create every commit with `git -c commit.gpgSign=false commit`. Create local integration merges with `git -c commit.gpgSign=false merge --no-ff --no-gpg-sign <ticket-branch>`. Pass the same per-command signing override to `/implement` and correction agents. Do not change global or repository signing configuration.
- Verify every commit created by the workflow has no `gpgsig` header. Record its branch, SHA, tree, parents, message, review result, and checks in the local run.
- Make no tracker, project, issue, branch-protection, pull-request, or other provider mutation. Child completion means a clean local review and successful local integration, not a published PR.

## Workflow

1. **Audit the available baseline.** Resolve the canonical parent repository, declared target and integration branches, planning baseline, parent issue tree, and current working-tree status without contacting a Git remote. Run `$issue-tree-audit` in read-only mode over the full parent and ticket tree. Compare the specification, acceptance criteria, ticket boundaries, blocker graph, named paths and APIs, implementation assumptions, and tests with the available code, documentation, schemas, and local history. Record that remote-tip freshness is deferred to publication.
2. **Decide whether the plan is locally executable.** Record an evidence-backed result for every ticket. Proceed only when the parent outcome and every required ticket remain correct, complete, nonduplicative, and implementable against the local planning baseline. Harmless code movement may be reconciled when behavior, acceptance criteria, boundaries, ordering, and architecture remain intact. Scope, behavior, decomposition, dependency, or architecture drift returns to specification work.
3. **Resolve the handoff.** Require a reachable local planning baseline, an integration branch distinct from the default and original target branches, and a distinct declared branch for every required ticket. Read the complete native child tree, blockers, acceptance criteria, and planning artifacts. Surface missing or conflicting metadata instead of inventing it.
4. **Create or resume local delivery state.** Keep the orchestration run under `<git-common-dir>/parent-deliveries/<parent-key>/<run-id>/run.md`. Record `publication_mode=deferred-local`, the local baseline and source revisions, issue identities, ticket graph, worktrees, branch tips, child runs, reviewed SHAs, unsigned-commit checks, local merge evidence, finalization run, and phase. Reuse existing worktrees and runs. On resume, verify recorded local inputs and continue the incomplete step without repeating commits or merges.
5. **Implement the next ticket.** Process required tickets in deterministic topological order. A ticket is ready when every required blocker is reachable from the local integration tip or explicitly excluded by the specification. Invoke `$implement-ticket` with the ticket, parent handoff, and local-only contract. Let it complete its implementation and review/fix loop on the declared ticket branch, stopping before tracker setup or publication. A ticket clears only when its exact local head has a clean independent review, passing candidate checks, no unresolved finding or decision, and no signature.
6. **Gate and merge locally.** Immediately before integration, require the ticket branch head to equal the reviewed candidate, the integration tip to equal its recorded expected base, the worktree to be clean, and the ticket diff to contain no unrelated commits. Merge the ticket branch into the local integration branch with a distinct unsigned merge commit that preserves the reviewed commits. Verify the reviewed ticket head and all blockers are ancestors of the new integration tip, then record the merge SHA and unsigned-commit evidence.
7. **Continue through the full tree.** Re-read the issue tree before selecting each ticket. Skip a ticket only when equivalent delivery is already reachable from the local integration branch with recorded review and merge evidence. Continue independent ready tickets when another ticket is blocked and their accepted bases and specifications remain valid.
8. **Finalize locally.** After every required ticket is reachable from the local integration branch, invoke `$finalize-parent` with the local-only contract. Skip opening or updating a draft PR and all provider checks. Perform cleanup selection, integrated verification, end-to-end evidence, the HTML delivery report, and the complete independent parent review/fix loop locally. Create finalization and correction commits unsigned and keep the final reviewed integration head local.
9. **Verify the local handoff.** Require a clean integration worktree; every required ticket head and merge commit reachable from the integration tip; no workflow-created commit containing a `gpgsig` header; passing required local checks and end-to-end scenarios; an accurate reviewed HTML report; and complete child and parent review records. Report the baseline limitation, delivered and excluded tickets, ticket branches and reviewed SHAs, local merge commits, integration head, checks, report path, review counts, decisions, and local run paths. Stop before signing or publication.

## Deferred publication

Publication is a separate continuation that requires an explicit user request after the local handoff. On that request:

1. Refresh the target and reconcile remote drift. Any semantic change to the reviewed diff returns through the affected verification and review loop.
2. Rewrite the unpublished delivery history with signed commits while preserving each commit's tree, message, author metadata, and merge topology. Record the old-to-new SHA map and verify final tree and diff equivalence. Renew evidence only where the rewrite or reconciled drift changes a reviewed input beyond commit identity.
3. Push the signed integration branch and create or update one draft integration pull request to the declared original target. Do not create child pull requests. Include the parent and every satisfied child association, delivery summary, validation evidence, HTML report, and local review record.
4. Verify the remote head, target, draft state, required checks, and native issue associations. Leave the integration pull request open and draft for the user's review.

## Stop conditions

Preserve state and stop when the issue tree is incomplete, the local planning baseline or branch handoff is missing, no ticket is ready because of an unresolved dependency, a child workflow reports `needs-human`, `blocked`, or `limit-reached`, a local merge gate fails, or finalization is incomplete.

Never close issues directly, merge or mark ready the final integration pull request, retarget it, or merge anything into the default branch. The user owns publication authorization and the final merge.
