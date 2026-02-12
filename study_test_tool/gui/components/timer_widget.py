"""Timer widget — displays elapsed time during test-taking."""

import customtkinter as ctk

from config.settings import FONT_FAMILY, FONT_SIZE_HEADING
from utils.timer import Timer


class TimerWidget(ctk.CTkLabel):
    """Displays a live-updating timer."""

    def __init__(self, parent: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(
            parent,
            text="00:00",
            font=(FONT_FAMILY, FONT_SIZE_HEADING),
            **kwargs,
        )
        self._timer = Timer()
        self._running = False

    def start(self) -> None:
        """Start the timer and begin updating the display."""
        self._timer.start()
        self._running = True
        self._tick()

    def stop(self) -> int:
        """Stop the timer and return elapsed seconds."""
        self._running = False
        elapsed = self._timer.stop()
        self.configure(text=self._timer.get_formatted_time())
        return int(elapsed)

    def pause(self) -> None:
        """Pause the timer."""
        self._timer.pause()
        self._running = False

    def resume(self) -> None:
        """Resume the timer."""
        self._timer.resume()
        self._running = True
        self._tick()

    def get_elapsed(self) -> int:
        """Return elapsed time in seconds."""
        return self._timer.get_elapsed_int()

    def _tick(self) -> None:
        """Update the display every second."""
        if self._running:
            self.configure(text=self._timer.get_formatted_time())
            self.after(1000, self._tick)
