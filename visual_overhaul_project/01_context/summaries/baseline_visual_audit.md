# Baseline Visual Audit

## Metadata

- Summary ID: CTX-AUDIT-BASELINE.
- Produced by: `visual_overhaul_project/02_research_tasks/R-001_baseline_visual_audit.md`.
- Capture dates: initial scripted screenshot set captured 2026-06-06; supplemental mixed-test partial/multi-group states captured 2026-06-15.
- Status: Ready.
- Environment: macOS GUI-capable runner, Python 3.13.4, CustomTkinter app launched through `visual_overhaul_project/tools/capture_baseline_screenshots.py`.
- Data setup: the capture harness created an isolated temporary SQLite database with representative active, archived, grouped, ungrouped, essay, mix-test, history, analytics, and review data. It did not touch the user's normal application database.
- Capture command for 2026-06-15 supplemental states:

```bash
MPLCONFIGDIR=/private/tmp/study-test-tool-mpl XDG_CACHE_HOME=/private/tmp/study-test-tool-xdg python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --mode both --states test_taking_mix_partial_group test_taking_mix_multi_group
```

- Validation command:

```bash
python3 visual_overhaul_project/tools/capture_baseline_screenshots.py --validate-only
```

- Validation result: passed for the combined 42 screenshot files.
- PM review: accepted on 2026-06-15 for foundation and implementation use.
- File-level manifest: `baseline_screenshot_manifest.md`.

## Purpose

Establish the current visual baseline of Study Testing Tool so Sprint 0
foundation work can target observed UI problems rather than guesses.

## Screenshot Inventory

Screenshots are stored under:

- `visual_overhaul_project/01_context/screenshots/baseline/light/`
- `visual_overhaul_project/01_context/screenshots/baseline/dark/`

The current validated set includes 42 files: 38 screenshots from the earlier
scripted capture pass and 4 supplemental mixed-test screenshots from
2026-06-15. See `baseline_screenshot_manifest.md` for per-file capture
timestamps and source labels. Captured in both light and dark mode:

- Home: `home_populated_grouped`, `home_empty_state`.
- Dialogs: `mode_selection_dialog`, `mix_test_dialog`.
- Editor: `editor_new_test`, `editor_existing_test_with_questions`.
- Test taking: `test_taking_unanswered`, `test_taking_answered_flagged`, `test_taking_practice_incorrect_feedback`, `test_taking_essay_question`, `test_taking_mix_test`, `test_taking_mix_partial_group`, `test_taking_mix_multi_group`.
- Results: `results_partial_score_essay_flagged`, `results_loaded_from_history`.
- Data views: `history_populated`, `analytics_populated`, `review_missed_questions`.
- Empty states: `history_empty_state`, `analytics_no_data`, `review_empty_state`.

Not captured or only indirectly represented:

- Separate ungrouped-only home state. The populated home screenshot includes an ungrouped collapsed section.
- Expanded archived-test card state. The populated home screenshot includes an archived collapsed section.
- Practice-mode correct-feedback state. Incorrect feedback is captured and should be enough for the initial foundation pass.
- Results all-correct/high-score state. Partial score, essay, flagged, and history-loaded result states are captured.
- Editor multiple-choice edit, essay edit, and validation-warning states. Existing/new editor states are captured, but field-level validation remains uncaptured.
- Native import summary, import error, delete confirmation, and archive confirmation dialogs. The custom mode and mix dialogs are captured; native dialogs remain behavior-only for MVP styling.
- Minimum supported window size. The capture harness uses the default 1000x700 app geometry, producing 2000x1456 retina screenshots.

## App-Wide Findings

- The app is functionally complete but still visually reads as a default CustomTkinter desktop tool. Gradients, default blue buttons, and default gray panels are visible across most screens.
- Button hierarchy is inconsistent. Primary, secondary, utility, warning, danger, and special actions often have the same size and similar emphasis, while color alone carries too much meaning.
- The current palette is split between default CTk theme colors, shared constants, inline grays, warning/success/danger colors, and a one-off purple Mix Test action.
- Screen backgrounds and content surfaces are close in tone. Many frames look like nested gray panels rather than deliberate cards, rows, or sections.
- Borders and dividers are mostly absent, so dense screens rely on spacing alone to separate toolbar, content, and action areas.
- Empty states are plain labels in otherwise empty gray areas. They explain the state but do not create a polished first-run or no-data experience.
- Light and dark modes both work, but the visual system is not equivalent across modes. Dark mode often has stronger contrast, while light mode can look washed out because large gray areas have low surface separation.
- The macOS window chrome and app title bar are visible in every screenshot; the app interior needs stronger hierarchy so it does not feel subordinate to the frame.

## Per-Screen Findings

### Home / Test Selector

- The top action area has six large buttons split across the width. Import, New Test, Mix Test, Review Missed, View History, and Analytics compete for attention even though New Test/Take Test workflows should be clearer priorities.
- Mix Test uses a distinct purple role, Review Missed uses warning orange, and Analytics uses gray; this creates a noisy action palette before the user reaches any study content.
- The populated grouped view uses large collapsed group headers with blue disclosure text. This is readable, but the content area below is mostly empty when groups are collapsed, which makes the page feel unfinished.
- The sort toolbar is functional but visually heavy relative to the collapsed content.
- Empty home state is a single gray sentence. It needs a designed empty surface with a clear import/create action hierarchy.
- Archived and ungrouped states are represented as collapsed sections, but expanded archived card treatment still needs validation during home implementation.

### Test Taking

- The test title is very large and competes with the timer/progress/flag row. At default size this is readable, but long titles or minimum-window checks remain a risk.
- The main question area is a broad gray card with a scrollbar even when the content is short. This gives the core study area less focus than it should have.
- Essay input uses a large default white textbox in light mode and a default dark textbox in dark mode; both are functional but not integrated with the surrounding panel.
- Multiple-choice answer rows still feel like controls placed in a frame rather than full-width selectable answer choices.
- Finish Test is styled as danger red even though finishing a test is a normal completion action. Destructive color should be reserved for destructive or irreversible operations.
- Progress buttons are useful and compact, but the current/current-success color overlap makes state meaning less precise.
- Practice incorrect feedback is captured and readable, but feedback presentation is still text-heavy and should become a calmer designed state.
- Mix-test states now include full, partial-group, and multi-group captures. These confirm that the shell must preserve source-test context without adding visual clutter.

### Results

- The score is immediately visible, but the result header is mostly a large centered number plus metadata. It needs a stronger summary composition without becoming decorative.
- Back to Home and Retake Test have equal visual weight. Retake is a primary follow-up action in some contexts, while Back is navigational.
- Review content is readable, but cards use stacked text blocks rather than a structured comparison layout. Incorrect/correct answer text colors work, but status badges would scan better.
- Essay self-evaluation uses muted gray text that is clear enough in dark mode but should become a named neutral status.
- Mix-test source breakdown is supported by the app and should share card/list rules with results and history.

### Editor

- The editor is dense but usable. The two-column structure is helpful, yet the panel hierarchy relies mostly on default CTk frames and spacing.
- New-test and existing-test states show that metadata, question list, and editing form all need a shared section/card treatment.
- Question list cards are present but less polished than home/results cards because padding, title treatment, and action emphasis are not standardized.
- Validation-warning and edit-mode field states remain uncaptured; implementation should preserve current messagebox behavior unless a separate story changes validation UX.

### History

- Populated history has a table-like layout with clear columns, but row styling is flat and has weak clickable affordance.
- Filter controls are large compared with the table rows, which can make the top area feel heavier than the data.
- Empty history is plain text and should use the shared empty-state pattern.
- Loading is not separately captured by the harness; keep loading treatment in the shared empty/loading/error state story.

### Analytics

- The analytics screen has the clearest need for chart token alignment. In dark mode, the chart itself is dark but sits inside a white Matplotlib figure background, creating a bright rectangle that breaks the dark theme.
- Tabs and filters are functional, but they look like default controls rather than a coherent segmented/tab pattern.
- Weak-topic cards and chart states need to share semantic status colors with the rest of the app.
- No-data analytics is plain text and should use the shared no-data pattern.

### Review

- Review has a dense control stack: back/title, scope selection, select/deselect actions, filter segment, selected count, start action, and missed-question list.
- The scope selector and question cards are functional but visually heavy, especially in dark mode where stacked gray panels dominate.
- Start Review is currently success green. Foundation work should decide whether green is reserved for outcomes/statuses or also for positive workflow actions.
- Empty review is a plain label and should follow the same empty-state pattern as home, history, and analytics.

### Dialogs

- Mode selection and Mix Test dialogs are clear and functional, but they use default modal surfaces and button styling.
- Mix Test has a useful grouped selection structure; visual work must preserve group/child checkbox synchronization and selected-count behavior.
- Native import, error, delete, archive, and confirmation dialogs are not captured and should remain behavior-only for MVP unless a later product decision replaces them with custom CTk dialogs.

## Light / Dark Differences

- Dark mode is generally readable and benefits from stronger background contrast, but default gray panels can stack into a heavy, low-polish look.
- Light mode is readable but has many low-contrast gray surfaces. Large content areas can look washed out, especially home and test-taking.
- Chart rendering is the most obvious dark-mode mismatch because the Matplotlib figure area remains bright around the dark plot.
- Status colors preserve meaning in both modes, but success/warning/danger/action colors need named roles and tuned hover states.
- Tuple colors should remain available in the token system because current CTk widgets already use light/dark tuples for a few surfaces.

## Minimum Window Concerns

Minimum size was not captured. Source inspection plus default-size screenshots indicate the highest-risk areas:

- Home: six-button top action row, sort controls, and group headers.
- Test taking: title, timer, progress, flag, scrollable question area, bottom navigation, and progress buttons.
- Editor: metadata form, question list, and form panel in a two-column layout.
- Review: scope selector, filter segment, selected count, action bar, and list content.
- History and analytics: filter controls above dense data/chart content.

`STORY-016_light_dark_and_min_size_validation.md` should keep minimum-window checks as a validation task after shared patterns and core screen work land.

## Priority Issues For Foundation vs Screen Work

Foundation work should solve:

- App background, surface, surface-muted, border, divider, and text roles.
- Button hierarchy and hover roles for primary, secondary, tertiary, danger, warning, success, and special actions.
- Status roles for correct, incorrect, essay/neutral, flagged, answered, unanswered, and current.
- Shared typography scale for page titles, section headings, card titles, body, metadata, labels, and compact controls.
- Card/list row spacing, radius, padding, border, and metadata treatment.
- Empty/loading/error state treatment.
- Chart colors and Matplotlib figure/background alignment.

Screen work should solve:

- Home composition, action order, expanded card presentation, and empty state.
- Test-taking shell, answer rows, practice feedback, progress state, and non-danger Finish action.
- Results summary, answer comparison cards, status badges, and mix breakdown.
- Editor density, form grouping, question list polish, and validation affordances.
- History row affordance, analytics tabs/charts/topic cards, and review selection density.
- Custom dialog polish for mode and mix flows.

## Dev 2 Quick Start

- Start with `visual_foundation_decisions.md`, `style_inventory.md`, and these baseline screenshots before writing visual code.
- Use the screenshots as before-state evidence, not as a design target.
- First implementation work should centralize tokens and role helpers, then pilot them on a narrow screen before broad replacement.
- Treat `fg_color="gray"` and `text_color="gray"` as multiple roles, not one token.
- Preserve current navigation, services, scoring, import/export, review selection, and session behavior.
- Do not replace native messageboxes or file dialogs during MVP visual token work.
- Verify every visual implementation story in light and dark mode; use minimum-size validation in Sprint 4 or when a story touches crowded layouts.

## Recommendation

The baseline audit is accepted as Ready. It is sufficient input, together with
`style_inventory.md`, for the visual foundation and later validation work.
