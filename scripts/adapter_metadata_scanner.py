#!/usr/bin/env python3
"""
Adapter Metadata Scanner

Walks a repository to extract:
- Tools: from JSON specs, Python @tool-decorated functions, YAML blocks, and README fenced blocks
- README blocks: sections titled "Tools" and their fenced code blocks

Outputs a JSON report with discovered items.

Usage:
  python scripts/adapter_metadata_scanner.py --root . --out adapter_metadata_report.json

This script avoids non-stdlib dependencies. YAML is captured as raw text.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional, Tuple

# -----------------------------
# Helpers
# -----------------------------

IGNORED_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    "venv",
    ".venv",
    ".idea",
    ".vscode",
}

README_NAMES = {"README", "Readme", "readme"}
README_EXTS = {"", ".md", ".markdown", ".MD"}

JSON_EXTS = {".json"}
YAML_EXTS = {".yaml", ".yml"}
PY_EXTS = {".py"}
MD_EXTS = {".md", ".markdown", ".MD"}


@dataclass
class Location:
    file: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None


@dataclass
class ToolRecord:
    source_file: str
    kind: str  # json_schema | python_decorator | yaml_block | readme_block | markdown_codeblock | unknown
    name: Optional[str] = None
    description: Optional[str] = None
    spec: Optional[Any] = None  # dict for JSON; str for YAML/markdown; None otherwise
    location: Optional[Location] = None


@dataclass
class ReadmeBlock:
    readme_path: str
    section: Optional[str]
    content: str
    code_blocks: List[Dict[str, Any]]
    location: Optional[Location]


@dataclass
class ScanReport:
    root: str
    tools: List[ToolRecord]
    readme_blocks: List[ReadmeBlock]

    def to_json(self) -> str:
        def default(o):
            if hasattr(o, "__dict__"):
                return asdict(o)
            return str(o)

        return json.dumps(asdict(self), indent=2, ensure_ascii=False)


# -----------------------------
# File walking & IO
# -----------------------------


def iter_files(root: str) -> Iterable[str]:
    for dirpath, dirnames, filenames in os.walk(root):
        # prune ignored dirs
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")]
        for fn in filenames:
            yield os.path.join(dirpath, fn)


def read_text_safely(path: str) -> Tuple[str, List[str]]:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
    except Exception:
        try:
            with open(path, "r", encoding="latin-1", errors="replace") as f:
                txt = f.read()
        except Exception:
            return "", []
    lines = txt.splitlines()
    return txt, lines


# -----------------------------
# Extractors
# -----------------------------

JSON_TOOL_KEYS = {"name", "description", "parameters"}


def try_parse_json(text: str) -> Optional[Any]:
    try:
        return json.loads(text)
    except Exception:
        return None


def extract_tools_from_json(path: str, text: str, lines: List[str]) -> List[ToolRecord]:
    recs: List[ToolRecord] = []
    data = try_parse_json(text)
    if data is None:
        return recs

    def add_tool(obj: Dict[str, Any], name_hint: Optional[str] = None):
        name = obj.get("name") if isinstance(obj, dict) else None
        desc = obj.get("description") if isinstance(obj, dict) else None
        recs.append(
            ToolRecord(
                source_file=path,
                kind="json_schema",
                name=name or name_hint,
                description=desc,
                spec=obj,
                location=Location(file=path),
            )
        )

    # Case 1: top-level { tools: [ ... ] }
    if isinstance(data, dict) and isinstance(data.get("tools"), list):
        for i, t in enumerate(data["tools"]):
            if isinstance(t, dict):
                add_tool(t, name_hint=f"tool_{i}")
        return recs

    # Case 2: array of tool specs
    if isinstance(data, list):
        for i, t in enumerate(data):
            if isinstance(t, dict) and JSON_TOOL_KEYS.issubset(t.keys()):
                add_tool(t, name_hint=f"tool_{i}")
        return recs

    # Case 3: single tool spec object
    if isinstance(data, dict) and JSON_TOOL_KEYS.issubset(data.keys()):
        add_tool(data)
        return recs

    return recs


PY_TOOL_DECORATOR_RE = re.compile(r"^\s*@tool(?:\([^)]*\))?\s*$")
PY_DEF_RE = re.compile(r"^\s*def\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\(")
PY_TRIPLE_QUOTE_START_RE = re.compile(r"^[ \t]*([ruRU]{0,2})?(?P<q>'''|\"\")")


def extract_tools_from_python(path: str, lines: List[str]) -> List[ToolRecord]:
    recs: List[ToolRecord] = []
    i = 0
    n = len(lines)
    while i < n:
        if PY_TOOL_DECORATOR_RE.match(lines[i]):
            # find next def
            j = i + 1
            while j < n and not lines[j].lstrip().startswith("def "):
                j += 1
            if j < n:
                m = re.match(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", lines[j])
                name = m.group(1) if m else None
                # Try to capture docstring following def
                k = j + 1
                desc = None
                if k < n and PY_TRIPLE_QUOTE_START_RE.match(lines[k]):
                    quote = PY_TRIPLE_QUOTE_START_RE.match(lines[k]).group("q")
                    k += 1
                    doc_lines = []
                    while k < n and not lines[k].strip().endswith(quote):
                        doc_lines.append(lines[k])
                        k += 1
                    if k < n:
                        # append line without closing quotes
                        closing_idx = lines[k].find(quote)
                        doc_lines.append(lines[k][:closing_idx])
                    desc = "\n".join([l.rstrip() for l in doc_lines]).strip() or None
                recs.append(
                    ToolRecord(
                        source_file=path,
                        kind="python_decorator",
                        name=name,
                        description=desc,
                        spec=None,
                        location=Location(file=path, line_start=i + 1, line_end=j + 1),
                    )
                )
                i = j
        i += 1
    return recs


MD_FENCE_RE = re.compile(r"^\s*```(?P<lang>[A-Za-z0-9_+-.]*)\s*$")
MD_HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*$")


def extract_readme_blocks(path: str, lines: List[str]) -> Tuple[List[ReadmeBlock], List[ToolRecord]]:
    blocks: List[ReadmeBlock] = []
    tools_from_md: List[ToolRecord] = []

    # Extract sections, focusing on those titled "Tools"
    i = 0
    n = len(lines)
    while i < n:
        m = MD_HEADING_RE.match(lines[i])
        if m:
            level = len(m.group("hashes"))
            title = m.group("title").strip()
            j = i + 1
            section_lines = []
            # collect until next heading of same or higher level
            while j < n:
                m2 = MD_HEADING_RE.match(lines[j])
                if m2 and len(m2.group("hashes")) <= level:
                    break
                section_lines.append(lines[j])
                j += 1

            section_text = "\n".join(section_lines)
            if title.lower() == "tools":
                # capture code fences within this section
                fence_blocks = list(extract_fenced_codeblocks(section_lines))
                blocks.append(
                    ReadmeBlock(
                        readme_path=path,
                        section=title,
                        content=section_text,
                        code_blocks=[{"lang": fb[0], "content": fb[1]} for fb in fence_blocks],
                        location=Location(file=path, line_start=i + 1, line_end=j),
                    )
                )
                # infer tools from code blocks if they look like JSON/YAML with tools
                for lang, content in fence_blocks:
                    if lang.lower() in {"json", ""}:
                        tools_from_md.extend(extract_tools_from_json(path, content, content.splitlines()))
                    elif lang.lower() in {"yaml", "yml"}:
                        # Heuristic: if content contains a top-level 'tools:' emit as a raw YAML tool block
                        if re.search(r"^tools\s*:", content, re.MULTILINE):
                            tools_from_md.append(
                                ToolRecord(
                                    source_file=path,
                                    kind="readme_block",
                                    name=None,
                                    description=None,
                                    spec=content,
                                    location=Location(file=path, line_start=i + 1, line_end=j),
                                )
                            )
            i = j
        else:
            i += 1

    # Also, capture standalone fenced code blocks anywhere in README that start with 'tools:' (YAML) or JSON arrays/objects
    for lang, content in extract_fenced_codeblocks(lines):
        if lang.lower() in {"json", ""}:
            tools_from_md.extend(extract_tools_from_json(path, content, content.splitlines()))
        elif lang.lower() in {"yaml", "yml"} and re.search(r"^tools\s*:", content, re.MULTILINE):
            tools_from_md.append(
                ToolRecord(
                    source_file=path,
                    kind="markdown_codeblock",
                    name=None,
                    description=None,
                    spec=content,
                    location=Location(file=path),
                )
            )

    return blocks, tools_from_md


def extract_fenced_codeblocks(lines: List[str]) -> Iterable[Tuple[str, str]]:
    i = 0
    n = len(lines)
    while i < n:
        m = MD_FENCE_RE.match(lines[i])
        if m:
            lang = (m.group("lang") or "").strip()
            i += 1
            block_lines = []
            while i < n and not lines[i].strip().startswith("```"):
                block_lines.append(lines[i])
                i += 1
            # skip closing fence line
            if i < n:
                i += 1
            yield (lang, "\n".join(block_lines))
        else:
            i += 1


YAML_TOOLS_RE = re.compile(r"(?m)^(tools\s*:\s*\n(?:^[ \t]+.+\n?)+)")


def extract_tools_from_yaml_text(path: str, text: str) -> List[ToolRecord]:
    recs: List[ToolRecord] = []
    for m in YAML_TOOLS_RE.finditer(text):
        yaml_snippet = m.group(1)
        recs.append(
            ToolRecord(
                source_file=path,
                kind="yaml_block",
                name=None,
                description=None,
                spec=yaml_snippet,
                location=Location(file=path),
            )
        )
    return recs


# -----------------------------
# Main scan logic
# -----------------------------


def is_readme_file(path: str) -> bool:
    base = os.path.basename(path)
    name, ext = os.path.splitext(base)
    return name in README_NAMES and ext in README_EXTS


def scan(root: str) -> ScanReport:
    tools: List[ToolRecord] = []
    readme_blocks: List[ReadmeBlock] = []

    for fp in iter_files(root):
        _, ext = os.path.splitext(fp)
        if is_readme_file(fp):
            text, lines = read_text_safely(fp)
            if not lines:
                continue
            blocks, md_tools = extract_readme_blocks(fp, lines)
            readme_blocks.extend(blocks)
            tools.extend(md_tools)
            # Also YAML heuristics in full text
            tools.extend(extract_tools_from_yaml_text(fp, text))
            continue

        if ext in MD_EXTS:
            text, lines = read_text_safely(fp)
            if not lines:
                continue
            # catch fenced code blocks with tools
            _, md_tools = extract_readme_blocks(fp, lines)
            tools.extend(md_tools)
            tools.extend(extract_tools_from_yaml_text(fp, text))
            continue

        if ext in JSON_EXTS:
            text, lines = read_text_safely(fp)
            if not lines and not text:
                continue
            tools.extend(extract_tools_from_json(fp, text, lines))
            continue

        if ext in YAML_EXTS:
            text, _ = read_text_safely(fp)
            if not text:
                continue
            tools.extend(extract_tools_from_yaml_text(fp, text))
            continue

        if ext in PY_EXTS:
            _, lines = read_text_safely(fp)
            if not lines:
                continue
            tools.extend(extract_tools_from_python(fp, lines))
            continue

    return ScanReport(root=os.path.abspath(root), tools=tools, readme_blocks=readme_blocks)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Scan a repo for adapter tools and README blocks")
    parser.add_argument("--root", default=".", help="Root directory to scan (default: .)")
    parser.add_argument("--out", default="adapter_metadata_report.json", help="Output JSON filepath")
    args = parser.parse_args(argv)

    report = scan(args.root)
    out_path = args.out
    try:
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    except Exception:
        pass
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report.to_json())
    print(f"Wrote {out_path} with {len(report.tools)} tools and {len(report.readme_blocks)} README blocks from {report.root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
