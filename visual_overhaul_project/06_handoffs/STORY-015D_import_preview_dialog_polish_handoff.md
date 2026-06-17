Story/Task:
STORY-015D: Import Preview Dialog Polish

Status:
Submitted For Review.

Summary:
Polished `ImportPreviewDialog` with semantic dialog surfaces, compact import
summary tiles, clearer group assignment hierarchy, styled preview rows, status
pills for Ready/Warnings/Skipped states, and clearer Import/Cancel action
hierarchy. Added Import Preview states to the screenshot harness so all required
light and dark dialog states can be captured repeatably.

Files changed:
- `study_test_tool/gui/components/import_preview_dialog.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-015D_import_preview_dialog_polish.md`
- `visual_overhaul_project/06_handoffs/STORY-015D_import_preview_dialog_polish_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015D/`

Definition of Ready checked:
- `dialog_context.md` is Ready.
- `visual_foundation_decisions.md` is Ready.
- Accepted `STORY-005` button hierarchy handoff was read.
- Accepted `STORY-006` card/list pattern handoff was read.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/dialog_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/STORY-005_button_hierarchy_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-006_card_and_list_patterns_handoff.md`
- `visual_overhaul_project/06_handoffs/STORY-015C_mix_dialog_polish_handoff.md`

Context summaries created/updated:
None.

Screens/states checked:
- Import Preview with all-ready previews and one shared detected group.
- Import Preview with mixed ready, warning, and skipped rows.
- Import Preview with no importable rows and disabled Import action.
- Import Preview with group override entry populated.
- Import confirmed path, cancel path, close path, modal grab, and light/dark
  visual states.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-015D/light/light_import_preview_all_ready.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015D/light/light_import_preview_mixed_warnings.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015D/light/light_import_preview_no_importable.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015D/light/light_import_preview_group_override.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015D/dark/dark_import_preview_all_ready.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015D/dark/dark_import_preview_mixed_warnings.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015D/dark/dark_import_preview_no_importable.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015D/dark/dark_import_preview_group_override.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/components/import_preview_dialog.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/components/import_preview_dialog.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- Focused Tk smoke for all-ready import, mixed cancel, group override result,
  no-importable disabled Import state, close path, and modal grab.
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states import_preview_all_ready import_preview_mixed_warnings import_preview_no_importable import_preview_group_override --output visual_overhaul_project/01_context/screenshots/after/STORY-015D`

Tests not run and why:
- Full pytest suite was not run because this change is scoped to one CustomTkinter
  dialog and screenshot harness state setup; import parsing, commit behavior,
  persistence, and scoring code were not changed.

Acceptance criteria notes:
- Importable, warning, and skipped rows now use distinct status labels and
  status colors while preserving parser output and commit behavior.
- Disabled Import is visually muted and remains disabled when no previews can
  be imported.
- `get_result()`, group override handling, cancel/close return paths, and modal
  behavior were preserved.
- Native file dialogs and import report message boxes remain out of scope.

Risks:
- Very long generated import reports and native messagebox content remain MVP
  exceptions per `STORY-015E`.
- Extremely long preview names may need additional truncation review during
  validation, but current scripted states fit the fixed dialog.

Follow-up backlog items:
- Use `STORY-016` or `STORY-017` for cross-screen validation if long Import
  Preview fixtures or minimum-size evidence expose additional layout issues.
