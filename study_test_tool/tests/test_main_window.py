"""Tests for the main-window lazy frame lifecycle."""

from gui import main_window


App = main_window.App


class _Frame:
    """Minimal frame double for lifecycle behavior tests."""

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.grid_calls = []
        self.raise_count = 0
        self.show_arguments = []

    def grid(self, **kwargs):
        self.grid_calls.append(kwargs)

    def tkraise(self):
        self.raise_count += 1

    def on_show(self, **kwargs):
        self.show_arguments.append(kwargs)


class _AppHarness:
    """Bind App lifecycle methods without creating a Tk root window."""

    _create_frame = App._create_frame


def test_show_frame_creates_and_reuses_a_lazy_frame(monkeypatch):
    """A frame is constructed once and still receives every navigation call."""
    app = _AppHarness()
    app.container = object()
    app.frames = {}
    monkeypatch.setattr(main_window, "FRAME_CLASSES", {"analytics": _Frame})

    App.show_frame(app, "analytics", source="home")
    frame = app.frames["analytics"]

    App.show_frame(app, "analytics", source="home")

    assert frame.parent is app.container
    assert frame.controller is app
    assert frame.grid_calls == [{"row": 0, "column": 0, "sticky": "nsew"}]
    assert frame.raise_count == 2
    assert frame.show_arguments == [{"source": "home"}, {"source": "home"}]
    assert app._current_screen == "analytics"
