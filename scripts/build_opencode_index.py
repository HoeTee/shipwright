#!/usr/bin/env python3
"""Write or check skills/index.json, the OpenCode HTTP catalog.

OpenCode loads a catalog from <base>/index.json. Each file is fetched from
<base>/<skill-name>/<file>. The version is a short hash of those file bytes,
so a content change refreshes the cache. See https://opencode.ai/docs/skills/
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
INDEX = SKILLS / "index.json"
ID = __import__("re").compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def skill_dirs() -> list[Path]:
    found = []
    for path in sorted(SKILLS.iterdir()):
        if not path.is_dir() or not (path / "SKILL.md").is_file():
            continue
        if not ID.match(path.name) or not 1 <= len(path.name) <= 64:
            raise SystemExit(f"skill id is not kebab-case: {path.name}")
        found.append(path)
    names = [path.name for path in found]
    if len(names) != len(set(names)):
        raise SystemExit("skill ids are not unique")
    return found


def skill_files(skill: Path) -> list[str]:
    files = []
    for path in skill.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(skill).as_posix()
        if rel.startswith("/") or rel.startswith("../") or "/../" in f"/{rel}/":
            raise SystemExit(f"unsafe catalog path: {skill.name}/{rel}")
        files.append(rel)
    if "SKILL.md" not in files:
        raise SystemExit(f"{skill.name} has no SKILL.md")
    return sorted(files)


def content_version(skill: Path, files: list[str]) -> str:
    digest = hashlib.sha256()
    for rel in files:
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update((skill / rel).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()[:12]


def catalog() -> dict:
    items = []
    for skill in skill_dirs():
        files = skill_files(skill)
        items.append(
            {
                "name": skill.name,
                "version": content_version(skill, files),
                "files": files,
            }
        )
    return {"skills": items}


def main() -> int:
    data = catalog()
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        current = INDEX.read_text(encoding="utf-8") if INDEX.is_file() else ""
        if current != text:
            print(
                "skills/index.json is out of date. Run: python scripts/build_opencode_index.py",
                file=sys.stderr,
            )
            return 1
        return 0
    INDEX.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
