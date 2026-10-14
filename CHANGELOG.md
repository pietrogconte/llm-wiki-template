# Changelog

All notable changes to this template are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-10-14

First "ready to use" release.

### Added
- `scripts/lint_wiki.py`: mechanical wiki linter (Python 3.9+, stdlib only, read-only). Errors: broken wikilinks, empty files, pages missing from the index, missing/incomplete frontmatter, relative links to extensionless files, wikilink examples outside backticks in docs. Warning: raw sources with no ingest. Non-zero exit on errors; `--strict` also fails on warnings.
- `.githooks/pre-commit`: optional hook (`git config core.hooksPath .githooks`). Plain `sh`; tries `py -3`, `python3`, `python` and skips with a warning if no working Python is found.
- GitHub Actions workflow running the linter on push and pull request (Python 3.9 and 3.12).
- `obsidian-preset/`: optional `app.json` (wikilinks, attachments in `raw/assets`, auto-update links) and `graph.json` (hides index/log/schema/docs, colors nodes by wiki folder).
- Optional provenance legend in the schema (✅ / 💡 / 🔎).
- `ARCHITECTURE.md` / `ARCHITECTURE.en.md`: layers, operations, schema conventions, wiki vs. RAG.
- `example` (Portuguese) and `example-en` (English) branches with a complete fictional wiki that passes the linter.
- README screenshots in `docs/img/`.
- `.gitattributes` normalizing line endings to LF.

### Changed
- README (pt/en) reorganized: what it is, 5-step quickstart, Obsidian + optional preset, linter, example branches, optional MemPalace.
- License link in the README no longer points to an extensionless relative path (Obsidian created an empty `LICENSE.md` when clicked).

## Before 1.0.0 (untagged, 2026-09-24 to 2026-10-14)

- Initial template: generic schema (`CLAUDE.md`/`AGENTS.md`), `raw/` and `wiki/` structure, bilingual README, optional MemPalace section (setup later moved to its own repo).
