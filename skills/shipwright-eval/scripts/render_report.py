#!/usr/bin/env python3
"""Write the eval HTML report and the plan verdict section."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def _esc(value) -> str:
    return html.escape(str(value), quote=True)


def render_html(report: dict) -> str:
    questions = "\n".join(
        f"<li><strong>{_esc(item.get('question', ''))}</strong> {_esc(item.get('answer', ''))}</li>"
        for item in report.get("questions", [])
    )
    tasks = "\n".join(
        f"<li>{_esc(task.get('kind', ''))}: {_esc(task.get('raw_subject', task.get('name', '')))}</li>"
        for task in report.get("tasks", [])
    )
    both = "\n".join(f"<li>{_esc(name)}</li>" for name in report.get("both_perfect", []))
    limits = "\n".join(f"<li>{_esc(item)}</li>" for item in report.get("limitations", []))
    return f"""<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<title>{_esc(report.get("title", "Eval"))}</title>
<style>
body {{ font: 16px/1.5 sans-serif; margin: 2rem auto; max-width: 46rem; color: #1c1c1c; }}
h1, h2 {{ font-weight: 600; }}
code {{ font-family: ui-monospace, monospace; }}
</style>
</head>
<body>
<h1>{_esc(report.get("title", "Eval"))}</h1>
<h2>Claim</h2>
<p>{_esc(report.get("claim", ""))}</p>
<h2>Verdict</h2>
<p><code>{_esc(report.get("verdict", ""))}</code></p>
<p>{_esc(report.get("verdict_note", ""))}</p>
<h2>Quality</h2>
<pre>{_esc(json.dumps(report.get("quality", {}), ensure_ascii=False, indent=2))}</pre>
<h2>Hard metrics</h2>
<pre>{_esc(json.dumps(report.get("hard", {}), ensure_ascii=False, indent=2))}</pre>
<h2>Seven questions</h2>
<ol>
{questions}
</ol>
<h2>Tasks</h2>
<ul>
{tasks}
</ul>
<h2>Both perfect</h2>
<ul>
{both}
</ul>
<h2>Limitations</h2>
<ul>
{limits}
</ul>
</body>
</html>
"""


def render_plan(report: dict) -> str:
    return "\n".join(
        [
            f"# Plan {report.get('plan', '')}: Eval {report.get('title', '')}",
            "",
            "- **Category**: eval",
            f"- **Mode**: {report.get('mode', '')}",
            f"- **Control**: {report.get('control', '')}",
            f"- **N**: {report.get('n', '')}",
            f"- **Claim**: {report.get('claim', '')}",
            f"- **Verdict**: {report.get('verdict', '')}",
            "",
            "判定只对这次题库、这次模型和这次运行有效。日常 Run record 的趋势指标不引用这里的节省数字。",
            "",
        ]
    )


def write_report(report: dict, html_path: Path, plan_path: Path | None = None) -> None:
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(render_html(report), encoding="utf-8")
    if plan_path is not None:
        plan_path.parent.mkdir(parents=True, exist_ok=True)
        plan_path.write_text(render_plan(report), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an eval HTML report")
    parser.add_argument("report", type=Path)
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--plan", type=Path)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    write_report(report, args.html, args.plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
