"""UI component library."""

from src.ui.components.auth import render_auth_page
from src.ui.components.dashboard import (
    dashboard_hero,
    empty_state,
    how_it_works,
    page_footer,
    panel_start,
    quarantine_panel,
    section,
    stat_grid,
    upload_zone,
)
from src.ui.components.header import render_header
from src.ui.components.theme_toggle import render_theme_toggle

__all__ = [
    "dashboard_hero",
    "empty_state",
    "how_it_works",
    "page_footer",
    "panel_start",
    "quarantine_panel",
    "render_auth_page",
    "render_header",
    "render_theme_toggle",
    "section",
    "stat_grid",
    "upload_zone",
]
