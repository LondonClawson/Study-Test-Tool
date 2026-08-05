"""Focused tests for test-taking UI helpers."""

from gui.test_taking import TestTakingFrame


class _Canvas:
    """Record viewport positions requested by the test-taking screen."""

    def __init__(self) -> None:
        self.positions = []

    def yview_moveto(self, position: float) -> None:
        """Record the requested viewport position."""
        self.positions.append(position)


class _ScrollableFrame:
    """Minimal scrollable-frame double with an optional backing canvas."""

    def __init__(self, canvas=None) -> None:
        self._parent_canvas = canvas


class _FrameHarness:
    """Bind the helper without constructing a Tk root window."""

    _scroll_question_area_to = TestTakingFrame._scroll_question_area_to


def test_scroll_question_area_moves_the_available_canvas():
    """The scroll helper delegates to the CustomTkinter backing canvas once."""
    canvas = _Canvas()
    frame = _FrameHarness()
    frame.question_area = _ScrollableFrame(canvas)

    frame._scroll_question_area_to(1.0)

    assert canvas.positions == [1.0]


def test_scroll_question_area_ignores_missing_canvas():
    """The scroll helper remains safe if CustomTkinter internals are absent."""
    frame = _FrameHarness()
    frame.question_area = object()

    frame._scroll_question_area_to(0.0)
