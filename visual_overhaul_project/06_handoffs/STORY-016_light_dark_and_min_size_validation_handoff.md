Story/Task:
STORY-016: Light/Dark And Minimum-Size Validation

Status:
Submitted For Review.

Summary:
Completed the validation-only pass across the MVP visual overhaul evidence set.
No application runtime code was changed. The screenshot harness now includes a
Results minimum-window state, and the `STORY-016` evidence folder contains 138
validated screenshots covering every harness-supported MVP screen, custom
dialog, empty state, and minimum-size state.

Files changed:
- `visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `visual_overhaul_project/00_project/status_board.md`
- `visual_overhaul_project/04_stories/STORY-016_light_dark_and_min_size_validation.md`
- `visual_overhaul_project/06_handoffs/STORY-016_light_dark_and_min_size_validation_handoff.md`
- `visual_overhaul_project/01_context/screenshots/after/STORY-016/`

Definition of Ready checked:
- `baseline_visual_audit.md` is Ready.
- `visual_foundation_decisions.md` is Ready.
- PM accepted `STORY-008` through `STORY-015E`.
- PM assigned `STORY-016` as a validation-only pass on 2026-06-17.

Context summaries read:
- `visual_overhaul_project/01_context/summaries/baseline_visual_audit.md`
- `visual_overhaul_project/01_context/summaries/visual_foundation_decisions.md`
- `visual_overhaul_project/06_handoffs/screenshot_checklist.md`
- Completed story handoffs and PM review notes for `STORY-008` through
  `STORY-015E`.

Context summaries created/updated:
None.

Screens/states checked:

| Area | Light/dark evidence | Minimum evidence | Result | Notes |
| --- | --- | --- | --- | --- |
| Home | Populated grouped, expanded active cards, expanded archived cards, empty state | Populated and empty | Pass | No clipping, hidden primary action, or unreadable contrast seen in captured states. |
| Test Taking | Unanswered, answered/flagged, selected answer, middle, last, review session, practice correct/incorrect/checked return, essay, mix variants | Unanswered shell | Pass | Long answer stress remains a follow-up coverage gap. |
| Results | All-correct, partial/essay/flagged, essay review, missing answer, mix breakdown, history-loaded | Partial score/essay/flagged | Pass | Added `results_minimum_partial_score` harness state for this validation pass. |
| Editor | New, existing populated, saved empty, MC add, essay add, edit question, group autocomplete | Existing populated | Pass | Minimum layout remains dense but usable in captured state. Long editor content remains a follow-up coverage gap. |
| History | Populated, filtered, loading, empty | Populated | Pass | Long test names remain a follow-up coverage gap. |
| Analytics | Score trends, test comparison, study activity, chart no-data, Weak Topics by test/group/category, no-category, no-data | Score trends and Weak Topics | Pass with note | Single-day Study Activity still renders as one wide bar; classify as post-MVP chart-readability follow-up unless PM wants more chart states before release. |
| Review | Missed questions, selected scope, selected question, no selected tests, no missed questions, empty/no active tests | Missed questions | Pass | Long missed-question text remains a follow-up coverage gap. |
| Mode dialog | Initial dialog | Fixed-size modal, no dedicated minimum-host state | Pass | Full-size light/dark evidence showed no clipping or contrast blocker. |
| Mix dialog | Empty/default, Select All, one group selected, deselected | Fixed-size modal, no dedicated minimum-host state | Pass | Larger source lists and long names remain follow-up coverage. |
| Import Preview dialog | All-ready, mixed warning/skipped, no-importable disabled Import, group override | Fixed-size modal, no dedicated minimum-host state | Pass | Extremely long preview names remain follow-up coverage. |
| Native dialogs | Documented exception | Documented exception | Accepted limitation | Native messageboxes/file dialogs intentionally remain native for MVP per `STORY-015E`. |

Screenshot evidence:
- Primary folder:
  `visual_overhaul_project/01_context/screenshots/after/STORY-016/`
- Count: 138 screenshots.
- Modes: light and dark.
- Capture command:
  `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --group all --output visual_overhaul_project/01_context/screenshots/after/STORY-016`
- Added Results minimum recapture:
  `MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states results_minimum_partial_score --output visual_overhaul_project/01_context/screenshots/after/STORY-016`

Tests run:
- `python3 -m compileall -q visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `python3 -m black --check visual_overhaul_project/tools/capture_baseline_screenshots.py`
- `PYTHONPATH=study_test_tool python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only --mode both --group all --output visual_overhaul_project/01_context/screenshots/after/STORY-016`
- `git diff --check`

Tests not run and why:
- Full pytest was not run because no application runtime code, service logic,
  persistence, scoring, import/export, or navigation behavior changed. The only
  code edit is a screenshot harness state for validation evidence.

Issues fixed:
- Added `results_minimum_partial_score` to the screenshot harness so Results
  minimum-window validation has direct light/dark evidence.

Follow-up issues:
- MVP blockers: none found in harness-covered states.
- Post-MVP follow-up: Analytics Study Activity with a single populated day
  renders as one very wide bar. This was previously accepted for chart-shell
  scope and remains service-consistent, but a future chart-readability story
  should add richer multi-day fixtures and tune the one-day presentation.
- Accepted limitation for MVP: native messageboxes and file dialogs remain
  native and visually inconsistent with CustomTkinter surfaces by design per
  `STORY-015E`.
- Coverage gap for PM decision: long-content stress cases are not fully covered
  by the current seeded harness data. Candidate stress states for `STORY-017`
  or a narrow follow-up are long Home card names/descriptions/groups, long
  answer options, long Results answer/essay text, long editor prompts/options
  and group names, long History test names, dense Weak Topics lists with long
  topic names, long Review question text, larger Mix dialog source lists, and
  long Import Preview names.

Acceptance criteria notes:
- Every MVP screen family has light/dark evidence in the `STORY-016` folder.
- Every main MVP screen family now has at least one minimum-window evidence
  state where practical.
- No captured state showed blocking text clipping, incoherent overlap,
  unreadable contrast, broken scroll behavior, or hidden primary actions.
- No application fixes were made because this story was assigned as validation
  only and no MVP blocker was found in the captured states.

Risks:
- The validation pass is only as strong as the seeded harness fixtures. It is
  representative, not exhaustive for arbitrary user-authored long text.
- Custom dialogs are fixed-size modal windows; they were validated in light and
  dark mode, but not through separate minimum-host screenshot states.

Follow-up backlog items:
- PM should decide whether the long-content stress coverage gap belongs in
  `STORY-017_mvp_visual_regression_pass.md` or a narrow post-MVP validation
  fixture story.
