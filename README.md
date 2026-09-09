# Engineering Workflows

Reusable agent skills for software delivery and team visibility.

## Agentic coding workflow

These skills form an orchestration layer on top of Matt Pocock's planning, implementation, and code-review skills. They add durable planning handoffs, isolated worktrees, and a local author/reviewer loop that publishes only the finished work.

| Skill | Purpose | Builds on |
| --- | --- | --- |
| [`plan-issue-tree`](skills/plan-issue-tree/SKILL.md) | Publish discovery documents on an integration branch, then the specification, tickets, and handoff in the tracker. | `grill-with-docs`, `to-spec`, `to-tickets` |
| [`implement-ticket`](skills/implement-ticket/SKILL.md) | Implement, coordinate up to three local correction/review cycles, then push the clean result and open its draft pull request. | `implement`, `code-review` |

The author agent coordinates implementation and corrections. A separate reviewer uses the same local repository and reports through local files. Issues and pushed documents supply planning context; GitHub is not used for intermediate review conversations. A clean review and passing checks authorize final publication.

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
