"""DataSentinel UI layer — design system and components."""

from src.ui.chart import chart_layout, render_quality_trend_charts, status_style
from src.ui.components import (
    dashboard_hero,
    empty_state,
    how_it_works,
    page_footer,
    panel_start,
    quarantine_panel,
    render_auth_page,
    render_header,
    render_theme_toggle,
    section,
    stat_grid,
    upload_zone,
)
from src.ui.stylesheet import build_global_css
from src.ui.tokens import get_chart_colors, get_theme_name, get_vars

__all__ = [
    "build_global_css",
    "chart_layout",
    "dashboard_hero",
    "empty_state",
    "get_chart_colors",
    "get_theme_name",
    "get_vars",
    "how_it_works",
    "page_footer",
    "panel_start",
    "quarantine_panel",
    "render_auth_page",
    "render_header",
    "render_quality_trend_charts",
    "render_theme_toggle",
    "section",
    "stat_grid",
    "status_style",
    "upload_zone",
]
