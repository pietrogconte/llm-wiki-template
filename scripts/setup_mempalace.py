#!/usr/bin/env python3
"""
Wire up MemPalace (https://github.com/MemPalace/mempalace) as an optional
cross-session memory layer for Claude Code, decoupled from the LLM Wiki
in this repo.

What this does:
  1. Installs the `mempalace` CLI if it isn't already on PATH (uv > pipx > pip).
  2. Merges Stop / SessionEnd / PreCompact hooks into your GLOBAL Claude Code
     settings (~/.claude/settings.json), using the native
     `mempalace hook run --hook <name> --harness claude-code` command - no
     shell scripts, so this works the same on Windows, Linux, and macOS.
  3. Appends a short, minimal recall note to your GLOBAL ~/.claude/CLAUDE.md
     (idempotent - safe to re-run).

What this deliberately does NOT do:
  - Mine any conversation history or project source files. That's a separate,
    explicit choice - run it yourself once you're happy with the setup:
        mempalace mine ~/.claude/projects/ --mode convos   # past conversations
        mempalace mine <some/project/dir>                  # project source files
  - Touch anything inside this wiki repo. MemPalace's palace lives at your
    OS-standard config path (e.g. ~/.config/mempalace on Linux/macOS,
    %USERPROFILE%\\.config\\mempalace on Windows), never inside a git repo.
  - Register the full MemPalace multi-agent "shared brain" rules block
    (MCP tools, task delegation, logstream watchers). That's a much bigger
    coordination protocol than "don't lose context between sessions" calls
    for - add it yourself later (`mempalace rules --help`) if you actually
    want multi-agent coordination.

Usage:
    python scripts/setup_mempalace.py            # do it
    python scripts/setup_mempalace.py --dry-run   # show what would change
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HOOK_COMMANDS = {
    "Stop": ("mempalace hook run --hook stop --harness claude-code", 30),
    "SessionEnd": ("mempalace hook run --hook session-end --harness claude-code", 10),
    "PreCompact": ("mempalace hook run --hook precompact --harness claude-code", 30),
}

RECALL_NOTE_MARKER = "<!-- llm-wiki-mempalace:mempalace-recall -->"
RECALL_NOTE = f"""{RECALL_NOTE_MARKER}
## Cross-session memory (MemPalace)

This machine has MemPalace installed (`mempalace` on PATH) for continuity
across long/restarted Claude Code sessions. Global hooks (Stop / SessionEnd /
PreCompact, in `~/.claude/settings.json`) already auto-save conversation
history — no manual action needed for that.

Use recall only when useful:
- If the user asks about something discussed in another session/project, or
  a decision/context you don't have in this conversation, run
  `mempalace search "<query>"` before saying you don't know.
- `mempalace wake-up` gives a broad summary of what's already been recorded.

Don't use this for anything beyond point-in-time recall — no multi-agent
coordination protocol is configured here.
{RECALL_NOTE_MARKER}
"""


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


def mempalace_available() -> bool:
    return shutil.which("mempalace") is not None


def install_mempalace(dry_run: bool) -> bool:
    if mempalace_available():
        print("[ok] mempalace already on PATH - skipping install.")
        return True

    candidates = [
        ("uv", ["uv", "tool", "install", "mempalace"]),
        ("pipx", ["pipx", "install", "mempalace"]),
        ("pip", [sys.executable, "-m", "pip", "install", "--user", "mempalace"]),
    ]
    for name, cmd in candidates:
        if shutil.which(name) is None and name != "pip":
            continue
        print(f"[..] trying install via {name}: {' '.join(cmd)}")
        if dry_run:
            print("     (dry-run, not actually running)")
            return True
        result = run(cmd)
        if result.returncode == 0:
            print(f"[ok] installed via {name}.")
            return True
        print(f"[!!] {name} install failed:\n{result.stderr.strip()}")

    print(
        "[!!] Could not install mempalace automatically. Install manually, e.g.:\n"
        "     uv tool install mempalace\n"
        "     (see https://github.com/MemPalace/mempalace for other options)"
    )
    return False


def backup(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = path.with_suffix(path.suffix + f".bak.{stamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def merge_hooks(settings_path: Path, dry_run: bool) -> None:
    settings: dict = {}
    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"[!!] {settings_path} is not valid JSON ({e}) - not touching it. Fix it by hand first.")
            return

    hooks = settings.setdefault("hooks", {})
    changed = False

    for event, (command, timeout) in HOOK_COMMANDS.items():
        entries = hooks.setdefault(event, [])
        already_present = any(
            h.get("type") == "command" and h.get("command") == command
            for entry in entries
            for h in entry.get("hooks", [])
        )
        if already_present:
            print(f"[ok] {event} hook already configured - leaving as is.")
            continue

        changed = True
        hook_def = {"type": "command", "command": command, "timeout": timeout}
        if event == "Stop":
            entries.append({"matcher": "*", "hooks": [hook_def]})
        else:
            entries.append({"hooks": [hook_def]})
        print(f"[+ ] adding {event} hook: {command}")

    if not changed:
        print("[ok] no changes needed in settings.json.")
        return

    if dry_run:
        print(f"[..] dry-run - would write {settings_path}")
        return

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    bak = backup(settings_path)
    if bak:
        print(f"[ok] backed up existing settings to {bak}")
    settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    print(f"[ok] wrote {settings_path}")


def append_recall_note(claude_md_path: Path, dry_run: bool) -> None:
    existing = claude_md_path.read_text(encoding="utf-8") if claude_md_path.exists() else ""
    if RECALL_NOTE_MARKER in existing:
        print(f"[ok] recall note already present in {claude_md_path} - leaving as is.")
        return

    if dry_run:
        print(f"[..] dry-run - would append recall note to {claude_md_path}")
        return

    claude_md_path.parent.mkdir(parents=True, exist_ok=True)
    with claude_md_path.open("a", encoding="utf-8") as f:
        if existing and not existing.endswith("\n"):
            f.write("\n")
        f.write("\n" + RECALL_NOTE + "\n")
    print(f"[ok] appended recall note to {claude_md_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing anything.")
    args = parser.parse_args()

    home = Path.home()
    settings_path = home / ".claude" / "settings.json"
    claude_md_path = home / ".claude" / "CLAUDE.md"

    print("== 1. mempalace CLI ==")
    ok = install_mempalace(args.dry_run)

    print("\n== 2. Claude Code hooks (global) ==")
    merge_hooks(settings_path, args.dry_run)

    print("\n== 3. Recall note (global CLAUDE.md) ==")
    append_recall_note(claude_md_path, args.dry_run)

    print("\n== Done ==")
    if args.dry_run:
        print("This was a dry run - nothing was written. Re-run without --dry-run to apply.")
    else:
        print(
            "Restart Claude Code for the hooks to take effect (hooks load once, at session "
            "start - this is a Claude Code limitation, not this script's).\n"
            "Optional next steps, run yourself when ready:\n"
            "  mempalace mine ~/.claude/projects/ --mode convos   # backfill past conversations\n"
            "  mempalace mine <project-dir>                       # index a project's source files\n"
        )
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
