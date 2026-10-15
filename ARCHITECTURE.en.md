# Architecture

[Português](ARCHITECTURE.md) | **English**

How an LLM Wiki works: the layers, the operations the agent runs, the schema conventions, and why you'd keep a wiki instead of doing RAG alone.

## Layers

```
 sources                synthesis                rules
┌──────────┐  Ingest  ┌──────────────┐        ┌──────────────────┐
│  raw/    │ ───────▶ │    wiki/     │ ◀───── │ CLAUDE.md        │
│immutable │          │ agent-owned  │        │ AGENTS.md        │
└──────────┘          └──────────────┘        │ (schema)         │
                        ▲        │             └──────────────────┘
                 Lint   │        │ Query
                        └────────┴──▶ answers with citations
```

| Layer | Who writes it | What it holds |
|---|---|---|
| `raw/` | you | Original sources (articles, transcripts, PDFs, notes), **immutable**. The agent only reads. Attachments in `raw/assets/` |
| `wiki/` | the agent | Markdown pages: `projects/`, `concepts/`, `entities/`, `sources/`, plus `index.md` and `log.md` |
| `CLAUDE.md` / `AGENTS.md` | you + the agent | The schema: domain, structure, conventions and operations. It evolves with use. Both files hold the same content (Claude Code reads one, Codex and other harnesses read the other) |

## Operations

**Ingest:** a new source lands in `raw/`.
1. The agent reads the source and discusses the key points with you (unless you ask for a bulk ingest).
2. It creates the source page in `wiki/sources/`.
3. It updates the affected pages. One source can touch many.
4. It updates `wiki/index.md` and appends a `## [YYYY-MM-DD] ingest | Title` entry to `wiki/log.md`.

**Query:** you ask a question.
1. The agent finds the pages through `index.md` and reads them.
2. It answers citing the source pages.
3. If the answer has lasting value (a comparison, an analysis, a new connection), it offers to file it as a page.
4. It logs the query in `log.md`.

**Lint:** maintenance. It has two halves:

| Kind | Who does it | Examples |
|---|---|---|
| Mechanical | `scripts/lint_wiki.py` (optional hook + CI) | broken links, empty `.md`, page missing from the index, frontmatter, extensionless link, `[[link]]` example outside backticks, duplicate frontmatter list item, source with no ingest |
| Semantic | the agent, when you ask | contradictions between pages, claims superseded by newer sources, orphan pages, concepts without a page, missing cross-references |

## Schema and conventions

- **YAML frontmatter** on every wiki page: `title`, `tags`, `date` (YYYY-MM-DD), `status` (`active`/`stale`/`archived`), `sources`. Lists one item per line, as Obsidian writes them (empty list: `[]`).
- **Wikilinks** in the `[[Page]]` format, with filename = page title. Obsidian-compatible.
- **`index.md`** is the catalog: every page must be in it. It's where the agent (and you) start.
- **`log.md`** is append-only: every ingest, query, lint and setup becomes a dated entry.
- **Provenance (optional):** ✅ decided by you · 💡 suggested by the agent (not a decision) · 🔎 verified in the environment. It keeps an agent suggestion from turning into a "decision" over time.
- **New folders** (e.g. `comparisons/`, `decisions/`) are welcome: record them in the schema when you add them.

## Why a wiki, not just RAG

| | RAG | LLM Wiki |
|---|---|---|
| When it synthesizes | on every question | once, at ingest, then maintained |
| What accumulates | nothing (a chunk index) | revised pages, links, flagged contradictions |
| Cost per question | retrieve and re-synthesize | read a few already-synthesized pages |
| Auditable | hard (loose chunks) | yes: markdown versioned in git, with cited sources and a log |
| Weak spot | questions spanning many sources | needs maintenance discipline (hence the linter) |

The two don't exclude each other: the wiki can be the curated layer on top of a search over the raw sources.

## Surrounding tools

- **Linter** (`scripts/lint_wiki.py`): stdlib only, read-only. Run it by hand, through the optional hook (`git config core.hooksPath .githooks`), or in CI (Python 3.9 and 3.12). Details in the [README](README.en.md#lint).
- **Obsidian preset** (`obsidian-preset/`): optional. Wikilinks, attachments in `raw/assets`, links updated on rename, and a graph colored by folder. The real `.obsidian/` is never versioned.
- **`example` / `example-en` branches**: a complete fictional wiki to see the schema applied. `main` gets no example pages.
- **MemPalace** (optional, external): recall of conversation history across sessions. It doesn't replace the wiki.
