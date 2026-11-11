"""trace_to_sqlite.py loads a trace and a profile into queryable tables."""

from __future__ import annotations

import gzip
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("trace_to_sqlite.py")


class TraceToSqliteTests(unittest.TestCase):
    def test_trace_and_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trace = root / "trace.json.gz"
            with gzip.open(trace, "wt", encoding="utf-8") as handle:
                json.dump(
                    {
                        "traceEvents": [
                            {"name": "layout", "ph": "X", "ts": 1, "dur": 30, "pid": 1, "tid": 1},
                            {"name": "paint", "ph": "X", "ts": 2, "dur": 5, "pid": 1, "tid": 1},
                        ]
                    },
                    handle,
                )
            profile = root / "app.cpuprofile"
            profile.write_text(
                json.dumps(
                    {
                        "nodes": [
                            {"id": 1, "callFrame": {"functionName": "hot", "url": "app.js", "lineNumber": 10}, "hitCount": 4},
                            {"id": 2, "callFrame": {"functionName": "cold", "url": "app.js", "lineNumber": 20}, "hitCount": 1},
                        ],
                        "samples": [1, 1, 1, 2],
                    }
                ),
                encoding="utf-8",
            )
            trace_out = subprocess.run(
                [sys.executable, str(SCRIPT), str(trace)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(trace_out.returncode, 0, trace_out.stderr)
            self.assertIn("event\t30\tlayout", trace_out.stdout)
            database = sqlite3.connect(root / "trace.sqlite")
            self.assertEqual(database.execute("SELECT COUNT(*) FROM events").fetchone()[0], 2)
            database.close()

            profile_out = subprocess.run(
                [sys.executable, str(SCRIPT), str(profile), "--out", str(root / "profile.sqlite")],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(profile_out.returncode, 0, profile_out.stderr)
            self.assertIn("sample\t3\thot", profile_out.stdout)

    def test_rejects_unknown_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "notes.json"
            path.write_text('{"hello": 1}', encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("neither", result.stderr)


if __name__ == "__main__":
    unittest.main()
