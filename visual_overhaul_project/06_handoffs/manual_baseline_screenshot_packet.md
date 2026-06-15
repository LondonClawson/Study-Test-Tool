# Manual Baseline Screenshot Packet

## Purpose

Provide a concise, executable capture checklist for a GUI-capable runner to collect the missing Sprint 0 baseline screenshots for `CTX-AUDIT-BASELINE`.

## Launch And Setup

- Repository root: `projects/Study-Test-Tool/`
- App code root: `projects/Study-Test-Tool/study_test_tool/`
- Project docs launch/setup commands:
  - `python3 -m venv venv`
  - `source venv/bin/activate`
  - `pip install -r study_test_tool/requirements.txt`
  - `cd study_test_tool`
  - `python main.py`
- If a local virtualenv already exists, activate it and install only missing requirements before launch.
- The project docs do not name a dedicated screenshot tool. Use your normal GUI capture method once the app window is visible.

## Required Capture Destinations

- Light mode screenshots:
  - `projects/Study-Test-Tool/visual_overhaul_project/01_context/screenshots/baseline/light/`
- Dark mode screenshots:
  - `projects/Study-Test-Tool/visual_overhaul_project/01_context/screenshots/baseline/dark/`
- Use ASCII-only filenames.
- Keep filenames descriptive enough that the screen and state are obvious without opening the image.

## Practical Capture Checklist

Use `visual_overhaul_project/06_handoffs/screenshot_checklist.md` and `R-001_baseline_visual_audit.md` as the state list below.

### Light And Dark Mode

- Capture every practical state in both light and dark mode.
- Capture the minimum supported window size where practical, especially for crowded screens.

### Home / Test Selector

- Populated grouped tests.
- Populated ungrouped tests.
- Archived tests.
- Empty state.

Example filenames:

- `light_home_grouped_populated.png`
- `light_home_ungrouped_populated.png`
- `light_home_archived_tests.png`
- `light_home_empty_state.png`
- `dark_home_grouped_populated.png`

### Test Taking

- Normal mode, unanswered question.
- Normal mode, answered question.
- Flagged question.
- Practice mode before check.
- Practice mode after correct feedback.
- Practice mode after incorrect feedback.
- Essay question.

Example filenames:

- `light_test_taking_unanswered.png`
- `light_test_taking_answered.png`
- `light_test_taking_flagged.png`
- `light_test_taking_practice_before_check.png`
- `light_test_taking_practice_correct_feedback.png`
- `light_test_taking_practice_incorrect_feedback.png`
- `light_test_taking_essay_question.png`

### Results

- All-correct or high score.
- Partial score.
- Essay question included.
- Flagged question included.
- Mix-test source breakdown if practical.
- Results loaded from history.

Example filenames:

- `light_results_high_score.png`
- `light_results_partial_score.png`
- `light_results_essay_included.png`
- `light_results_flagged_included.png`
- `light_results_mix_breakdown.png`
- `light_results_loaded_from_history.png`

### Editor

- New test.
- Existing test with questions.
- Multiple-choice edit state.
- Essay edit state.
- Validation warning.

Example filenames:

- `light_editor_new_test.png`
- `light_editor_existing_test_with_questions.png`
- `light_editor_multiple_choice_edit.png`
- `light_editor_essay_edit.png`
- `light_editor_validation_warning.png`

### Data Views

- History populated.
- History empty/loading if practical.
- Analytics populated.
- Analytics no-data.
- Review with missed questions.
- Review empty.

Example filenames:

- `light_history_populated.png`
- `light_history_empty.png`
- `light_history_loading.png`
- `light_analytics_populated.png`
- `light_analytics_no_data.png`
- `light_review_missed_questions.png`
- `light_review_empty.png`

### Dialogs

- Mode selection.
- Mix test.
- Import summary or import error where practical.
- Delete/archive confirmation where practical.

Example filenames:

- `light_mode_selection_dialog.png`
- `light_mix_test_dialog.png`
- `light_import_summary.png`
- `light_import_error.png`
- `light_delete_confirmation.png`
- `light_archive_confirmation.png`

## Realistic Seeded Or Populated States

- If the local database is empty, create temporary tests only as needed to make the screenshots realistic.
- Prefer populated grouped and ungrouped home states over synthetic placeholders.
- Capture archived tests only after there is at least one archived test to show.
- For results, history, analytics, and review, seed enough data to show the intended layout and any state-specific markers such as mix breakdown, missed questions, or no-data messaging.
- If the app has an import flow that can be used to seed data quickly, use it; otherwise create temporary test records in the smallest way that produces representative screens.

## What To Report If A State Cannot Be Captured

Report the exact missing state, not a substitute.

- State name.
- Why it could not be captured.
- Whether the blocker was app launch, missing data, unreachable UI flow, or a modal that could not be triggered.
- Any exact command or error observed.
- Whether a partial fallback screenshot was captured instead.

If the state remains uncaptured, leave it explicitly listed as missing in the baseline audit summary.

