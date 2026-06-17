# Visual Overhaul Backlog Index

## Backlog Policy

Stories should stay narrow. Prefer one screen, one shared component family, or
one design-system decision per story. If a story needs broad research, create or
complete a research task first.

Do not assign implementation stories to junior developers until the required
research summaries are Ready under `00_project/definition_of_ready.md`.

## Epic Order

| Epic | Goal | Story Files |
| --- | --- | --- |
| E0 Discovery And Context | Build reusable context and baseline audit before visual changes | `STORY-001_context_batch_one.md`, `STORY-002_baseline_visual_audit.md` |
| E1 Visual Foundation | Define app-wide tokens and reusable patterns | `STORY-003_visual_foundation_spec.md`, `STORY-004_shared_style_entrypoints.md`, `STORY-005_button_hierarchy.md`, `STORY-006_card_and_list_patterns.md`, `STORY-007_page_header_pattern.md` |
| E2 Home Screen | Polish first impression and test-card workflows | `STORY-008_home_screen_layout.md`, `STORY-009_home_test_cards_and_actions.md` |
| E3 Core Study Flow | Polish test-taking and results | `STORY-010_test_taking_shell.md`, `STORY-011_answer_rows_and_practice_feedback.md`, `STORY-012_results_summary_and_review_cards.md` |
| E4 Secondary Screens | Polish editor, history, analytics, review, and dialogs | `STORY-013_editor_layout.md`, `STORY-014_history_and_analytics_polish.md` split into `STORY-014A_history_list_and_filters.md`, `STORY-014B_analytics_chart_shell.md`, `STORY-014C_analytics_weak_topics_and_no_data.md`; `STORY-015_review_and_dialog_polish.md` split into child stories |
| E5 Stabilization | Validate light/dark mode, minimum size, and MVP closure | `STORY-016_light_dark_and_min_size_validation.md`, `STORY-017_mvp_visual_regression_pass.md` |

## Priority Queue

1. Assign Sprint 0 research tasks and produce context summaries.
2. Review summaries against the Definition of Ready.
3. Approve the visual foundation.
4. Implement shared style entrypoints.
5. Polish home screen.
6. Polish test-taking.
7. Polish results.
8. Polish editor.
9. Polish history, analytics, review, and dialogs through their split child
   stories.
10. Complete validation and closeout.

## Backlog Status

All stories are initially `Ready` only when their required context summaries
exist and pass the Definition of Ready. Stories that depend on missing or stale
summaries are `Blocked` until the relevant research task is complete and
reviewed.

For the current project scan, use
`visual_overhaul_project/00_project/status_board.md`. For dependency planning,
use `visual_overhaul_project/03_backlog/dependency_map.md`.

## Post-MVP Recommendation Queue

The MVP visual overhaul is closed through
`STORY-017_mvp_visual_regression_pass.md`. Do not assign these recommendations
as MVP work unless the product owner reopens scope.

1. Add long-content stress screenshot fixtures across Home, Test Taking,
   Results, Editor, History, Analytics Weak Topics, Review, Mix dialog, and
   Import Preview.
2. Tune Analytics Study Activity for one populated day, where the current chart
   renders a readable but visually heavy wide bar.
3. Evaluate custom report or confirmation patterns for native import reports,
   export warnings, missing-answer confirmations, and other native dialogs.
4. Track the pre-existing History loading exception callback issue as a
   non-visual engineering cleanup if it is not already handled elsewhere.
