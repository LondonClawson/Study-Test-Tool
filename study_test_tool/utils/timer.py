"""Timer utility for tracking elapsed time during tests."""

import time


class Timer:
    """Tracks elapsed time with pause/resume support."""

    def __init__(self) -> None:
        self._start_time: float = 0.0
        self._elapsed: float = 0.0
        self._running: bool = False

    def start(self) -> None:
        """Start or restart the timer."""
        self._start_time = time.time()
        self._elapsed = 0.0
        self._running = True

    def pause(self) -> None:
        """Pause the timer, accumulating elapsed time."""
        if self._running:
            self._elapsed += time.time() - self._start_time
            self._running = False

    def resume(self) -> None:
        """Resume the timer after a pause."""
        if not self._running:
            self._start_time = time.time()
            self._running = True

    def stop(self) -> float:
        """Stop the timer and return total elapsed seconds."""
        if self._running:
            self._elapsed += time.time() - self._start_time
            self._running = False
        return self._elapsed

    def get_elapsed(self) -> float:
        """Return total elapsed seconds (works while running or paused)."""
        if self._running:
            return self._elapsed + (time.time() - self._start_time)
        return self._elapsed

    def get_elapsed_int(self) -> int:
        """Return total elapsed seconds as an integer."""
        return int(self.get_elapsed())

    def get_formatted_time(self) -> str:
        """Return elapsed time formatted as MM:SS or HH:MM:SS."""
        total = int(self.get_elapsed())
        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"

    @property
    def is_running(self) -> bool:
        """Whether the timer is currently running."""
        return self._running
