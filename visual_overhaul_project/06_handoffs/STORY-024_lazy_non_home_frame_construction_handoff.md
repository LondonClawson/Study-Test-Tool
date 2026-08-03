# STORY-024 Lazy Non-Home Frame Construction Handoff

Story/Task: `STORY-024_lazy_non_home_frame_construction.md`

Status: Done. Accepted by user authorization.

Summary: Home is the only screen frame constructed during application startup.
Each non-Home frame is constructed once on first navigation, then reused with
the existing raise and `on_show(**kwargs)` behavior. The shared frame registry
is module-level so it is declared once and remains easy to inspect.

Files changed:

- `study_test_tool/gui/main_window.py`
- `study_test_tool/tests/test_main_window.py`
- `04_stories/STORY-024_lazy_non_home_frame_construction.md`
- `00_project/status_board.md`
- This handoff

Definition of Ready checked: `CTX-GUI-ARCH` and `CTX-PERFORMANCE-SCALE` are
Ready.

Acceptance: The user accepted the implementation after the focused lifecycle
test and full regression passed.

Context summaries read:

- `gui_architecture_summary.md`
- `performance_scalability_audit.md`

Context summaries created/updated: None.

Screens/states checked:

- Headless lifecycle coverage for initial lazy construction, repeat navigation,
  grid placement, frame raising, and `on_show` arguments.
- No interactive GUI smoke check was available in this execution environment.

Screenshot evidence: The requested capture command for light/dark
`home_populated_grouped` and `analytics_populated` returned without creating
any files or output. No screenshot evidence is claimed; acceptance was by user
authorization with this capture limitation recorded.

Tests run:

- `PYTHONPATH=study_test_tool python3 -m pytest study_test_tool/tests/test_main_window.py`
- `PYTHONPATH=study_test_tool python3 -m pytest study_test_tool/tests`
- `PYTHONPATH=study_test_tool python3 -m py_compile study_test_tool/gui/main_window.py`
- `git diff --check`

Tests not run and why: A real Tk/CustomTkinter interaction smoke test was not
run because the screenshot harness did not produce files in this environment.

Acceptance criteria notes: The frame registry contains every existing screen;
the shared lazy creation path creates, grids, raises, and invokes `on_show` for
each entry. The focused test verifies one-time construction and repeated
navigation behavior without creating a Tk root window.

Risks: Importing the GUI screen modules, including Analytics, still occurs at
module import time. This story defers frame and embedded Matplotlib widget
construction only, as scoped.

Follow-up backlog items:

- Investigate why the screenshot harness returned without output before using
  it as evidence for future GUI stories.
- Benchmark Mix and History at representative production scale before adding
  indexes or pagination changes.
