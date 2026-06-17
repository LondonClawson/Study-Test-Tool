# STORY-015B Mode Dialog Polish - PM Review

Status:
Accepted. `STORY-015B_mode_dialog_polish.md` is Done as of 2026-06-16.

Review scope:
- Inspected the submitted `ModeSelectionDialog` implementation in
  `study_test_tool/gui/components/mode_dialog.py`.
- Reviewed light and dark screenshot evidence for the initial Mode Selection
  dialog state.
- Checked the story against CTX-DIALOGS constraints for `get_mode()`, close,
  modal grab, parent centering, and `wait_window()`.

Verification run by PM:
- `python3 -m compileall -q study_test_tool/gui/components/mode_dialog.py`
- `python3 -m black --check study_test_tool/gui/components/mode_dialog.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states mode_selection_dialog --output visual_overhaul_project/01_context/screenshots/after/STORY-015B`
- Non-GUI return-path smoke confirmed `_select_test()` sets `MODE_TEST`,
  `_select_practice()` sets `MODE_PRACTICE`, both selection methods destroy the
  dialog, and `get_mode()` returns the current `_mode` after `wait_window()`.

Acceptance notes:
- Test Mode is visually primary.
- Practice Mode is no longer styled as success.
- Both options use comparable card structure and descriptions.
- Source preserves `transient(parent)`, `grab_set()`, parent centering, and
  `wait_window()`.
- No native dialogs, mix dialog behavior, import preview behavior, services,
  database code, or navigation callers were changed.

Verification limitation:
- PM could not independently rerun a full CTk modal smoke in this shell because
  a bare `ctk.CTk()` aborts during Tk initialization. The failure occurs before
  `ModeSelectionDialog` is constructed, so it is not evidence of a dialog
  regression. Acceptance relies on submitted GUI smoke notes, screenshot
  evidence, source inspection, and the non-GUI return-path smoke above.

Residual risks:
- Larger fixed dialog dimensions should be rechecked in
  `STORY-016_light_dark_and_min_size_validation.md` if modal positioning is
  included in that validation pass.
