"""GUI-independent pagination and selection state for missed-question Review."""

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Set


@dataclass
class ReviewPaginationState:
    """Track one Review page and explicit selections across page changes."""

    page_size: int
    offset: int = 0
    total: int = 0
    page_question_ids: List[int] = field(default_factory=list)
    selected_question_ids: Set[int] = field(default_factory=set)

    def reset(self) -> None:
        """Clear page data and explicit selections for a new filter scope."""
        self.offset = 0
        self.total = 0
        self.page_question_ids = []
        self.selected_question_ids.clear()

    def set_loading_offset(self, offset: int) -> None:
        """Record the requested page offset before its data arrives."""
        self.offset = max(offset, 0)

    def set_page(self, offset: int, total: int, question_ids: Iterable[int]) -> None:
        """Replace current-page metadata while preserving explicit selections."""
        self.offset = max(offset, 0)
        self.total = max(total, 0)
        self.page_question_ids = list(question_ids)

    def previous_offset(self) -> Optional[int]:
        """Return the preceding page offset, or None on the first page."""
        if self.offset <= 0:
            return None
        return max(0, self.offset - self.page_size)

    def next_offset(self) -> Optional[int]:
        """Return the following page offset, or None when this is the last page."""
        next_offset = self.offset + len(self.page_question_ids)
        if next_offset >= self.total:
            return None
        return next_offset

    def set_selected(self, question_id: int, selected: bool) -> None:
        """Persist one question selection independently of the visible page."""
        if selected:
            self.selected_question_ids.add(question_id)
        else:
            self.selected_question_ids.discard(question_id)

    def set_visible_selected(self, selected: bool) -> None:
        """Select or clear only questions on the current page."""
        for question_id in self.page_question_ids:
            self.set_selected(question_id, selected)

    def is_selected(self, question_id: int) -> bool:
        """Return whether a question is explicitly selected."""
        return question_id in self.selected_question_ids

    def are_all_visible_selected(self) -> bool:
        """Return whether every question on the current page is selected."""
        return bool(self.page_question_ids) and set(self.page_question_ids).issubset(
            self.selected_question_ids
        )

    def review_question_ids(self) -> List[int]:
        """Return explicit selections, or the visible page when none exist."""
        if self.selected_question_ids:
            return sorted(self.selected_question_ids)
        return list(self.page_question_ids)
