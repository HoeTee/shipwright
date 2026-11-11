#!/usr/bin/env python3
"""Check a multi-PR plan written from shipwright-plan's multi-pr reference.

Ported from pstack scripts/check-plan.mjs. Ordinary plans do not use this
script. It stays off unless that reference is explicitly enabled.

The host-only scheduler marker is now "one-hour cadence". The execution
pointer marker is "shipwright-autopilot".
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RULE = (
    "Tests alone are not sufficient verification. "
    "A PR is verified only when its unit, live, and perf boxes are all checked."
)
LANES = re.compile(r"Ten lanes on `[^`<>]+` at the PR head")
SUB_BLOCKS = [
    "Depends on.",
    "Files.",
    "Build.",
    "You see.",
    "Verify, unit.",
    "Verify, live.",
    "Verify, perf.",
    "Review gate.",
    "Merge.",
]
PROGRAM_H3 = [
    "Arm the program",
    "Spawn owners",
    "PR mechanics",
    "Verdict and merge",
    "Boot recipe",
]
PROGRAM_MARKERS = ["git show origin/main:", "one-hour cadence", "status message"]
HOW_TO_READ_MARKERS = [
    "One box is one unit of work",
    "names the evidence",
    "Check a box only when its evidence exists",
    "shipwright-autopilot",
    RULE,
]
PERF_ITEMS = ["Metric.", "Probe.", "Baseline.", "Rule."]
BOX = re.compile(r"^\s*- \[[ x]\] (.*)$")
INLINE = re.compile(r"(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)")
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK = re.compile(r"\]\([^)]*\)")
H3_PREFIX = re.compile(r"^\*\*([^*]+)\*\*(.*)$")
OPEN_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
CLOSE_FENCE = re.compile(r"^ {0,3}(`+|~+)[ \t]*$")
LANE_ITEM = re.compile(r"^Lane (\d+)\. ")
SAVE_SHOT = re.compile(r"Save `[^`]+`")


def opening_fence(text: str) -> tuple[str, int] | None:
    match = OPEN_FENCE.match(text)
    if not match or (match.group(1)[0] == "`" and "`" in match.group(2)):
        return None
    return match.group(1)[0], len(match.group(1))


def closing_fence(text: str, opening: tuple[str, int]) -> bool:
    match = CLOSE_FENCE.match(text)
    return bool(
        match
        and match.group(1)[0] == opening[0]
        and len(match.group(1)) >= opening[1]
    )


def check(path: Path) -> tuple[list[str], list[str]]:
    raw = path.read_text(encoding="utf-8").splitlines()
    problems: list[str] = []
    report: list[str] = []

    def fail(line: int, message: str) -> None:
        problems.append(f"{path}:{line}: {message}")

    start = 0
    if raw and raw[0] == "---":
        try:
            start = raw.index("---", 1) + 1
        except ValueError:
            start = 0

    lines: list[dict] = []
    fence: tuple[str, int] | None = None
    for index in range(start, len(raw)):
        text = raw[index]
        number = index + 1
        code = fence is not None
        if fence and closing_fence(text, fence):
            code = False
            fence = None
        elif fence is None:
            fence = opening_fence(text)
            code = fence is not None
        lines.append({"n": number, "text": text, "code": code})
        if code:
            continue
        prose = LINK.sub("]", IMAGE.sub("", INLINE.sub("`", text)))
        if re.search(r"[\u2013\u2014]", prose):
            fail(number, "long dash")
        if re.search(r"[\u2018\u2019\u201c\u201d]", prose):
            fail(number, "curly quote")
        if re.search(r": \S", prose):
            fail(number, "mid-sentence colon")

    def h2(item: dict) -> str | None:
        if item["code"] or not item["text"].startswith("## "):
            return None
        return item["text"][3:].strip()

    sections: list[dict] = []
    for item in lines:
        title = h2(item)
        if title is not None:
            sections.append({"title": title, "n": item["n"], "body": []})
        elif sections:
            sections[-1]["body"].append(item)

    def find(title: str) -> dict | None:
        return next((section for section in sections if section["title"] == title), None)

    def body_text(section: dict) -> str:
        return "\n".join(item["text"] for item in section["body"])

    def boxes(items: list[dict]) -> list[dict]:
        found = []
        for item in items:
            if item["code"]:
                continue
            match = BOX.match(item["text"])
            if match:
                found.append({"n": item["n"], "text": match.group(1)})
        return found

    h1 = next((i for i, item in enumerate(lines) if not item["code"] and item["text"].startswith("# ")), -1)
    how_to_read = find("How to read this")
    if h1 == -1:
        fail(1, "no H1 title")
    if how_to_read is None:
        fail(1, 'no "## How to read this" section')
    if h1 != -1 and how_to_read is not None:
        intro = [
            item
            for item in lines[h1 + 1 :]
            if item["n"] < how_to_read["n"] and item["text"].strip() != ""
        ]
        if len(intro) >= 10:
            fail(lines[h1]["n"], f"intro is {len(intro)} lines, under ten required")
        for marker in HOW_TO_READ_MARKERS:
            if marker not in body_text(how_to_read):
                fail(how_to_read["n"], f'How to read this lacks "{marker}"')

    program = find("Program checklist")
    if program is None:
        fail(1, 'no "## Program checklist" section')
    else:
        h3s = [
            item["text"][4:].strip()
            for item in program["body"]
            if not item["code"] and item["text"].startswith("### ")
        ]
        cursor = 0
        for name in PROGRAM_H3:
            at = next((i for i, title in enumerate(h3s) if i >= cursor and title.startswith(name)), -1)
            if at == -1:
                fail(program["n"], f'Program checklist lacks "### {name}" in order')
            else:
                cursor = at + 1
        for marker in PROGRAM_MARKERS:
            if marker not in body_text(program):
                fail(program["n"], f'Program checklist lacks "{marker}"')

    close = find("Close the program")
    if close is None:
        fail(1, 'no "## Close the program" section')
    program_index = sections.index(program) if program in sections else -1
    close_index = sections.index(close) if close in sections else -1
    pr_sections = [] if program_index == -1 or close_index == -1 else sections[program_index + 1 : close_index]
    if not pr_sections:
        fail(1, "no PR sections between Program checklist and Close the program")

    for pr in pr_sections:
        heads: list[dict] = []
        for item in pr["body"]:
            if item["code"]:
                continue
            match = H3_PREFIX.match(item["text"])
            if match and match.group(1) in SUB_BLOCKS:
                heads.append(
                    {
                        "name": match.group(1),
                        "n": item["n"],
                        "rest": match.group(2).strip(),
                        "lines": [],
                    }
                )
            elif heads:
                heads[-1]["lines"].append(item)
        names = [head["name"] for head in heads]
        if "|".join(names) != "|".join(SUB_BLOCKS):
            fail(
                pr["n"],
                f"{pr['title']}: sub-blocks are [{', '.join(names)}], expected [{', '.join(SUB_BLOCKS)}]",
            )
        counts: dict[str, int] = {}
        for head in heads:
            counts[head["name"]] = len(boxes(head["lines"]))

        def block(name: str) -> dict | None:
            return next((head for head in heads if head["name"] == name), None)

        depends = block("Depends on.")
        if depends is not None and depends["rest"] == "":
            fail(depends["n"], f"{pr['title']}: Depends on names nothing")
        for name in ["Files.", "Build.", "You see.", "Verify, unit.", "Merge."]:
            item = block(name)
            if item is not None and not boxes(item["lines"]):
                fail(item["n"], f"{pr['title']}: {name} has no box")
        for name in ["Verify, unit.", "Verify, live.", "Verify, perf."]:
            item = block(name)
            if item is not None and not item["rest"].startswith(RULE):
                fail(item["n"], f"{pr['title']}: {name} does not open with the rule")

        live = block("Verify, live.")
        if live is not None:
            if not LANES.search(live["rest"]):
                fail(
                    live["n"],
                    f"{pr['title']}: Verify, live lacks \"Ten lanes on `<model>` at the PR head\" with the model filled in",
                )
            lanes = []
            for item in boxes(live["lines"]):
                lanes.append({**item, "m": LANE_ITEM.match(item["text"])})
            numbers = sorted(int(item["m"].group(1)) for item in lanes if item["m"])
            if ",".join(str(number) for number in numbers) != "1,2,3,4,5,6,7,8,9,10":
                fail(live["n"], f"{pr['title']}: lanes are [{','.join(str(number) for number in numbers)}], expected 1 to 10")
            for lane in lanes:
                if not lane["m"]:
                    fail(lane["n"], f"{pr['title']}: live box is not a lane")
                elif not SAVE_SHOT.search(lane["text"]):
                    fail(lane["n"], f"{pr['title']}: lane {lane['m'].group(1)} names no screenshot")
                elif "Pass when" not in lane["text"]:
                    fail(lane["n"], f"{pr['title']}: lane {lane['m'].group(1)} has no pass predicate")

        perf = block("Verify, perf.")
        if perf is not None:
            items = [item["text"].split(" ")[0] for item in boxes(perf["lines"])]
            if "|".join(items) != "|".join(PERF_ITEMS):
                fail(
                    perf["n"],
                    f"{pr['title']}: perf boxes are [{', '.join(items)}], expected [{', '.join(PERF_ITEMS)}]",
                )

        gate = block("Review gate.")
        if gate is not None:
            gate_boxes = boxes(gate["lines"])
            if gate["rest"].startswith("None."):
                if gate_boxes:
                    fail(gate["n"], f"{pr['title']}: Review gate says None but has boxes")
            else:
                text = "\n".join(item["text"] for item in gate["lines"])
                if not gate_boxes:
                    fail(gate["n"], f"{pr['title']}: Review gate has no box")
                for word in ["screenshot", "video", "operator"]:
                    if word not in text:
                        fail(gate["n"], f'{pr["title"]}: Review gate lacks "{word}"')

        total = len(boxes(pr["body"]))
        cells = []
        for name in SUB_BLOCKS:
            if name == "Depends on.":
                continue
            slug = re.sub(r"-$", "", re.sub(r"[ ,.]+", "-", name)).lower()
            cells.append(f"{slug}={counts.get(name, 0)}")
        report.append(f"{pr['title']}  boxes={total}  {' '.join(cells)}")

    if close_index != -1 and close is not None:
        tail = sections[close_index + 1 :]
        for section in tail:
            if not section["title"].startswith("Appendix"):
                fail(section["n"], f'"## {section["title"]}" after Close the program is not an appendix')
        if not any("Prototype evidence" in section["title"] for section in tail):
            fail(close["n"], 'no "## Appendix ... Prototype evidence" section')

    return report, problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python check_plan.py <plan.md>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    report, problems = check(path)
    for line in report:
        print(line)
    print(f"{len(report)} PR sections, {len(problems)} problems")
    for problem in problems:
        print(problem, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
