"""Graph widget — wraps matplotlib for embedding charts in CustomTkinter."""

import matplotlib

matplotlib.use("TkAgg")

from typing import List, Optional, Tuple

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class GraphWidget(ctk.CTkFrame):
    """Embeds a matplotlib chart in a CustomTkinter frame."""

    def __init__(
        self,
        parent: ctk.CTkFrame,
        figsize: Tuple[float, float] = (8, 4),
        **kwargs,
    ) -> None:
        super().__init__(parent, **kwargs)
        self._figsize = figsize
        self._figure: Optional[Figure] = None
        self._canvas: Optional[FigureCanvasTkAgg] = None
        self._init_figure()

    def _get_theme_colors(self) -> dict:
        """Get colors based on current appearance mode."""
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            return {
                "bg": "#2b2b2b",
                "text": "#ffffff",
                "grid": "#404040",
                "line": "#4a9eff",
                "bar": "#4a9eff",
            }
        return {
            "bg": "#ffffff",
            "text": "#333333",
            "grid": "#e0e0e0",
            "line": "#1f6aa5",
            "bar": "#1f6aa5",
        }

    def _init_figure(self) -> None:
        """Create the matplotlib figure and embed in tkinter."""
        colors = self._get_theme_colors()

        self._figure = Figure(figsize=self._figsize, dpi=100)
        self._figure.patch.set_facecolor(colors["bg"])

        self._canvas = FigureCanvasTkAgg(self._figure, master=self)
        self._canvas.get_tk_widget().pack(fill="both", expand=True)

    def clear(self) -> None:
        """Clear the current chart."""
        self._figure.clear()
        self._canvas.draw()

    def refresh(self) -> None:
        """Redraw the canvas."""
        self._figure.tight_layout()
        self._canvas.draw()

    def draw_line_chart(
        self,
        x_data: list,
        y_data: list,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
    ) -> None:
        """Draw a line chart.

        Args:
            x_data: X-axis values.
            y_data: Y-axis values.
            title: Chart title.
            x_label: X-axis label.
            y_label: Y-axis label.
        """
        colors = self._get_theme_colors()
        self._figure.clear()

        ax = self._figure.add_subplot(111)
        ax.set_facecolor(colors["bg"])
        ax.plot(x_data, y_data, color=colors["line"], marker="o", linewidth=2)

        if title:
            ax.set_title(title, color=colors["text"], fontsize=12)
        if x_label:
            ax.set_xlabel(x_label, color=colors["text"])
        if y_label:
            ax.set_ylabel(y_label, color=colors["text"])

        ax.tick_params(colors=colors["text"])
        ax.grid(True, alpha=0.3, color=colors["grid"])

        for spine in ax.spines.values():
            spine.set_color(colors["grid"])

        if x_data:
            ax.set_ylim(0, 105)

        self.refresh()

    def draw_bar_chart(
        self,
        labels: list,
        values: list,
        title: str = "",
        y_label: str = "",
        colors_list: Optional[list] = None,
    ) -> None:
        """Draw a bar chart.

        Args:
            labels: Bar labels.
            values: Bar values.
            title: Chart title.
            y_label: Y-axis label.
            colors_list: Optional per-bar colors.
        """
        theme = self._get_theme_colors()
        self._figure.clear()

        ax = self._figure.add_subplot(111)
        ax.set_facecolor(theme["bg"])

        bar_colors = colors_list if colors_list else [theme["bar"]] * len(labels)
        bars = ax.bar(range(len(labels)), values, color=bar_colors)

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=9)

        if title:
            ax.set_title(title, color=theme["text"], fontsize=12)
        if y_label:
            ax.set_ylabel(y_label, color=theme["text"])

        ax.tick_params(colors=theme["text"])
        ax.grid(True, axis="y", alpha=0.3, color=theme["grid"])

        for spine in ax.spines.values():
            spine.set_color(theme["grid"])

        self.refresh()

    def draw_activity_chart(
        self,
        dates: list,
        counts: list,
        title: str = "",
    ) -> None:
        """Draw a daily activity bar chart.

        Args:
            dates: Date strings.
            counts: Counts per date.
            title: Chart title.
        """
        theme = self._get_theme_colors()
        self._figure.clear()

        ax = self._figure.add_subplot(111)
        ax.set_facecolor(theme["bg"])

        ax.bar(range(len(dates)), counts, color=theme["bar"], alpha=0.7)
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=45, ha="right", fontsize=8)

        if title:
            ax.set_title(title, color=theme["text"], fontsize=12)
        ax.set_ylabel("Attempts", color=theme["text"])

        ax.tick_params(colors=theme["text"])
        ax.grid(True, axis="y", alpha=0.3, color=theme["grid"])

        for spine in ax.spines.values():
            spine.set_color(theme["grid"])

        self.refresh()
