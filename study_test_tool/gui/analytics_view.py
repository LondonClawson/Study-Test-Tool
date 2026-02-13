"""Analytics view — performance graphs and weak topic identification."""

import customtkinter as ctk

from config.settings import (
    COLOR_TOPIC_MODERATE,
    COLOR_TOPIC_STRONG,
    COLOR_TOPIC_WEAK,
    FONT_FAMILY,
    FONT_SIZE_BODY,
    FONT_SIZE_HEADING,
    FONT_SIZE_SMALL,
    FONT_SIZE_TITLE,
)
from gui.components.graph_widget import GraphWidget
from services.analytics_service import AnalyticsService
from services.test_service import TestService
from utils.constants import SCREEN_HOME


class AnalyticsViewFrame(ctk.CTkFrame):
    """Screen for viewing performance analytics and graphs."""

    def __init__(self, parent: ctk.CTkFrame, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.analytics_service = AnalyticsService()
        self.test_service = TestService()

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the analytics layout."""
        # Top bar
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkButton(
            top_frame,
            text="< Back",
            width=80,
            fg_color="gray",
            command=lambda: self.controller.show_frame(SCREEN_HOME),
        ).pack(side="left")

        ctk.CTkLabel(
            top_frame,
            text="Analytics",
            font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
        ).pack(side="left", padx=20)

        # Tab selector
        tab_frame = ctk.CTkFrame(self, fg_color="transparent")
        tab_frame.pack(fill="x", padx=30, pady=(0, 5))

        self.tab_var = ctk.StringVar(value="Score Trends")
        self.tab_seg = ctk.CTkSegmentedButton(
            tab_frame,
            values=["Score Trends", "Test Comparison", "Study Activity", "Weak Topics"],
            variable=self.tab_var,
            command=self._on_tab_change,
        )
        self.tab_seg.pack(side="left")

        # Filter row
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", padx=30, pady=(0, 10))

        ctk.CTkLabel(
            filter_frame,
            text="Test:",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
        ).pack(side="left", padx=(0, 10))

        self.test_filter_var = ctk.StringVar(value="All Tests")
        self.test_filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.test_filter_var,
            values=["All Tests"],
            command=self._on_filter_change,
            width=250,
        )
        self.test_filter_menu.pack(side="left")

        # Content area — holds either graph or weak topics list
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # Graph widget (created once, reused)
        self.graph_widget = GraphWidget(self.content_frame, figsize=(8, 4))

        # Scrollable frame for weak topics (created once, shown when needed)
        self.weak_topics_frame = ctk.CTkScrollableFrame(self.content_frame)

        # Empty state
        self.empty_label = ctk.CTkLabel(
            self.content_frame,
            text="No data available yet. Take some tests first!",
            font=(FONT_FAMILY, FONT_SIZE_BODY),
            text_color="gray",
        )

    def on_show(self, **kwargs) -> None:
        """Load data when shown."""
        tests = self.test_service.get_all_tests()
        test_names = ["All Tests"] + [t.name for t in tests]
        self.test_filter_menu.configure(values=test_names)
        self.test_filter_var.set("All Tests")
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

        # Hide everything first
        self.graph_widget.pack_forget()
        self.weak_topics_frame.pack_forget()
        self.empty_label.pack_forget()

        if tab == "Score Trends":
            self._render_score_trends()
        elif tab == "Test Comparison":
            self._render_test_comparison()
        elif tab == "Study Activity":
            self._render_study_activity()
        elif tab == "Weak Topics":
            self._render_weak_topics()

    def _render_score_trends(self) -> None:
        """Render score trends line chart."""
        test_id = self._get_selected_test_id()
        data = self.analytics_service.get_scores_over_time(test_id=test_id)

        if not data:
            self.empty_label.pack(pady=40)
            return

        x_data = list(range(1, len(data) + 1))
        y_data = [d["percentage"] for d in data]

        self.graph_widget.pack(fill="both", expand=True)
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
            self.empty_label.pack(pady=40)
            return

        labels = [d["test_name"] for d in data]
        values = [d["avg_score"] for d in data]

        self.graph_widget.pack(fill="both", expand=True)
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
            self.empty_label.pack(pady=40)
            return

        dates = [d["day"] for d in data]
        # Shorten date labels
        short_dates = [d[-5:] if d and len(d) >= 5 else d for d in dates]
        counts = [d["count"] for d in data]

        self.graph_widget.pack(fill="both", expand=True)
        self.graph_widget.draw_activity_chart(
            short_dates,
            counts,
            title="Study Activity (Last 30 Days)",
        )

    def _render_weak_topics(self) -> None:
        """Render weak topics list with color-coded indicators."""
        test_id = self._get_selected_test_id()
        topics = self.analytics_service.get_weak_topics(test_id=test_id)

        if not topics:
            self.empty_label.pack(pady=40)
            return

        # Clear and show scrollable frame
        for widget in self.weak_topics_frame.winfo_children():
            widget.destroy()

        self.weak_topics_frame.pack(fill="both", expand=True)

        for topic in topics:
            self._create_topic_card(topic)

    def _create_topic_card(self, topic: dict) -> None:
        """Create a color-coded topic card."""
        status = topic["status"]
        if status == "weak":
            color = COLOR_TOPIC_WEAK
        elif status == "moderate":
            color = COLOR_TOPIC_MODERATE
        else:
            color = COLOR_TOPIC_STRONG

        card = ctk.CTkFrame(self.weak_topics_frame, corner_radius=8)
        card.pack(fill="x", pady=4, padx=5)

        # Color indicator bar
        indicator = ctk.CTkFrame(card, width=6, corner_radius=3, fg_color=color)
        indicator.pack(side="left", fill="y", padx=(4, 0), pady=4)

        # Content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        # Top: category name and status
        top_row = ctk.CTkFrame(content, fg_color="transparent")
        top_row.pack(fill="x")

        ctk.CTkLabel(
            top_row,
            text=topic["category"],
            font=(FONT_FAMILY, FONT_SIZE_HEADING, "bold"),
            anchor="w",
        ).pack(side="left")

        ctk.CTkLabel(
            top_row,
            text=status.capitalize(),
            font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            text_color=color,
        ).pack(side="right")

        # Progress bar
        progress = ctk.CTkProgressBar(content, height=12)
        progress.pack(fill="x", pady=(5, 2))
        progress.set(topic["percentage"] / 100.0)
        progress.configure(progress_color=color)

        # Stats
        ctk.CTkLabel(
            content,
            text=f"{topic['correct']}/{topic['total']} correct ({topic['percentage']}%)",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color="gray",
            anchor="w",
        ).pack(fill="x")
