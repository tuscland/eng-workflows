# Engineering Workflows

Reusable agent skills for software delivery and team visibility.

## Agentic coding workflow

These skills form an orchestration layer on top of Matt Pocock's planning, implementation, and code-review skills. They preserve that specialist workflow while adding durable planning handoffs, integration branches, isolated worktrees, cross-agent review state, and explicit publication boundaries.

| Skill | Purpose | Builds on |
| --- | --- | --- |
| [`plan-issue-tree`](skills/plan-issue-tree/SKILL.md) | Turn a substantial change into a published specification and dependency-aware ticket tree on an integration branch. | `grill-with-docs`, `to-spec`, `to-ticket` |
| [`implement-ticket`](skills/implement-ticket/SKILL.md) | Validate a ticket's planning handoff, implement it in an isolated worktree, and open its draft pull request. | `implement` |
| [`review-ticket`](skills/review-ticket/SKILL.md) | Independently review the implementation linked to a ticket using only durable remote state. | `code-review` |
| [`address-review`](skills/address-review/SKILL.md) | Verify review findings, implement accepted fixes, commit locally, and prepare the push and reply for approval. | `implement` |

The author agent normally performs planning, implementation, and review response. Review runs in an independent agent and may use a different model or harness. Issues, pushed commits, pull-request data, and published reviews are therefore the handoff contract between phases.

See [Tracked Delivery Workflow](WORKFLOW.md) for the branch model, durable-state contract, approval boundaries, and complete lifecycle.

## Team reporting

| Skill | Purpose |
| --- | --- |
| [`eng-review-report`](skills/eng-review-report/SKILL.md) | Prepare a weekly engineering-review report focused on pull requests merged directly into `main`, with per-PR summaries of product impact, architecture changes, implementation challenges, and operational risk. |
| [`list-merged-prs`](skills/list-merged-prs/SKILL.md) | Produce a chronological, categorized list of pull requests merged into `main` since yesterday for standups or Slack updates. |

## Project management

| Skill | Purpose |
| --- | --- |
| [`issue-tree-audit`](skills/issue-tree-audit/SKILL.md) | Reconcile an issue tree with the current codebase and propose phased cleanup for completed, obsolete, duplicate, overlapping, or mis-prioritized work. |
