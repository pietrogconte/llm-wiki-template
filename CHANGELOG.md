# Changelog

All notable changes to this template are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [1.0.2] - 2026-10-15

### Changed
- GitHub Actions workflow: `actions/checkout` v4 → v7 and `actions/setup-python` v5 → v7, both running on Node.js 24. GitHub has deprecated Node.js 20 on Actions runners and was forcing the old versions onto Node.js 24 with a warning. No change to what the workflow does (linter on push and pull request, Python 3.9 and 3.12).

## [1.0.1] - 2026-10-15

### Added
- Linter check **E7**: duplicate item in a frontmatter list (`tags`, `sources`, any list key), in flow (`[a, b]`) or block (`- item`) format, case-insensitive. Reported on the line of the repeated item.

### Changed
- Schema (`CLAUDE.md`/`AGENTS.md`): frontmatter lists use one item per line with a two-space indent, the format Obsidian's Properties panel writes, so opening a page in Obsidian no longer produces a diff. Empty lists stay `[]`; wikilinks in lists are double-quoted.
- `example` and `example-en` branches: frontmatter converted to the new list format.

## [1.0.0] - 2026-10-14

First "ready to use" release.

### Added
- `scripts/lint_wiki.py`: mechanical wiki linter (Python 3.9+, stdlib only, read-only). Errors: broken wikilinks, empty files, pages missing from the index, missing/incomplete frontmatter, relative links to extensionless files, wikilink examples outside backticks in docs. Warning: raw sources with no ingest. Non-zero exit on errors; `--strict` also fails on warnings.
- `.githooks/pre-commit`: optional hook (`git config core.hooksPath .githooks`). Plain `sh`; tries `py -3`, `python3`, `python` and skips with a warning if no working Python is found.
- GitHub Actions workflow running the linter on push and pull request (Python 3.9 and 3.12).
- `obsidian-preset/`: optional `app.json` (wikilinks, attachments in `raw/assets`, auto-update links, inline title off) and `graph.json` (hides index/log/schema/docs, colors nodes by wiki folder and `raw/`).
- Optional provenance legend in the schema (✅ / 💡 / 🔎).
- `ARCHITECTURE.md` / `ARCHITECTURE.en.md`: layers, operations, schema conventions, wiki vs. RAG.
- `example` (Portuguese) and `example-en` (English) branches with a complete fictional home-baking wiki (4 projects, 6 hub concepts, 4 entities, 10 sources) that passes the linter.
- README screenshots in `docs/img/`.
- `.gitattributes` normalizing line endings to LF.

### Changed
- README (pt/en) reorganized: what it is, 5-step quickstart, Obsidian + optional preset, linter, example branches, optional MemPalace.
- License link in the README no longer points to an extensionless relative path (Obsidian created an empty `LICENSE.md` when clicked).

## Before 1.0.0 (untagged, 2026-09-24 to 2026-10-14)

- Initial template: generic schema (`CLAUDE.md`/`AGENTS.md`), `raw/` and `wiki/` structure, bilingual README, optional MemPalace section (setup later moved to its own repo).
