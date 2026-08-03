# STORY-024: Lazy Non-Home Frame Construction

## Status

Done. Accepted by user authorization on 2026-08-03.

## Goal

Show Home without constructing unused non-Home frames, including the embedded
Matplotlib Analytics surface, while preserving existing frame navigation and
`on_show` behavior.

## Required Context

- `CTX-GUI-ARCH`
- `CTX-PERFORMANCE-SCALE`

## In Scope

- Eager construction of the Home frame only.
- Deferred, one-time construction of each non-Home frame on its first
  `show_frame()` navigation.
- Preservation of the existing screen registry, grid placement, navigation,
  and `on_show(**kwargs)` contract.
- Focused startup/navigation smoke checks and screenshot evidence for the
  touched Home and Analytics states.

## Out Of Scope

- Changes to screen layouts, data loading, services, persistence, scoring,
  history pagination/indexes, or frame destruction/eviction.
- Changes to screen constants or callers' `show_frame()` arguments.

## Acceptance Criteria

- Application initialization creates Home but does not instantiate the Editor,
  Test Taking, Results, History, Review, or Analytics frames.
- Navigating to any registered screen creates it once, raises it, and invokes
  `on_show(**kwargs)` exactly as before.
- Returning Home and revisiting a constructed screen preserve the current
  frame instance and navigation behavior.
- Analytics is not constructed until Analytics is first selected.

## Verification

- Run focused navigation tests, then the full pytest suite.
- Capture light/dark `home_populated_grouped` and `analytics_populated`
  evidence in `01_context/screenshots/after/STORY-024/`.
- Smoke-check Home startup, first/repeated Analytics navigation, and a
  parameterized transition to Results or Test Taking.
- Run `git diff --check`.
