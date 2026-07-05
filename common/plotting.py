from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import matplotlib

matplotlib.use("Agg")  # safe default for headless environments / CI
import matplotlib.pyplot as plt  # noqa: E402  (must follow matplotlib.use())

from common.utils import ensure_dir  # noqa: E402

__all__ = ["plot_line_comparison", "plot_bar_comparison"]

# A small, consistent, colour-blind-friendly palette used across all plots
# so that every figure in the report has a uniform visual style.
_PALETTE: tuple[str, ...] = (
    "#1F4E79",  # dark blue
    "#C55A11",  # burnt orange
    "#548235",  # green
    "#7030A0",  # purple
    "#BF0000",  # red
)

_FIGURE_SIZE: tuple[float, float] = (7.0, 4.5)
_DPI: int = 150


def _apply_common_style(axes: plt.Axes, title: str, x_label: str, y_label: str) -> None:
    axes.set_title(title, fontsize=13, fontweight="bold", pad=10)
    axes.set_xlabel(x_label, fontsize=11)
    axes.set_ylabel(y_label, fontsize=11)
    axes.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
    axes.legend(frameon=False, fontsize=9.5)


def plot_line_comparison(
    x_values: Sequence[float],
    series: Mapping[str, Sequence[float]],
    title: str,
    x_label: str,
    y_label: str,
    output_path: Path,
    log_scale_y: bool = False,
) -> Path:
    
    if not series:
        raise ValueError("'series' must contain at least one named series.")
    for name, y_values in series.items():
        if len(y_values) != len(x_values):
            raise ValueError(
                f"Series '{name}' has {len(y_values)} points but there are "
                f"{len(x_values)} x-values."
            )

    figure, axes = plt.subplots(figsize=_FIGURE_SIZE)
    for index, (name, y_values) in enumerate(series.items()):
        colour = _PALETTE[index % len(_PALETTE)]
        axes.plot(
            x_values,
            y_values,
            marker="o",
            markersize=5,
            linewidth=1.8,
            color=colour,
            label=name,
        )
    if log_scale_y:
        axes.set_yscale("log")
    _apply_common_style(axes, title, x_label, y_label)

    ensure_dir(output_path.parent)
    figure.tight_layout()
    figure.savefig(output_path, dpi=_DPI)
    plt.close(figure)
    return output_path


def plot_bar_comparison(
    categories: Sequence[str],
    series: Mapping[str, Sequence[float]],
    title: str,
    x_label: str,
    y_label: str,
    output_path: Path,
    log_scale_y: bool = False,
) -> Path:
    
    if not series:
        raise ValueError("'series' must contain at least one named series.")
    for name, values in series.items():
        if len(values) != len(categories):
            raise ValueError(
                f"Series '{name}' has {len(values)} values but there are "
                f"{len(categories)} categories."
            )

    figure, axes = plt.subplots(figsize=_FIGURE_SIZE)
    num_series = len(series)
    bar_width = 0.8 / num_series
    x_positions = range(len(categories))

    for index, (name, values) in enumerate(series.items()):
        colour = _PALETTE[index % len(_PALETTE)]
        offsets = [x + (index - (num_series - 1) / 2) * bar_width for x in x_positions]
        axes.bar(offsets, values, width=bar_width, color=colour, label=name)

    if log_scale_y:
        axes.set_yscale("log")
    axes.set_xticks(list(x_positions))
    axes.set_xticklabels(categories)
    _apply_common_style(axes, title, x_label, y_label)

    ensure_dir(output_path.parent)
    figure.tight_layout()
    figure.savefig(output_path, dpi=_DPI)
    plt.close(figure)
    return output_path