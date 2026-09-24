# llm-wiki-mempalace

[Português](README.md) | **English**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

A ready-to-use template for instantiating an **LLM Wiki**: a persistent, interlinked markdown knowledge base maintained by an LLM agent (Claude Code, Codex, etc.), instead of a RAG that rederives everything on every query. Includes a generic schema (`CLAUDE.md`/`AGENTS.md`) and, optionally, a script to wire up [MemPalace](https://github.com/MemPalace/mempalace) as a cross-session memory layer.

## The idea

Most RAG experiences (NotebookLM, ChatGPT file uploads, etc.) retrieve relevant chunks at query time but accumulate nothing — any subtle question that requires synthesizing several documents forces the LLM to rebuild everything from scratch.

Here the logic is different: the agent **builds and maintains a persistent wiki**. When it processes a new source, it doesn't just index it — it reads it, extracts what matters, and integrates it into the existing wiki: updates entity pages, revises summaries, flags where new data contradicts old claims. Knowledge is compiled once and **kept current**, not re-derived on every query.

Idea originally described by Andrej Karpathy in the [`llm-wiki.md` gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). This repository is a ready-to-use implementation of the pattern, plus the optional MemPalace integration we tested and documented.

## Structure

```
.
├── CLAUDE.md             # schema — how the agent maintains the wiki (edit for your domain)
├── AGENTS.md             # same content, for Codex CLI / other harnesses
├── raw/
│   ├── assets/            # locally downloaded images (Obsidian attachment folder, if used)
│   └── ...                # original sources: transcripts, articles, PDFs, notes
├── wiki/
│   ├── index.md           # catalog of all pages
│   ├── log.md              # append-only chronological log
│   ├── projects/
│   ├── concepts/
│   ├── entities/
│   └── sources/
└── scripts/
    └── setup_mempalace.py # optional — see MemPalace section below
```

## Quickstart

1. Use this repository as a template ("Use this template" button on GitHub) or clone it and drop the git history.
2. Open `CLAUDE.md` and replace the `<domain>` placeholder — describe what this wiki will track (personal research, a topic, a book, a team, etc.) and adjust the sections that don't fit your case.
3. (Optional) Open the folder in Obsidian as a vault — the schema already uses YAML frontmatter and `[[Page]]` wikilinks.
4. Drop the first source into `raw/` and ask the agent to run the **Ingest** flow described in `CLAUDE.md`.

## MemPalace (optional, cross-session memory)

The wiki works standalone — MemPalace is an additional layer, deliberately **decoupled**: it solves "don't lose context across long sessions / agent restarts," never "how the wiki should answer questions."

### How the two pieces fit together

| | `wiki/` (this repo) | MemPalace |
|---|---|---|
| What it holds | **Curated** synthesis — only what the agent decided was worth turning into a page | **Verbatim** history of everything — every conversation, unfiltered |
| Where it lives | Inside this repository, versioned in git | Outside any repo, in a single per-machine "palace" (`~/.config/mempalace`), **shared across all your projects** — not one palace per wiki |
| Do you read it directly? | Yes — it's markdown, opens in Obsidian, it's the actual deliverable | No — it's a search (`mempalace search`), not a place you browse |
| When the agent uses it | Always, to answer anything **already** documented in the wiki (`wiki/index.md`) | Only when context is missing that never made it into a page yet — e.g. "what did we discuss about X last week?" |

In practice: the wiki is the "finished version" you cultivate; MemPalace is a safety net that keeps you from losing what hasn't been promoted to a page yet. A source can go straight into the wiki (the Ingest flow) without ever touching MemPalace, and a conversation can stay in MemPalace forever if nothing in it was worth turning into a page.

**Heads up if you instantiate this template more than once:** every repo on the same machine that runs `setup_mempalace.py` lands in the *same* palace (`~/.config/mempalace`) — it's not an isolated database per wiki. If you spin up a second wiki from this template (a different domain, a different project) and run the setup there too, both will share the same memory, and a search from one can surface content from the other. If you need real isolation between wikis, point `palace_path` at a different location for each one (see MemPalace's `config.json`), or use separate machines/profiles.

```
python scripts/setup_mempalace.py --dry-run   # preview changes
python scripts/setup_mempalace.py             # apply
```

The script:
- Installs the `mempalace` CLI if not already available (`uv` → `pipx` → `pip`, whichever exists).
- Configures global Claude Code hooks (`Stop`/`SessionEnd`/`PreCompact`) using the native `mempalace hook run` command — no `.sh` scripts involved, so it works the same on Windows/Linux/macOS.
- Appends a minimal recall note to your global `~/.claude/CLAUDE.md` (idempotent).

What it deliberately does **not** do automatically (your call, whenever you want it):
```
mempalace mine ~/.claude/projects/ --mode convos   # mine past conversations
mempalace mine <project-dir>                        # mine a project's source/docs
```

It also doesn't register the `mempalace rules` block (the full multi-agent coordination protocol, MCP with 45 tools) — that's a much bigger scope than "memory across sessions," and would add coupling this template intentionally avoids. If you want that, it's a separate decision (`mempalace rules --help`).

## Credits

- LLM Wiki pattern: Andrej Karpathy.
- MemPalace: [MemPalace/mempalace](https://github.com/MemPalace/mempalace) (MIT).
- This template was put together with [Claude Code](https://claude.com/claude-code).

## License

MIT — see [LICENSE](LICENSE).
