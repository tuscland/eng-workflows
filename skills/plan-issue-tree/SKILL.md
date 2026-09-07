---
name: plan-issue-tree
description: "Plan a multi-ticket change on an integration branch by orchestrating /grill-with-docs, /to-spec, and /to-ticket, then publish a durable planning handoff. Use before implementation begins."
---

# Plan Issue Tree

Usage:

```text
/plan-issue-tree <parent-issue-or-goal>
```

The upstream planning skills own discovery, specification quality, and ticket decomposition. This skill owns the integration branch, planning worktree, durable handoff, tracker publication, and approval boundary.

The issue tracker and pushed Git history are the shared state. Do not rely on conversation memory, an unpublished local file, or a separate hidden state store.

1. Load the repository instructions and its issue-tracker, branch, worktree, and documentation conventions. Resolve the target branch and either the existing parent issue or the goal from which one will be created.
2. Before planning, create the integration branch and its worktree from the target branch. Put the worktree under the repository's `.worktrees/` directory. If the intended branch already exists, fetch and inspect it rather than creating a competing branch; ask the user when its ownership or state is ambiguous.
3. In the integration worktree, run `/grill-with-docs`. Keep every resulting ADR, research note, and supporting document in the repository paths required by its conventions.
4. Run `/to-spec` to produce the authoritative specification, then run `/to-ticket` through preparation of the implementation tree, acceptance criteria, and dependency relationships. Stop at its publication boundary: do not authorize tracker writes, start implementation, or create child worktrees yet.
5. Present the proposed planning artifacts, issue tree, dependencies, integration branch, and intended tracker mutations. Wait for approval before publishing the plan.
6. Approval authorizes committing only the planning artifacts, pushing the integration branch normally, and creating or updating the named parent and child issues. Publish the planning commit before implementation begins. If issue publication adds links or identifiers to planning files, commit and push that follow-up, then treat the last pushed commit as the planning baseline.
7. Record a visible handoff on the parent issue:

   ```text
   Implementation base: <integration branch>
   Planning baseline: <commit SHA>
   Planning artifacts:
   - <path>
   ```

   Give every child its native parent relationship, blockers, acceptance criteria, implementation base, and planning baseline. Keep shared context on the parent instead of duplicating its full specification into every child.
8. Fetch the remote integration branch and verify that the recorded baseline is reachable from it and contains every declared planning artifact. Re-read the issue tree and verify its parent, blocker, and baseline metadata.
9. Report the published branch, baseline commit, planning artifacts, and tickets that are ready to implement. Keep the integration worktree for later author-side phases.

Never declare a child ready, create its implementation worktree, or spawn implementation while any required planning artifact exists only locally. Never merge the integration branch or close issues in this workflow.
