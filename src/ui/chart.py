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
        "tickfont": {"size": 11, "color": muted, "family": "Outfit"},
        "title": {"text": "", "font": {"size": 11, "color": muted, "family": "Outfit"}},
        "zeroline": False,
        "automargin": True,
    }
    return {
        "title": {"text": title, "font": {"size": 14, "color": text, "family": "Outfit"}, "x": 0, "xanchor": "left"},
        "paper_bgcolor": v["--ui-chart-bg"],
        "plot_bgcolor": v["--ui-chart-bg"],
        "font": {"family": "Outfit, sans-serif", "color": text, "size": 11},
        "margin": {"l": 45, "r": 25, "t": 35, "b": 45},
        "height": 350,
        "xaxis": dict(axis, tickangle=0, nticks=6),
        "yaxis": dict(axis),
        "legend": {
            "orientation": "h",
            "yanchor": "top",
            "y": -0.22,
            "xanchor": "center",
            "x": 0.5,
            "title": {"text": ""},
            "bgcolor": "rgba(0,0,0,0)",
            "font": {"size": 11, "color": text},
        },
        "hoverlabel": {
            "bgcolor": v["--ui-surface"],
            "bordercolor": v["--ui-border-strong"],
            "font": {"family": "Outfit", "size": 11, "color": text},
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

        # Show only the last 5 runs to keep the chart spacious and uncrowded
        work = work.tail(5)

        theme = get_theme_name()
        if theme == "light":
            palette = [
                "#0284C7",  # Vivid Blue
                "#EA580C",  # Vivid Orange
                "#059669",  # Emerald Green
                "#9333EA",  # Vivid Purple
                "#D97706",  # Amber
                "#DB2777",  # Magenta Pink
                "#0D9488",  # Teal
                "#4F46E5",  # Indigo
                "#DC2626",  # Red
                "#65A30D",  # Lime Green
            ]
        else:
            palette = [
                "#38BDF8",  # Sky Blue
                "#F97316",  # Vibrant Orange
                "#10B981",  # Emerald Green
                "#A855F7",  # Purple
                "#F59E0B",  # Amber Yellow
                "#EC4899",  # Bright Pink
                "#14B8A6",  # Teal
                "#6366F1",  # Indigo
                "#EF4444",  # Bright Red
                "#84CC16",  # Lime Green
            ]
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
        color_map = {}
        if color_col:
            unique_files = list(work[color_col].unique())
            color_map = {fname: palette[i % len(palette)] for i, fname in enumerate(unique_files)}

        c1, c2 = st.columns(2, gap="large")
        with c1:
            fig = px.line(
                work,
                x=x_col,
                y="quality_score",
                color=color_col,
                markers=True,
                color_discrete_map=color_map if color_map else None,
                color_discrete_sequence=palette if not color_map else None,
                labels={"file_name": "", "run_label": "", "quality_score": ""},
            )
            fig.update_traces(line=dict(width=2.5), marker=dict(size=9), cliponaxis=False)
            if threshold is not None:
                fig.add_hline(
                    y=float(threshold),
                    line_dash="dot",
                    line_color=get_vars()["--ui-danger"],
                    line_width=1.5,
                )
                fig.add_annotation(
                    x=0.01,
                    y=float(threshold),
                    xref="paper",
                    yref="y",
                    text="Threshold",
                    showarrow=False,
                    yshift=12,
                    xanchor="left",
                    font=dict(size=11, color=get_vars()["--ui-danger"], family="Outfit"),
                )
            layout = chart_layout("Quality score over time")
            layout["yaxis"]["range"] = [0, 105]
            if x_col == "run_label":
                layout["xaxis"]["type"] = "category"
            fig.update_layout(**layout)
            fig.update_layout(xaxis_title="", yaxis_title="", legend_title_text="", legend=dict(title=dict(text="")))
            fig.update_xaxes(title_text="", tickangle=0)
            fig.update_yaxes(title_text="", range=[0, 105])
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": True,
                    "scrollZoom": True,
                    "displaylogo": False,
                    "responsive": True,
                    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                },
            )

        with c2:
            max_a = max(int(work["anomalies_found"].max() or 0), 1)
            fig2 = px.line(
                work,
                x=x_col,
                y="anomalies_found",
                color=color_col,
                markers=True,
                color_discrete_map=color_map if color_map else None,
                color_discrete_sequence=palette if not color_map else None,
                labels={"file_name": "", "run_label": "", "anomalies_found": ""},
            )
            fig2.update_traces(line=dict(width=2.5), marker=dict(size=9), cliponaxis=False)
            layout2 = chart_layout("Anomalies per run")
            if max_a == 0:
                y_lower, y_upper = -0.5, 5
            elif max_a < 10:
                y_lower, y_upper = -0.5, max_a + 1.5
            else:
                y_lower, y_upper = -max_a * 0.05, max_a * 1.15
            layout2["yaxis"]["range"] = [y_lower, y_upper]
            if max_a < 10:
                layout2["yaxis"]["dtick"] = 1
            if x_col == "run_label":
                layout2["xaxis"]["type"] = "category"
            fig2.update_layout(**layout2)
            fig2.update_layout(xaxis_title="", yaxis_title="", legend_title_text="", legend=dict(title=dict(text="")))
            fig2.update_xaxes(title_text="", tickangle=0)
            fig2.update_yaxes(title_text="")
            st.plotly_chart(
                fig2,
                use_container_width=True,
                config={
                    "displayModeBar": True,
                    "scrollZoom": True,
                    "displaylogo": False,
                    "responsive": True,
                    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                },
            )
    except Exception as exc:
        st.warning(f"Could not render charts: {exc}")
