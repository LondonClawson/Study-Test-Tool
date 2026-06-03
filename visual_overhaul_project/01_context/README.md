# Context Library

This directory stores reusable context so implementation agents do not need to
rediscover the same GUI structure for every story.

## Context Rule

Before starting a story, read the summaries named in that story. Do not perform
broad fresh exploration unless:

- A required summary is missing.
- A required summary is stale.
- The story asks for a state that the summary does not cover.
- The implementation reveals a conflict between summary and live code.

When any of those happen, run the linked research task and update the summary
before continuing.

For junior assignments, use the two-agent flow:

1. Dev 1 completes the research task and writes the summary.
2. The PM or reviewer checks the summary against
   `00_project/definition_of_ready.md`.
3. Dev 2 reads the story and summary, then implements without broad rediscovery.

## Summary Location

All reusable summaries live in `01_context/summaries/`.

Screenshots, when collected, should live under:

```text
visual_overhaul_project/01_context/screenshots/
```

Use subfolders such as `baseline/light`, `baseline/dark`, and
`mvp-comparison`.

## Summary Requirements

Each summary should include:

- Summary date.
- Research task that produced it.
- Source files or screens inspected.
- Relevant workflows and UI states.
- Visual issues found.
- Recommendations for implementation story splits.
- Implementation risks.
- Open questions.
- A Dev 2 Quick Start section.
- Refresh triggers.

Use [summary_template.md](summary_template.md) when creating new summaries.

## Status Terms

- Missing: expected summary does not exist yet.
- Placeholder: file exists but does not contain ready-to-use decisions or
  research.
- Seeded: initial context exists and can guide research, but it is not a complete
  replacement for task-specific summaries.
- Ready: summary passes the Context Summary Ready gate in
  `00_project/definition_of_ready.md`.
- Stale: source files changed or the summary no longer covers required states.
