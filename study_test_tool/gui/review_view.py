"""Review view — browse and review missed questions."""

from typing import Dict, List, Optional, Set

import customtkinter as ctk

from gui.components.formatted_text import FormattedText
from gui.styles import (
    RADIUS_CONTROL,
    SPACE_4,
    SPACE_8,
    SPACE_12,
    SPACE_16,
    SPACE_24,
    get_button_style,
    get_card_style,
    get_color,
    get_header_style,
    get_text_style,
)
from gui.mix_test_display import group_tests_by_name
from services.review_service import ReviewService
from services.test_service import TestService
from utils.constants import MODE_PRACTICE, SCREEN_HOME, SCREEN_TEST_TAKING


class ReviewViewFrame(ctk.CTkFrame):
    """Screen for browsing and reviewing missed questions."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent, fg_color=get_color("app_bg"))
        self.controller = controller
        self.review_service = ReviewService()
        self.test_service = TestService()

        self._missed_data = []
        self._checkboxes = {}  # question_id -> BooleanVar
        self._scope_tests = []
        self._test_scope_vars: Dict[int, ctk.BooleanVar] = {}
        self._group_scope_vars: Dict[str, ctk.BooleanVar] = {}
        self._group_to_test_ids: Dict[str, List[int]] = {}

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the review layout."""
        page_header = ctk.CTkFrame(self, **get_header_style("page"))
        page_header.pack(fill="x", padx=SPACE_24, pady=(SPACE_24, SPACE_12))
        page_header.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            page_header,
            text="< Back",
            width=80,
            **get_button_style("secondary"),
            command=lambda: self.controller.show_frame(SCREEN_HOME),
        ).grid(row=0, column=0, padx=(SPACE_16, SPACE_12), pady=SPACE_16)

        title_frame = ctk.CTkFrame(page_header, fg_color="transparent")
        title_frame.grid(row=0, column=1, sticky="ew", pady=SPACE_12)

        ctk.CTkLabel(
            title_frame,
            text="Missed Questions",
            **get_text_style("page_title"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Choose missed questions for a focused practice session",
            **get_text_style("page_subtitle"),
        ).pack(anchor="w", pady=(SPACE_4, 0))

        filter_frame = ctk.CTkFrame(self, **get_card_style("default"))
        filter_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_12))
        filter_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            filter_frame,
            text="Scope",
            **get_text_style("body_bold"),
        ).grid(row=0, column=0, sticky="w", padx=(SPACE_16, SPACE_8), pady=SPACE_16)

        self.scope_summary_label = ctk.CTkLabel(
            filter_frame,
            text="All Active Tests",
            **get_text_style("metadata"),
        )
        self.scope_summary_label.grid(row=0, column=1, sticky="w", pady=SPACE_16)

        self.filter_type_var = ctk.StringVar(value="All Missed")
        self.filter_type_seg = ctk.CTkSegmentedButton(
            filter_frame,
            values=["All Missed", "Frequently Missed"],
            variable=self.filter_type_var,
            command=self._on_filter_change,
            **self._segmented_style(),
        )
        self.filter_type_seg.grid(
            row=0,
            column=2,
            sticky="e",
            padx=(SPACE_16, SPACE_16),
            pady=SPACE_16,
        )

        scope_frame = ctk.CTkFrame(self, **get_card_style("default"))
        scope_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_12))

        scope_actions = ctk.CTkFrame(scope_frame, fg_color="transparent")
        scope_actions.pack(fill="x", padx=SPACE_16, pady=(SPACE_12, SPACE_8))
        scope_actions.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            scope_actions,
            text="Review scope",
            **get_text_style("section_title"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            scope_actions,
            text="Select All",
            width=90,
            height=28,
            **get_button_style("tertiary"),
            command=self._select_all_scope,
        ).grid(row=0, column=1, padx=(SPACE_8, SPACE_4))

        ctk.CTkButton(
            scope_actions,
            text="Deselect All",
            width=100,
            height=28,
            **get_button_style("tertiary"),
            command=self._deselect_all_scope,
        ).grid(row=0, column=2)

        self.scope_list = ctk.CTkScrollableFrame(
            scope_frame,
            height=120,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
            scrollbar_button_color=get_color("surface_muted"),
            scrollbar_button_hover_color=get_color("border"),
        )
        self.scope_list.pack(fill="x", padx=SPACE_16, pady=(0, SPACE_16))

        action_frame = ctk.CTkFrame(self, **get_card_style("default"))
        action_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_12))
        action_frame.grid_columnconfigure(1, weight=1)

        self.select_all_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            action_frame,
            text="Select All",
            variable=self.select_all_var,
            command=self._on_select_all,
            **self._checkbox_style("body"),
        ).grid(row=0, column=0, sticky="w", padx=SPACE_16, pady=SPACE_16)

        self.start_review_btn = ctk.CTkButton(
            action_frame,
            text="Start Review",
            width=120,
            **get_button_style("primary"),
            command=self._on_start_review,
        )
        self.start_review_btn.grid(
            row=0,
            column=3,
            sticky="e",
            padx=(SPACE_8, SPACE_16),
            pady=SPACE_16,
        )

        self.selected_label = ctk.CTkLabel(
            action_frame,
            text="0 selected",
            **get_text_style("metadata"),
        )
        self.selected_label.grid(row=0, column=2, sticky="e", padx=SPACE_8)

        self.question_list = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=get_color("surface_muted"),
            scrollbar_button_hover_color=get_color("border"),
        )
        self.question_list.pack(
            fill="both",
            expand=True,
            padx=SPACE_24,
            pady=(0, SPACE_24),
        )

        self.empty_state = ctk.CTkFrame(self.question_list, **get_card_style("default"))
        self.empty_title = ctk.CTkLabel(
            self.empty_state,
            text="No missed questions found",
            **get_text_style("card_title"),
        )
        self.empty_title.pack(anchor="center", pady=(SPACE_16, SPACE_4))
        self.empty_helper = ctk.CTkLabel(
            self.empty_state,
            text="Questions you miss will appear here after an attempt.",
            wraplength=560,
            justify="center",
            **get_text_style("card_description"),
        )
        self.empty_helper.pack(anchor="center", padx=SPACE_24, pady=(0, SPACE_16))

    def _segmented_style(self) -> dict:
        """Return semantic segmented-button styling."""
        return {
            "fg_color": get_color("surface_subtle"),
            "selected_color": get_color("surface_muted"),
            "selected_hover_color": get_color("surface_muted"),
            "unselected_color": get_color("surface_subtle"),
            "unselected_hover_color": get_color("surface_muted"),
            "text_color": get_color("text_primary"),
            "corner_radius": RADIUS_CONTROL,
        }

    def _checkbox_style(self, text_role: str) -> dict:
        """Return semantic checkbox styling."""
        style = get_text_style(text_role)
        style.update(
            {
                "fg_color": get_color("primary"),
                "hover_color": get_color("primary_hover"),
                "border_color": get_color("border"),
                "checkmark_color": get_color("text_inverse"),
            }
        )
        return style

    def _show_empty_state(self, title: str, helper: str) -> None:
        """Show the designed empty state for the current Review condition."""
        self.empty_title.configure(text=title)
        self.empty_helper.configure(text=helper)
        self.empty_state.pack(fill="x", padx=SPACE_8, pady=SPACE_8)

    def _hide_empty_state(self) -> None:
        """Hide the designed empty state."""
        self.empty_state.pack_forget()

    def _create_scope_empty_state(self) -> None:
        """Render the no-active-tests message in the scope selector."""
        empty_scope = ctk.CTkFrame(
            self.scope_list,
            fg_color="transparent",
        )
        ctk.CTkLabel(
            empty_scope,
            text="No active tests available.",
            **get_text_style("body"),
        ).pack(anchor="w", pady=(SPACE_8, SPACE_4), padx=SPACE_8)
        ctk.CTkLabel(
            empty_scope,
            text="Active tests with questions will appear here.",
            **get_text_style("metadata"),
        ).pack(anchor="w", pady=(0, SPACE_8), padx=SPACE_8)
        empty_scope.pack(fill="x", padx=SPACE_8, pady=SPACE_8)

    def on_show(self, **kwargs) -> None:
        """Load missed questions when shown."""
        self._refresh_scope_options()
        self.filter_type_var.set("All Missed")

        self._load_questions()

    def _on_filter_change(self, value: str) -> None:
        """Reload questions when filter changes."""
        self._load_questions()

    def _refresh_scope_options(self) -> None:
        """Load active tests into the grouped scope selector."""
        for widget in self.scope_list.winfo_children():
            widget.destroy()

        self._scope_tests = []
        self._test_scope_vars.clear()
        self._group_scope_vars.clear()
        self._group_to_test_ids.clear()

        for test in self.test_service.get_all_tests():
            q_count = self.test_service.get_question_count(test.id)
            if q_count > 0:
                self._scope_tests.append((test, q_count))

        if not self._scope_tests:
            self._create_scope_empty_state()
            self._update_scope_summary()
            return

        for group_name, group_tests in group_tests_by_name(self._scope_tests):
            group_var = ctk.BooleanVar(value=True)
            self._group_scope_vars[group_name] = group_var
            self._group_to_test_ids[group_name] = []

            group_cb = ctk.CTkCheckBox(
                self.scope_list,
                text=group_name,
                variable=group_var,
                command=lambda gn=group_name: self._on_scope_group_toggled(gn),
                **self._checkbox_style("body_bold"),
            )
            group_cb.pack(anchor="w", pady=(SPACE_8, SPACE_4), padx=SPACE_8)

            for test, q_count in group_tests:
                var = ctk.BooleanVar(value=True)
                self._test_scope_vars[test.id] = var
                self._group_to_test_ids[group_name].append(test.id)

                cb = ctk.CTkCheckBox(
                    self.scope_list,
                    text=f"{test.name}  ({q_count} questions)",
                    variable=var,
                    command=lambda gn=group_name: self._on_scope_test_changed(gn),
                    **self._checkbox_style("body"),
                )
                cb.pack(anchor="w", pady=SPACE_4, padx=(SPACE_24, SPACE_8))

        self._update_scope_summary()

    def _select_all_scope(self) -> None:
        """Select every active test in the review scope."""
        for var in self._test_scope_vars.values():
            var.set(True)
        for var in self._group_scope_vars.values():
            var.set(True)
        self._load_questions()

    def _deselect_all_scope(self) -> None:
        """Clear every test from the review scope."""
        for var in self._test_scope_vars.values():
            var.set(False)
        for var in self._group_scope_vars.values():
            var.set(False)
        self._load_questions()

    def _on_scope_group_toggled(self, group_name: str) -> None:
        """Toggle all tests in a group when the group checkbox changes."""
        is_selected = self._group_scope_vars[group_name].get()
        for test_id in self._group_to_test_ids[group_name]:
            self._test_scope_vars[test_id].set(is_selected)
        self._load_questions()

    def _on_scope_test_changed(self, group_name: str) -> None:
        """Sync a group checkbox after an individual test changes."""
        group_ids = self._group_to_test_ids[group_name]
        all_selected = all(
            self._test_scope_vars[test_id].get() for test_id in group_ids
        )
        self._group_scope_vars[group_name].set(all_selected)
        self._load_questions()

    def _get_selected_test_ids(self) -> Optional[List[int]]:
        """Return selected test ids, or None when all active tests are selected."""
        if not self._test_scope_vars:
            return []

        selected_ids = [
            test_id for test_id, var in self._test_scope_vars.items() if var.get()
        ]
        if len(selected_ids) == len(self._test_scope_vars):
            return None
        return selected_ids

    def _update_scope_summary(self) -> None:
        """Update the label that summarizes the selected review scope."""
        if not self._test_scope_vars:
            self.scope_summary_label.configure(text="No active tests")
            return

        selected: Set[int] = {
            test_id for test_id, var in self._test_scope_vars.items() if var.get()
        }
        if not selected:
            self.scope_summary_label.configure(text="No tests selected")
            return

        if len(selected) == len(self._test_scope_vars):
            self.scope_summary_label.configure(text="All Active Tests")
            return

        for group_name, test_ids in self._group_to_test_ids.items():
            group_set = set(test_ids)
            if selected == group_set:
                self.scope_summary_label.configure(text=f"Group: {group_name}")
                return

        if len(selected) == 1:
            test_id = next(iter(selected))
            for test, _ in self._scope_tests:
                if test.id == test_id:
                    self.scope_summary_label.configure(text=test.name)
                    return

        self.scope_summary_label.configure(text=f"{len(selected)} tests selected")

    def _load_questions(self) -> None:
        """Load missed questions based on current filters."""
        self._update_scope_summary()
        test_ids = self._get_selected_test_ids()

        filter_type = self.filter_type_var.get()
        if filter_type == "Frequently Missed":
            self._missed_data = self.review_service.get_frequently_missed(
                test_ids=test_ids
            )
        else:
            self._missed_data = self.review_service.get_missed_questions(
                test_ids=test_ids
            )

        self._display_questions()

    def _display_questions(self) -> None:
        """Render the missed question cards."""
        # Clear existing
        for widget in self.question_list.winfo_children():
            if widget != self.empty_state:
                widget.destroy()

        self._checkboxes.clear()
        self.select_all_var.set(False)

        if not self._missed_data:
            self._show_current_empty_state()
            self._update_selected_count()
            return

        self._hide_empty_state()

        for item in self._missed_data:
            self._create_question_card(item)

        self._update_selected_count()

    def _show_current_empty_state(self) -> None:
        """Show the empty state that matches the current review condition."""
        if not self._test_scope_vars:
            self._show_empty_state(
                "No active tests",
                "Active tests with questions are needed before missed-question review can start.",
            )
            return

        if self._get_selected_test_ids() == []:
            self._show_empty_state(
                "No tests selected",
                "Select at least one active test in the review scope.",
            )
            return

        if self.filter_type_var.get() == "Frequently Missed":
            self._show_empty_state(
                "No frequently missed questions",
                "Try All Missed or complete more attempts to build a stronger pattern.",
            )
            return

        self._show_empty_state(
            "No missed questions",
            "Questions answered incorrectly will appear here for focused practice.",
        )

    def _create_question_card(self, item: dict) -> None:
        """Create a card for a missed question."""
        card = ctk.CTkFrame(self.question_list, **get_card_style("default"))
        card.pack(fill="x", pady=(0, SPACE_8), padx=SPACE_4)

        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=SPACE_16, pady=(SPACE_16, SPACE_8))

        var = ctk.BooleanVar(value=False)
        self._checkboxes[item["question_id"]] = var

        ctk.CTkCheckBox(
            top_row,
            text="",
            variable=var,
            width=24,
            command=self._update_selected_count,
            **self._checkbox_style("body"),
        ).pack(side="left", padx=(0, SPACE_8))

        FormattedText(
            top_row,
            text=item["question_text"],
            text_role="body",
            background_color=get_color("surface"),
        ).pack(side="left", fill="x", expand=True)

        meta_row = ctk.CTkFrame(card, fg_color="transparent")
        meta_row.pack(fill="x", padx=SPACE_16, pady=(0, SPACE_16))

        ctk.CTkFrame(meta_row, fg_color="transparent", width=32).pack(side="left")

        ctk.CTkLabel(
            meta_row,
            text=item.get("test_name", ""),
            **get_text_style("card_metadata"),
        ).pack(side="left", padx=(0, SPACE_16))

        if item.get("category"):
            ctk.CTkLabel(
                meta_row,
                text=item["category"],
                **get_text_style("card_metadata"),
            ).pack(side="left", padx=(0, SPACE_16))

        miss_rate = (
            item["times_missed"] / item["total_attempts"] * 100
            if item["total_attempts"] > 0
            else 0
        )
        miss_pill = ctk.CTkFrame(
            meta_row,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
        )
        miss_pill.pack(side="left")

        miss_style = get_text_style("metadata")
        miss_style["text_color"] = get_color("status_incorrect")
        ctk.CTkLabel(
            miss_pill,
            text=f"Missed {item['times_missed']}/{item['total_attempts']} ({miss_rate:.0f}%)",
            **miss_style,
        ).pack(padx=SPACE_8, pady=SPACE_4)

    def _on_select_all(self) -> None:
        """Toggle all checkboxes."""
        val = self.select_all_var.get()
        for var in self._checkboxes.values():
            var.set(val)
        self._update_selected_count()

    def _update_selected_count(self) -> None:
        """Update the selected count label."""
        count = sum(1 for v in self._checkboxes.values() if v.get())
        self.selected_label.configure(text=f"{count} selected")

    def _on_start_review(self) -> None:
        """Start a practice review with the selected questions."""
        selected_ids = [qid for qid, var in self._checkboxes.items() if var.get()]
        if not selected_ids:
            # If none selected, use all displayed
            selected_ids = [item["question_id"] for item in self._missed_data]

        if not selected_ids:
            return

        self.controller.show_frame(
            SCREEN_TEST_TAKING,
            mode=MODE_PRACTICE,
            review_question_ids=selected_ids,
        )
