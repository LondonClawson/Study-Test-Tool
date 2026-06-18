"""Graph widget — wraps matplotlib for embedding charts in CustomTkinter."""

import matplotlib

matplotlib.use("TkAgg")

from typing import List, Optional, Tuple

import customtkinter as ctk
from gui.styles import get_color
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
        self._figure_canvas: Optional[FigureCanvasTkAgg] = None
        self._init_figure()

    def _get_theme_colors(self) -> dict:
        """Get chart colors from shared visual roles."""
        return {
            "bg": self._resolve_color(get_color("chart_bg")),
            "plot_bg": self._resolve_color(get_color("chart_plot_bg")),
            "text": self._resolve_color(get_color("chart_text")),
            "grid": self._resolve_color(get_color("chart_grid")),
            "line": self._resolve_color(get_color("chart_series_primary")),
            "bar": self._resolve_color(get_color("chart_series_primary")),
        }

    @staticmethod
    def _resolve_color(color):
        """Resolve a CustomTkinter tuple color for matplotlib."""
        if isinstance(color, tuple):
            return color[1] if ctk.get_appearance_mode() == "Dark" else color[0]
        return color

    def _scaled_font_size(self, size: int) -> int:
        """Return a matplotlib font size adjusted to the active UI scale."""
        try:
            scale = ctk.ScalingTracker.get_widget_scaling(self)
        except (AttributeError, KeyError):
            scale = 1.0
        return max(1, round(size * scale))

    def _init_figure(self) -> None:
        """Create the matplotlib figure and embed in tkinter."""
        colors = self._get_theme_colors()

        self._figure = Figure(figsize=self._figsize, dpi=100)
        self._figure.patch.set_facecolor(colors["bg"])

        self._figure_canvas = FigureCanvasTkAgg(self._figure, master=self)
        self._figure_canvas.get_tk_widget().configure(bg=colors["bg"])
        self._figure_canvas.get_tk_widget().pack(fill="both", expand=True)

    def clear(self) -> None:
        """Clear the current chart."""
        colors = self._get_theme_colors()
        self._figure.clear()
        self._figure.patch.set_facecolor(colors["bg"])
        self._figure_canvas.get_tk_widget().configure(bg=colors["bg"])
        self._figure_canvas.draw()

    def refresh(self) -> None:
        """Redraw the canvas."""
        self._figure.tight_layout()
        self._figure_canvas.draw()

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
        self._figure.patch.set_facecolor(colors["bg"])
        self._figure_canvas.get_tk_widget().configure(bg=colors["bg"])

        ax = self._figure.add_subplot(111)
        ax.set_facecolor(colors["plot_bg"])
        ax.plot(x_data, y_data, color=colors["line"], marker="o", linewidth=2)

        if title:
            ax.set_title(
                title, color=colors["text"], fontsize=self._scaled_font_size(12)
            )
        if x_label:
            ax.set_xlabel(
                x_label,
                color=colors["text"],
                fontsize=self._scaled_font_size(10),
            )
        if y_label:
            ax.set_ylabel(
                y_label,
                color=colors["text"],
                fontsize=self._scaled_font_size(10),
            )

        ax.tick_params(colors=colors["text"], labelsize=self._scaled_font_size(9))
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
        self._figure.patch.set_facecolor(theme["bg"])
        self._figure_canvas.get_tk_widget().configure(bg=theme["bg"])

        ax = self._figure.add_subplot(111)
        ax.set_facecolor(theme["plot_bg"])

        bar_colors = colors_list if colors_list else [theme["bar"]] * len(labels)
        bars = ax.bar(range(len(labels)), values, color=bar_colors)

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(
            labels,
            rotation=30,
            ha="right",
            fontsize=self._scaled_font_size(9),
        )

        if title:
            ax.set_title(
                title, color=theme["text"], fontsize=self._scaled_font_size(12)
            )
        if y_label:
            ax.set_ylabel(
                y_label,
                color=theme["text"],
                fontsize=self._scaled_font_size(10),
            )

        ax.tick_params(colors=theme["text"], labelsize=self._scaled_font_size(9))
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
        self._figure.patch.set_facecolor(theme["bg"])
        self._figure_canvas.get_tk_widget().configure(bg=theme["bg"])

        ax = self._figure.add_subplot(111)
        ax.set_facecolor(theme["plot_bg"])

        ax.bar(range(len(dates)), counts, color=theme["bar"], alpha=0.7)
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(
            dates,
            rotation=45,
            ha="right",
            fontsize=self._scaled_font_size(8),
        )

        if title:
            ax.set_title(
                title, color=theme["text"], fontsize=self._scaled_font_size(12)
            )
        ax.set_ylabel(
            "Attempts",
            color=theme["text"],
            fontsize=self._scaled_font_size(10),
        )

        ax.tick_params(colors=theme["text"], labelsize=self._scaled_font_size(9))
        ax.grid(True, axis="y", alpha=0.3, color=theme["grid"])

        for spine in ax.spines.values():
            spine.set_color(theme["grid"])

        self.refresh()
