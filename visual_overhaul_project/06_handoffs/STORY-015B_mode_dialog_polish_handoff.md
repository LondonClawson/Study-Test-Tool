Story/Task:
`STORY-015B_mode_dialog_polish.md`

Status:
Submitted For Review. PM/reviewer acceptance is still required.

Summary:
Polished `ModeSelectionDialog` with the accepted visual foundation while
preserving modal behavior. The dialog now uses semantic app/surface colors,
shared text roles, balanced Test and Practice option cards, a primary Test
action, and a secondary Practice action instead of success styling.

Files changed:
- `study_test_tool/gui/components/mode_dialog.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-015B_mode_dialog_polish.md`
- `visual_overhaul_project/06_handoffs/STORY-015B_mode_dialog_polish_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015B/`

Definition of Ready checked:
`CTX-DIALOGS`, `CTX-FOUNDATION`, and the accepted `STORY-005` button hierarchy
handoff were available and sufficient.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/dialog_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/STORY-005_button_hierarchy_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-006_card_and_list_patterns_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-007_page_header_pattern_handoff.md`

Context summaries created/updated:
None.

Screens/states checked:
- Mode Selection dialog initial display in light mode.
- Mode Selection dialog initial display in dark mode.
- Test Mode selection path.
- Practice Mode selection path.
- Window close/cancel path.
- Modal grab behavior.
- Parent centering behavior.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-015B/light/light_mode_selection_dialog.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015B/dark/dark_mode_selection_dialog.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/components/mode_dialog.py`
- `python3 -m black --check study_test_tool/gui/components/mode_dialog.py`
- GUI smoke: opened `ModeSelectionDialog` against a Tk parent, verified modal
  grab and parent centering, and confirmed Test returns `MODE_TEST`, Practice
  returns `MODE_PRACTICE`, and close returns `None`.
- Screenshot capture: `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states mode_selection_dialog --output visual_overhaul_project/01_context/screenshots/after/STORY-015B`
- `git diff --check`

Tests not run and why:
Full pytest was not run because this story only changes one CustomTkinter dialog
surface. No services, database code, navigation callers, import/export, scoring,
or persistence behavior changed.

Acceptance criteria notes:
- Test Mode is the primary action.
- Practice Mode now uses a secondary action role instead of success styling.
- Both options use the same card structure and comparable descriptions.
- `get_mode()`, `_select_test()`, `_select_practice()`, close/cancel behavior,
  `transient(parent)`, `grab_set()`, parent centering, and `wait_window()` are
  preserved.
- No native message boxes, file dialogs, mix dialogs, or import preview dialogs
  were changed.

Risks:
- The larger fixed dialog size improves readability for the two-card layout but
  should be rechecked in `STORY-016_light_dark_and_min_size_validation.md` if
  minimum-window validation includes modal positioning.

Follow-up backlog items:
- Use `STORY-015C_mix_dialog_polish.md` for Mix Test dialog hierarchy and list
  readability.
- Use `STORY-015D_import_preview_dialog_polish.md` for Import Preview row and
  status treatment.
