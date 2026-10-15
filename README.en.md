# llm-wiki-template

[Português](README.md) | **English**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/pietrogconte/llm-wiki-template/blob/main/LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Lint](https://github.com/pietrogconte/llm-wiki-template/actions/workflows/lint.yml/badge.svg)](https://github.com/pietrogconte/llm-wiki-template/actions/workflows/lint.yml)

A ready-to-use template for an **LLM Wiki**: a persistent, interlinked markdown knowledge base **maintained by an LLM agent** (Claude Code, Codex, etc.) instead of a RAG that rederives everything on every query. It ships with a generic schema (`CLAUDE.md`/`AGENTS.md`), the folder structure, a wiki linter (optional hook + CI), an optional Obsidian preset, and a complete example wiki on a separate branch.

## Screenshots

<p align="center">
  <img src="docs/img/graph.png" alt="Obsidian Graph View with the preset: nodes colored by wiki folder" width="49%">
  <img src="docs/img/legend.png" alt="Project page with the ✅ 💡 🔎 provenance legend" width="49%">
</p>

<p align="center"><sub>Fictional wiki from the <a href="https://github.com/pietrogconte/llm-wiki-template/tree/example"><code>example</code></a> branch (Portuguese), opened in Obsidian with this repo's preset.</sub></p>

## What it is

Most RAG workflows (NotebookLM, file uploads in ChatGPT, etc.) retrieve chunks at question time and accumulate nothing: every question that needs several sources forces the LLM to rebuild the synthesis from scratch.

Here the agent **builds and maintains a wiki**. For each new source it reads, extracts what matters and integrates it into the existing wiki: it updates project, concept and entity pages, revises summaries and flags contradictions with what was already written. Knowledge is compiled once and **kept current**.

The idea comes from Andrej Karpathy ([`llm-wiki.md` gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)); this repo is a ready-to-use implementation. Layers, operations and design decisions are in [ARCHITECTURE.en.md](ARCHITECTURE.en.md).

## Quickstart

1. **Create your repo** from this one ("Use this template" on GitHub) and clone it.
2. **Edit `CLAUDE.md`**: replace the `<domain>` placeholder with what the wiki will track and delete what doesn't fit. Keep `AGENTS.md` identical (for Codex and other harnesses).
3. **Drop the first source** into `raw/` (article, transcript, PDF, note).
4. **Ask the agent for an Ingest** (e.g. "ingest `raw/my-source.md`"). It creates the source page, updates the affected pages, `wiki/index.md` and `wiki/log.md`.
5. **Read and ask**: browse the wiki (in Obsidian, if you like) and ask the agent for **Queries**. Run `python scripts/lint_wiki.py` now and then, or enable the hook (see [Lint](#lint)).

### Structure

```
.
├── CLAUDE.md / AGENTS.md   # schema: how the agent maintains the wiki
├── raw/                    # original, immutable sources (attachments in raw/assets/)
├── wiki/
│   ├── index.md            # catalog of every page
│   ├── log.md              # append-only chronological log
│   ├── projects/  concepts/  entities/  sources/
├── scripts/lint_wiki.py    # wiki linter (stdlib only)
├── .githooks/pre-commit    # optional hook that runs the linter
├── obsidian-preset/        # optional Obsidian settings
└── docs/img/               # README images
```

## Using with Obsidian

Obsidian makes a good reader for the wiki: the agent writes, you read and navigate.

- **Install (Windows):** `winget install --id Obsidian.Obsidian -e --source winget`. The installer is digitally signed (Dynalist Inc), so Smart App Control doesn't block it.
- **Open the repo root as the vault** (*Open folder as vault*), not just `wiki/`: pages link into `raw/`, and `CLAUDE.md` stays at hand. `.obsidian/` is in `.gitignore`.
- **Navigation:** start at `wiki/index.md`; `wiki/log.md` is the history. Use the Quick Switcher (`Ctrl+O`), search (`Ctrl+Shift+F`), backlinks, Graph View (`Ctrl+G`) and the local graph (`Ctrl+P` → "Open local graph"). Careful: clicking a link to a page that doesn't exist creates an empty file (the linter catches it).
- **Workflow:** the agent writes (Ingest, Query, Lint). If you edit by hand, commit from the terminal and tell the agent next session. Never edit `raw/`.
- **Community plugins** (including *Obsidian Git*) are third-party code with access to the whole vault: keep **Restricted mode** on and only install something after reviewing it. The terminal is enough for git.

### Optional preset

The `obsidian-preset/` folder is a starting point. It is **optional**: you don't need it to use the wiki.

- `app.json`: `[[wikilinks]]` link format, attachments in `raw/assets`, auto-update links on rename, and the inline title turned off (pages already have their own H1, so it would duplicate the title).
- `graph.json`: the graph hides `index`, `log`, `CLAUDE`, `AGENTS` and the repo docs, and colors nodes by folder (projects, concepts, entities, sources and the `raw/` notes).

Copy it into `.obsidian/` **before opening the vault** (or with Obsidian closed, since it overwrites existing settings):

```powershell
# Windows (PowerShell), at the repo root
New-Item -ItemType Directory -Force .obsidian | Out-Null; Copy-Item obsidian-preset\*.json .obsidian\
```
```bash
# Linux/macOS, at the repo root
mkdir -p .obsidian && cp obsidian-preset/*.json .obsidian/
```

Then adjust anything you like in Obsidian's settings; the preset doesn't lock you in.

## Lint

`scripts/lint_wiki.py` runs the **mechanical** checks. It uses only the standard library (Python 3.9+), only reads files, and exits non-zero on errors:

```bash
python scripts/lint_wiki.py            # warnings don't fail
python scripts/lint_wiki.py --strict   # warnings fail too
python scripts/lint_wiki.py --root ../another-wiki
```

| Code | Check |
|---|---|
| E1 | broken `[[link]]` |
| E2 | empty `.md` |
| E3 | wiki page missing from `wiki/index.md` |
| E4 | missing or incomplete frontmatter (`title`, `tags`, `date`, `status`, `sources`) |
| E5 | relative markdown link to a file without extension (Obsidian would create an empty `.md`) or to a missing `.md` |
| E6 | `[[link]]` example outside backticks in docs (README, CLAUDE, etc.) |
| E7 | duplicate item in a frontmatter list (`tags`, `sources`, etc.), flow or block |
| W1 | warning: file in `raw/` not mentioned in `log.md` or `wiki/sources/` (ingest pending?) |

The **semantic** checks (contradictions, stale claims, missing cross-references) remain the agent's **Lint** operation, described in `CLAUDE.md`.

<details>
<summary><strong>Optional pre-commit hook and CI (click to expand)</strong></summary>

**Hook.** Enable it once per clone; disable it whenever you want:

```bash
git config core.hooksPath .githooks          # enable
git config --unset core.hooksPath            # disable
```

The hook is an `sh` script run by Git itself: no `.bat` or `.ps1`, which Windows Smart App Control blocks. It tries `py -3`, `python3` and `python`, in that order, and only uses an interpreter that actually runs (the Microsoft Store alias, which opens the store, is skipped). If none is found, it warns and **lets the commit through**.

**CI.** The `.github/workflows/lint.yml` workflow runs the linter on every push and pull request, on Python 3.9 and 3.12.

</details>

## Example wiki

`main` ships empty, ready for your own wiki. To see a complete wiki that follows the schema — 4 projects, 6 hub concepts, 4 entities, 10 sources, index, log and the provenance legend — check out the example branches. The content is fictional and passes the linter:

| Branch | Language |
|---|---|
| [`example`](https://github.com/pietrogconte/llm-wiki-template/tree/example) | Portuguese |
| [`example-en`](https://github.com/pietrogconte/llm-wiki-template/tree/example-en) | English |

```bash
git clone -b example-en https://github.com/pietrogconte/llm-wiki-template.git llm-wiki-example
```

## Optional: cross-session memory

The wiki works standalone. If you want the agent not to lose context across long sessions or restarts, you can pair it with [MemPalace](https://github.com/MemPalace/mempalace), which is set up once per machine, not per wiki: see [pietrogconte/mempalace-setup](https://github.com/pietrogconte/mempalace-setup). The wiki stays the curated synthesis; MemPalace is just recall over your conversation history.

## Contributing

Suggestions, fixes and pull requests are welcome. Open an issue describing the problem or improvement before larger changes, and run `python scripts/lint_wiki.py` before submitting. Version history in [CHANGELOG.md](CHANGELOG.md).

## Credits

- LLM Wiki pattern: Andrej Karpathy.
- Template built with [Claude Code](https://claude.com/claude-code).

## License

MIT. See the `LICENSE` file at the repository root.
