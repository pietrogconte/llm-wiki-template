# llm-wiki-template

[Português](README.md) | **English**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/pietrogconte/llm-wiki-template/blob/main/LICENSE)

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
3. (Optional) Open the folder in Obsidian as a vault (see [Using with Obsidian](#using-with-obsidian)).
4. Drop the first source into `raw/` and ask the agent to run the **Ingest** flow described in `CLAUDE.md`.

## Using with Obsidian

Obsidian makes a good reader for the wiki: the agent writes, you read and navigate.

1. **Install (Windows):** `winget install --id Obsidian.Obsidian -e --source winget`. The installer is digitally signed (Dynalist Inc), so Smart App Control doesn't block it.
2. **Open the repo root as the vault** (*Open folder as vault*), not just `wiki/`. Pages link into `raw/` (sources and attachments in `raw/assets/`), and `CLAUDE.md` stays at hand. `.obsidian/` is already in `.gitignore`.
3. **Settings** (*Settings → Files and links*): **Use `[[Wikilinks]]`** on; attachments in `raw/assets`; **Automatically update internal links** on. Renaming a page counts as a manual edit (see item 6).
4. **Navigation:** start at `wiki/index.md` (the catalog); `wiki/log.md` has the history. Use the Quick Switcher (`Ctrl+O`), search (`Ctrl+Shift+F`), the **backlinks** pane, **Graph View** (`Ctrl+G`) and the local graph (`Ctrl+P` → "Open local graph"). Frontmatter shows up as *Properties*; click a tag to list the pages that have it. Careful: clicking a link to a page that doesn't exist creates an empty file.
5. **How to read it:** `projects/` holds one project or research thread per page; `concepts/` and `entities/` hold what appears in 2+ projects; `sources/` has one summary per source; `raw/` keeps the original, immutable sources. If your schema marks provenance, for example ✅ decided by you, 💡 suggested by the agent and 🔎 verified, put the legend at the top of the pages.
6. **Workflow:** the agent writes the wiki (Ingest, Query and Lint, per `CLAUDE.md`). If you edit something by hand, commit it from the terminal and tell the agent next session. Never edit `raw/`.
7. **Git from the terminal:**
   ```bash
   git status
   git add -A
   git diff --cached   # review what's going in (no secrets)
   git commit -m "Describe the change"
   git push
   ```
   Community plugins (including *Obsidian Git*) are third-party code with access to the whole vault. Keep **Restricted mode** on and only install something after reviewing it.
8. **Asking the wiki:** ask the agent for a **Query**, naming the relevant pages (e.g. "Run a Query about X, considering `[[Page A]]` and `[[Page B]]`"). It answers with citations, logs the query in `log.md`, and offers to turn answers of lasting value into a new page.

## Optional: cross-session memory

The wiki works standalone. If you want the agent not to lose context across long sessions or restarts, you can pair it with [MemPalace](https://github.com/MemPalace/mempalace) — which is set up once per machine, not per wiki: see [pietrogconte/mempalace-setup](https://github.com/pietrogconte/mempalace-setup). The wiki stays the curated synthesis; MemPalace is just recall over your conversation history.

## Credits

- LLM Wiki pattern: Andrej Karpathy.
- This template was put together with [Claude Code](https://claude.com/claude-code).

## License

MIT — see the `LICENSE` file at the repository root.
