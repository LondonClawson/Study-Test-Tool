# STORY-015C Mix Dialog Polish - PM Review

Status:
Accepted. `STORY-015C_mix_dialog_polish.md` is Done as of 2026-06-16.

Review scope:
- Inspected the submitted `MixTestDialog` implementation in
  `study_test_tool/gui/components/mix_test_dialog.py`.
- Inspected the new Mix dialog screenshot harness states in
  `visual_overhaul_project/tools/capture_baseline_screenshots.py`.
- Reviewed light and dark evidence for default empty selection, Select All,
  one-group-selected, and Select All then Deselect All states.
- Checked the story against CTX-DIALOGS constraints for selection semantics,
  group sync, question count parsing, silent invalid starts, `get_result()`, and
  modal behavior preservation.

Verification run by PM:
- `python3 -m compileall -q study_test_tool/gui/components/mix_test_dialog.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/components/mix_test_dialog.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states mix_test_dialog mix_test_dialog_select_all mix_test_dialog_group_selected mix_test_dialog_deselected --output visual_overhaul_project/01_context/screenshots/after/STORY-015C`
- Non-GUI behavior smoke covered Select All, Deselect All, group toggle, child
  toggle group sync, selected test ID order, valid start, empty selection,
  non-numeric count, non-positive count, and `get_result()` return behavior.

Acceptance notes:
- Grouped test selection is easier to scan without changing checkbox controls
  or selected ID order.
- Select All and Deselect All use tertiary button roles.
- Start Mix Test is primary and Cancel is secondary.
- Empty, non-numeric, and non-positive invalid starts remain silent and
  non-submitting.
- Source preserves `transient(parent)`, `grab_set()`, parent centering, and
  `wait_window()`.
- No Mode Selection, Import Preview, native dialog, service, database,
  persistence, or navigation caller behavior changed.

Verification limitation:
- PM could not independently rerun a full CTk modal smoke in this shell because
  a bare `ctk.CTk()` aborts during Tk initialization. The failure occurs before
  `MixTestDialog` is constructed, so it is not evidence of a dialog regression.
  Acceptance relies on submitted GUI smoke notes, screenshot evidence, source
  inspection, and the non-GUI behavior smoke above.

Residual risks:
- Long test names and larger source-test lists should be rechecked in
  `STORY-016_light_dark_and_min_size_validation.md`.
- Inline validation for silent invalid starts remains a separate behavior-story
  decision, not part of this visual polish acceptance.
