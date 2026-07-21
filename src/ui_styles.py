"""Backward-compatible re-exports."""

from src.app_shell import init_theme, inject_css, render_app_header, render_sidebar, toggle_theme
from src.auth_ui import render_auth_page
from src.dashboard_ui import (
    dashboard_hero,
    empty_state,
    metric_row,
    page_footer,
    section,
    stat_grid,
)
from src.design_system import (
    build_global_css,
    chart_layout,
    get_chart_colors,
    get_vars as get_colors,
    status_style,
)

section_title = section
render_theme_toggle = toggle_theme


def get_login_css():
    return build_global_css(login=True)


def get_app_css():
    return build_global_css(login=False)
