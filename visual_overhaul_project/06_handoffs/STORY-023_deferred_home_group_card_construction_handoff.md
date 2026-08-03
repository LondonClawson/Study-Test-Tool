# STORY-023 Deferred Home Group-Card Construction Handoff

Story/Task: `STORY-023_deferred_home_group_card_construction.md`

Status: Done. Accepted by user authorization.

Summary: Home now creates active and archived test-card widgets only when the
corresponding group first expands. Each refresh resets deferred state, restores
cards for previously expanded groups, and continues to use the existing batched
question-count lookup.

Files changed:

- `study_test_tool/gui/components/collapsible_group.py`
- `study_test_tool/gui/test_selector.py`
- `04_stories/STORY-023_deferred_home_group_card_construction.md`
- `00_project/status_board.md`
- This handoff

Definition of Ready checked: `CTX-HOME` and `CTX-PERFORMANCE-SCALE` are Ready.

Acceptance: The user accepted the submitted implementation and evidence.

Context summaries read:

- `home_screen_context.md`
- `performance_scalability_audit.md`

Context summaries created/updated: None.

Screens/states checked:

- `home_populated_grouped`
- `home_expanded_cards`
- `home_expanded_archived_cards`
- `home_minimum_populated`
- Light and dark mode for every state above.

Screenshot evidence:

- `01_context/screenshots/after/STORY-023/light/`
- `01_context/screenshots/after/STORY-023/dark/`
- Compared against the Home states documented by `home_screen_context.md`.

Tests run:

- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests/test_group_sort.py`
- `PYTHONPATH=study_test_tool pytest --rootdir=. study_test_tool/tests`
- `PYTHONPATH=study_test_tool python3 -m py_compile study_test_tool/gui/test_selector.py study_test_tool/gui/components/collapsible_group.py`
- `black --check study_test_tool/gui/components/collapsible_group.py study_test_tool/gui/test_selector.py`
- `git diff --check`

Tests not run and why: No dedicated headless CustomTkinter widget harness
exists; the required light/dark screenshot harness exercises collapsed and
expanded Home group rendering.

Acceptance criteria notes: Collapsed groups contain only headers until their
first expansion. The expansion callback renders each group once per refresh
cycle, including archived cards. Repeated toggle operations do not duplicate
cards, and refreshed expanded groups render immediately from current data.

Risks: Card construction remains synchronous at the moment a large group is
expanded. This intentionally shifts cost from initial Home load to explicit
user interaction; virtualization or incremental batches are separate work if a
single group proves too large.

Follow-up backlog items:

- Consider lazy non-Home frame construction for Finding 7.
- Benchmark Mix and History at representative production scale before adding
  indexes or pagination changes.
