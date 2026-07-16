"""
Backward-compatible shim — all UI lives in src.ui.
"""

from src.ui.chart import chart_layout, status_style
from src.ui.stylesheet import build_global_css
from src.ui.tokens import SP, SPACE, get_chart_colors, get_theme_name, get_vars

__all__ = [
    "SP",
    "SPACE",
    "build_global_css",
    "chart_layout",
    "get_chart_colors",
    "get_theme_name",
    "get_vars",
    "status_style",
]
