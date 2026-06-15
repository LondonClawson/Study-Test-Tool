# Baseline Screenshot Manifest

## Metadata

- Purpose: File-level manifest for the baseline visual audit screenshots.
- Related summary: `baseline_visual_audit.md`.
- Last updated: 2026-06-15.
- Validation command: `python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only`.
- Validation result: 42 screenshots passed.

## Capture Sources

- Initial scripted capture: screenshots captured by the baseline harness on 2026-06-06.
- Supplemental mixed-test capture: screenshots captured on 2026-06-15 with:

```bash
MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states test_taking_mix_partial_group test_taking_mix_multi_group
```

## Manifest

| Mode | State | File | Captured | Source |
| --- | --- | --- | --- | --- |
| dark | `analytics_no_data` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_analytics_no_data.png` | 2026-06-06 17:17:07 | Initial scripted capture |
| dark | `analytics_populated` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_analytics_populated.png` | 2026-06-06 17:17:04 | Initial scripted capture |
| dark | `editor_existing_test_with_questions` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_editor_existing_test_with_questions.png` | 2026-06-06 17:16:57 | Initial scripted capture |
| dark | `editor_new_test` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_editor_new_test.png` | 2026-06-06 17:16:56 | Initial scripted capture |
| dark | `history_empty_state` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_history_empty_state.png` | 2026-06-06 17:17:07 | Initial scripted capture |
| dark | `history_populated` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_history_populated.png` | 2026-06-06 17:17:03 | Initial scripted capture |
| dark | `home_empty_state` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_home_empty_state.png` | 2026-06-06 17:17:06 | Initial scripted capture |
| dark | `home_populated_grouped` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_home_populated_grouped.png` | 2026-06-06 17:16:54 | Initial scripted capture |
| dark | `mix_test_dialog` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_mix_test_dialog.png` | 2026-06-06 17:16:56 | Initial scripted capture |
| dark | `mode_selection_dialog` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_mode_selection_dialog.png` | 2026-06-06 17:16:55 | Initial scripted capture |
| dark | `results_loaded_from_history` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_results_loaded_from_history.png` | 2026-06-06 17:17:03 | Initial scripted capture |
| dark | `results_partial_score_essay_flagged` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_results_partial_score_essay_flagged.png` | 2026-06-06 17:17:02 | Initial scripted capture |
| dark | `review_empty_state` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_review_empty_state.png` | 2026-06-06 17:17:08 | Initial scripted capture |
| dark | `review_missed_questions` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_review_missed_questions.png` | 2026-06-06 17:17:05 | Initial scripted capture |
| dark | `test_taking_answered_flagged` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_test_taking_answered_flagged.png` | 2026-06-06 17:16:59 | Initial scripted capture |
| dark | `test_taking_essay_question` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_test_taking_essay_question.png` | 2026-06-06 17:17:00 | Initial scripted capture |
| dark | `test_taking_mix_multi_group` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_test_taking_mix_multi_group.png` | 2026-06-15 11:58:23 | Supplemental mixed-test capture |
| dark | `test_taking_mix_partial_group` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_test_taking_mix_partial_group.png` | 2026-06-15 11:58:23 | Supplemental mixed-test capture |
| dark | `test_taking_mix_test` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_test_taking_mix_test.png` | 2026-06-06 17:17:01 | Initial scripted capture |
| dark | `test_taking_practice_incorrect_feedback` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_test_taking_practice_incorrect_feedback.png` | 2026-06-06 17:17:00 | Initial scripted capture |
| dark | `test_taking_unanswered` | `visual_overhaul_project/01_context/screenshots/baseline/dark/dark_test_taking_unanswered.png` | 2026-06-06 17:16:58 | Initial scripted capture |
| light | `analytics_no_data` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_analytics_no_data.png` | 2026-06-06 17:16:52 | Initial scripted capture |
| light | `analytics_populated` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_analytics_populated.png` | 2026-06-06 17:16:49 | Initial scripted capture |
| light | `editor_existing_test_with_questions` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_editor_existing_test_with_questions.png` | 2026-06-06 17:16:42 | Initial scripted capture |
| light | `editor_new_test` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_editor_new_test.png` | 2026-06-06 17:16:41 | Initial scripted capture |
| light | `history_empty_state` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_history_empty_state.png` | 2026-06-06 17:16:52 | Initial scripted capture |
| light | `history_populated` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_history_populated.png` | 2026-06-06 17:16:48 | Initial scripted capture |
| light | `home_empty_state` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_home_empty_state.png` | 2026-06-06 17:16:51 | Initial scripted capture |
| light | `home_populated_grouped` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_home_populated_grouped.png` | 2026-06-06 17:16:39 | Initial scripted capture |
| light | `mix_test_dialog` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_mix_test_dialog.png` | 2026-06-06 17:16:41 | Initial scripted capture |
| light | `mode_selection_dialog` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_mode_selection_dialog.png` | 2026-06-06 17:16:40 | Initial scripted capture |
| light | `results_loaded_from_history` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_results_loaded_from_history.png` | 2026-06-06 17:16:47 | Initial scripted capture |
| light | `results_partial_score_essay_flagged` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_results_partial_score_essay_flagged.png` | 2026-06-06 17:16:47 | Initial scripted capture |
| light | `review_empty_state` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_review_empty_state.png` | 2026-06-06 17:16:53 | Initial scripted capture |
| light | `review_missed_questions` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_review_missed_questions.png` | 2026-06-06 17:16:50 | Initial scripted capture |
| light | `test_taking_answered_flagged` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_test_taking_answered_flagged.png` | 2026-06-06 17:16:44 | Initial scripted capture |
| light | `test_taking_essay_question` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_test_taking_essay_question.png` | 2026-06-06 17:16:45 | Initial scripted capture |
| light | `test_taking_mix_multi_group` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_test_taking_mix_multi_group.png` | 2026-06-15 11:58:21 | Supplemental mixed-test capture |
| light | `test_taking_mix_partial_group` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_test_taking_mix_partial_group.png` | 2026-06-15 11:58:21 | Supplemental mixed-test capture |
| light | `test_taking_mix_test` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_test_taking_mix_test.png` | 2026-06-06 17:16:46 | Initial scripted capture |
| light | `test_taking_practice_incorrect_feedback` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_test_taking_practice_incorrect_feedback.png` | 2026-06-06 17:16:44 | Initial scripted capture |
| light | `test_taking_unanswered` | `visual_overhaul_project/01_context/screenshots/baseline/light/light_test_taking_unanswered.png` | 2026-06-06 17:16:43 | Initial scripted capture |
