# Context Index

Use this index to find the summary required by a story. If a story needs context
that is not represented here, create a research task or add the missing summary
before implementation.

Only mark a summary Ready after it passes
`00_project/definition_of_ready.md`.

Status terms match `00_project/status_board.md`: Missing, Placeholder, Seeded,
Ready, In Progress, Blocked, Done, and Stale.

| Context ID | Summary | Source Scope | Status | Refresh Trigger | Research Task |
| --- | --- | --- | --- | --- | --- |
| CTX-GUI-ARCH | `summaries/gui_architecture_summary.md` | `main_window.py`, screen constants, GUI file inventory | Seeded | Any navigation, screen registration, or frame lifecycle change | `02_research_tasks/R-002_component_style_inventory.md` |
| CTX-SCREEN-INV | `summaries/screen_inventory.md` | Major GUI screens and components | Seeded | New screen/component or renamed GUI file | `02_research_tasks/R-002_component_style_inventory.md` |
| CTX-VISUAL-SEED | `summaries/current_visual_state_seed.md` | Static visual read of GUI code and visual plan | Seeded, needs screenshots | First screenshot audit or major style refactor | `02_research_tasks/R-001_baseline_visual_audit.md` |
| CTX-AUDIT-BASELINE | `summaries/baseline_visual_audit.md` | Light/dark screenshots of major screens | Missing | Required before foundation implementation | `02_research_tasks/R-001_baseline_visual_audit.md` |
| CTX-STYLE-INVENTORY | `summaries/style_inventory.md` | Inline colors, fonts, widgets, repeated surfaces | Ready | Required before visual foundation spec | `02_research_tasks/R-002_component_style_inventory.md` |
| CTX-HOME | `summaries/home_screen_context.md` | Home/test selector, groups, cards, dialogs launched from home | Ready | Home layout, card data, action set, grouping, archive behavior, or import/mix launch flow changes | `02_research_tasks/R-003_home_screen_context.md` |
| CTX-TEST-TAKING | `summaries/test_taking_context.md` | Test-taking screen, question widget, timer, progress, practice feedback | Missing | Required before test-taking stories | `02_research_tasks/R-004_test_taking_context.md` |
| CTX-RESULTS | `summaries/results_context.md` | Results view, score summary, review cards, mix breakdown | Missing | Required before results stories | `02_research_tasks/R-005_results_context.md` |
| CTX-EDITOR | `summaries/editor_context.md` | Test editor layout, question list, form states | Missing | Required before editor stories | `02_research_tasks/R-006_editor_context.md` |
| CTX-DATA-VIEWS | `summaries/history_analytics_review_context.md` | History, analytics, review, charts, data states | Missing | Required before secondary screen stories | `02_research_tasks/R-007_history_analytics_review_context.md` |
| CTX-DIALOGS | `summaries/dialog_context.md` | Mode, mix, import/error/confirmation dialogs | Missing | Required before dialog polish | `02_research_tasks/R-008_dialog_context.md` |
| CTX-FOUNDATION | `summaries/visual_foundation_decisions.md` | Approved visual tokens and component rules | Placeholder | Required before implementation stories after Sprint 0 | `04_stories/STORY-003_visual_foundation_spec.md` |
