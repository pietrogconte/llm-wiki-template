# llm-wiki-template

[Português](README.md) | **English**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A ready-to-use template for instantiating an **LLM Wiki**: a persistent, interlinked markdown knowledge base maintained by an LLM agent (Claude Code, Codex, etc.), instead of a RAG that rederives everything on every query. Includes a generic schema (`CLAUDE.md`/`AGENTS.md`) and the folder structure, ready to go.

## The idea

Most RAG experiences (NotebookLM, ChatGPT file uploads, etc.) retrieve relevant chunks at query time but accumulate nothing — any subtle question that requires synthesizing several documents forces the LLM to rebuild everything from scratch.

Here the logic is different: the agent **builds and maintains a persistent wiki**. When it processes a new source, it doesn't just index it — it reads it, extracts what matters, and integrates it into the existing wiki: updates entity pages, revises summaries, flags where new data contradicts old claims. Knowledge is compiled once and **kept current**, not re-derived on every query.

Idea originally described by Andrej Karpathy in the [`llm-wiki.md` gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). This repository is a ready-to-use implementation of the pattern.

## Structure

```
.
├── CLAUDE.md             # schema — how the agent maintains the wiki (edit for your domain)
├── AGENTS.md             # same content, for Codex CLI / other harnesses
├── raw/
│   ├── assets/            # locally downloaded images (Obsidian attachment folder, if used)
│   └── ...                # original sources: transcripts, articles, PDFs, notes
└── wiki/
    ├── index.md           # catalog of all pages
    ├── log.md              # append-only chronological log
    ├── projects/
    ├── concepts/
    ├── entities/
    └── sources/
```

## Quickstart

1. Use this repository as a template ("Use this template" button on GitHub) or clone it and drop the git history.
2. Open `CLAUDE.md` and replace the `<domain>` placeholder — describe what this wiki will track (personal research, a topic, a book, a team, etc.) and adjust the sections that don't fit your case.
3. (Optional) Open the folder in Obsidian as a vault — the schema already uses YAML frontmatter and `[[Page]]` wikilinks.
4. Drop the first source into `raw/` and ask the agent to run the **Ingest** flow described in `CLAUDE.md`.

## Optional: cross-session memory

The wiki works standalone. If you want the agent not to lose context across long sessions or restarts, you can pair it with [MemPalace](https://github.com/MemPalace/mempalace) — which is set up once per machine, not per wiki: see [pietrogconte/mempalace-setup](https://github.com/pietrogconte/mempalace-setup). The wiki stays the curated synthesis; MemPalace is just recall over your conversation history.

## Credits

- LLM Wiki pattern: Andrej Karpathy.
- This template was put together with [Claude Code](https://claude.com/claude-code).

## License

MIT — see [LICENSE](LICENSE).
