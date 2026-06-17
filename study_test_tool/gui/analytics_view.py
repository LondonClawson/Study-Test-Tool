"""Analytics view — performance graphs and weak topic identification."""

import customtkinter as ctk

from gui.components.graph_widget import GraphWidget
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
from services.analytics_service import AnalyticsService
from services.test_service import TestService
from utils.constants import SCREEN_HOME

ANALYTICS_TABS = ["Score Trends", "Test Comparison", "Study Activity", "Weak Topics"]


class AnalyticsViewFrame(ctk.CTkFrame):
    """Screen for viewing performance analytics and graphs."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent, fg_color=get_color("app_bg"))
        self.controller = controller
        self.analytics_service = AnalyticsService()
        self.test_service = TestService()

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the analytics layout."""
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
            text="Analytics",
            **get_text_style("page_title"),
        ).pack(anchor="w")

        self.header_meta_label = ctk.CTkLabel(
            title_frame,
            text="Score trends and study activity",
            **get_text_style("page_subtitle"),
        )
        self.header_meta_label.pack(anchor="w", pady=(SPACE_4, 0))

        controls_frame = ctk.CTkFrame(self, **get_card_style("default"))
        controls_frame.pack(fill="x", padx=SPACE_24, pady=(0, SPACE_12))
        controls_frame.grid_columnconfigure(1, weight=1)
        controls_frame.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(
            controls_frame,
            text="View",
            **get_text_style("body"),
        ).grid(row=0, column=0, sticky="w", padx=(SPACE_16, SPACE_8), pady=SPACE_16)

        self.tab_var = ctk.StringVar(value="Score Trends")
        self.tab_seg = ctk.CTkSegmentedButton(
            controls_frame,
            values=ANALYTICS_TABS,
            variable=self.tab_var,
            command=self._on_tab_change,
            **self._segmented_style(),
        )
        self.tab_seg.grid(row=0, column=1, columnspan=3, sticky="ew", pady=SPACE_16)

        ctk.CTkLabel(
            controls_frame,
            text="Test",
            **get_text_style("body"),
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(SPACE_16, SPACE_8),
            pady=(0, SPACE_16),
        )

        self.test_filter_var = ctk.StringVar(value="All Tests")
        self.test_filter_menu = ctk.CTkOptionMenu(
            controls_frame,
            variable=self.test_filter_var,
            values=["All Tests"],
            command=self._on_filter_change,
            width=250,
            **self._option_menu_style(),
        )
        self.test_filter_menu.grid(row=1, column=1, sticky="w", pady=(0, SPACE_16))

        self.group_by_label = ctk.CTkLabel(
            controls_frame,
            text="Group by",
            **get_text_style("body"),
        )
        self.group_by_var = ctk.StringVar(value="Test")
        self.group_by_seg = ctk.CTkSegmentedButton(
            controls_frame,
            values=["Test", "Group", "Category"],
            variable=self.group_by_var,
            command=self._on_filter_change,
            **self._segmented_style(),
        )

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=SPACE_24,
            pady=(0, SPACE_24),
        )

        self.chart_shell = ctk.CTkFrame(self.content_frame, **get_card_style("default"))
        self.chart_body = ctk.CTkFrame(
            self.chart_shell,
            fg_color=get_color("chart_bg"),
            corner_radius=RADIUS_CONTROL,
        )
        self.chart_body.pack(
            fill="both",
            expand=True,
            padx=SPACE_16,
            pady=SPACE_16,
        )

        self.graph_widget = GraphWidget(
            self.chart_body,
            figsize=(8, 4),
            fg_color=get_color("chart_bg"),
        )

        self.chart_empty_state = self._build_chart_empty_state()

        self.weak_topics_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_button_color=get_color("surface_muted"),
            scrollbar_button_hover_color=get_color("border"),
        )

        self.weak_topics_empty_state = self._build_weak_topics_empty_state()

    def _option_menu_style(self) -> dict:
        """Return semantic option-menu styling for Analytics filters."""
        return {
            "fg_color": get_color("surface_subtle"),
            "button_color": get_color("primary"),
            "button_hover_color": get_color("primary_hover"),
            "dropdown_fg_color": get_color("surface"),
            "dropdown_hover_color": get_color("surface_subtle"),
            "dropdown_text_color": get_color("text_primary"),
            "text_color": get_color("text_primary"),
            "corner_radius": RADIUS_CONTROL,
        }

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

    def _build_chart_empty_state(self) -> ctk.CTkFrame:
        """Create the chart-tab no-data surface."""
        state = ctk.CTkFrame(self.chart_body, **get_card_style("default"))

        self.chart_empty_title = ctk.CTkLabel(
            state,
            text="No chart data yet",
            **get_text_style("card_title"),
        )
        self.chart_empty_title.pack(pady=(SPACE_24, SPACE_4))

        self.chart_empty_helper = ctk.CTkLabel(
            state,
            text="Take a test to populate this chart.",
            wraplength=520,
            **get_text_style("card_description"),
        )
        self.chart_empty_helper.pack(padx=SPACE_24, pady=(0, SPACE_24))
        return state

    def _build_weak_topics_empty_state(self) -> ctk.CTkFrame:
        """Create the Weak Topics empty-state surface."""
        state = ctk.CTkFrame(self.content_frame, **get_card_style("default"))

        self.weak_topics_empty_title = ctk.CTkLabel(
            state,
            text="No weak-topic data yet",
            **get_text_style("card_title"),
        )
        self.weak_topics_empty_title.pack(pady=(SPACE_24, SPACE_4))

        self.weak_topics_empty_helper = ctk.CTkLabel(
            state,
            text="Complete scored attempts to identify topics that need review.",
            wraplength=560,
            justify="center",
            **get_text_style("card_description"),
        )
        self.weak_topics_empty_helper.pack(padx=SPACE_24, pady=(0, SPACE_24))
        return state

    def on_show(self, **kwargs) -> None:
        """Load data when shown."""
        tests = self.test_service.get_all_tests()
        test_names = ["All Tests"] + [t.name for t in tests]
        self.test_filter_menu.configure(values=test_names)
        self.test_filter_var.set("All Tests")
        self.group_by_var.set("Test")
        self.tab_var.set("Score Trends")

        self._render_current_tab()

    def _on_tab_change(self, value: str) -> None:
        """Handle tab switch."""
        self._render_current_tab()

    def _on_filter_change(self, value: str) -> None:
        """Handle filter change."""
        self._render_current_tab()

    def _get_selected_test_id(self):
        """Get test_id from filter, or None for 'All Tests'."""
        test_filter = self.test_filter_var.get()
        if test_filter == "All Tests":
            return None
        tests = self.test_service.get_all_tests()
        for t in tests:
            if t.name == test_filter:
                return t.id
        return None

    def _render_current_tab(self) -> None:
        """Render the currently selected tab."""
        tab = self.tab_var.get()

        self.chart_shell.pack_forget()
        self.graph_widget.pack_forget()
        self.chart_empty_state.pack_forget()
        self.weak_topics_frame.pack_forget()
        self.weak_topics_empty_state.pack_forget()

        if tab == "Weak Topics":
            self.group_by_label.grid(
                row=1,
                column=2,
                sticky="e",
                padx=(SPACE_16, SPACE_8),
                pady=(0, SPACE_16),
            )
            self.group_by_seg.grid(row=1, column=3, sticky="ew", pady=(0, SPACE_16))
        else:
            self.group_by_label.grid_remove()
            self.group_by_seg.grid_remove()

        if tab == "Score Trends":
            self._render_score_trends()
        elif tab == "Test Comparison":
            self._render_test_comparison()
        elif tab == "Study Activity":
            self._render_study_activity()
        elif tab == "Weak Topics":
            self._render_weak_topics()

    def _show_chart_shell(self) -> None:
        """Show the shared chart surface."""
        self.chart_shell.pack(fill="both", expand=True)
        self.graph_widget.pack(fill="both", expand=True)

    def _show_chart_empty(self, title: str, helper: str) -> None:
        """Show a chart no-data surface."""
        self.chart_shell.pack(fill="both", expand=True)
        self.graph_widget.pack_forget()
        self.chart_empty_title.configure(text=title)
        self.chart_empty_helper.configure(text=helper)
        self.chart_empty_state.pack(fill="x", padx=SPACE_24, pady=SPACE_24)

    def _show_weak_topics_empty(self, title: str, helper: str) -> None:
        """Show a Weak Topics empty-state surface."""
        self.weak_topics_empty_title.configure(text=title)
        self.weak_topics_empty_helper.configure(text=helper)
        self.weak_topics_empty_state.pack(fill="x", pady=SPACE_24)

    def _render_score_trends(self) -> None:
        """Render score trends line chart."""
        test_id = self._get_selected_test_id()
        data = self.analytics_service.get_scores_over_time(test_id=test_id)

        if not data:
            self._show_chart_empty(
                "No score trend yet",
                "Complete a test attempt to plot score changes over time.",
            )
            return

        x_data = list(range(1, len(data) + 1))
        y_data = [d["percentage"] for d in data]

        self._show_chart_shell()
        self.graph_widget.draw_line_chart(
            x_data,
            y_data,
            title="Score Trends",
            x_label="Attempt #",
            y_label="Score (%)",
        )

    def _render_test_comparison(self) -> None:
        """Render test comparison bar chart."""
        data = self.analytics_service.get_average_scores_by_test()

        if not data:
            self._show_chart_empty(
                "No comparison data yet",
                "Complete attempts across tests to compare average scores.",
            )
            return

        labels = [d["test_name"] for d in data]
        values = [d["avg_score"] for d in data]

        self._show_chart_shell()
        self.graph_widget.draw_bar_chart(
            labels,
            values,
            title="Average Scores by Test",
            y_label="Average Score (%)",
        )

    def _render_study_activity(self) -> None:
        """Render study activity chart."""
        data = self.analytics_service.get_attempt_frequency(days=30)

        if not data:
            self._show_chart_empty(
                "No study activity yet",
                "Complete attempts to see activity from the last 30 days.",
            )
            return

        dates = [d["day"] for d in data]
        short_dates = [d[-5:] if d and len(d) >= 5 else d for d in dates]
        counts = [d["count"] for d in data]

        self._show_chart_shell()
        self.graph_widget.draw_activity_chart(
            short_dates,
            counts,
            title="Study Activity (Last 30 Days)",
        )

    def _render_weak_topics(self) -> None:
        """Render weak topics list with color-coded indicators."""
        test_id = self._get_selected_test_id()
        group_by = {
            "Test": "test",
            "Group": "group",
            "Category": "category",
        }.get(self.group_by_var.get(), "test")
        topics = self.analytics_service.get_weak_topics(
            test_id=test_id, group_by=group_by
        )

        if not topics:
            if group_by == "category":
                self._show_weak_topics_empty(
                    "No categories tagged",
                    "Add question categories or switch to Test or Group grouping.",
                )
            else:
                self._show_weak_topics_empty(
                    "No weak-topic data yet",
                    "Complete scored attempts to identify topics that need review.",
                )
            return

        for widget in self.weak_topics_frame.winfo_children():
            widget.destroy()

        self.weak_topics_frame.pack(fill="both", expand=True)

        for topic in topics:
            self._create_topic_card(topic)

    def _create_topic_card(self, topic: dict) -> None:
        """Create a color-coded topic card."""
        status_label, color_role = self._topic_status_style(topic["status"])
        color = get_color(color_role)

        card = ctk.CTkFrame(self.weak_topics_frame, **get_card_style("default"))
        card.pack(fill="x", pady=(0, SPACE_8), padx=SPACE_4)

        indicator = ctk.CTkFrame(
            card,
            width=6,
            height=1,
            corner_radius=RADIUS_CONTROL,
            fg_color=color,
        )
        indicator.pack(side="left", fill="y", padx=(SPACE_8, 0), pady=SPACE_8)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=SPACE_12,
            pady=SPACE_12,
        )

        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x")

        ctk.CTkLabel(
            top_row,
            text=topic["category"],
            wraplength=560,
            anchor="w",
            justify="left",
            **get_text_style("card_title"),
        ).pack(side="left", fill="x", expand=True)

        status_pill = ctk.CTkFrame(
            top_row,
            height=28,
            fg_color=get_color("surface_subtle"),
            corner_radius=RADIUS_CONTROL,
        )
        status_pill.pack(side="right", padx=(SPACE_12, 0))

        status_style = get_text_style("metadata")
        status_style["text_color"] = color
        ctk.CTkLabel(
            status_pill,
            text=status_label,
            **status_style,
        ).pack(padx=SPACE_8, pady=SPACE_4)

        progress_row = ctk.CTkFrame(content, fg_color="transparent")
        progress_row.pack(fill="x", pady=(SPACE_12, SPACE_4))

        progress = ctk.CTkProgressBar(
            progress_row,
            height=10,
            fg_color=get_color("surface_subtle"),
            progress_color=color,
        )
        progress.pack(fill="x", expand=True)
        progress.set(topic["percentage"] / 100.0)

        meta_row = ctk.CTkFrame(content, fg_color="transparent")
        meta_row.pack(fill="x")

        ctk.CTkLabel(
            meta_row,
            text=f"{topic['correct']}/{topic['total']} correct",
            anchor="w",
            **get_text_style("card_metadata"),
        ).pack(side="left")

        percent_style = get_text_style("metadata")
        percent_style["text_color"] = color
        ctk.CTkLabel(
            meta_row,
            text=f"{topic['percentage']}%",
            anchor="e",
            **percent_style,
        ).pack(side="right")

    @staticmethod
    def _topic_status_style(status: str) -> tuple[str, str]:
        """Return display text and semantic color role for a topic status."""
        if status == "weak":
            return "Weak", "status_incorrect"
        if status == "moderate":
            return "Moderate", "status_warning"
        return "Strong", "status_correct"
