# Dependency Map

This map shows the intended path from research to summaries to stories. Use it
when assigning work or checking whether a story is ready.

An implementation story is not ready until every required summary exists and
passes `00_project/definition_of_ready.md`.

## Sprint 0 Dependencies

| Research/Story | Produces | Unblocks |
| --- | --- | --- |
| `STORY-001_context_batch_one.md` | Coordinates R-002 output and seeded summary refresh | `STORY-003`, `STORY-004` |
| `STORY-002_baseline_visual_audit.md` | Coordinates R-001 output and screenshot review | `STORY-003`, `STORY-016`, `STORY-017` |
| `R-002_component_style_inventory.md` | `style_inventory.md` | `STORY-003`, `STORY-004`, `STORY-005`, `STORY-006` |
| `R-001_baseline_visual_audit.md` | `baseline_visual_audit.md` | `STORY-003`, validation stories |

## Foundation Dependencies

| Story | Requires | Produces/Enables |
| --- | --- | --- |
| `STORY-003_visual_foundation_spec.md` | CTX-AUDIT-BASELINE, CTX-STYLE-INVENTORY | CTX-FOUNDATION |
| `STORY-004_shared_style_entrypoints.md` | CTX-FOUNDATION, CTX-STYLE-INVENTORY | Shared style implementation path |
| `STORY-005_button_hierarchy.md` | CTX-FOUNDATION | Button role consistency |
| `STORY-006_card_and_list_patterns.md` | CTX-FOUNDATION, named pilot area | Card/list pattern pilot |
| `STORY-007_page_header_pattern.md` | CTX-FOUNDATION | Header pattern pilot |

## Screen Context Dependencies

| Research Task | Produces | Unblocks |
| --- | --- | --- |
| `R-003_home_screen_context.md` | CTX-HOME | `STORY-008`, `STORY-009` |
| `R-004_test_taking_context.md` | CTX-TEST-TAKING | `STORY-010`, `STORY-011` |
| `R-005_results_context.md` | CTX-RESULTS | `STORY-012` |
| `R-006_editor_context.md` | CTX-EDITOR | `STORY-013` |
| `R-007_history_analytics_review_context.md` | CTX-DATA-VIEWS | `STORY-014A`, `STORY-014B`, `STORY-014C`, `STORY-015A` |
| `R-008_dialog_context.md` | CTX-DIALOGS | `STORY-015B`, `STORY-015C`, `STORY-015D`, `STORY-015E` |

`R-007` and `R-008` recommend smaller story splits before broad parent stories
are assigned to junior implementation agents. `STORY-014` and `STORY-015` have
been split; assign the child stories instead.

## Implementation Dependencies

| Story | Requires | Should Run After |
| --- | --- | --- |
| `STORY-008_home_screen_layout.md` | CTX-HOME, CTX-FOUNDATION | `STORY-004`, `STORY-005`, optional `STORY-007` |
| `STORY-009_home_test_cards_and_actions.md` | CTX-HOME, CTX-FOUNDATION | `STORY-006`, `STORY-008` |
| `STORY-010_test_taking_shell.md` | CTX-TEST-TAKING, CTX-FOUNDATION | `STORY-004`, `STORY-005`, optional `STORY-007` |
| `STORY-011_answer_rows_and_practice_feedback.md` | CTX-TEST-TAKING, CTX-FOUNDATION | `STORY-010` |
| `STORY-012_results_summary_and_review_cards.md` | CTX-RESULTS, CTX-FOUNDATION | `STORY-006` |
| `STORY-013_editor_layout.md` | CTX-EDITOR, CTX-FOUNDATION | Foundation stories |
| `STORY-014_history_and_analytics_polish.md` | CTX-DATA-VIEWS, CTX-FOUNDATION, PM split | Parent split complete; do not assign |
| `STORY-014A_history_list_and_filters.md` | CTX-DATA-VIEWS, CTX-FOUNDATION, accepted foundation handoffs | Foundation stories |
| `STORY-014B_analytics_chart_shell.md` | CTX-DATA-VIEWS, CTX-FOUNDATION, accepted foundation handoffs | Foundation stories |
| `STORY-014C_analytics_weak_topics_and_no_data.md` | CTX-DATA-VIEWS, CTX-FOUNDATION, accepted foundation handoffs | Foundation stories |
| `STORY-015_review_and_dialog_polish.md` | CTX-DATA-VIEWS, CTX-DIALOGS, CTX-FOUNDATION, PM split | Parent split complete; do not assign |
| `STORY-015A_review_screen_polish.md` | CTX-DATA-VIEWS, CTX-FOUNDATION, accepted foundation handoffs | Foundation stories |
| `STORY-015B_mode_dialog_polish.md` | CTX-DIALOGS, CTX-FOUNDATION, accepted foundation handoffs | Foundation stories |
| `STORY-015C_mix_dialog_polish.md` | CTX-DIALOGS, CTX-FOUNDATION, accepted foundation handoffs | Foundation stories |
| `STORY-015D_import_preview_dialog_polish.md` | CTX-DIALOGS, CTX-FOUNDATION, accepted foundation handoffs | Foundation stories |
| `STORY-015E_native_dialog_inventory_followup.md` | CTX-DIALOGS, PM post-MVP decision | Post-MVP PM decision |

## Closeout Dependencies

| Story | Requires |
| --- | --- |
| `STORY-016_light_dark_and_min_size_validation.md` | Completed MVP screen stories |
| `STORY-017_mvp_visual_regression_pass.md` | Acceptance matrix, baseline audit, foundation decisions, completed handoffs |
