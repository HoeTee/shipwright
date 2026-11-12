#!/usr/bin/env python3
"""Print or create the labels named by .github/repo-ops.yml.

Default mode prints `gh label create --force` lines. `--apply` runs them.
A second run updates the same labels because every command passes `--force`.

The loader accepts the block dialect these intake files use. It does not
execute file contents.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / ".github" / "repo-ops.yml"

FIXED_LABELS = (
    ("triage", "fbca04", "Issue form is waiting for intake"),
    ("needs-info", "d93f0b", "A required form field is empty or the module is not allowed"),
    ("agent:ready", "0e8a16", "Intake passed and a worker may start"),
    ("agent:running", "1d76db", "A worker is running on this issue"),
    ("blocked", "b60205", "A worker stopped and needs a person"),
    ("touches:shared", "5319e7", "The change touches a shared boundary"),
    ("eval", "c5def5", "Run the eval lane"),
)


class YamlError(ValueError):
    pass


class _Line:
    def __init__(self, indent: int, text: str, lineno: int) -> None:
        self.indent = indent
        self.text = text
        self.lineno = lineno


class BlockYaml:
    """Indent-based YAML maps and lists, without flow collections or block scalars."""

    def __init__(self, text: str) -> None:
        self.lines: list[_Line] = []
        for lineno, raw in enumerate(text.splitlines(), 1):
            if raw.endswith("\r"):
                raw = raw[:-1]
            stripped = raw.strip()
            if stripped == "" or stripped.startswith("#"):
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            if raw[:indent].find("\t") != -1:
                raise YamlError(f"line {lineno}: tabs are not allowed")
            self.lines.append(_Line(indent, stripped, lineno))
        self.index = 0

    def parse(self):
        if not self.lines:
            return None
        value = self._parse_block(self.lines[0].indent)
        if self.index != len(self.lines):
            line = self.lines[self.index]
            raise YamlError(f"line {line.lineno}: unparsed {line.text!r}")
        return value

    def _peek(self) -> _Line | None:
        if self.index >= len(self.lines):
            return None
        return self.lines[self.index]

    def _parse_block(self, indent: int):
        peeked = self._peek()
        if peeked is None or peeked.indent < indent:
            return None
        if peeked.text.startswith("- "):
            return self._parse_list(indent)
        return self._parse_map(indent)

    def _parse_list(self, indent: int) -> list:
        items = []
        while True:
            peeked = self._peek()
            if peeked is None or peeked.indent != indent or not peeked.text.startswith("- "):
                break
            self.index += 1
            item_text = peeked.text[2:]
            key, rest, is_key = _split_key(item_text)
            if is_key:
                node: dict = {}
                node[key] = self._value(rest, indent + 2, peeked.lineno)
                self._fill_map(node, indent + 2)
                items.append(node)
            else:
                items.append(_scalar(item_text, peeked.lineno))
        return items

    def _parse_map(self, indent: int) -> dict:
        node: dict = {}
        self._fill_map(node, indent)
        return node

    def _fill_map(self, node: dict, indent: int) -> None:
        while True:
            peeked = self._peek()
            if peeked is None or peeked.indent != indent or peeked.text.startswith("- "):
                return
            self.index += 1
            key, rest, is_key = _split_key(peeked.text)
            if not is_key:
                raise YamlError(f"line {peeked.lineno}: expected a key, got {peeked.text!r}")
            if key in node:
                raise YamlError(f"line {peeked.lineno}: duplicate key {key!r}")
            node[key] = self._value(rest, indent + 2, peeked.lineno)

    def _value(self, rest: str, child_indent: int, lineno: int):
        if rest == "":
            peeked = self._peek()
            if peeked is not None and peeked.indent >= child_indent:
                return self._parse_block(peeked.indent)
            return None
        if rest[:1] in {">", "|"}:
            raise YamlError(f"line {lineno}: block scalars are not used in repo-ops files")
        if rest.startswith("[") or rest.startswith("{"):
            raise YamlError(f"line {lineno}: write lists and maps in block form")
        return _scalar(rest, lineno)


def _split_key(text: str) -> tuple[str, str, bool]:
    if text.startswith(("'", '"')):
        return "", "", False
    if text.endswith(":") and ": " not in text:
        return text[:-1], "", True
    if ": " in text:
        key, rest = text.split(": ", 1)
        if key == "":
            return "", "", False
        return key, rest, True
    return "", "", False


def _scalar(text: str, lineno: int):
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {'"', "'"}:
        inner = text[1:-1]
        if text[0] == "'":
            inner = inner.replace("''", "'")
        elif "\\" in inner:
            raise YamlError(f"line {lineno}: quoted escapes are not used in repo-ops files")
        return inner
    if text == "true":
        return True
    if text == "false":
        return False
    if text in {"null", "~"}:
        return None
    if text[0:1].isdigit() or (text.startswith("-") and text[1:2].isdigit()):
        if text.lstrip("-").isdigit():
            return int(text)
    return text


def parse_yaml(text: str):
    return BlockYaml(text).parse()


def load_config(path: Path = CONFIG_PATH) -> dict:
    data = parse_yaml(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise YamlError(f"{path} did not parse as a map")
    return data


def label_specs(config: dict) -> list[tuple[str, str, str]]:
    specs = list(FIXED_LABELS)
    modules = config["modules"]
    if not isinstance(modules, dict) or not modules:
        raise YamlError("modules must be a non-empty map")
    for name in modules:
        specs.append((f"module:{name}", "bfd4f2", f"Work is in the {name} module"))
    workers = config["workers"]
    if not isinstance(workers, list) or not workers:
        raise YamlError("workers must be a non-empty list")
    for worker in workers:
        specs.append((f"bot:{worker}", "c2e0c6", f"Assigned to {worker}"))
    eval_label = config["cost"]["eval_label"]
    names = [item[0] for item in specs]
    if eval_label not in names:
        raise YamlError(f"cost.eval_label {eval_label!r} is missing from the label list")
    if len(names) != len(set(names)):
        raise YamlError("duplicate label name")
    return specs


def gh_command(repo: str, name: str, color: str, description: str) -> list[str]:
    return [
        "gh",
        "label",
        "create",
        name,
        "--repo",
        repo,
        "--force",
        "--color",
        color,
        "--description",
        description,
    ]


def shell_join(parts: list[str]) -> str:
    rendered = []
    for part in parts:
        if all(ch.isalnum() or ch in ":-._/@" for ch in part):
            rendered.append(part)
        else:
            rendered.append("'" + part.replace("'", "'\\''") + "'")
    return " ".join(rendered)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print or create repo-ops labels.")
    parser.add_argument("--apply", action="store_true", help="run gh label create --force")
    parser.add_argument("--config", type=Path, default=CONFIG_PATH)
    args = parser.parse_args(argv)
    config = load_config(args.config)
    repo = config["repo"]
    if not isinstance(repo, str) or "/" not in repo:
        raise YamlError("repo must look like owner/name")
    for name, color, description in label_specs(config):
        command = gh_command(repo, name, color, description)
        print(shell_join(command))
        if args.apply:
            subprocess.run(command, check=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (YamlError, subprocess.CalledProcessError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
