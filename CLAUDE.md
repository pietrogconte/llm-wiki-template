# LLM Wiki — Schema & Instructions

This is an **LLM Wiki**: a persistent, interlinked markdown knowledge base that an LLM agent builds and maintains over time, based on the pattern described by Andrej Karpathy (see README for the source). Unlike plain RAG — which rediscovers knowledge from scratch on every query — the agent here **compiles synthesis once and keeps it current**: it updates entity pages, revises summaries, flags contradictions, and maintains cross-references as new sources come in.

> **Customize this file first.** Replace the `<domain>` placeholder below with what this wiki is actually about (personal knowledge, a research topic, a book companion, a team wiki, etc.), and rewrite the sections that don't fit your use case. This file is the schema — it should evolve with real usage, not stay generic.

**Domain**: home baking (bread, pizza, focaccia, panettone) — a **fictional example** wiki for the `example-en` branch of `llm-wiki-template`.

## Layers

1. **`raw/`** — immutable raw sources (articles, transcripts, PDFs, notes). The agent reads from here, never edits.
2. **`wiki/`** — markdown pages owned entirely by the agent. You read; the agent writes.
3. **This file (`CLAUDE.md`)** — the schema. Evolves as conventions get figured out.

## Directory structure

```
.
├── CLAUDE.md
├── AGENTS.md            # same content as CLAUDE.md, for Codex CLI / other agents
├── raw/
│   ├── assets/           # downloaded images (Obsidian attachment folder, if used)
│   └── ...               # original sources: transcripts, articles, PDFs, notes
└── wiki/
    ├── index.md          # catalog of all pages, updated on every ingest
    ├── log.md            # append-only chronological log
    ├── projects/         # one page per project / research thread
    ├── concepts/         # cross-cutting concepts/themes
    ├── entities/         # people, tools, papers, companies, models, etc.
    └── sources/          # one summary page per ingested source
```

Add categories as needed (e.g. `wiki/comparisons/`, `wiki/decisions/`) — update this section when you do.

## Page conventions (Obsidian-friendly)

YAML frontmatter on every new page:

```yaml
---
title: Page Name
tags:
  - some-tag
  - another-tag
date: YYYY-MM-DD
status: active | stale | archived
sources:
  - "[[YYYY-MM-DD Source title]]"
---
```

- Lists in the frontmatter use one item per line (`  - item`, two-space indent), the format Obsidian's Properties panel writes, so opening a page in Obsidian produces no diff. An empty list stays `[]`. Wikilinks in lists go in double quotes. No duplicate items (the linter flags them).
- Internal links use wikilinks: `[[Page Name]]`.
- Filename = page title.
- Images referenced via `raw/assets/`.

## Provenance (optional)

Useful when the wiki records decisions made in conversations with an agent. Mark claims on project pages with a legend and put it at the top of the page:

> **Legend:** ✅ decided/done by the user · 💡 suggested by the agent (not confirmed) · 🔎 verified in the local environment (with date).

- An agent suggestion the user did not confirm is never a "decision" — keep it under 💡 / open options.
- When the user states where an item came from, that statement prevails.

Delete this section if you don't need it.

## Operations

### Ingest

When a new source lands in `raw/`:

1. Read the source.
2. Discuss key takeaways with the user (unless bulk/unsupervised ingest was explicitly requested).
3. Create/update the summary page in `wiki/sources/`.
4. Update affected project/concept/entity pages — one source can touch many pages.
5. Update `wiki/index.md`.
6. Append to `wiki/log.md`:
   `## [YYYY-MM-DD] ingest | Source title`

### Query

1. Read `wiki/index.md` to locate relevant pages.
2. Read those pages.
3. Synthesize an answer, citing source pages.
4. If the answer has lasting value (a comparison, an analysis, a new connection), offer to file it as a new wiki page.
5. Log to `wiki/log.md`:
   `## [YYYY-MM-DD] query | Summarized question`

### Lint

When asked, check for:

- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages (no inbound links)
- Concepts mentioned but lacking their own page
- Missing cross-references
- Gaps that could be filled with a web search

The mechanical checks (broken links, empty files, pages missing from the index, incomplete frontmatter, wikilink examples outside backticks in docs, raw sources with no ingest) are automated in `scripts/lint_wiki.py` — run `python scripts/lint_wiki.py` first, then do the semantic checks above.

Log to `wiki/log.md`:
`## [YYYY-MM-DD] lint | Summary of what was found/fixed`

## Optional: MemPalace for session continuity

This template can pair with [MemPalace](https://github.com/MemPalace/mempalace) — a separate, third-party memory tool — for **cross-session recall** (so a long-running or restarted agent session doesn't lose context). It is intentionally decoupled from the wiki:

- MemPalace auto-saves conversation transcripts via Claude Code hooks (global, machine-level — see [mempalace-setup](https://github.com/pietrogconte/mempalace-setup)).
- The wiki's Ingest/Query/Lint operations above are unaffected either way — MemPalace is a recall aid, not a replacement for the curated synthesis in `wiki/`.
- If installed, use `mempalace search "<query>"` (or `<tool venv python> -m mempalace search "<query>"` if the launcher is blocked, e.g. by Windows Smart App Control) when you need to recall something from a past session that isn't in this wiki yet. Don't use it as a substitute for `wiki/index.md` when answering questions about content *already* in the wiki.

If you didn't set up MemPalace, ignore this section entirely — the wiki works standalone.

## Git

State your own git policy here — for example: *"Never run git commands automatically; always hand the user the exact command to run themselves."* (This is optional — some users are fine with the agent committing directly. Pick what you want and delete this note.)

## Style

- Content language: English.
- Be factual; cite the source page for non-trivial claims.
- Prefer lists and tables when they help compare information.
- No filler: pages should be dense with information, not prose padding.
