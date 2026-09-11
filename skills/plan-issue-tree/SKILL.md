---
name: plan-issue-tree
description: "Plan a tracked change on an integration branch by running /grill-with-docs, /to-spec, and /to-tickets in sequence, then publish its implementation handoff. Use before implementation begins."
---

# Plan Issue Tree

Usage:

```text
/plan-issue-tree <parent-issue-or-goal>
```

The upstream skills own discovery, specification quality, ticket decomposition, and their user checkpoints. This wrapper owns the integration branch, worktree, publication of supporting documents, and durable handoff.

## Shared state and authorization

- The configured issue tracker owns the authoritative specification, tickets, acceptance criteria, dependencies, and implementation handoff. Local drafts are temporary working material, not repository deliverables.
- Only repository documents created or updated by `/grill-with-docs` are eligible for a planning commit: typically ADRs, research notes, and glossary changes. Use the repository's document conventions. The wrapper creates no specification copy, planning runbook, or handoff file in Git.
- Explicit invocation authorizes committing and normally pushing those documents and running the upstream skills through tracker publication. Preserve their interview, test-seam, and ticket-breakdown checkpoints; honor answers and approvals already supplied. There is no additional wrapper-level publication approval.

Pause for an unanswered decision, an upstream checkpoint, required tool authorization, or an actual blocker. Otherwise continue to the next step automatically; reporting discovery findings or preparing local drafts does not complete this workflow.

## Workflow

1. Load the repository instructions and its issue-tracker, branch, worktree, and documentation conventions. Resolve the target branch and either the existing parent issue or the goal from which one will be created.
2. Before planning, create the integration branch and its worktree from the target branch. Put the worktree under the repository's `.worktrees/` directory. If the intended branch already exists, fetch and inspect it rather than creating a competing branch; ask the user when its ownership or state is ambiguous.
3. In the integration worktree, run `/grill-with-docs` to resolve the design. Treat decisions already settled by the user or current issue as inputs. Once its checkpoints are satisfied, proceed to specification rather than ending with a discovery report or asking whether to continue.
4. Validate, commit, and normally push only the documents produced by `/grill-with-docs`. If it produced no document changes, push the integration branch at its existing tip; no empty commit or artificial artifact is needed. The pushed tip is the planning baseline. Establish this before either upstream skill publishes an issue as ready.
5. Run `/to-spec` through publication to the configured tracker. Synthesize the settled design into the authoritative specification, updating the existing issue when one was supplied. Re-read concurrent issue edits before writing. An existing detailed issue is input to this step, not a reason to skip it or create a parallel specification in Git.
6. Then run `/to-tickets` through its breakdown checkpoint and tracker publication, including acceptance criteria and native parent/blocker relationships. Let it determine the necessary granularity; when one implementation ticket suffices, retain that ticket instead of manufacturing a child tree. In that case, designate the integration branch and its existing worktree as the ticket's implementation branch and worktree; do not create a nested ticket branch. Continue when its checkpoint is satisfied, without another publication question.
7. If tracker publication requires links or identifiers in the documents from step 4, commit and normally push only those document updates and use the last pushed commit as the baseline. Record a visible handoff on the parent issue:

   ```text
   Implementation base: <integration branch>
   Implementation branch: <integration branch for a single ticket; ticket branch for each child>
   Pull request base: <target branch for a single ticket; integration branch for each child>
   Closing issue: <canonical owner/repository#number for this implementation ticket>
   Planning baseline: <commit SHA>
   Planning artifacts: <paths of documents from grill-with-docs, or none>
   ```

   Give every child its native parent relationship, blockers, acceptance criteria, implementation base, implementation branch, pull-request base, canonical closing issue, and planning baseline. Choose ticket branch names using repository conventions, but leave their creation to `implement-ticket`. Keep shared context on the parent instead of duplicating its full specification into every child. For a single implementation issue, put the handoff on that issue and use the integration branch as its implementation branch.
8. Fetch the remote integration branch and verify that the recorded baseline is reachable from it and contains every declared planning artifact. Re-read the issue tree and verify its parent, blocker, and baseline metadata.
9. Report the published branch, baseline commit, planning artifacts, and tickets that are ready to implement. Keep the integration worktree for later author-side phases.

Never declare a child ready, create its implementation worktree, or spawn implementation while any required planning artifact exists only locally. Never merge the integration branch or close issues in this workflow.
