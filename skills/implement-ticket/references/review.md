# Independent reviewer

Read [the local loop contract](local-review-loop.md). The supplied run, local commits, and specification snapshot provide the review context; no author conversation history or pull request is required.

1. Read the run's specification, review mode, verification evidence, previous findings, and author response. Verify the candidate exists and the pinned review base is its ancestor, with provenance appropriate to the workflow under **Review base and planning baseline** in the shared contract. Surface missing or ambiguous inputs to the coordinator.
2. Create a detached worktree at the candidate under `.worktrees/`, or reuse a clean one already at that SHA. Follow repository test-environment conventions. Leave author code untouched; write only the report and test outputs.
3. Apply `/code-review` against the pinned base on every pass, explicitly supplying the specification snapshot and the selected composition from the shared contract. In single-reviewer mode, perform both Standards and Spec analyses yourself; in specialist mode, delegate those analyses separately and reconcile their reports. Escalate the mode if the scope requires it. The full ticket diff stays in scope, including rebuttal-only passes at an unchanged SHA. An empty full diff requires a scope decision, not an automatic clean result.
4. Recheck every previous finding, retain its ID, and mark it `open`, `partial`, or `closed` with evidence. Keep actionable findings with a concrete consequence and resolution direction; omit nits, tooling-enforced matters, and speculative smells. Keep the two axes separate. Apply **Decisions requiring human input** in the shared contract; routine implementation choices do not require escalation.
5. Write the report defined by the shared contract. Confirm the author candidate still matches the reviewed SHA, then return the report path and outcome. A changed candidate or incomplete analysis is `blocked`, never clean.

Do not fix code, commit, push, change PR metadata, or post to the tracker. Return the local report to the author/coordinator.
