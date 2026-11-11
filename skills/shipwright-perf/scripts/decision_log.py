#!/usr/bin/env python3
"""Append one validated row to a hillclimb decision.tsv outside the work tree."""

from __future__ import annotations

import argparse
import csv
import subprocess
import tempfile
from pathlib import Path

COLUMNS = ("id", "hypothesis", "change", "before", "after", "delta", "tests", "verdict", "note")
VERDICTS = {"kept", "reverted"}


def inside_work_tree(path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False
    root = Path(result.stdout.strip()).resolve()
    try:
        path.resolve().relative_to(root)
    except ValueError:
        return False
    return True


def existing_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return {row.get("id", "") for row in reader}


def append_row(path: Path, row: dict[str, str], *, allow_inside_repo: bool) -> None:
    if not allow_inside_repo and inside_work_tree(path):
        raise SystemExit(f"refusing to write {path} inside a work tree; keep decision.tsv outside git")
    missing = [key for key in COLUMNS if key not in row or row[key] == ""]
    if missing:
        raise SystemExit(f"missing columns: {', '.join(missing)}")
    if row["verdict"] not in VERDICTS:
        raise SystemExit("verdict must be kept or reverted")
    if "\t" in "".join(row[key] for key in COLUMNS) or "\n" in "".join(row[key] for key in COLUMNS):
        raise SystemExit("fields cannot contain tabs or newlines")
    if row["id"] in existing_ids(path):
        raise SystemExit(f"id already in the log: {row['id']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, delimiter="\t", lineterminator="\n")
        if new_file:
            writer.writeheader()
        writer.writerow({key: row[key] for key in COLUMNS})


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "decision.tsv"
        row = {
            "id": "1",
            "hypothesis": "defer boot parse",
            "change": "lazy init",
            "before": "40",
            "after": "30",
            "delta": "-10",
            "tests": "green",
            "verdict": "kept",
            "note": "past noise",
        }
        append_row(path, row, allow_inside_repo=False)
        try:
            append_row(path, row, allow_inside_repo=False)
        except SystemExit as exc:
            assert "already" in str(exc), exc
        else:
            raise SystemExit("duplicate id was accepted")
        bad = dict(row, id="2", verdict="maybe")
        try:
            append_row(path, bad, allow_inside_repo=False)
        except SystemExit as exc:
            assert "verdict" in str(exc), exc
        else:
            raise SystemExit("bad verdict was accepted")
        text = path.read_text(encoding="utf-8")
        assert text.splitlines()[0] == "\t".join(COLUMNS)
        assert "defer boot parse" in text
    print("decision_log self-test ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append a hillclimb decision row outside the work tree.")
    parser.add_argument("--path", required=False, help="decision.tsv path, outside the repository")
    parser.add_argument("--allow-inside-repo", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    for column in COLUMNS:
        parser.add_argument(f"--{column}")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.path:
        parser.error("--path is required")
    row = {column: getattr(args, column) or "" for column in COLUMNS}
    append_row(Path(args.path), row, allow_inside_repo=args.allow_inside_repo)
    print(f"appended {row['id']} ({row['verdict']}) to {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
