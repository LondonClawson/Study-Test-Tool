"""Tests for Analytics asynchronous request state."""

from gui.analytics_loading import AnalyticsLoadState


def test_newer_analytics_request_invalidates_older_result():
    """A stale worker result cannot replace the latest Analytics view."""
    state = AnalyticsLoadState()
    first_generation = state.begin_request()
    second_generation = state.begin_request()

    assert not state.is_current(first_generation)
    assert state.is_current(second_generation)
