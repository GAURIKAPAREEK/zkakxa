"""Dashboard UI — delegates to src.ui.components.dashboard."""

from src.ui.components.dashboard import (
    dashboard_hero,
    empty_state,
    how_it_works,
    page_footer,
    page_intro,
    panel_start,
    quarantine_panel,
    section,
    stat_grid,
    themed_table,
    upload_zone,
)

upload_card = upload_zone
metric_row = lambda items: stat_grid([(l, v, "") for l, v in items])

__all__ = [
    "dashboard_hero",
    "empty_state",
    "how_it_works",
    "metric_row",
    "page_footer",
    "page_intro",
    "panel_start",
    "quarantine_panel",
    "section",
    "stat_grid",
    "themed_table",
    "upload_card",
    "upload_zone",
]
