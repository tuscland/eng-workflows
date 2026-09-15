# Engineering Workflows

Take a feature from a tracked idea to reviewed draft pull requests and a clear demonstration of what it does. These agent skills handle planning, implementation, cleanup, and verification, while you make product decisions and choose when to merge.

The final HTML report explains the user and developer experience first, shows the feature in action, then walks through the code and validation evidence. You can understand the outcome before digging into implementation details.

## Deliver a feature

With the skills available to your agent, start in the repository you want to change:

1. **[Plan](skills/plan-issue-tree/SKILL.md)** — `$plan-issue-tree <parent-issue-or-goal>` turns the goal into a specification, implementation tickets, and a shared integration branch.
2. **[Implement](skills/implement-ticket/SKILL.md)** — `$implement-ticket <ticket>` sets the ticket's project status to In progress, implements and reviews the change, and opens a linked draft PR with cleanup recommendations. Repeat for each child ticket.
3. **[Finalize](skills/finalize-parent/SKILL.md)** — Once required child changes have landed on the integration branch, run `$finalize-parent <parent-issue>`. It opens the integration draft PR, executes worthwhile cleanup, verifies the combined feature end to end, and produces the HTML report with a final independent review.

For a standalone ticket, start with `implement-ticket`. Parent finalization is for the combined delivery after child implementation.

End-to-end results and demonstrations are reused when the relevant code and test inputs are unchanged. Isolated fixes rerun affected scenarios; broad or uncertain changes receive wider testing. Report edits do not trigger another application replay.

## Report progress and maintain the backlog

| Need | Skill |
| --- | --- |
| A copy-ready daily update of your PRs merged into `main` since yesterday | [`list-merged-prs`](skills/list-merged-prs/SKILL.md) |
| A weekly account of delivered value, architecture changes, and risks from merged PRs | [`eng-review-report`](skills/eng-review-report/SKILL.md) |
| Reconcile issues with current code while preserving product intent and open specification questions | [`issue-tree-audit`](skills/issue-tree-audit/SKILL.md) |

## How it works

The author agent implements and fixes findings; a separate reviewer checks the code against the specification. Bounded tickets use one independent reviewer covering Standards and Spec; complex changes and parent finalization use separate specialists coordinated by that reviewer. Routine implementation choices follow the specification and repository conventions; unresolved consequential decisions return to you. New implementation and cleanup commits are pushed after a clean review and passing checks. Each run allows up to three correction cycles and preserves local state for resumption. Pull requests remain drafts for your merge decision.

The delivery skills build on Matt Pocock's skills, which must also be available: planning uses `grill-with-docs`, `to-spec`, and `to-tickets`; implementation and finalization use `implement` and `code-review`. Planning checks its prerequisites before creating branches or worktrees. Independent review requires an agent environment with subagent support; specialist mode needs capacity for the author, reviewer, and two specialists.

See [Tracked Delivery Workflow](WORKFLOW.md) for branch and worktree conventions, review state, publication conditions, and report requirements.

The daily PR skill includes a Python 3.9+ retrieval helper using the authenticated `gh` CLI. Run its offline pagination, timezone, and command tests with `python3 -B -m unittest discover -s tests -v`.
