#!/usr/bin/env python3
"""List functions and classes already in a tree so a change can reuse them.

Python files are parsed with ast. Other source files use a small set of
declaration patterns. This is a map, not a call graph.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

SKIP = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
TEXT_EXT = {".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".rb", ".java", ".c", ".h", ".cc", ".cpp"}
DECL = re.compile(
    r"^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)"
    r"|^\s*(?:pub\s+)?(?:async\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)"
    r"|^\s*func\s+(?:\([^)]*\)\s*)?([A-Za-z_][A-Za-z0-9_]*)"
    r"|^\s*(?:public|private|protected)?\s*(?:static\s+)?[\w<>\[\]]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("
)


def py_symbols(path: Path) -> list[tuple[int, str, str]]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeError):
        return []
    found: list[tuple[int, str, str]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found.append((node.lineno, "function", node.name))
        elif isinstance(node, ast.ClassDef):
            found.append((node.lineno, "class", node.name))
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    found.append((child.lineno, "method", f"{node.name}.{child.name}"))
    return found


def text_symbols(path: Path) -> list[tuple[int, str, str]]:
    found: list[tuple[int, str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return found
    for number, line in enumerate(lines, start=1):
        match = DECL.match(line)
        if not match:
            continue
        name = next(group for group in match.groups() if group)
        found.append((number, "function", name))
    return found


def scan(root: Path) -> list[str]:
    rows: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP for part in path.parts):
            continue
        if path.suffix == ".py":
            symbols = py_symbols(path)
        elif path.suffix in TEXT_EXT:
            symbols = text_symbols(path)
        else:
            continue
        for line, kind, name in symbols:
            rows.append(f"{path}:{line}: {kind} {name}")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    args = parser.parse_args()
    rows = scan(args.root)
    sys.stdout.write("\n".join(rows) + ("\n" if rows else ""))


if __name__ == "__main__":
    main()
