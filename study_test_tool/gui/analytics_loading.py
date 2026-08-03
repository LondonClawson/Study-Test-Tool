"""GUI-independent request state for asynchronous Analytics loading."""


class AnalyticsLoadState:
    """Track the latest Analytics request so stale worker results are ignored."""

    def __init__(self) -> None:
        self._generation = 0

    def begin_request(self) -> int:
        """Start a request and return its unique generation."""
        self._generation += 1
        return self._generation

    def is_current(self, generation: int) -> bool:
        """Return whether a worker result belongs to the latest request."""
        return generation == self._generation
