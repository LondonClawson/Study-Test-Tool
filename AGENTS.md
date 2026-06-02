# AGENTS.md

Guidance for coding agents working in this repository.

## Current Project State

This is an implemented Python desktop app, not just a planning/spec repo. Some older root docs still describe a planning phase or older PDF-conversion behavior. In particular, `CLAUDE.md`, `GEMINI.md`, and parts of `README-convert_study_test_pdfs.md` are stale where they conflict with current code; treat the live code under `study_test_tool/` and the tests as authoritative.

Study Testing Tool is a macOS-oriented Python 3.9+ desktop application for importing, taking, mixing, reviewing, and analyzing study tests. The GUI uses CustomTkinter/Tkinter, persistence is local SQLite, and import/export data is JSON plus plain-text, PDF, and DOCX import paths.

## Repository Layout

- `study_test_tool/main.py` initializes runtime directories, database schema, migrations, and launches the GUI.
- `study_test_tool/config/` contains settings, paths, constants, and SQLite connection initialization.
- `study_test_tool/database/` contains `schema.sql`, `db_manager.py`, and `migrations.py`.
- `study_test_tool/models/` contains dataclass models for tests, questions/options, attempts, and responses.
- `study_test_tool/services/` contains business logic: test/question management, scoring, import/export, PDF/DOCX parsing, mix tests, randomization, review, analytics, and session state.
- `study_test_tool/gui/` contains CustomTkinter frames and reusable widgets. Navigation is frame-based through `gui/main_window.py`.
- `study_test_tool/tests/` contains pytest tests. Tests use temporary SQLite files rather than `:memory:` because the app opens multiple connections.
- `convert_study_test_pdfs.py` is a root CLI shim around `study_test_tool/services/pdf_import_service.py`.
- `study_test_tool/scripts/install.sh` and `launch.sh` are macOS installer/launcher scripts for the end-user desktop app.

## Commands

From the repo root:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r study_test_tool/requirements.txt
pytest --rootdir=. study_test_tool/tests
PYTHONPATH=study_test_tool python3 study_test_tool/main.py
python3 convert_study_test_pdfs.py --help
```

From `study_test_tool/`:

```bash
python3 main.py
pytest tests
black .
pylint services models gui database config utils
```

The code currently imports package directories as top-level modules (`from config...`, `from services...`). `main.py`, the CLI shim, and tests add `study_test_tool` to `sys.path`; if running ad hoc commands from repo root, set `PYTHONPATH=study_test_tool`.

## Architecture Rules

Maintain the existing layered architecture:

```text
GUI (CustomTkinter frames/widgets)
  -> Services (business logic)
  -> DatabaseManager / migrations / schema
  -> SQLite

Models are dataclasses passed between layers.
```

- GUI code should call services, not raw SQLite.
- Services should use `DatabaseManager` for persistence and model dataclasses for structured data.
- Keep all SQL centralized in `database/db_manager.py`, `database/schema.sql`, or `database/migrations.py`.
- Use `config.settings` and `utils.constants` for shared constants instead of duplicating string literals.
- Runtime data belongs under `study_test_tool/data/`; do not commit generated databases, imports, backups, caches, or local virtualenvs.

## Database Guidance

- `initialize_database()` applies `database/schema.sql`; `run_migrations()` applies incremental migrations using `PRAGMA user_version`.
- `DatabaseManager.__init__()` also has compatibility migration logic for older local databases. Be careful when changing schema behavior because first-run installs and already-installed user databases both matter.
- New tables/columns should update `schema.sql`, add a migration in `database/migrations.py`, and include tests for both fresh schema and migration behavior when practical.
- Connections should enable `sqlite3.Row` and foreign keys through `config.database.get_connection()`.
- Preserve cascading deletes and indexes for common query paths.

## Import And Scoring Behavior

- JSON import contract uses a root object with `name`, `description`, optional `group_name`, and a non-empty `questions` array.
- Multiple-choice questions use `type: "multiple_choice"` and options with `text` plus `correct`.
- Essay questions use `type: "essay"` and `expected_answer`; essay responses score as `None`, not correct/incorrect.
- PDF/DOCX import is implemented in `services/pdf_import_service.py` and called by `ImportService`. The current code uses `pdfminer.six` for PDFs and `python-docx` for DOCX; do not assume Poppler is required unless code changes.
- Practice mode locks the first checked response via `TestSession.checked_responses`; final scoring prefers checked responses over later edits.
- Mixed tests preserve each question's original `test_id`; `ScoringService.save_mixed_attempt()` saves separate attempts per source test so analytics remain per-test.

## GUI Guidance

- `App.show_frame(name, **kwargs)` raises frames and calls `on_show(**kwargs)` when present.
- Screen names live in `utils/constants.py`.
- Follow existing CustomTkinter layout patterns: frames own their widgets, navigation goes through the controller, and reusable controls belong in `gui/components/`.
- Keep long-running parsing/import work user-visible with dialogs or summaries; avoid silent failures and surface actionable errors.

## Testing Practices

- Prefer focused pytest tests under `study_test_tool/tests/` for service, database, migration, import, scoring, and session behavior.
- Use temporary SQLite files with `initialize_database(path)` for database tests. Avoid `:memory:` unless the code path uses a single connection.
- For parsing changes, include edge cases that prove malformed input is skipped or rejected explicitly rather than guessed.
- For scoring/session changes, cover practice mode first-check locking, essay `None` scores, flagged questions, and timing/session bookkeeping where relevant.
- Before finishing substantive changes, run at least the relevant subset of `pytest study_test_tool/tests`; run the full suite when database/import/scoring/shared behavior changes.

## Style And Conventions

- Use Python 3.9+ compatible syntax unless the project baseline changes.
- Follow PEP 8 and Black formatting.
- Use type hints on public function signatures and keep docstrings on public modules/classes/functions.
- Naming: modules/functions/variables `lowercase_with_underscores`, classes `CamelCase`, constants `UPPERCASE_WITH_UNDERSCORES`.
- Group imports as standard library, third-party, then local imports.
- Keep comments sparse and useful; explain non-obvious parsing, migration, or weighting behavior.
- Prefer small service methods and existing abstractions over new cross-cutting frameworks.
- Keep files ASCII unless editing existing non-ASCII text or preserving user-facing punctuation already present.

## End-User Install Notes

The macOS installer expects the GitHub repo at `https://github.com/LondonClawson/Study-Test-Tool.git`, clones to `~/StudyTestTool`, creates a venv inside `study_test_tool/`, and builds a Desktop `.app` wrapper. The launcher does a quiet `git pull`, syncs requirements, and runs `python3 main.py`.

Changes to dependencies, app launch paths, or Tkinter/Python assumptions should be reflected in `study_test_tool/scripts/install.sh`, `study_test_tool/scripts/launch.sh`, and user-facing docs.
