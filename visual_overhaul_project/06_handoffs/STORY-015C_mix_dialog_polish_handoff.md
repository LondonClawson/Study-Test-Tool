Story/Task:
`STORY-015C_mix_dialog_polish.md`

Status:
Done. Accepted by PM/reviewer on 2026-06-16.

Summary:
Polished `MixTestDialog` with the accepted visual foundation while preserving
selection and return behavior. The dialog now uses semantic surfaces, shared
text roles, tertiary Select All/Deselect All utility buttons, grouped source
cards, clearer child test rows, a structured selected-pool/question-count area,
and primary Start Mix Test plus secondary Cancel actions.

Files changed:
- `study_test_tool/gui/components/mix_test_dialog.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-015C_mix_dialog_polish.md`
- `visual_overhaul_project/06_handoffs/STORY-015C_mix_dialog_polish_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015C/`

Definition of Ready checked:
`CTX-DIALOGS`, `CTX-FOUNDATION`, accepted `STORY-005` button hierarchy handoff,
and accepted `STORY-006` card/list pattern handoff were available and
sufficient.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/dialog_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/STORY-005_button_hierarchy_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-015B_mode_dialog_polish_handoff.md`

Context summaries created/updated:
None.

Screens/states checked:
- Mix Test dialog empty/default selection state.
- Mix Test dialog after Select All.
- Mix Test dialog with one source group selected.
- Mix Test dialog after Select All then Deselect All.
- Empty selection invalid-start path.
- Group checkbox toggle and child checkbox sync.
- Deselect All path.
- Valid Start Mix Test path.
- Cancel/close path.
- Light and dark mode for every captured state.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-015C/light/light_mix_test_dialog.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015C/light/light_mix_test_dialog_select_all.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015C/light/light_mix_test_dialog_group_selected.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015C/light/light_mix_test_dialog_deselected.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015C/dark/dark_mix_test_dialog.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015C/dark/dark_mix_test_dialog_select_all.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015C/dark/dark_mix_test_dialog_group_selected.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015C/dark/dark_mix_test_dialog_deselected.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/components/mix_test_dialog.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/components/mix_test_dialog.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- GUI smoke: opened `MixTestDialog` against a Tk parent, verified modal grab,
  empty selection stays open with `_result is None`, Select All updates the
  total, valid Start returns selected IDs in existing order with parsed count,
  group toggle selects child tests, child toggle syncs the group checkbox,
  Deselect All clears the total, and close returns `None`.
- Screenshot capture: `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states mix_test_dialog mix_test_dialog_select_all mix_test_dialog_group_selected mix_test_dialog_deselected --output visual_overhaul_project/01_context/screenshots/after/STORY-015C`
- Screenshot validation: `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states mix_test_dialog mix_test_dialog_select_all mix_test_dialog_group_selected mix_test_dialog_deselected --output visual_overhaul_project/01_context/screenshots/after/STORY-015C`
- `git diff --check`

Tests not run and why:
Full pytest was not run because this story changes one CustomTkinter dialog and
the development screenshot harness. No services, database code, mix-test
creation service, navigation callers, scoring, import/export, or persistence
behavior changed.

Acceptance criteria notes:
- Grouped test selection uses clearer group cards and child rows while keeping
  the existing checkbox controls and order.
- Select All and Deselect All use tertiary button roles.
- Start Mix Test uses the primary role and Cancel uses the secondary role.
- `get_result()`, selected test ID order, group/child checkbox sync, question
  count parsing, empty/non-numeric/non-positive silent invalid-start behavior,
  `transient(parent)`, `grab_set()`, parent centering, and `wait_window()` are
  preserved.
- No Mode Selection, Import Preview, native messagebox, file dialog, service,
  or caller behavior was changed.

Risks:
- Long test names and larger source-test lists should be covered again in
  `STORY-016_light_dark_and_min_size_validation.md`.
- Silent invalid-start behavior remains intentionally unchanged per CTX-DIALOGS;
  any inline validation should be a later behavior story.

Follow-up backlog items:
- Use `STORY-015D_import_preview_dialog_polish.md` for Import Preview row and
  status treatment.
- Keep native message boxes and file dialogs as MVP documented exceptions unless
  PM opens a focused post-MVP replacement story.

PM/reviewer acceptance:
- Accepted on 2026-06-16 after inspection of the submitted implementation,
  light/dark screenshot evidence, source-level behavior preservation, and
  focused verification.
- PM verification covered Select All, Deselect All, group toggle, child toggle
  group sync, selected test ID order, valid start, empty selection, non-numeric
  count, non-positive count, and `get_result()` return behavior.
- Full CTk modal smoke could not be independently rerun in this shell because
  bare `ctk.CTk()` creation aborted at Tk initialization. That appears
  environment-level rather than dialog-specific; submitted GUI smoke notes,
  screenshot evidence, source inspection, and non-GUI behavior checks were used
  for acceptance.
