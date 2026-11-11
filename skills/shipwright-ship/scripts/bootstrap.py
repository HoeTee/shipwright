#!/usr/bin/env python3
"""Install the watch-pr runtime dependency with npm.

The old installer was a Bun script. It hashed bun.lock and refused to run
without that file. This repository does not ship a Bun lockfile. commander
is the only runtime dependency, declared in package.json.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "package.json"
COMMANDER = ROOT / "node_modules" / "commander" / "package.json"
INSTALL_KEY = ROOT / "node_modules" / ".shipwright-watch-pr-install-key"


def install_key(package_json: bytes) -> str:
    return hashlib.sha256(package_json).hexdigest()


def already_installed(package_json: bytes) -> bool:
    expected = install_key(package_json)
    return (
        COMMANDER.is_file()
        and INSTALL_KEY.is_file()
        and INSTALL_KEY.read_text(encoding="utf-8").strip() == expected
    )


def main() -> int:
    if not PACKAGE.is_file():
        print(f"missing {PACKAGE}", file=sys.stderr)
        return 1
    package_json = PACKAGE.read_bytes()
    if already_installed(package_json):
        return 0
    npm = shutil.which("npm")
    if npm is None:
        print(
            "npm was not found. Install Node.js, then run: python3 bootstrap.py",
            file=sys.stderr,
        )
        return 1
    result = subprocess.run(
        [npm, "install", "--omit=dev", "--ignore-scripts", "--no-fund", "--no-audit"],
        cwd=ROOT,
    )
    if result.returncode != 0:
        print("npm install failed.", file=sys.stderr)
        return result.returncode
    if not COMMANDER.is_file():
        print("npm install finished without installing commander.", file=sys.stderr)
        return 1
    INSTALL_KEY.parent.mkdir(parents=True, exist_ok=True)
    INSTALL_KEY.write_text(install_key(package_json) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
