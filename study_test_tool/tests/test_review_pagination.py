"""Tests for GUI-independent Review pagination and selection state."""

from gui.review_pagination import ReviewPaginationState


class TestReviewPaginationState:
    """Verify Review page navigation and explicit selection behavior."""

    def test_navigation_uses_current_page_size_and_total(self):
        state = ReviewPaginationState(page_size=2)
        state.set_page(offset=0, total=5, question_ids=[10, 20])

        assert state.previous_offset() is None
        assert state.next_offset() == 2

        state.set_page(offset=2, total=5, question_ids=[30, 40])

        assert state.previous_offset() == 0
        assert state.next_offset() == 4

        state.set_page(offset=4, total=5, question_ids=[50])
        assert state.next_offset() is None

    def test_explicit_selections_persist_and_visible_selection_is_page_local(self):
        state = ReviewPaginationState(page_size=2)
        state.set_page(offset=0, total=3, question_ids=[10, 20])
        state.set_visible_selected(True)

        state.set_page(offset=2, total=3, question_ids=[30])
        state.set_selected(30, True)
        state.set_visible_selected(False)

        assert state.selected_question_ids == {10, 20}
        assert state.review_question_ids() == [10, 20]

    def test_no_explicit_selection_uses_visible_page_and_reset_clears_state(self):
        state = ReviewPaginationState(page_size=2)
        state.set_page(offset=2, total=3, question_ids=[30])

        assert state.review_question_ids() == [30]

        state.set_selected(30, True)
        state.reset()

        assert state.offset == 0
        assert state.total == 0
        assert state.page_question_ids == []
        assert state.review_question_ids() == []
