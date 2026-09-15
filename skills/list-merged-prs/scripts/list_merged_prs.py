#!/usr/bin/env python3
"""Retrieve a complete merged-PR window through the authenticated gh CLI."""

import argparse
from datetime import date, datetime, time, timedelta, timezone
import json
import subprocess
import sys
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


QUERY = """
query($searchQuery: String!, $cursor: String) {
  search(query: $searchQuery, type: ISSUE, first: 100, after: $cursor) {
    issueCount
    pageInfo { hasNextPage endCursor }
    nodes {
      ... on PullRequest {
        id number title url mergedAt
        repository { nameWithOwner }
      }
    }
  }
}
"""


def gh_json(arguments):
    result = subprocess.run(
        ["gh", *arguments], capture_output=True, text=True, check=False
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "gh request failed")
    payload = json.loads(result.stdout)
    if isinstance(payload, dict) and payload.get("errors"):
        raise RuntimeError(f"GitHub API errors: {payload['errors']}")
    return payload


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include a UTC offset or Z")
    return parsed.astimezone(timezone.utc)


def boundary(value, zone):
    if len(value) == 10:
        # With no named zone, converting a naive midnight uses the system's
        # offset on that date, including daylight-saving transitions.
        return datetime.combine(date.fromisoformat(value), time.min, zone).astimezone(
            timezone.utc
        )
    return timestamp(value)


def window(since=None, until=None, zone=None, now=None):
    now = now or datetime.now(timezone.utc)
    start = boundary(since, zone) if since else boundary(
        (now.astimezone(zone).date() - timedelta(days=1)).isoformat(), zone
    )
    end = boundary(until, zone) if until else now.astimezone(timezone.utc)
    if start >= end:
        raise ValueError("--since must be earlier than --until")
    return start, end


def qualifier(name, value):
    # GitHub search syntax needs quoting independently of shell safety.
    return f"{name}:{json.dumps(value)}"


def search_query(author, base, repositories, organizations, start, end):
    # Search at second precision with outward-rounded bounds, then filter the
    # actual mergedAt instants against the exact half-open interval locally.
    lower = start.replace(microsecond=0)
    upper = end.replace(microsecond=0)
    if end.microsecond:
        upper += timedelta(seconds=1)
    return " ".join([
        "is:pr", "is:merged", qualifier("author", author), qualifier("base", base),
        f"merged:>={lower.isoformat().replace('+00:00', 'Z')}",
        f"merged:<{upper.isoformat().replace('+00:00', 'Z')}",
        *[qualifier("repo", repo) for repo in repositories],
        *[qualifier("org", org) for org in organizations],
        "sort:created-asc",
    ])


def collect(query, start, end, api=gh_json):
    cursor = None
    cursors = set()
    records = {}
    expected_count = None
    while True:
        arguments = ["api", "graphql", "-f", f"query={QUERY}", "-f", f"searchQuery={query}"]
        if cursor is not None:
            arguments.extend(["-f", f"cursor={cursor}"])
        payload = api(arguments)
        if payload.get("errors"):
            raise RuntimeError(f"GitHub API errors: {payload['errors']}")
        page = payload["data"]["search"]
        count = page["issueCount"]
        if count > 1000:
            raise RuntimeError(
                "GitHub search exceeds its 1,000-result cap; split the time window "
                "or repository scope and combine the successful results."
            )
        if expected_count is not None and count != expected_count:
            raise RuntimeError("Search results changed during pagination; rerun the query.")
        expected_count = count
        for node in page["nodes"]:
            if not node or not node.get("mergedAt"):
                raise RuntimeError("GitHub returned an incomplete merged pull request.")
            # Validate output fields before retaining a record or emitting anything.
            for key in ("id", "number", "title", "url"):
                if key not in node:
                    raise RuntimeError(f"GitHub omitted pull request field {key}.")
            node["repository"]["nameWithOwner"]
            timestamp(node["mergedAt"])
            records[node["id"]] = node
        info = page["pageInfo"]
        if not info["hasNextPage"]:
            break
        cursor = info["endCursor"]
        if not cursor or cursor in cursors:
            raise RuntimeError("GitHub pagination did not advance; results are incomplete.")
        cursors.add(cursor)
    if len(records) != expected_count:
        raise RuntimeError("GitHub search count and retrieved results differ; results are incomplete.")
    matching = [node for node in records.values() if start <= timestamp(node["mergedAt"]) < end]
    return sorted(matching, key=lambda node: (timestamp(node["mergedAt"]), node["url"]))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author", help="GitHub login; defaults to the authenticated user")
    parser.add_argument("--base", default="main")
    parser.add_argument("--repo", action="append", default=[], help="owner/repository; repeatable")
    parser.add_argument("--org", action="append", default=[], help="organization; repeatable")
    parser.add_argument("--timezone", help="IANA zone such as Europe/Paris; defaults to system local time")
    parser.add_argument("--since", help="inclusive date at local midnight, or timestamp with offset")
    parser.add_argument("--until", help="exclusive date at local midnight, or timestamp with offset; default now")
    args = parser.parse_args(argv)
    try:
        zone = ZoneInfo(args.timezone) if args.timezone else None
        start, end = window(args.since, args.until, zone)
        author = args.author or gh_json(["api", "user"])["login"]
        query = search_query(author, args.base, args.repo, args.org, start, end)
        records = collect(query, start, end)
        json.dump({
            "author": author, "base": args.base,
            "since": start.isoformat(), "until": end.isoformat(),
            "pull_requests": records,
        }, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, ZoneInfoNotFoundError) as error:
        print(f"Unable to retrieve a complete PR list: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
