from datetime import timezone
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo


SCRIPT = Path(__file__).resolve().parents[1] / "skills/list-merged-prs/scripts/list_merged_prs.py"
SPEC = importlib.util.spec_from_file_location("list_merged_prs", SCRIPT)
prs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prs)


def node(number, merged="2026-09-14T10:00:00Z"):
    return {
        "id": f"PR_{number}", "number": number, "title": f"fix: item {number}",
        "url": f"https://github.com/example/project/pull/{number}",
        "mergedAt": merged, "repository": {"nameWithOwner": "example/project"},
    }


def page(nodes, count, cursor=None):
    return {"data": {"search": {
        "issueCount": count, "nodes": nodes,
        "pageInfo": {"hasNextPage": cursor is not None, "endCursor": cursor},
    }}}


class WindowTests(unittest.TestCase):
    def test_paris_midnight_is_previous_utc_date(self):
        start, end = prs.window(zone=ZoneInfo("Europe/Paris"), now=prs.timestamp("2026-09-15T12:00:00Z"))
        self.assertEqual(start, prs.timestamp("2026-09-13T22:00:00Z"))
        self.assertEqual(end, prs.timestamp("2026-09-15T12:00:00Z"))

    def test_midnight_uses_offset_before_dst_change(self):
        zone = ZoneInfo("Europe/Paris")
        start, end = prs.window("2026-03-29", "2026-03-30", zone)
        self.assertEqual(start, prs.timestamp("2026-03-28T23:00:00Z"))
        self.assertEqual((end - start).total_seconds(), 23 * 3600)
        start, end = prs.window("2026-10-25", "2026-10-26", zone)
        self.assertEqual(start, prs.timestamp("2026-10-24T22:00:00Z"))
        self.assertEqual((end - start).total_seconds(), 25 * 3600)

    def test_explicit_offsets_and_invalid_intervals(self):
        start, end = prs.window("2026-09-14T00:00:00+02:00", "2026-09-15T00:00:00+02:00")
        self.assertEqual(start, prs.timestamp("2026-09-13T22:00:00Z"))
        self.assertEqual((end - start).total_seconds(), 86400)
        with self.assertRaises(ValueError):
            prs.window("2026-09-15", "2026-09-14", timezone.utc)
        with self.assertRaises(ValueError):
            prs.timestamp("2026-09-14T12:00:00")

    def test_system_zone_resolves_dst_at_midnight(self):
        import time
        if not hasattr(time, "tzset"):
            self.skipTest("system timezone switching is unavailable")
        try:
            with patch.dict(os.environ, {"TZ": "Europe/Paris"}):
                time.tzset()
                start, _ = prs.window(now=prs.timestamp("2026-03-30T12:00:00Z"))
                self.assertEqual(start, prs.timestamp("2026-03-28T23:00:00Z"))
        finally:
            time.tzset()


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.start = prs.timestamp("2026-09-13T22:00:00Z")
        self.end = prs.timestamp("2026-09-15T10:00:00Z")

    def test_paginates_beyond_one_hundred_and_sorts(self):
        pages = iter([
            page([node(i) for i in range(100, 0, -1)], 101, "next"),
            page([node(101, "2026-09-14T09:00:00Z")], 101),
        ])
        calls = []

        def api(arguments):
            calls.append(arguments)
            return next(pages)

        result = prs.collect("query", self.start, self.end, api)
        self.assertEqual(len(result), 101)
        self.assertEqual(result[0]["number"], 101)
        self.assertIn("cursor=next", calls[1])

    def test_filters_exact_half_open_interval(self):
        records = [node(1, "2026-09-13T21:59:59Z"), node(2, "2026-09-13T22:00:00Z"),
                   node(3, "2026-09-15T09:59:59Z"), node(4, "2026-09-15T10:00:00Z")]
        result = prs.collect("query", self.start, self.end, lambda _: page(records, 4))
        self.assertEqual([record["number"] for record in result], [2, 3])

    def test_empty_results(self):
        self.assertEqual(prs.collect("query", self.start, self.end, lambda _: page([], 0)), [])

    def test_search_cap_count_mismatch_and_api_errors_fail(self):
        for payload in (page([], 1001), page([node(1)], 2), {"errors": [{"message": "denied"}]}):
            with self.subTest(payload=payload), self.assertRaises(RuntimeError):
                prs.collect("query", self.start, self.end, lambda _: payload)

    def test_repeated_cursor_fails_instead_of_looping(self):
        with self.assertRaisesRegex(RuntimeError, "did not advance"):
            prs.collect("query", self.start, self.end, lambda _: page([node(1)], 2, "same"))

    def test_changing_count_and_duplicate_pages_fail(self):
        for pages in ([page([node(1)], 2, "next"), page([node(2)], 3)],
                      [page([node(1)], 2, "next"), page([node(1)], 2)]):
            responses = iter(pages)
            with self.subTest(pages=pages), self.assertRaises(RuntimeError):
                prs.collect("query", self.start, self.end, lambda _: next(responses))

    def test_search_preserves_scope_and_timezone_bounds(self):
        query = prs.search_query("alice", "release/next", ["example/project"], ["example"], self.start, self.end)
        for term in ('author:"alice"', 'base:"release/next"', 'repo:"example/project"',
                     'org:"example"', 'merged:>=2026-09-13T22:00:00Z', 'merged:<2026-09-15T10:00:00Z'):
            self.assertIn(term, query)


class CommandTests(unittest.TestCase):
    def run_helper(self, responses):
        with tempfile.TemporaryDirectory(prefix="pr-query-test-") as directory:
            fake_gh = Path(directory) / "gh"
            fake_gh.write_text(
                f"#!{sys.executable}\n"
                "import json, sys\n"
                f"responses = {responses!r}\n"
                "key = 'user' if sys.argv[1:] == ['api', 'user'] else "
                "('next' if 'cursor=next' in sys.argv else 'first')\n"
                "print(json.dumps(responses[key]))\n"
            )
            fake_gh.chmod(0o755)
            return subprocess.run(
                [sys.executable, "-B", str(SCRIPT), "--timezone", "Europe/Paris",
                 "--since", "2026-09-14", "--until", "2026-09-15"],
                env={**os.environ, "PATH": directory + os.pathsep + os.environ.get("PATH", "")},
                capture_output=True, text=True, check=False,
            )

    def test_cli_resolves_identity_and_reads_all_pages(self):
        result = self.run_helper({"user": {"login": "alice"},
                                  "first": page([node(1)], 2, "next"),
                                  "next": page([node(2)], 2)})
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["author"], "alice")
        self.assertEqual(output["since"], "2026-09-13T22:00:00+00:00")
        self.assertEqual(len(output["pull_requests"]), 2)

    def test_later_page_failure_emits_no_partial_output(self):
        result = self.run_helper({"user": {"login": "alice"},
                                  "first": page([node(1)], 2, "next"),
                                  "next": {"errors": [{"message": "permission denied"}]}})
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("permission denied", result.stderr)


if __name__ == "__main__":
    unittest.main()
