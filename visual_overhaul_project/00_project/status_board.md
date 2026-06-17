# Visual Overhaul Status Board

Use this board as the fast project scan. Update it when a research task,
summary, story, or sprint changes state.

## Status Terms

- Missing: expected artifact does not exist yet.
- Placeholder: artifact exists but is not ready for implementation use.
- Seeded: artifact has initial context and may be useful, but should be refreshed
  when source files change or screenshots become available.
- Ready: artifact passes the relevant Definition of Ready gate.
- In Progress: actively owned.
- Submitted For Review: assigned work is complete from the agent side and is
  waiting for reviewer or PM acceptance.
- Changes Requested: reviewer or PM inspected the submitted work and found
  required fixes, missing evidence, or acceptance gaps before it can be accepted.
- Blocked: waiting on a dependency, decision, or environment.
- Done: complete and handed off.
- Stale: artifact exists but source changes or new requirements make it unsafe
  to rely on without refresh.

Use `00_project/definition_of_ready.md` before marking any research task,
context summary, or implementation story Ready.
Use `00_project/status_transition_rules.md` when moving items between statuses.

## Summary Status

| Summary | Status | Unblocks |
| --- | --- | --- |
| `gui_architecture_summary.md` | Ready | Most stories |
| `screen_inventory.md` | Ready | Most stories |
| `current_visual_state_seed.md` | Seeded | Sprint 0 research |
| `baseline_visual_audit.md` | Ready | `STORY-003`, validation stories; 42 scripted light/dark screenshots validate, with remaining uncaptured states documented |
| `style_inventory.md` | Ready | `STORY-003`, `STORY-004` |
| `home_screen_context.md` | Ready | `STORY-008`, `STORY-009` |
| `test_taking_context.md` | Ready | `STORY-010`, `STORY-011` |
| `results_context.md` | Ready | `STORY-012` |
| `editor_context.md` | Ready | `STORY-013` |
| `history_analytics_review_context.md` | Ready | `STORY-014A`, `STORY-014B`, `STORY-014C`, `STORY-015A` |
| `dialog_context.md` | Ready | `STORY-015B`, `STORY-015C`, `STORY-015D`, `STORY-015E` |
| `visual_foundation_decisions.md` | Ready | `STORY-004` through `STORY-017`; accepted for MVP implementation sequencing |

## Research Task Status

| Task | Status | Output | Assignment Gate |
| --- | --- | --- | --- |
| `R-001_baseline_visual_audit.md` | Done | `baseline_visual_audit.md` | None |
| `R-002_component_style_inventory.md` | Done | `style_inventory.md` | None |
| `R-003_home_screen_context.md` | Done | `home_screen_context.md` | R-002 Done |
| `R-004_test_taking_context.md` | Done | `test_taking_context.md` | R-002 Done |
| `R-005_results_context.md` | Done | `results_context.md` | R-002 Done |
| `R-006_editor_context.md` | Done | `editor_context.md` | R-002 Done |
| `R-007_history_analytics_review_context.md` | Done | `history_analytics_review_context.md` | R-002 Done |
| `R-008_dialog_context.md` | Done | `dialog_context.md` | R-001 Done |

## Story Status

| Story                                             | Status               | Blocked By               |
| ------------------------------------------------- | -------------------- | ------------------------ |
| `STORY-001_context_batch_one.md`                  | Done                 | None                     |
| `STORY-002_baseline_visual_audit.md`              | Done                 | None                     |
| `STORY-003_visual_foundation_spec.md`             | Done                 | None                     |
| `STORY-004_shared_style_entrypoints.md`           | Done                 | None                     |
| `STORY-005_button_hierarchy.md`                   | Done                 | None                     |
| `STORY-006_card_and_list_patterns.md`             | Done                 | None                     |
| `STORY-007_page_header_pattern.md`                | Done                 | None                     |
| `STORY-008_home_screen_layout.md`                 | Done                 | None                     |
| `STORY-009_home_test_cards_and_actions.md`        | Done                 | None                     |
| `STORY-010_test_taking_shell.md`                  | Done                 | None                     |
| `STORY-011_answer_rows_and_practice_feedback.md`  | Done                 | None                     |
| `STORY-012_results_summary_and_review_cards.md`   | Done                 | None                     |
| `STORY-013_editor_layout.md`                      | Done                 | None                     |
| `STORY-014_history_and_analytics_polish.md`       | Done                 | split into child stories |
| `STORY-014A_history_list_and_filters.md`          | Done                 | None                     |
| `STORY-014B_analytics_chart_shell.md`             | Done                 | None                     |
| `STORY-014C_analytics_weak_topics_and_no_data.md` | Done                 | None                     |
| `STORY-015_review_and_dialog_polish.md`           | Done                 | split into child stories |
| `STORY-015A_review_screen_polish.md`              | Done                 | None                     |
| `STORY-015B_mode_dialog_polish.md`                | Done                 | None                     |
| `STORY-015C_mix_dialog_polish.md`                 | Done                 | None                     |
| `STORY-015D_import_preview_dialog_polish.md`      | Done                 | None                     |
| `STORY-015E_native_dialog_inventory_followup.md`  | Done                 | None                     |
| `STORY-016_light_dark_and_min_size_validation.md` | Done                 | None                     |
| `STORY-017_mvp_visual_regression_pass.md`         | Submitted For Review | None                     |

## Next Recommended Work

1. Review `STORY-017_mvp_visual_regression_pass.md` final closeout package.
   Dev 2 submitted the acceptance-matrix review notes, evidence validation,
   full pytest summary, final classifications, and handoff on 2026-06-17.
2. `STORY-016_light_dark_and_min_size_validation.md` is accepted after PM
   review of the 138-screenshot light/dark and minimum-size evidence set plus
   the screen-family validation matrix. Long-content stress coverage gaps and
   the single-day Analytics Study Activity chart presentation should be
   classified during `STORY-017`, not treated as blockers to starting closeout.
3. `STORY-015D_import_preview_dialog_polish.md` is accepted after PM review of
   light/dark all-ready, mixed-warning, no-importable, and group-override
   screenshot evidence plus focused Import Preview return-path verification. No
   follow-up Import Preview work should be assigned unless validation finds a
   concrete issue.
4. `STORY-015E_native_dialog_inventory_followup.md` is closed by PM decision:
   no native messagebox or file-dialog replacement is approved for MVP, and
   all native dialogs remain documented MVP exceptions unless a future
   post-MVP story explicitly replaces one.
5. `STORY-015C_mix_dialog_polish.md` is accepted after PM review of light/dark
   Mix Test dialog empty, Select All, one-group-selected, and deselected
   evidence plus selection sync, invalid-start, valid-start, and cancel
   behavior. No follow-up Mix dialog polish work should be assigned unless a
   validation story or new bug names it.
6. `STORY-015B_mode_dialog_polish.md` is accepted after PM review of
   light/dark Mode Selection dialog evidence plus Test, Practice, close/cancel,
   modal grab, and centering preservation. No follow-up Mode dialog polish work
   should be assigned unless a validation story or new bug names it.
7. `STORY-014C_analytics_weak_topics_and_no_data.md` is accepted after PM
   review of light/dark Weak Topics grouped by Test, Group, and Category,
   no-category, no-data, and minimum-window evidence plus focused analytics
   verification. No follow-up Weak Topics polish work should be assigned unless
   a validation story or new bug names it.
8. `STORY-015A_review_screen_polish.md` is accepted after PM review of
   light/dark missed questions, selected scope, selected question, no selected
   tests, no missed questions, no active tests, and minimum-window evidence
   plus Start Review smoke coverage. No follow-up Review screen polish work
   should be assigned unless a validation story or new bug names it.
9. `STORY-014B_analytics_chart_shell.md` is accepted after PM review of
   light/dark Score Trends, Test Comparison, Study Activity, chart no-data,
   and minimum-window evidence plus analytics service test coverage. No
   follow-up chart-shell work should be assigned unless a validation story or
   new bug names it.
10. `STORY-014A_history_list_and_filters.md` is accepted after PM review of
   light/dark populated, filtered, loading, empty, and minimum-window History
   evidence plus row-to-results smoke coverage. No follow-up History list work
   should be assigned unless a new bug or validation story names it.
11. `STORY-013_editor_layout.md` is accepted after the clean minimum-window
   evidence resubmission. No follow-up editor work should be assigned unless a
   new bug or validation story names it.
12. `STORY-012_results_summary_and_review_cards.md` is accepted after the
   retake-state resubmission. No follow-up results work should be assigned
   unless a new bug or validation story names it.
13. Use the PM readiness pass handoff before assigning Sprint 2 or Sprint 3
   Ready stories so developers follow the priority order instead of cherry
   picking lower-priority work.
