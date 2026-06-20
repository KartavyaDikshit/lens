#!/usr/bin/env python3
"""Attach Lens-enabling Pulse issues to Knitweb Project 2.

This script is intentionally dependency-free. It shells out only to `gh auth
token` so it can reuse the user's GitHub CLI login, then talks to GitHub
GraphQL with urllib from the standard library.

Required token scopes:
  - read:project
  - project

Refresh scopes with:
  gh auth refresh -h github.com -s read:project -s project
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

API_URL = "https://api.github.com/graphql"

DEFAULT_ISSUES = (152, 153, 154, 155, 156, 157, 158)


@dataclass(frozen=True)
class ProjectInfo:
    project_id: str
    title: str
    url: str
    status_field_id: str | None = None
    backlog_option_id: str | None = None


def gh_token() -> str:
    result = subprocess.run(
        ["gh", "auth", "token"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    token = result.stdout.strip()
    if not token:
        raise RuntimeError("gh auth token returned an empty token")
    return token


def graphql(token: str, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            decoded = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub GraphQL HTTP {exc.code}: {body}") from exc
    if decoded.get("errors"):
        messages = "; ".join(error.get("message", str(error)) for error in decoded["errors"])
        raise RuntimeError(messages)
    return decoded["data"]


def get_project(token: str, *, org: str, number: int) -> ProjectInfo:
    data = graphql(
        token,
        """
        query($org: String!, $number: Int!) {
          organization(login: $org) {
            projectV2(number: $number) {
              id
              title
              url
              fields(first: 50) {
                nodes {
                  ... on ProjectV2Field {
                    id
                    name
                    dataType
                  }
                  ... on ProjectV2SingleSelectField {
                    id
                    name
                    options {
                      id
                      name
                    }
                  }
                }
              }
            }
          }
        }
        """,
        {"org": org, "number": number},
    )
    project = data["organization"]["projectV2"]
    status_field_id = None
    backlog_option_id = None
    for field in project["fields"]["nodes"]:
        if not field:
            continue
        if field.get("name", "").casefold() == "status":
            status_field_id = field["id"]
            for option in field.get("options", []):
                if option["name"].casefold() in {"backlog", "todo", "to do"}:
                    backlog_option_id = option["id"]
                    break
    return ProjectInfo(
        project_id=project["id"],
        title=project["title"],
        url=project["url"],
        status_field_id=status_field_id,
        backlog_option_id=backlog_option_id,
    )


def get_issue_id(token: str, *, owner: str, repo: str, number: int) -> tuple[str, str, str]:
    data = graphql(
        token,
        """
        query($owner: String!, $repo: String!, $number: Int!) {
          repository(owner: $owner, name: $repo) {
            issue(number: $number) {
              id
              title
              url
            }
          }
        }
        """,
        {"owner": owner, "repo": repo, "number": number},
    )
    issue = data["repository"]["issue"]
    return issue["id"], issue["title"], issue["url"]


def add_item(token: str, *, project_id: str, content_id: str) -> str:
    data = graphql(
        token,
        """
        mutation($projectId: ID!, $contentId: ID!) {
          addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
            item {
              id
            }
          }
        }
        """,
        {"projectId": project_id, "contentId": content_id},
    )
    return data["addProjectV2ItemById"]["item"]["id"]


def set_status(
    token: str,
    *,
    project_id: str,
    item_id: str,
    field_id: str,
    option_id: str,
) -> None:
    graphql(
        token,
        """
        mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
          updateProjectV2ItemFieldValue(input: {
            projectId: $projectId,
            itemId: $itemId,
            fieldId: $fieldId,
            value: { singleSelectOptionId: $optionId }
          }) {
            projectV2Item {
              id
            }
          }
        }
        """,
        {
            "projectId": project_id,
            "itemId": item_id,
            "fieldId": field_id,
            "optionId": option_id,
        },
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--org", default="Knitweb")
    parser.add_argument("--project", type=int, default=2)
    parser.add_argument("--owner", default="Knitweb")
    parser.add_argument("--repo", default="pulse")
    parser.add_argument("--issue", type=int, action="append", dest="issues")
    parser.add_argument("--set-backlog-status", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    issue_numbers = tuple(args.issues or DEFAULT_ISSUES)
    token = gh_token()
    project = get_project(token, org=args.org, number=args.project)
    print(f"Project: {project.title} ({project.url})")
    for number in issue_numbers:
        content_id, title, url = get_issue_id(token, owner=args.owner, repo=args.repo, number=number)
        item_id = add_item(token, project_id=project.project_id, content_id=content_id)
        if args.set_backlog_status and project.status_field_id and project.backlog_option_id:
            set_status(
                token,
                project_id=project.project_id,
                item_id=item_id,
                field_id=project.status_field_id,
                option_id=project.backlog_option_id,
            )
        print(f"added #{number}: {title} -> {url}")
    if args.set_backlog_status and not (project.status_field_id and project.backlog_option_id):
        print("status field or Backlog option not found; items were added without status")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

