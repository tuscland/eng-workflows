# End-to-end testing and delivery report

End-to-end verification, an observed demonstration, and an HTML code explanation are required parent-finalization deliverables. Prepare them before independent review and refresh them whenever the candidate changes. They apply even if finalization selects no cleanup.

## Exercise the integrated delivery

Derive scenarios from the parent and required child acceptance criteria. Cover the primary user/consumer journeys, interactions between children, and consequential failure or recovery paths affected by the delivery. Record which criteria each scenario exercises and explain coverage gaps. Inspect and reuse the repository's end-to-end harness, fixtures, startup commands, and isolated test environment. Add or adapt scenarios when existing coverage misses the delivered behavior.

Run the actual built candidate through its supported boundary: browser UI, CLI, API/service, or a real consumer of a library. Unit tests, mocked component tests, and child-level checks supplement this execution; they cannot replace it. Use repository test adapters for external dependencies when appropriate and identify their boundaries in the report. Do not present a simulated dependency as a verified live integration.

For browser journeys, prefer the repository's runner. Use `agent-browser` only for end-to-end testing, including capturing demonstrations of those tested journeys. For loopback tests, prefix **every** invocation with `agent-browser --allowed-domains localhost,127.0.0.1`. Do not use it for documentation lookup or general report browsing. For a CLI or service, demonstrate actual commands/requests and their observable outputs rather than inventing a UI.

For every execution, persist the candidate SHA, scenario/criterion IDs, environment and fixture setup, commands, execution time, assertions, expected and observed outcomes, result, and evidence paths. Capture screenshots or recordings for important UI steps; retain terminal or request/response transcripts for non-UI flows. Use test data suitable for inclusion in a shareable report and omit credentials from captured output.

Resolve environment and test failures within the authorized workflow. Mark scenarios honestly as passed, failed, blocked, or skipped. Required scenarios that are failed, blocked, or skipped prevent completion; do not silently waive end-to-end testing when tooling, credentials, or services are unavailable. Continue independent report preparation and preserve a clearly incomplete report while resolving the blocker. After a code fix, execute required scenarios against the new candidate and refresh its demonstration evidence; an earlier SHA's successful run does not verify the final SHA.

## Build the HTML artifact

Create `<local-run>/delivery-report.html` with evidence under `<local-run>/evidence/`, following repository artifact conventions if they supply an equivalent persistent location. Keep the generated report outside tracked source by default so refreshing evidence does not change the candidate being tested. This is a user-facing deliverable, distinct from raw reviewer reports and internal coordination.

Make the HTML readable on its own, with inline styles, semantic headings, a navigable contents list, readable code, and accessible captions. Embed the essential screenshots, transcripts, and diagrams so the report remains useful offline without the live application, a running development server, or CDN assets. A recording may be embedded or supplied alongside the HTML with a relative link; deliver accompanying assets together and keep a useful inline walkthrough. Escape inserted code, logs, and issue text as content. Do not embed live application controls whose behavior was not tested.

Include these sections, scaled to the delivery:

| Section | Required content |
| --- | --- |
| Delivery overview | Parent and child issue/PR links, user-visible outcome, target branch, exact candidate SHA, test environment/time, and current completion/review status. |
| Demonstration | A guided replay of the actual tested workflows: starting state, actions or commands, expected and observed outcomes, and captioned screenshots, recordings, or transcripts tied to scenario IDs. State clearly when a replay is recorded rather than a live demo. |
| End-to-end results | Acceptance-criterion-to-scenario coverage, commands/setup needed to reproduce, assertions, per-scenario results, evidence, external test adapters, and any failures, skips, or gaps. A successful build alone is not an end-to-end result. |
| Code explanation | Explain how the demonstrated behavior works: entry points, control/data flow across the changed modules, relevant state or persistence, error handling, and interactions between child changes. Use paths/symbols, concise annotated snippets, and a rendered diagram when it clarifies the flow; pin remote source links to the candidate SHA. Explain the design decisions and tradeoffs, not just a file list or diff. |
| Cleanup and remaining debt | Executed cleanup with before/after rationale and verification, deferred opportunities ranked by impact/cost, and human decisions. |
| Verification and review | Other required checks, independent review outcome, correction/review counts, remaining limitations, and final PR/CI status when available. Distinguish pending review from verified completion. |

A planned walkthrough or illustrative mockup is not demonstration evidence. Report only behavior actually observed at the stated candidate, and identify limitations rather than inventing missing screenshots, results, or explanations.

## Validate, review, and deliver

Check that the HTML renders, navigation works, essential assets are embedded or included, and code/evidence links resolve as intended. Use the repository's available renderer or a suitable non-`agent-browser` preview tool for report inspection; `agent-browser` remains restricted to application end-to-end testing. Verify that the report's SHA, scenario results, captions, and code explanation agree with the run and current code before handing it to the independent reviewer.

The reviewer inspects the report and its underlying evidence with the exact candidate. A clean review requires the required journeys to pass and the demonstration/code explanation to be supported. Refresh stale evidence and return substantive report corrections through review. After clearance, status-only additions may record the actual final review counts, PR URL, and CI results for that same SHA; changes to demonstrated behavior, technical explanation, or evidence require renewed review. Preserve prior versions referenced by review reports.

Return a clickable absolute path to the HTML file in the final user handoff, along with any accompanying media bundle. If the repository has an authorized artifact channel, publish the report there and verify the downloadable artifact before adding its link to the PR. Otherwise summarize the report and end-to-end results in the PR and deliver the HTML locally; never present a local filesystem path as a remotely accessible PR link or introduce public hosting solely for this report. Keep the report summary/link before closing directives and the final local review record.

Finalization is incomplete until passing evidence, an accurate reviewed HTML report, and accessible report files exist for the final candidate. A blocked run still retains its partial report with an explicit incomplete status.
