#!/usr/bin/env python3
"""Write or check skills/index.json, the OpenCode skill catalog.

OpenCode loads a catalog from a base URL with index.json. Each skill's files
are downloaded from <base>/<skill-name>/<file>. See https://opencode.ai/docs/skills/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
INDEX = SKILLS / "index.json"


def skill_files(skill: Path) -> list[str]:
    files = [
        path.relative_to(skill).as_posix()
        for path in skill.rglob("*")
        if path.is_file()
    ]
    return sorted(files)


def catalog(previous: dict | None = None) -> dict:
    prior = {}
    if previous:
        prior = {item["name"]: item for item in previous.get("skills", [])}
    items = []
    for skill in sorted(path for path in SKILLS.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()):
        files = skill_files(skill)
        old = prior.get(skill.name)
        if old and old.get("files") == files:
            version = str(old.get("version", "1"))
        elif old:
            version = str(int(str(old.get("version", "0"))) + 1)
        else:
            version = "1"
        items.append({"name": skill.name, "version": version, "files": files})
    return {"skills": items}


def main() -> int:
    previous = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.is_file() else None
    data = catalog(previous)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        current = INDEX.read_text(encoding="utf-8") if INDEX.is_file() else ""
        if current != text:
            print("skills/index.json is out of date. Run: python scripts/build_opencode_index.py", file=sys.stderr)
            return 1
        return 0
    INDEX.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
