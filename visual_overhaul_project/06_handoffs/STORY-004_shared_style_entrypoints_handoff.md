# STORY-004 Shared Style Entry Points Handoff

Story/Task:
`STORY-004_shared_style_entrypoints.md`

Status:
Done. Accepted by PM review on 2026-06-15.

Summary:
Added a small GUI style entry point and migrated only the `ProgressBar` proof
target to use semantic status colors, compact typography, and row radius roles.
No screen redesign or behavior changes were included.

Files changed:
- `study_test_tool/gui/styles.py`
- `study_test_tool/gui/components/progress_bar.py`
- `visual_overhaul_project/04_stories/STORY-004_shared_style_entrypoints.md`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/06_handoffs/STORY-004_shared_style_entrypoints_handoff.md`

Definition of Ready checked:
Yes. CTX-FOUNDATION, CTX-STYLE-INVENTORY, and CTX-GUI-ARCH were Ready before
implementation.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/01_context/summaries/style_inventory.md`
- `visual_overhaul_project/01_context/summaries/gui_architecture_summary.md`

Context summaries created/updated:
None.

Screens/states checked:
- App startup smoke check reached the GUI main loop with no immediate startup
  error.
- Progress button status behavior was checked against the existing code path:
  current, flagged, answered, and unanswered precedence remains unchanged.
- Light/dark note: shared base/text surface roles use CustomTkinter light/dark
  tuples. Progress status colors intentionally remain the accepted single-value
  semantic status colors from CTX-FOUNDATION.

Tests run:
- `PYTHONPATH=study_test_tool python3 -m py_compile study_test_tool/gui/styles.py study_test_tool/gui/components/progress_bar.py`
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 study_test_tool/main.py`

Tests not run and why:
Pytest was not run because this story only changed GUI style constants and a
visual component's styling references. No service, database, scoring, import,
session, or navigation behavior changed.

Acceptance criteria notes:
- Shared style entry points are semantic and GUI-scoped in `gui.styles`.
- Light/dark tuples are available for base surfaces and text roles.
- `ProgressBar` still creates one clickable button per question.
- Progress status precedence and callback wiring were preserved.
- No unrelated screens, cards, headers, dialogs, or buttons were migrated.

PM review notes:
Accepted. `gui.styles` is the shared style entry point for upcoming MVP visual
stories, and `ProgressBar` is accepted as the narrow proof target. PM
verification re-ran `py_compile` for `styles.py` and `progress_bar.py`
successfully. The remaining risk is intentionally carried forward to
`STORY-005`: button role helpers still need a full screen-level proof.

Risks:
- Button role helpers are available for upcoming stories but are not yet proven
  in a screen-level migration.
- Later stories may need to add local helper functions for cards, headers, or
  chart styling after the first pilot areas are selected.

Follow-up backlog items:
- `STORY-005_button_hierarchy.md`: use Home/Test Selector as the narrow target
  area and prove the new button role entry points at screen level.
- `STORY-006_card_and_list_patterns.md`: select a named pilot area before
  starting.
- `STORY-007_page_header_pattern.md` and screen-specific stories should reuse
  `gui.styles` instead of adding new inline role colors.
