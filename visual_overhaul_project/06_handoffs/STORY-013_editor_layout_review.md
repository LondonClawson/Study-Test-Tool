# STORY-013 Editor Layout Review

Story/Task:
`STORY-013_editor_layout.md`

Status:
Changes Requested by PM/reviewer on 2026-06-17.

Summary:
The editor implementation is broadly on track and the focused automated checks
pass, but it cannot be accepted yet because the required minimum-window editor
evidence is contaminated by the group autocomplete dropdown. That means the
submission does not prove the minimum-window layout acceptance criterion.

Required Fix:
- Recapture light and dark `editor_minimum_existing` screenshots with no group
  autocomplete dropdown obscuring the editor layout, or document an exact
  capture blocker and provide alternate manual evidence.
- If this is caused by the screenshot harness, close the editor autocomplete
  dropdown between capture states or in the minimum editor state setup before
  capture.
- If this is caused by runtime editor behavior, fix the dropdown cleanup path
  so it cannot persist into unrelated editor states, then recapture the
  evidence.

Finding:
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/light/light_editor_minimum_existing.png`
  shows the group autocomplete dropdown open over the left editor panel.
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/dark/dark_editor_minimum_existing.png`
  shows the same dropdown contamination.
- The intended group autocomplete evidence already exists separately at
  `visual_overhaul_project/01_context/screenshots/after/STORY-013/light/light_editor_group_autocomplete.png`
  and its dark counterpart, so the minimum-layout evidence needs to stand on its
  own.

Files reviewed:
- `study_test_tool/gui/test_editor.py`
- `study_test_tool/gui/components/autocomplete_entry.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/04_stories/STORY-013_editor_layout.md`
- `visual_overhaul_project/06_handoffs/STORY-013_editor_layout_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/`

Context checked:
- `visual_overhaul_project/01_context/summaries/editor_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/00_project/screenshot_evidence_policy.md`
- `visual_overhaul_project/00_project/status_transition_rules.md`

Verification run during review:
- `python3 -m compileall -q study_test_tool/gui/results_view.py study_test_tool/gui/test_editor.py study_test_tool/gui/components/autocomplete_entry.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/results_view.py study_test_tool/gui/test_editor.py study_test_tool/gui/components/autocomplete_entry.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_scoring_service.py study_test_tool/tests/test_mix_service.py study_test_tool/tests/test_group_sort.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --states editor_new_test editor_existing_test_with_questions editor_saved_empty_test editor_mc_add_form editor_essay_add_form editor_edit_question editor_group_autocomplete editor_minimum_existing --output visual_overhaul_project/01_context/screenshots/after/STORY-013`
- `git diff --check`

Verification results:
- Syntax check passed.
- Black check passed.
- Focused pytest passed: 57 passed, 5 collection warnings.
- Screenshot validation passed: 16 screenshots, but validation only proves the
  files are readable and sized correctly. It does not catch the dropdown
  contamination described above.

Notes:
- I did not find a required source-level blocker in the sampled editor CRUD,
  validation, group persistence, dirty-form protection, option ordering, or
  save/cancel paths.
- Keep this as an evidence fix unless recapture proves the dropdown persists
  because of runtime editor behavior.

Resubmission Acceptance Addendum - 2026-06-17:
- Accepted. `STORY-013_editor_layout.md` is Done.
- The screenshot harness now returns a cleanup callback from
  `show_editor_group_autocomplete(...)` and closes the group autocomplete
  dropdown after that evidence state.
- The light and dark `editor_minimum_existing` screenshots were recaptured and
  no longer show the autocomplete dropdown over the editor layout.
- Screenshot validation passed for the full 16-image `STORY-013` evidence set.
- Compileall and Black checks passed for the screenshot harness during the
  resubmission review.
