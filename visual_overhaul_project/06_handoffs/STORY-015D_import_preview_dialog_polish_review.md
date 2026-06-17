# STORY-015D Import Preview Dialog Polish Review

Status:
Accepted by PM/reviewer on 2026-06-17.

Reviewed files:

- `study_test_tool/gui/components/import_preview_dialog.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/04_stories/STORY-015D_import_preview_dialog_polish.md`
- `visual_overhaul_project/06_handoffs/STORY-015D_import_preview_dialog_polish_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-015D/`

Evidence reviewed:

- Light/dark all-ready Import Preview.
- Light/dark mixed ready, warning, and skipped Import Preview.
- Light/dark no-importable Import Preview with disabled Import action.
- Light/dark group-override Import Preview.

Verification run:

- `python3 -m compileall -q study_test_tool/gui/components/import_preview_dialog.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/components/import_preview_dialog.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states import_preview_all_ready import_preview_mixed_warnings import_preview_no_importable import_preview_group_override --output visual_overhaul_project/01_context/screenshots/after/STORY-015D`
- Non-GUI return-path smoke covering `_on_import()`, `_on_cancel()`, and
  `_preview_status()` for ready, warning, and skipped rows.

Acceptance notes:

- `ImportPreviewDialog.get_result()` contract remains unchanged.
- Group override handling still trims the entry value and returns it only on
  confirmed import.
- Cancel and close paths remain non-committing.
- Import remains disabled when no preview rows are importable.
- Native file dialogs and import report message boxes remain out of scope per
  `STORY-015E`.

Follow-up:

- `STORY-016_light_dark_and_min_size_validation.md` is Ready for the next
  validation pass.
