# History, Analytics, And Review Context

## Metadata

- Summary ID: `CTX-DATA-VIEWS`.
- Produced by: `R-007_history_analytics_review_context.md`.
- Source scope: history, analytics, review, charts, and data-state UI only.
- Status note: the task header still says "Blocked until R-001 or R-002 is Done," but the status board already marks `R-007` Ready with assignment gate `R-002 Done`, so work proceeded on the basis of the board and the already-complete `R-002` gate.

## Purpose

Give implementation stories focused context for the secondary data-view screens so polish work can start without re-reading the full screen code.

## Findings

### 1. Per-screen workflow and state map

#### History

- Structure: a transparent top bar with a gray `< Back` button and `Test History` title, followed by a filter row, a table header, a scrollable table body, and a plain empty label. (source: `study_test_tool/gui/history_view.py:34-129`)
- Filters: one `CTkOptionMenu` for test name and one for mode (`All Modes`, `Test`, `Practice`). The filter list is populated from `TestService.get_all_tests()` on load. (source: `study_test_tool/gui/history_view.py:54-88`, `study_test_tool/gui/history_view.py:148-158`)
- Loading state: `on_show()` shows `Loading...`, clears the table, and loads attempts/tests on a background thread before updating the UI on the main thread. (source: `study_test_tool/gui/history_view.py:131-163`)
- Row model: each attempt row shows Date, Test Name, Mode, Score, %, and Time. Dates are truncated to 16 characters, mode is capitalized, and click targets are attached to the whole row and every label. (source: `study_test_tool/gui/history_view.py:203-245`)
- Empty/no-data state: one gray label, `No test history yet.`; there is no richer empty illustration or helper text. (source: `study_test_tool/gui/history_view.py:123-129`, `study_test_tool/gui/history_view.py:190-199`)

#### Analytics

- Structure: a back/title top bar, a segmented tab strip, a test filter row, a content area, a reusable graph widget, a weak-topics scroll area, and one shared empty label. (source: `study_test_tool/gui/analytics_view.py:32-115`)
- Tabs: `Score Trends`, `Test Comparison`, `Study Activity`, and `Weak Topics`. Tab changes rerender the content immediately. (source: `study_test_tool/gui/analytics_view.py:52-63`, `study_test_tool/gui/analytics_view.py:147-171`)
- Filters: a test `CTkOptionMenu` is always visible; `Group by` appears only on `Weak Topics` and offers `Test`, `Group`, and `Category`. (source: `study_test_tool/gui/analytics_view.py:65-97`, `study_test_tool/gui/analytics_view.py:156-162`)
- Score Trends state: pulls chronological scores, converts them to attempt indices, and renders a line chart labeled `Attempt #` vs `Score (%)`. Empty data uses the shared gray no-data label. (source: `study_test_tool/gui/analytics_view.py:173-193`, `study_test_tool/tests/test_analytics_service.py:11-47`)
- Test Comparison state: pulls per-test averages and renders a bar chart titled `Average Scores by Test`. (source: `study_test_tool/gui/analytics_view.py:194-211`, `study_test_tool/tests/test_analytics_service.py:53-75`)
- Study Activity state: pulls attempt frequency for the last 30 days, shortens the x-axis date labels, and renders a bar chart titled `Study Activity (Last 30 Days)`. (source: `study_test_tool/gui/analytics_view.py:213-231`, `study_test_tool/tests/test_analytics_service.py:80-96`)
- Weak Topics state: uses `get_weak_topics()` with the selected grouping, then renders scrollable cards with a color indicator bar, category title, status label, progress bar, and small gray stats line. Empty category grouping gets a special helper message about missing tags. (source: `study_test_tool/gui/analytics_view.py:233-320`, `study_test_tool/tests/test_analytics_service.py:267-315`, `study_test_tool/tests/test_analytics_service.py:359-493`)

#### Review

- Structure: a back/title top bar, a scope summary/filter row, a grouped test-scope selector, an action bar, a scrollable question list, and a plain empty label. (source: `study_test_tool/gui/review_view.py:39-155`)
- Scope workflow: `on_show()` rebuilds the active-test scope list, resets the filter to `All Missed`, and reloads the question list. Scope state is grouped by test name using `group_tests_by_name()`. (source: `study_test_tool/gui/review_view.py:157-166`, `study_test_tool/gui/review_view.py:168-223`)
- Selection behavior: there are group checkboxes, per-test checkboxes, a `Select All` checkbox, `Select All` and `Deselect All` buttons, a selected-count label, and a green `Start Review` button. (source: `study_test_tool/gui/review_view.py:86-144`, `study_test_tool/gui/review_view.py:225-255`)
- Question card state: each missed-question card contains a checkbox, the question text, and metadata for test name, category, and miss rate. (source: `study_test_tool/gui/review_view.py:322-406`)
- Empty/no-data states: `No active tests available.` when no active tests exist, `No missed questions found.` when filters produce nothing, and `No tests selected` / `No active tests` status text in the scope summary label. (source: `study_test_tool/gui/review_view.py:183-191`, `study_test_tool/gui/review_view.py:271-304`, `study_test_tool/gui/review_view.py:332-335`)
- Start behavior: when nothing is selected, `Start Review` falls back to all displayed missed questions and launches practice mode in `SCREEN_TEST_TAKING` with `review_question_ids`. (source: `study_test_tool/gui/review_view.py:409-428`)

### 2. Common data-view visual patterns

- All three screens use the same top-bar pattern: transparent frame, 30px horizontal margin, gray back button, and bold page title. (source: `study_test_tool/gui/history_view.py:34-52`, `study_test_tool/gui/analytics_view.py:32-50`, `study_test_tool/gui/review_view.py:39-57`)
- Filters and controls sit in dedicated rows above the content instead of being embedded in the list/chart surface. That makes the content area the main focus and creates a reusable layout pattern. (source: `study_test_tool/gui/history_view.py:54-88`, `study_test_tool/gui/analytics_view.py:65-97`, `study_test_tool/gui/review_view.py:59-144`)
- Empty states are still plain gray text labels, not designed states. Loading is also plain text (`Loading...`) rather than a branded skeleton or panel. (source: `study_test_tool/gui/history_view.py:90-97`, `study_test_tool/gui/history_view.py:123-129`, `study_test_tool/gui/analytics_view.py:109-115`, `study_test_tool/gui/review_view.py:149-155`)
- Interactive data rows are inconsistent: history uses full-row click targets, review uses checkboxes plus action buttons, and analytics uses tab/filter controls plus cards. The visual redesign should standardize list-row spacing, metadata placement, and selected-state affordances without changing the underlying behaviors. (source: `study_test_tool/gui/history_view.py:203-245`, `study_test_tool/gui/review_view.py:322-428`, `study_test_tool/gui/analytics_view.py:233-320`)
- Typography is already constrained to the shared app scale: title, body, small, and heading fonts from `config.settings`. That makes hierarchy a spacing/padding/card problem more than a font-family problem. (source: `study_test_tool/gui/history_view.py:8-14`, `study_test_tool/gui/analytics_view.py:5-13`, `study_test_tool/gui/review_view.py:7-14`, `study_test_tool/config/settings.py:38-42`)

### 3. Chart theme findings

- `GraphWidget` owns its own matplotlib theme instead of inheriting app surface tokens. Light mode uses white chart backgrounds and dark-gray text/grid; dark mode uses `#2b2b2b` backgrounds, white text, `#404040` grid lines, and `#4a9eff` line/bar colors. (source: `study_test_tool/gui/components/graph_widget.py:29-46`)
- Chart titles and axes are bare matplotlib defaults with no legend, subtitle, or annotation layer. The charts are functional, but they feel visually separate from the rest of the app because they are not framed with the same card/spacing language. (source: `study_test_tool/gui/components/graph_widget.py:68-185`)
- The topic-status palette in settings maps directly to analytics weak-topic states: weak uses danger red, moderate uses warning orange, and strong uses success green. (source: `study_test_tool/config/settings.py:26-35`, `study_test_tool/config/settings.py:49-51`, `study_test_tool/gui/analytics_view.py:269-313`)

### 4. Empty/loading/no-data findings

- History: only one loading label and one empty label. There is no distinct empty-state treatment for "no tests yet" versus "filter removed everything," so the same plain label covers both conditions. (source: `study_test_tool/gui/history_view.py:90-97`, `study_test_tool/gui/history_view.py:190-199`)
- Analytics: every chart tab shares the same empty label. Weak Topics has one extra message for the "no categories tagged" case, but there is no separate empty design for chart tabs versus list tabs. (source: `study_test_tool/gui/analytics_view.py:109-115`, `study_test_tool/gui/analytics_view.py:173-257`)
- Review: the screen has three empty-ish states already in play: no active tests, no tests selected, and no missed questions. These states are text-only and will need careful visual distinction in polish work so the user knows whether they should change scope or simply switch tests. (source: `study_test_tool/gui/review_view.py:183-191`, `study_test_tool/gui/review_view.py:271-304`, `study_test_tool/gui/review_view.py:332-335`)

### 5. Behavior constraints the visual work must not change

- Analytics calculations are fixed by service behavior: score trends and test comparison default to `mode="test"`, study activity is based on a 30-day lookback, and weak-topic classification uses the threshold/status rules from `AnalyticsService`. (source: `study_test_tool/services/analytics_service.py:11-64`, `study_test_tool/tests/test_analytics_service.py:11-96`, `study_test_tool/tests/test_analytics_service.py:267-315`)
- Category/grouping behavior is semantic, not visual: `group_by` supports `auto`, `category`, `test`, and `group`; invalid values raise `ValueError`; and explicit `group_by="category"` returns `[]` if no categories exist instead of falling back. (source: `study_test_tool/tests/test_analytics_service.py:359-493`)
- Review selection behavior is constrained by the service: archived tests are excluded, a single-test filter and multi-test filter cannot be combined, and `create_review_session_questions()` resolves IDs into full `Question` objects. (source: `study_test_tool/services/review_service.py:14-52`, `study_test_tool/tests/test_review_service.py:94-153`, `study_test_tool/tests/test_review_service.py:192-297`)
- Scoring behavior is also fixed: essay questions do not count toward scored totals, and practice mode uses checked responses rather than later-edited answers. That matters because review polish must not imply a different session or scoring contract. (source: `study_test_tool/tests/test_scoring_service.py:65-104`)

### 6. Screenshots and seeded data still needed

- I did not verify any live screenshots, so light/dark polish still needs runtime confirmation on history, analytics, and review.
- Seeded data is still needed to validate the important visual branches: populated history rows, an empty history, score-trend lines, comparison bars, 30-day activity bars, weak-topic cards in all three statuses, no-category weak topics, no active tests, and review scope selection across multiple groups.
- The review and analytics screens both have state combinations that are hard to judge statically. They should be validated with runtime data before any final spacing or emphasis choices are locked.

### 7. Recommended story split

- History should be its own story: filter row, table header, row styling, click affordance, and empty/loading treatment.
- Analytics should be split at least into two stories: one for the chart shell and filter/tab hierarchy, and one for weak-topic card polish and grouping states.
- Review should be its own story: scope selector, selected-count/action bar, question-card polish, and the selection-to-practice launch surface.
- Do not bundle history, analytics, and review into one implementation story. The shared patterns are real, but the screen behaviors are different enough that one large ticket would be difficult to verify and likely too broad for a clean handoff.

### 8. Dev 2 quick start notes

- Read `CTX-DATA-VIEWS` before touching any polish work, and treat `history_view.py`, `analytics_view.py`, `review_view.py`, and `graph_widget.py` as the visual source of truth for this lane.
- Keep service calls, filter semantics, and review-launch behavior unchanged.
- Treat the shared empty/loading text as a visual gap to improve, not a behavior to redesign.
- Verify the work in both light and dark mode with seeded data, because `GraphWidget` has its own theme and the weak-topic palette is status-coded.
- If a story needs to touch analytics or review polish, confirm whether the runtime data you are looking at represents the no-data, partially populated, or fully populated state before judging spacing and emphasis.

### 9. Source files inspected

- `study_test_tool/gui/history_view.py`
- `study_test_tool/gui/analytics_view.py`
- `study_test_tool/gui/review_view.py`
- `study_test_tool/gui/components/graph_widget.py`
- `study_test_tool/services/analytics_service.py`
- `study_test_tool/services/review_service.py`
- `study_test_tool/config/settings.py`
- `study_test_tool/tests/test_analytics_service.py`
- `study_test_tool/tests/test_review_service.py`
- `study_test_tool/tests/test_scoring_service.py`

### 10. States not inspected

- No live GUI screenshots were captured.
- No seeded runtime data was inspected in the app.
- I did not inspect dialogs, home screen, editor, results, or other unrelated GUI screens for this task.
- I did not change application code, tests, screenshots, or data flow.

## Recommendation

Mark `CTX-DATA-VIEWS` Ready and use it to unblock the next stage of secondary-screen polish, but keep implementation split by screen or by tightly related component family. The most efficient next step is a history story first, then a two-part analytics/review split if the planner wants to preserve small, verifiable tickets.
