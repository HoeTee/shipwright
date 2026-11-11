#!/usr/bin/env python3
"""Keep critical and high rows from an ecosystem audit JSON feed.

Read-only filter. It does not run audits, install packages, or emit
demonstration inputs. Unknown severity is listed, not dropped, so a feed
that omits severity cannot hide an advisory.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

KEEP = {"critical", "high"}
DROP = {"moderate", "medium", "low", "info", "informational", "none"}


def _severity(value: object) -> str:
    text = str(value or "").strip().lower()
    if text in KEEP or text in DROP:
        return text
    return "unknown"


def _row(advisory_id: str, package: str, severity: str, title: str) -> dict[str, str]:
    return {
        "id": advisory_id or "unknown",
        "package": package or "unknown",
        "severity": _severity(severity),
        "title": " ".join(title.split()) if title else "",
    }


def from_npm(data: dict[str, Any]) -> list[dict[str, str]]:
    vulns = data.get("vulnerabilities")
    if not isinstance(vulns, dict):
        return []
    rows: list[dict[str, str]] = []
    for name, body in vulns.items():
        if not isinstance(body, dict):
            continue
        via = body.get("via")
        title = ""
        advisory_id = ""
        if isinstance(via, list):
            for item in via:
                if isinstance(item, dict):
                    title = str(item.get("title") or item.get("name") or title)
                    advisory_id = str(item.get("source") or item.get("url") or advisory_id)
                    break
                if isinstance(item, str) and not title:
                    title = item
        rows.append(_row(advisory_id, str(body.get("name") or name), str(body.get("severity") or ""), title))
    return rows


def from_pip(data: dict[str, Any]) -> list[dict[str, str]]:
    deps = data.get("dependencies")
    if not isinstance(deps, list):
        return []
    rows: list[dict[str, str]] = []
    for dep in deps:
        if not isinstance(dep, dict):
            continue
        package = str(dep.get("name") or "")
        for vuln in dep.get("vulns") or []:
            if not isinstance(vuln, dict):
                continue
            rows.append(
                _row(
                    str(vuln.get("id") or ""),
                    package,
                    str(vuln.get("severity") or ""),
                    str(vuln.get("description") or vuln.get("id") or ""),
                )
            )
    return rows


def from_cargo(data: dict[str, Any]) -> list[dict[str, str]]:
    report = data.get("vulnerabilities")
    items: list[Any] = []
    if isinstance(report, dict) and isinstance(report.get("list"), list):
        items = report["list"]
    elif isinstance(data.get("advisories"), list):
        items = data["advisories"]
    rows: list[dict[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        advisory = item.get("advisory") if isinstance(item.get("advisory"), dict) else item
        package = item.get("package")
        package_name = ""
        if isinstance(package, dict):
            package_name = str(package.get("name") or "")
        elif isinstance(package, str):
            package_name = package
        rows.append(
            _row(
                str(advisory.get("id") or item.get("id") or ""),
                package_name,
                str(advisory.get("severity") or item.get("severity") or ""),
                str(advisory.get("title") or item.get("title") or ""),
            )
        )
    return rows


def select(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    kept = [row for row in rows if row["severity"] in KEEP or row["severity"] == "unknown"]
    dropped = [row for row in rows if row["severity"] in DROP]
    return kept, dropped


def parse_feed(data: Any, ecosystem: str) -> list[dict[str, str]]:
    if not isinstance(data, dict):
        raise SystemExit("audit JSON must be an object")
    if ecosystem == "npm":
        return from_npm(data)
    if ecosystem == "pip":
        return from_pip(data)
    if ecosystem == "cargo":
        return from_cargo(data)
    if "vulnerabilities" in data and isinstance(data["vulnerabilities"], dict):
        return from_npm(data)
    if "dependencies" in data:
        return from_pip(data)
    return from_cargo(data)


def render(kept: list[dict[str, str]], dropped: list[dict[str, str]]) -> str:
    lines = ["# Advisory filter", ""]
    if not kept:
        lines.append("No critical, high, or unknown-severity advisories.")
    else:
        lines.append("| Severity | Package | Id | Title |")
        lines.append("| --- | --- | --- | --- |")
        for row in kept:
            lines.append(f"| {row['severity']} | {row['package']} | {row['id']} | {row['title']} |")
    lines.append("")
    lines.append(f"Kept {len(kept)}. Dropped {len(dropped)} moderate-or-lower.")
    lines.append("Unknown severity is kept so it can be checked. Confirm reachability before reporting.")
    return "\n".join(lines)


def self_test() -> int:
    npm = {
        "vulnerabilities": {
            "left-pad": {"name": "left-pad", "severity": "low", "via": [{"title": "noise"}]},
            "auth-lib": {"name": "auth-lib", "severity": "high", "via": [{"title": "auth bypass class", "source": 1}]},
            "mystery": {"name": "mystery", "severity": "", "via": ["nested"]},
        }
    }
    kept, dropped = select(parse_feed(npm, "npm"))
    assert [row["package"] for row in kept] == ["auth-lib", "mystery"], kept
    assert [row["package"] for row in dropped] == ["left-pad"], dropped
    pip = {"dependencies": [{"name": "req", "vulns": [{"id": "PYSEC-1", "description": "check me"}]}]}
    kept, _dropped = select(parse_feed(pip, "pip"))
    assert kept[0]["severity"] == "unknown" and kept[0]["id"] == "PYSEC-1"
    cargo = {"vulnerabilities": {"list": [{"package": {"name": "rustls"}, "advisory": {"id": "RUSTSEC-1", "severity": "critical", "title": "parser"}}]}}
    kept, _dropped = select(parse_feed(cargo, "cargo"))
    assert kept[0]["id"] == "RUSTSEC-1" and kept[0]["severity"] == "critical"
    moderate = {"advisories": [{"id": "X", "package": "p", "severity": "moderate", "title": "skip"}]}
    kept, dropped = select(parse_feed(moderate, "cargo"))
    assert kept == [] and len(dropped) == 1
    print("filter_advisories self-test ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Filter ecosystem audit JSON to critical and high advisories.")
    parser.add_argument("--ecosystem", choices=("npm", "pip", "cargo", "auto"), default="auto")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("path", nargs="?", help="JSON file. Default: stdin")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    raw = sys.stdin.read() if not args.path else open(args.path, encoding="utf-8").read()
    data = json.loads(raw)
    kept, dropped = select(parse_feed(data, args.ecosystem))
    print(render(kept, dropped))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
