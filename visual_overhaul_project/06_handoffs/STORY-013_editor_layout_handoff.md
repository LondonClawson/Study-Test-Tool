Story/Task:
`STORY-013_editor_layout.md`

Status:
Submitted For Review. PM/reviewer acceptance is still required; this is not
marked Done.

Summary:
Polished the editor page header, metadata area, two-column panel hierarchy,
question list cards, add/edit form sections, option rows, essay expected-answer
panel, add/update/cancel actions, and group autocomplete styling. Existing
editor CRUD, validation rules, group persistence, dirty-form protection, native
messagebox behavior, and save/cancel behavior were preserved.

Resubmission addendum:
PM/reviewer returned the story because the minimum-window editor screenshots
were contaminated by the previous group autocomplete dropdown capture. The
screenshot harness now closes the autocomplete dropdown after the dropdown
evidence state, and the full light/dark editor evidence set was recaptured.

Files changed:
- `study_test_tool/gui/test_editor.py`
- `study_test_tool/gui/components/autocomplete_entry.py`
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-013_editor_layout.md`
- `visual_overhaul_project/06_handoffs/STORY-013_editor_layout_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/`

Definition of Ready checked:
Yes. `STORY-013` was Ready and unblocked before claiming. CTX-EDITOR and
CTX-FOUNDATION were Ready, and the PM readiness review confirmed this editor
scope.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/editor_context.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/STORY-013_editor_layout_readiness_review.md`
- `visual_overhaul_project/06_handoffs/PM_readiness_pass_2026-06-16.md`

Context summaries created/updated:
None.

Screens/states checked:
- New test editor in light and dark mode.
- Existing populated test with questions in light and dark mode.
- Saved empty test/no questions in light and dark mode.
- Multiple-choice add form and option rows in light and dark mode.
- Essay add form and expected-answer panel in light and dark mode.
- Edit-question mode with Update/Cancel visible in light and dark mode.
- Group autocomplete dropdown in light and dark mode.
- Minimum-window editor layout in light and dark mode.
- Validation warning path via stubbed messagebox smoke check.

Screenshot evidence:
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/light/light_editor_new_test.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/light/light_editor_existing_test_with_questions.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/light/light_editor_saved_empty_test.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/light/light_editor_mc_add_form.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/light/light_editor_essay_add_form.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/light/light_editor_edit_question.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/light/light_editor_group_autocomplete.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/light/light_editor_minimum_existing.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/dark/dark_editor_new_test.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/dark/dark_editor_existing_test_with_questions.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/dark/dark_editor_saved_empty_test.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/dark/dark_editor_mc_add_form.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/dark/dark_editor_essay_add_form.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/dark/dark_editor_edit_question.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/dark/dark_editor_group_autocomplete.png`
- `visual_overhaul_project/01_context/screenshots/after/STORY-013/dark/dark_editor_minimum_existing.png`

Tests run:
- `python3 -m compileall -q study_test_tool/gui/test_editor.py study_test_tool/gui/components/autocomplete_entry.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check study_test_tool/gui/test_editor.py study_test_tool/gui/components/autocomplete_entry.py visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_group_sort.py`
- Focused editor GUI smoke with a seeded temporary database and stubbed
  messageboxes for Save First validation, create test, edit metadata, add MC
  question, add essay question, edit/update question, cancel edit, option
  add/remove, group autocomplete selection, delete question, and dirty-back
  confirmation.
- `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states editor_new_test editor_existing_test_with_questions editor_saved_empty_test editor_mc_add_form editor_essay_add_form editor_edit_question editor_group_autocomplete editor_minimum_existing --output visual_overhaul_project/01_context/screenshots/after/STORY-013`
- Recaptured the same STORY-013 light/dark editor screenshot set after adding
  autocomplete dropdown cleanup; validation passed for 16 screenshots.
- `git diff --check`

Tests not run and why:
Full pytest was not run. This story changed editor GUI presentation and
autocomplete styling only. Focused group sorting tests covered
autocomplete-adjacent group behavior, and the GUI smoke covered editor CRUD,
validation, option-row, group, dirty-form, delete, and save/cancel paths.

Acceptance criteria notes:
- Existing editor workflows still work in the focused smoke check.
- Question list cards are more scannable, with Q badges, type/category badges,
  wrapped prompt text, and narrower vertical action stacks.
- Add, edit, update, and cancel states are visually clearer through the form
  title, mode badge, primary update/add button, and secondary cancel action.
- Native validation warnings remain unchanged; the warning path was smoke
  checked with messagebox stubs because native dialogs block scripted capture.
- Dense two-column editing is preserved at the documented minimum window size,
  with both columns independently scrollable.
- Minimum-window editor evidence is now clean in light and dark mode; the group
  autocomplete dropdown is visible only in the dedicated autocomplete evidence
  screenshots.

Risks:
- Minimum-width editor layout remains dense. It is usable in the captured state,
  but very long question text, group names, and options should be rechecked in
  `STORY-016_light_dark_and_min_size_validation.md`.
- The autocomplete dropdown still uses its existing toplevel click-binding
  implementation. This story only restyled it and smoke-checked display and
  selection.
- `CTkScrollableFrame` internal canvas access is used only by screenshot states
  to position evidence; runtime editor behavior does not depend on it.

Follow-up backlog items:
- Include long editor prompt, option, group, and essay answer cases in
  `STORY-016_light_dark_and_min_size_validation.md`.
