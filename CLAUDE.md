# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Study Testing Tool — a Python 3.9+ desktop application for importing, taking, and reviewing tests (multiple-choice and essay). Built with CustomTkinter for the GUI and SQLite3 for local persistence. Targets macOS.

**Current status:** Specification/planning phase. Comprehensive documentation exists but implementation code has not yet been written.

## Build & Run Commands

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r study_test_tool/requirements.txt

# Run (from the study_test_tool directory)
cd study_test_tool
python main.py

# Test
pytest
pytest --cov                    # with coverage report
pytest tests/test_scoring.py    # single test file

# Code quality
black .                         # format code
pylint services/ models/ gui/   # lint
```

## Architecture

**Layered architecture** with strict separation — GUI never calls the database directly.

```
GUI (CustomTkinter) → Services (business logic) → Database Layer (SQLite3)
                         ↕
                    Models (dataclasses)
```

### Key layers

- **`config/`** — App settings (`settings.py`) and database connection handler (`database.py`)
- **`models/`** — Python dataclasses: `Test`, `Question`, `TestResult`, `UserSettings`, `Achievement`
- **`database/`** — `db_manager.py` centralizes all CRUD operations; `schema.sql` defines the schema
- **`gui/`** — Screens (test selector, editor, test taking, results, history) plus `components/` for reusable widgets (question display, timer, progress bar, graphs)
- **`services/`** — Business logic: test management, question handling, scoring, JSON import/export, randomization, analytics, spaced repetition (Phase 3)
- **`utils/`** — Timer, validators, formatters, constants
- **`data/`** — Runtime storage: `database/study_tool.db`, imported test JSON files, backups

### Data flow

GUI calls services → services use models for structure and database layer for persistence → results flow back up through services to GUI.

### Database

SQLite3 with file at `data/database/study_tool.db`. Auto-created on first run with schema from `database/schema.sql`.

**MVP tables:** `tests`, `questions`, `question_options`, `test_attempts`, `question_responses`

**Later phases add:** `achievements`, `user_achievements`, `study_sessions`, `question_notes` (Phase 2); `spaced_repetition`, `study_plan` (Phase 3); `user_settings` (Nice-to-Have)

Table names are plural. Column names use `lowercase_with_underscores`. Foreign keys use `ON DELETE CASCADE`.

## Development Phases

- **MVP:** Test CRUD, test-taking with timer/flagging/randomization, results/history, JSON import, SQLite persistence
- **Phase 1:** Practice mode, missed questions review, performance graphs, weak topic identification
- **Phase 2:** Achievements, study streaks, per-question notes, custom test builder
- **Phase 3:** Spaced repetition (SM-2), answer explanations, study session planner

## Conventions

- **PEP 8** compliance, enforced via `black` (formatter) and `pylint` (linter)
- **Naming:** modules `lowercase_with_underscores.py`, classes `CamelCase`, functions/variables `lowercase_with_underscores`, constants `UPPERCASE_WITH_UNDERSCORES`, private members prefixed with `_`
- **Type hints** required on all function signatures (PEP 484)
- **Docstrings** on all public modules, classes, and functions (triple double-quotes)
- **Imports** grouped: stdlib → third-party → local, alphabetically sorted within groups
- **Test coverage** target: >80% for core logic and services
- Use in-memory SQLite for integration tests

## Key Dependencies

| Package | Purpose |
|---------|---------|
| `customtkinter` | Modern GUI widgets |
| `Pillow` | Image/icon handling |
| `python-dateutil` | Date/time utilities |
| `matplotlib` (Phase 1) | Performance visualization |
| `numpy` (Phase 1) | Numerical computing |

## Reference Documentation

Detailed specs live in the repo root as markdown files:
- `projectGoal.md` / `PROJECT_OVERVIEW.md` — Vision and MVP features
- `technicalArchitecture.md` / `ARCHITECTURE_OVERVIEW.md` — Technical blueprint
- `DATABASE_SCHEMA.md` — Full schema with all phases
- `PRODUCT_ROADMAP.md` — Feature phases and timelines
- `CODING_STANDARDS.md` — Code conventions
- `TESTING_STRATEGY.md` — Testing approach
- `test.txt` — Example test questions (legal scenarios) for import testing
