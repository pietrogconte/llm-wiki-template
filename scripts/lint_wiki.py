#!/usr/bin/env python3
"""Mechanical lint for an LLM Wiki (pure Python 3.9+, standard library only).

Read-only: it never writes to the repository.

Errors (exit code 1):
  E1  broken [[wikilink]]
  E2  empty .md file
  E3  wiki page not linked from wiki/index.md
  E4  missing or incomplete frontmatter on a wiki page
  E5  relative markdown link to a file without extension (Obsidian would
      create an empty "<name>.md" when clicked) or to a missing .md file
  E6  [[wikilink]] example outside backticks in a doc (README, CLAUDE, ...)

Warnings (exit code 0, or 1 with --strict):
  W1  file in raw/ not mentioned in wiki/log.md or wiki/sources/ (no ingest?)

Usage:
  python scripts/lint_wiki.py [--root PATH] [--strict]
"""

import argparse
import os
import re
import sys
import unicodedata
from collections import defaultdict
from urllib.parse import unquote

SKIP_DIRS = {".git", ".obsidian", ".venv", "venv", "node_modules", "obsidian-preset", "__pycache__"}
REQUIRED_KEYS = ("title", "tags", "date", "status", "sources")
STATUSES = {"active", "stale", "archived"}

CHECKS = {
    "E1": "broken wikilink",
    "E2": "empty markdown file",
    "E3": "wiki page missing from wiki/index.md",
    "E4": "missing or incomplete frontmatter",
    "E5": "bad relative markdown link",
    "E6": "wikilink example outside backticks in a doc",
    "W1": "raw source with no ingest in log/sources",
}

WIKILINK_RE = re.compile(r"!?\[\[([^\[\]]+?)\]\]")
MDLINK_RE = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def norm(text):
    return unicodedata.normalize("NFC", text).casefold()


def rel(path, root):
    return os.path.relpath(path, root).replace(os.sep, "/")


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            yield os.path.join(dirpath, name)


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def strip_code(text):
    """Return the lines of text with fenced blocks and inline code blanked."""
    lines = text.splitlines()
    out = []
    fence = None
    for line in lines:
        m = FENCE_RE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            out.append("")
            continue
        if m:
            fence = m.group(1)
            out.append("")
            continue
        out.append(INLINE_CODE_RE.sub("", line))
    return out


def wikilink_target(inner):
    target = inner.split("|", 1)[0].rstrip("\\")
    target = target.split("#", 1)[0].strip()
    if norm(target).endswith(".md"):
        target = target[:-3]
    return target


def parse_frontmatter(text):
    """Return a dict of top-level keys, or None if there is no frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    keys = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return keys
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            keys[m.group(1)] = m.group(2).strip().strip("\"'")
    return None  # unterminated block


class Linter:
    def __init__(self, root):
        self.root = root
        self.findings = defaultdict(list)
        self.md_files = []
        self.md_stems = set()
        self.md_paths = set()
        self.other_names = set()
        self.other_paths = set()
        for path in walk(root):
            r = rel(path, root)
            if r.lower().endswith(".md"):
                self.md_files.append(path)
                self.md_stems.add(norm(os.path.basename(r)[:-3]))
                self.md_paths.add(norm(r[:-3]))
            else:
                self.other_names.add(norm(os.path.basename(r)))
                self.other_paths.add(norm(r))

    def add(self, code, path, line, message):
        self.findings[code].append((rel(path, self.root), line, message))

    def resolves(self, target):
        t = norm(target).replace("\\", "/").lstrip("/")
        if t in self.md_stems or t in self.md_paths:
            return True
        if t in self.other_names or t in self.other_paths:
            return True
        return any(p.endswith("/" + t) for p in self.md_paths)

    def run(self):
        for path in self.md_files:
            r = rel(path, self.root)
            if r.startswith("raw/"):
                continue
            text = read(path)
            if not text.strip():
                self.add("E2", path, 1, "file is empty")
                continue
            is_wiki = r.startswith("wiki/")
            for lineno, line in enumerate(strip_code(text), 1):
                for m in WIKILINK_RE.finditer(line):
                    target = wikilink_target(m.group(1))
                    if not target:
                        continue
                    if not is_wiki:
                        self.add("E6", path, lineno, "%s should be in backticks" % m.group(0))
                    elif not self.resolves(target):
                        self.add("E1", path, lineno, "[[%s]] does not match any file" % target)
                for m in MDLINK_RE.finditer(line):
                    self.check_mdlink(path, lineno, m.group(1))
            if is_wiki and r not in ("wiki/index.md", "wiki/log.md"):
                self.check_frontmatter(path, text)
        self.check_index()
        self.check_raw()

    def check_mdlink(self, path, lineno, target):
        if "://" in target or target.startswith(("#", "mailto:", "tel:")):
            return
        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not target:
            return
        base = self.root if target.startswith("/") else os.path.dirname(path)
        full = os.path.normpath(os.path.join(base, target.lstrip("/")))
        if target.endswith("/") or os.path.isdir(full):
            return
        ext = os.path.splitext(os.path.basename(target))[1]
        if not ext:
            self.add("E5", path, lineno,
                     "(%s) has no extension; Obsidian creates an empty '%s.md' when clicked "
                     "(use an absolute URL or plain text)" % (target, os.path.basename(target)))
        elif ext.lower() == ".md" and not os.path.isfile(full):
            self.add("E5", path, lineno, "(%s) points to a missing file" % target)

    def check_frontmatter(self, path, text):
        fm = parse_frontmatter(text)
        if fm is None:
            self.add("E4", path, 1, "no YAML frontmatter (--- block at the top)")
            return
        missing = [k for k in REQUIRED_KEYS if k not in fm]
        if missing:
            self.add("E4", path, 1, "missing keys: %s" % ", ".join(missing))
        if "title" in fm and not fm["title"]:
            self.add("E4", path, 1, "empty title")
        if "date" in fm and not DATE_RE.match(fm["date"]):
            self.add("E4", path, 1, "date '%s' is not YYYY-MM-DD" % fm["date"])
        if "status" in fm and fm["status"] not in STATUSES:
            self.add("E4", path, 1, "status '%s' not in %s" % (fm["status"], "/".join(sorted(STATUSES))))

    def check_index(self):
        wiki_pages = [p for p in self.md_files if rel(p, self.root).startswith("wiki/")
                      and rel(p, self.root) not in ("wiki/index.md", "wiki/log.md")]
        index = os.path.join(self.root, "wiki", "index.md")
        if not os.path.isfile(index):
            if wiki_pages:
                self.add("E3", index, 1, "wiki/index.md not found")
            return
        linked = set()
        for line in strip_code(read(index)):
            for m in WIKILINK_RE.finditer(line):
                linked.add(norm(wikilink_target(m.group(1))))
        for path in wiki_pages:
            r = rel(path, self.root)
            stem, noext = norm(os.path.basename(r)[:-3]), norm(r[:-3])
            if stem not in linked and noext not in linked:
                self.add("E3", path, 1, "not linked from wiki/index.md")

    def check_raw(self):
        raw = os.path.join(self.root, "raw")
        if not os.path.isdir(raw):
            return
        haystack = []
        log = os.path.join(self.root, "wiki", "log.md")
        if os.path.isfile(log):
            haystack.append(read(log))
        sources = os.path.join(self.root, "wiki", "sources")
        if os.path.isdir(sources):
            haystack.extend(read(p) for p in walk(sources) if p.lower().endswith(".md"))
        haystack = norm("\n".join(haystack))
        for path in walk(raw):
            r = rel(path, self.root)
            name = os.path.basename(r)
            if r.startswith("raw/assets/") or name.startswith("."):
                continue
            stem = os.path.splitext(name)[0]
            if norm(stem) not in haystack and norm(r) not in haystack:
                self.add("W1", path, 1, "not mentioned in wiki/log.md or wiki/sources/ (ingest pending?)")


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Mechanical lint for an LLM Wiki (read-only).")
    parser.add_argument("--root", default=".", help="wiki repository root (default: current dir)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print("error: --root %s is not a directory" % args.root, file=sys.stderr)
        return 2

    linter = Linter(root)
    linter.run()

    errors = sum(len(v) for k, v in linter.findings.items() if k.startswith("E"))
    warnings = sum(len(v) for k, v in linter.findings.items() if k.startswith("W"))
    for code in CHECKS:
        items = linter.findings.get(code)
        if not items:
            continue
        print("%s %s (%d)" % (code, CHECKS[code], len(items)))
        for r, line, message in sorted(items):
            print("  %s:%d: %s" % (r, line, message))
        print()
    print("%d markdown files checked: %d error(s), %d warning(s)"
          % (len(linter.md_files), errors, warnings))
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
