#!/usr/bin/env python3
"""Write the human-review draft and render it with the repo HTML renderer.

The renderer stays at scripts/render_html.mjs. This script does not move or
copy it. The generated page is an HTML report: do not screenshot that page.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

RENDERER = Path(__file__).resolve().parents[3] / "scripts" / "render_html.mjs"

DRAFT = """---
title: {title}
subtitle: {subtitle}
source: {source}
scope: {scope}
lang: zh
template: sheet
theme: blueprint
mode: light
cols: 2
---

## A Decision {{meta="human review"}}

{decision}

## B Object

| Field | Value |
| --- | --- |
| PR | {pr} |
| Candidate | {sha} |
| Baseline | {baseline} |

## C Findings

{findings}

## D Evidence

{evidence}

## E Open

{open_items}
"""


def draft(fields: dict[str, str]) -> str:
    return DRAFT.format(**fields)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", default="Human review")
    parser.add_argument("--subtitle", default="Technical checks are ready for a person.")
    parser.add_argument("--source", default="The candidate commit and the checks that ran.")
    parser.add_argument("--scope", default="")
    parser.add_argument("--decision", default="State the decision you need, the recommendation, and what changes if it is refused.")
    parser.add_argument("--pr", default="")
    parser.add_argument("--sha", default="")
    parser.add_argument("--baseline", default="")
    parser.add_argument("--findings", default="P0: 0 · P1: 0 · P2: 0")
    parser.add_argument("--evidence", default="List commands, results, and evidence paths that were actually produced.")
    parser.add_argument("--open", dest="open_items", default="None.")
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--draft", type=Path, help="write the markdown draft here")
    parser.add_argument("--draft-only", action="store_true")
    args = parser.parse_args()
    body = draft(
        {
            "title": args.title,
            "subtitle": args.subtitle,
            "source": args.source,
            "scope": args.scope or args.sha,
            "decision": args.decision,
            "pr": args.pr or "none",
            "sha": args.sha or "unknown",
            "baseline": args.baseline or "unknown",
            "findings": args.findings,
            "evidence": args.evidence,
            "open_items": args.open_items,
        }
    )
    if args.draft:
        args.draft.parent.mkdir(parents=True, exist_ok=True)
        args.draft.write_text(body, encoding="utf-8")
        print(args.draft)
    if args.draft_only:
        if not args.draft:
            sys.stdout.write(body)
        return
    if not args.output:
        raise SystemExit("pass -o page.html or --draft-only")
    if not RENDERER.is_file():
        raise SystemExit(f"renderer missing at {RENDERER}; the chat packet still stands")
    draft_path = args.draft or args.output.with_suffix(".md")
    if not args.draft:
        draft_path.write_text(body, encoding="utf-8")
    result = subprocess.run(
        ["node", str(RENDERER), "render", str(draft_path), "-o", str(args.output), "--no-open"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)
    print(args.output)


if __name__ == "__main__":
    main()
