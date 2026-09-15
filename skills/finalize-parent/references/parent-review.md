# Parent review

Use this when preparing the final review, alongside the [shared loop contract](../../implement-ticket/references/local-review-loop.md) and [delivery report requirements](delivery-report.md).

## Run and inputs

Use workflow kind `parent-finalization`, distinct from a parent implementation run and its budget. Add the parent/child specification snapshot, child and PR inventory with source revisions and delivery evidence, accepted cleanup scope and dispositions, fetched target tip, planning baseline, initial remote integration head, and PR URL to the shared run state. Link the scenario manifest, demonstration evidence, and HTML report version maintained under the delivery report reference.

The integration branch is both the implementation branch and implementation base for publication checks. Confirm it retains the planning baseline and required artifacts. Pin the review base to the merge base of the fetched target and integration candidate under the shared contract; the final diff must include planning documents and all delivered child work. Supply the parent specification, required child acceptance criteria, and accepted cleanup scope with source revisions.

## Independent review

Use specialist-reviewer mode for the combined parent delivery. Spawn the reviewer without author conversation history with the [reviewer instructions](../../implement-ticket/references/review.md), run path, pinned base, candidate, specification, child inventory, scenario manifest and evidence, HTML report version, and prior reports/responses.

The Standards and Spec agents review the entire parent diff, including interactions between children and cleanup. They also check acceptance-criteria coverage, observed results, evidence applicability to the candidate, and the report's demonstration and code explanation under the delivery report reference. Record the inspected HTML version. Child PR approvals do not replace this review. Share applicable execution evidence and request additional runs only under the reference's reuse/invalidation policy. Wait for the complete report and its subagents before authoring further changes.

## Corrections and publication recovery

Finish initial cleanup before review 0. After that review, newly selected cleanup or author code fixes reserve the next correction attempt before authoring, even if the previous review was clean. The shared contract owns cycle counting, dispositions, and resumption; the delivery report reference owns scenario invalidation, report refresh, and which report changes need renewed review.

External branch movement invalidates clearance when it changes the reviewed diff, without itself consuming a correction. Reconcile it without resetting the budget or authorizing extra fixes. After three attempts, defer additional optional cleanup or obtain explicit authorization for a new budget; required defects still prevent completion.

The initial draft uses only already-published history. Keep cleanup and correction commits local until publication conditions pass. Preserve blocked runs and drafts. On partial publication, verify the remote head and resume only missing push, PR-update, association, or check-verification steps under the shared contract.
