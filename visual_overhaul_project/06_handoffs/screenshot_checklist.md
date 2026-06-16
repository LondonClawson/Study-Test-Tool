# Screenshot Checklist

Use this checklist for baseline audit, sprint review, and MVP closeout.
For Sprint 0, this checklist is part of
`02_research_tasks/R-001_baseline_visual_audit.md`.

For implementation stories, use this checklist with
`00_project/screenshot_evidence_policy.md`. Capture only the states touched by
the story unless the assignment asks for a broader sprint or regression pass.

Harness examples from the repository root:

```bash
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --group home --output visual_overhaul_project/01_context/screenshots/after/STORY-008
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states home_populated_grouped home_empty_state --output visual_overhaul_project/01_context/screenshots/after/STORY-008
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --output visual_overhaul_project/01_context/screenshots/after/STORY-008
```

## Modes

- Light mode.
- Dark mode.
- Minimum supported window size where practical.

## Home

- Populated grouped tests.
- Ungrouped tests.
- Archived tests.
- Empty state.

## Test Taking

- Normal mode, unanswered question.
- Normal mode, answered question.
- Flagged question.
- Practice mode before check.
- Practice mode after correct feedback.
- Practice mode after incorrect feedback.
- Essay question.

## Results

- All-correct or high score.
- Partial score.
- Essay question included.
- Flagged question included.
- Mix-test source breakdown if practical.
- Results loaded from history.

## Editor

- New test.
- Existing test with questions.
- Multiple-choice edit state.
- Essay edit state.
- Validation warning.

## Data Views

- History populated.
- History empty/loading if practical.
- Analytics populated.
- Analytics no-data.
- Review with missed questions.
- Review empty.

## Dialogs

- Mode selection.
- Mix test.
- Import summary or import error where practical.
- Delete/archive confirmation where practical.
