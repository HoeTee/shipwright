#!/usr/bin/env python3
"""Load a trace or CPU profile into sqlite so it can be queried.

Accepts a Chrome trace JSON (`traceEvents`) or a DevTools `.cpuprofile`
(`nodes` plus `samples`). A `.gz` file is decompressed first. The artifact
is read only. The sqlite file is the queryable shape from the trace-forensics
playbook: one row per event, sample, or node.
"""

from __future__ import annotations

import argparse
import gzip
import json
import sqlite3
import sys
from pathlib import Path


def load_json(path: Path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def create(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE events (
            id INTEGER PRIMARY KEY,
            name TEXT,
            cat TEXT,
            ph TEXT,
            ts REAL,
            dur REAL,
            pid INTEGER,
            tid INTEGER
        );
        CREATE TABLE nodes (
            id INTEGER PRIMARY KEY,
            function_name TEXT,
            url TEXT,
            line INTEGER,
            hit_count INTEGER
        );
        CREATE TABLE samples (
            ord INTEGER PRIMARY KEY,
            node_id INTEGER
        );
        """
    )


def fill_trace(connection: sqlite3.Connection, events: list) -> int:
    rows = []
    for event in events:
        if not isinstance(event, dict):
            continue
        rows.append(
            (
                str(event.get("name", "")),
                str(event.get("cat", "")),
                str(event.get("ph", "")),
                float(event.get("ts") or 0),
                float(event.get("dur") or 0),
                int(event.get("pid") or 0),
                int(event.get("tid") or 0),
            )
        )
    connection.executemany(
        "INSERT INTO events (name, cat, ph, ts, dur, pid, tid) VALUES (?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    return len(rows)


def fill_profile(connection: sqlite3.Connection, profile: dict) -> tuple[int, int]:
    nodes = []
    for node in profile.get("nodes", []):
        frame = node.get("callFrame") or {}
        nodes.append(
            (
                int(node.get("id") or 0),
                str(frame.get("functionName", "")),
                str(frame.get("url", "")),
                int(frame.get("lineNumber") or 0),
                int(node.get("hitCount") or 0),
            )
        )
    connection.executemany(
        "INSERT INTO nodes (id, function_name, url, line, hit_count) VALUES (?, ?, ?, ?, ?)",
        nodes,
    )
    samples = [(index, int(node_id)) for index, node_id in enumerate(profile.get("samples") or [])]
    connection.executemany("INSERT INTO samples (ord, node_id) VALUES (?, ?)", samples)
    return len(nodes), len(samples)


def report(connection: sqlite3.Connection) -> list[str]:
    lines = []
    event_count = connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    if event_count:
        lines.append(f"events={event_count}")
        for name, total in connection.execute(
            "SELECT name, SUM(dur) AS total FROM events GROUP BY name ORDER BY total DESC LIMIT 10"
        ):
            lines.append(f"event\t{total:.0f}\t{name}")
    node_count = connection.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    sample_count = connection.execute("SELECT COUNT(*) FROM samples").fetchone()[0]
    if node_count:
        lines.append(f"nodes={node_count} samples={sample_count}")
        for name, hits in connection.execute(
            """
            SELECT nodes.function_name, COUNT(samples.node_id) AS hits
            FROM samples JOIN nodes ON nodes.id = samples.node_id
            GROUP BY nodes.function_name
            ORDER BY hits DESC
            LIMIT 10
            """
        ):
            lines.append(f"sample\t{hits}\t{name}")
    return lines


def convert(source: Path, output: Path) -> list[str]:
    data = load_json(source)
    if output.exists():
        output.unlink()
    connection = sqlite3.connect(output)
    try:
        create(connection)
        if isinstance(data, dict) and isinstance(data.get("traceEvents"), list):
            fill_trace(connection, data["traceEvents"])
        elif isinstance(data, dict) and isinstance(data.get("nodes"), list) and "samples" in data:
            fill_profile(connection, data)
        else:
            raise SystemExit(f"{source} is neither a Chrome trace nor a cpuprofile")
        connection.commit()
        return report(connection)
    finally:
        connection.close()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    source = args.artifact
    output = args.out or source.with_suffix("").with_suffix(".sqlite")
    if source.suffix == ".gz":
        output = args.out or source.with_suffix("").with_suffix(".sqlite")
    for line in convert(source, output):
        print(line)
    print(f"sqlite={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
