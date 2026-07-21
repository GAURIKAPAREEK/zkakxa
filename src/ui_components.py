"""Backward-compatible re-exports (lazy — no import cycles)."""

from __future__ import annotations

_EXPORTS = {
  # app shell
  "init_theme": "src.app_shell",
  "inject_css": "src.app_shell",
  "render_app_header": "src.app_shell",
  "render_sidebar": "src.app_shell",
  "toggle_theme": "src.app_shell",
  # dashboard blocks
  "dashboard_hero": "src.dashboard_ui",
  "empty_state": "src.dashboard_ui",
  "metric_row": "src.dashboard_ui",
  "page_footer": "src.dashboard_ui",
  "section": "src.dashboard_ui",
  "stat_grid": "src.dashboard_ui",
  "upload_card": "src.dashboard_ui",
  "upload_zone": "src.dashboard_ui",
  # helpers
  "suppress_enter_hint": "src.ui_helpers",
}

__all__ = list(_EXPORTS) + ["get_chart_config", "styled_dataframe"]


def __getattr__(name: str):
    if name == "get_chart_config":
        from src.design_system import chart_layout, get_chart_colors, get_vars

        def get_chart_config():
            return chart_layout, get_chart_colors, get_vars

        return get_chart_config

    if name == "styled_dataframe":
        from src.design_system import status_style

        def styled_dataframe(df, status_col: str | None = None):
            if status_col and status_col in df.columns:
                return df.style.map(status_style, subset=[status_col])
            return df

        return styled_dataframe

    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    import importlib

    module = importlib.import_module(target)
    return getattr(module, name)
