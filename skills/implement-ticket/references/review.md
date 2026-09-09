# Independent reviewer

Read [the local loop contract](local-review-loop.md). The supplied run, local commits, and specification snapshot provide the review context; no author conversation history or pull request is required.

1. Read the run's specification, verification evidence, previous findings, and author response. Verify the candidate exists and the pinned implementation base is its ancestor. Surface missing or ambiguous inputs to the coordinator.
2. Create a detached worktree at the candidate under `.worktrees/`, or reuse a clean one already at that SHA. Follow repository test-environment conventions. Leave author code untouched; write only the report and test outputs.
3. Run `/code-review` against the original pinned base on every pass, explicitly using the specification snapshot. Preserve its parallel Standards and Spec analyses. The full ticket diff stays in scope, including rebuttal-only passes at an unchanged SHA. An empty full diff requires a scope decision, not an automatic clean result.
4. Recheck every previous finding, retain its ID, and mark it `open`, `partial`, or `closed` with evidence. Keep actionable findings with a concrete consequence and resolution direction; omit nits, tooling-enforced matters, and speculative smells. Keep the two axes separate. Product or architecture decisions become `needs-human`.
5. Write the report defined by the shared contract. Confirm the author candidate still matches the reviewed SHA, then return the report path and outcome. A changed candidate or incomplete analysis is `blocked`, never clean.

Do not fix code, commit, push, change PR metadata, or post to the tracker. Return the local report to the author/coordinator.
