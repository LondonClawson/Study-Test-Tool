"""Main application window with frame-based navigation."""

import tkinter.messagebox as messagebox

import customtkinter as ctk

from config.settings import (
    APP_NAME,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from gui.history_view import HistoryViewFrame
from gui.results_view import ResultsViewFrame
from gui.test_editor import TestEditorFrame
from gui.test_selector import TestSelectorFrame
from gui.test_taking import TestTakingFrame
from utils.constants import (
    SCREEN_EDITOR,
    SCREEN_HISTORY,
    SCREEN_HOME,
    SCREEN_RESULTS,
    SCREEN_TEST_TAKING,
)


class App(ctk.CTk):
    """Main application window managing screen navigation."""

    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        # Container for all screens
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create all screens
        self.frames = {}
        for name, FrameClass in [
            (SCREEN_HOME, TestSelectorFrame),
            (SCREEN_EDITOR, TestEditorFrame),
            (SCREEN_TEST_TAKING, TestTakingFrame),
            (SCREEN_RESULTS, ResultsViewFrame),
            (SCREEN_HISTORY, HistoryViewFrame),
        ]:
            frame = FrameClass(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        # Track the current screen for close confirmation
        self._current_screen = SCREEN_HOME

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Show home screen
        self.show_frame(SCREEN_HOME)

    def show_frame(self, name: str, **kwargs) -> None:
        """Raise a screen to the front and call its on_show method.

        Args:
            name: The screen name constant.
            **kwargs: Data to pass to the screen's on_show method.
        """
        self._current_screen = name
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show(**kwargs)

    def _on_close(self) -> None:
        """Handle window close — confirm if a test is in progress."""
        if self._current_screen == SCREEN_TEST_TAKING:
            if not messagebox.askyesno(
                "Quit",
                "A test is in progress. Are you sure you want to quit?\n\n"
                "Your progress will be lost.",
            ):
                return
        self.destroy()
