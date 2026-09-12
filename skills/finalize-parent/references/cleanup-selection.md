# Cleanup selection

Use this after reading the parent specification and every child PR. Read current PR descriptions, cleanup sections, review summaries, and relevant discussions; retain source URLs and revisions in the local run. A missing cleanup section on an older PR is not evidence that no cleanup is possible: inspect its diff and the resulting integration code. Local child reports can supplement this evidence when available, but are not required inputs.

Build one deduplicated table:

| Opportunity and sources | Current code evidence | Expected impact | Cost and risk | Disposition and rationale |
| --- | --- | --- | --- | --- |
| Concrete change with child PR links | Paths/symbols and observed problem | Benefit and who or what it affects | Small/medium/large effort, scope, confidence, compatibility risk | Execute, needs guidance, defer, already resolved, or unsupported |

Estimate impact concretely: remove a failure mode, eliminate duplicate logic that can diverge, reduce maintenance, or remove measurable runtime/build cost. Cost includes implementation, verification, migration, and coordination. Prefer high-impact, low-cost changes with strong evidence. Explain dependencies or risk that change the ordering; do not manufacture numeric scores or a cleanup quota.

Recheck every proposal against the current combined code. Later child work may have removed the debt, introduced a caller, or made two proposals the same change. For dead code, inspect callers, exports, public interfaces, registration/configuration, dynamic loading, and relevant tests before removal. An unreferenced symbol in a text search is only a candidate. Inspect interactions between children for duplicate helpers, temporary compatibility paths, and obsolete scaffolding exposed by integration, keeping the search within the parent's delivery scope.

Execute worthwhile, bounded, behavior-preserving cleanup whose intent and verification are clear. Group dependent changes into a coherent scope and record expected behavior/checks before implementation. Do not interpret a child PR suggestion as authorization for broad refactoring, dependency migrations, public API removal, data deletion, or changed product behavior.

When a promising proposal requires a consequential choice or uncertain cost, present the concrete change, source evidence, expected benefit, effort/risk, alternatives, and recommendation to the user. Request only the unresolved decision; previously accepted scope is already authorized. Continue independent selected work, but do not execute the dependent change or treat silence as approval. If that decision is required for completion, keep the run pending; optional work may be explicitly deferred with its rationale.

Record what was executed, declined, deferred, already resolved, or unsupported in the final integration PR. Preserve unresolved opportunities with enough source and code evidence to act on later; do not file new tickets automatically. Required correctness or specification defects belong in the final review/fix loop and cannot be relabeled optional debt to obtain a clean result.
