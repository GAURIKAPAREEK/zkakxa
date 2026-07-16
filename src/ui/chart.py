"""Chart helpers and status badges."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ui.tokens import get_chart_colors, get_theme_name, get_vars


def chart_layout(title: str = "") -> dict:
    v = get_vars()
    text = v["--ui-chart-text"]
    muted = v["--ui-chart-muted"]
    grid = v["--ui-chart-grid"]
    axis = {
        "gridcolor": grid,
        "linecolor": v["--ui-border-strong"],
        "tickfont": {"size": 12, "color": muted, "family": "Outfit"},
        "title": {"font": {"size": 12, "color": muted, "family": "Outfit"}},
        "zeroline": False,
    }
    return {
        "title": {"text": title, "font": {"size": 15, "color": text, "family": "Outfit"}, "x": 0, "xanchor": "left"},
        "paper_bgcolor": v["--ui-chart-bg"],
        "plot_bgcolor": v["--ui-chart-bg"],
        "font": {"family": "Outfit, sans-serif", "color": text, "size": 12},
        "margin": {"l": 48, "r": 20, "t": 44, "b": 64},
        "height": 340,
        "xaxis": dict(axis),
        "yaxis": dict(axis),
        "legend": {
            "orientation": "h",
            "yanchor": "top",
            "y": -0.22,
            "xanchor": "center",
            "x": 0.5,
            "bgcolor": "rgba(0,0,0,0)",
            "font": {"size": 12, "color": text},
        },
        "hoverlabel": {
            "bgcolor": v["--ui-surface"],
            "bordercolor": v["--ui-border-strong"],
            "font": {"family": "Outfit", "size": 12, "color": text},
        },
        "colorway": v["--ui-chart-colors"].split(","),
        "autosize": True,
    }


def status_style(status: str) -> str:
    v = get_vars()
    mapping = {
        "CRITICAL": (v["--ui-danger-soft"], v["--ui-danger"]),
        "WARNING": ("rgba(251,191,36,0.12)", "#FBBF24"),
        "OK": (v["--ui-success-soft"], v["--ui-success"]),
    }
    bg, fg = mapping.get(status, (v["--ui-muted"], v["--ui-text"]))
    return f"background-color:{bg};color:{fg};font-weight:500;border-radius:6px;padding:2px 8px;"


def render_quality_trend_charts(
    chart_df: pd.DataFrame,
    *,
    threshold: float | None = None,
    key_prefix: str = "trend",
) -> None:
    """Render quality + anomalies charts that stay readable with few runs."""
    if chart_df is None or chart_df.empty:
        return

    try:
        work = chart_df.copy()
        if "run_timestamp" in work.columns:
            work["run_timestamp"] = pd.to_datetime(work["run_timestamp"], errors="coerce")
            work = work.dropna(subset=["run_timestamp"]).sort_values("run_timestamp")
        if work.empty:
            return

        work["quality_score"] = pd.to_numeric(work.get("quality_score"), errors="coerce").fillna(0)
        work["anomalies_found"] = pd.to_numeric(work.get("anomalies_found"), errors="coerce").fillna(0)

        palette = get_chart_colors()
        theme = get_theme_name()
        n_points = len(work)
        if n_points <= 8:
            work = work.copy()
            work["run_label"] = work["run_timestamp"].dt.strftime("%d %b %H:%M")
            x_col = "run_label"
        else:
            x_col = "run_timestamp"

        color_col = (
            "file_name"
            if "file_name" in work.columns and work["file_name"].nunique() > 1
            else None
        )

        c1, c2 = st.columns(2, gap="large")
        with c1:
            fig = px.line(
                work,
                x=x_col,
                y="quality_score",
                color=color_col,
                markers=True,
                color_discrete_sequence=palette,
            )
            fig.update_traces(line=dict(width=2.5), marker=dict(size=9))
            if threshold is not None:
                fig.add_hline(
                    y=float(threshold),
                    line_dash="dot",
                    line_color=get_vars()["--ui-danger"],
                    annotation_text="Threshold",
                    annotation_font_color=get_vars()["--ui-danger"],
                )
            layout = chart_layout("Quality score over time")
            layout["yaxis"]["range"] = [0, 105]
            layout["yaxis"]["tickfont"] = {"size": 12, "color": get_vars()["--ui-chart-muted"], "family": "Outfit"}
            layout["xaxis"]["tickfont"] = {"size": 12, "color": get_vars()["--ui-chart-muted"], "family": "Outfit"}
            if x_col == "run_label":
                layout["xaxis"]["type"] = "category"
            fig.update_layout(**layout)
            # Theme in key forces Plotly remount so colors update without hard refresh
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False, "responsive": True},
                key=f"{key_prefix}_quality_{theme}",
            )

        with c2:
            max_a = max(int(work["anomalies_found"].max() or 0), 1)
            fig2 = px.bar(
                work,
                x=x_col,
                y="anomalies_found",
                color=color_col,
                color_discrete_sequence=palette,
                barmode="group",
            )
            fig2.update_traces(opacity=0.9, marker_line_width=0)
            layout2 = chart_layout("Anomalies per run")
            layout2["yaxis"]["range"] = [0, max_a + max(1, max_a // 3)]
            layout2["bargap"] = 0.5 if n_points <= 8 else 0.2
            layout2["bargroupgap"] = 0.15
            if x_col == "run_label":
                layout2["xaxis"]["type"] = "category"
            fig2.update_layout(**layout2)
            st.plotly_chart(
                fig2,
                use_container_width=True,
                config={"displayModeBar": False, "responsive": True},
                key=f"{key_prefix}_anomalies_{theme}",
            )
    except Exception as exc:
        st.warning(f"Could not render charts: {exc}")
