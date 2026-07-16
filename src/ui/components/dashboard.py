"""Dashboard UI blocks."""

from __future__ import annotations

import html
import os
from glob import glob

import pandas as pd
import streamlit as st

from src.paths import resolve_path
from src.ui.logo import crystal_svg

HOW_IT_WORKS = (
    ("01", "Ingest", "Secure upload of raw CSV, JSON, or Excel."),
    ("02", "Validate", "Automatic profiling, null checks, and scoring."),
    ("03", "Quarantine", "Isolate invalid rows; keep only clean data."),
    ("04", "Monitor", "Anomalies, schema drift, and quality trend graphs."),
)


def dashboard_hero(*, has_data: bool = False) -> None:
    status = "Pipeline ready" if has_data else "Ready to ingest"
    st.markdown(
        f"""
<div class="ui-hero ui-fade">
  <div class="ui-hero-copy">
    <p class="ui-hero-kicker">Data Quality Command Center</p>
    <p class="ui-hero-title">Monitor, validate, and trust every dataset</p>
    <p class="ui-hero-lede">Upload files, quarantine bad rows, and track quality trends in one place.</p>
  </div>
  <div class="ui-hero-status">
    <div class="ui-status"><span class="ui-status-dot"></span>{html.escape(status)}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def how_it_works() -> None:
    steps = "".join(
        f'<li class="ui-how-step">'
        f'<div class="ui-how-inner">'
        f'<span class="ui-how-num" aria-hidden="true">{n}</span>'
        f'<span class="ui-how-body">'
        f'<strong class="ui-how-title">{html.escape(title)}</strong>'
        f'<span class="ui-how-desc">{html.escape(body)}</span>'
        f"</span></div></li>"
        for n, title, body in HOW_IT_WORKS
    )
    st.markdown(
        f'<div class="ui-how ui-fade">'
        f'<p class="ui-how-kicker">How it works</p>'
        f'<ol class="ui-how-grid" aria-label="How it works">{steps}</ol>'
        f"</div>",
        unsafe_allow_html=True,
    )


def page_intro(title: str, subtitle: str = "") -> None:
    sub = f"<p>{html.escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f'<div class="ui-page-intro ui-fade"><h1>{html.escape(title)}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )


def stat_grid(items: list[tuple[str, str | int | float, str]]) -> None:
    st.markdown('<div class="ui-stat-anchor" aria-hidden="true"></div>', unsafe_allow_html=True)
    cols = st.columns(len(items), gap="medium")
    for col, (label, value, hint) in zip(cols, items):
        with col:
            st.markdown(
                f'<div class="ui-stat ui-fade">'
                f'<span class="ui-stat-label">{html.escape(str(label))}</span>'
                f'<span class="ui-stat-value">{html.escape(str(value))}</span>'
                f'<span class="ui-stat-hint">{html.escape(str(hint))}</span></div>',
                unsafe_allow_html=True,
            )


def section(title: str, subtitle: str = "") -> None:
    sub = f"<p>{html.escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f'<div class="ui-section"><h3>{html.escape(title)}</h3>{sub}</div>',
        unsafe_allow_html=True,
    )


def panel_start() -> None:
    st.markdown('<div class="ui-panel-anchor" aria-hidden="true"></div>', unsafe_allow_html=True)


def upload_zone() -> None:
    """No-op: the styled st.file_uploader dropzone is the single upload component."""
    return


def empty_state(title: str, body: str, *, compact: bool = False) -> None:
    icon = crystal_svg("sm", animated=False, glow=True) if compact else ""
    icon_html = (
        f'<div style="display:flex;justify-content:center;margin-bottom:8px">{icon}</div>'
        if icon
        else ""
    )
    st.markdown(
        f'<div class="ui-empty"><h4>{html.escape(title)}</h4>{icon_html}'
        f'<p>{html.escape(body)}</p></div>',
        unsafe_allow_html=True,
    )


def themed_table(df: pd.DataFrame, *, max_rows: int | None = 20) -> None:
    """Theme-matched HTML table — avoids Streamlit's pure-black dataframe grid."""
    if df is None or df.empty:
        empty_state("No records", "Nothing to show yet.", compact=True)
        return

    view = df.head(max_rows) if max_rows else df
    headers = "".join(f"<th>{html.escape(str(c))}</th>" for c in view.columns)
    rows: list[str] = []
    for _, row in view.iterrows():
        cells = "".join(f"<td>{html.escape(str(v))}</td>" for v in row.tolist())
        rows.append(f"<tr>{cells}</tr>")
    st.markdown(
        f'<div class="ui-table-wrap"><table class="ui-table">'
        f'<thead><tr>{headers}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>',
        unsafe_allow_html=True,
    )


def load_latest_quarantine(config: dict) -> tuple[pd.DataFrame, str]:
    """Return the newest quarantine CSV and its filename, or empty."""
    try:
        folder = resolve_path(config.get("output", {}).get("quarantine_path", "data/quarantine/"))
        if not os.path.isdir(folder):
            return pd.DataFrame(), ""
        files = sorted(
            glob(os.path.join(folder, "quarantine_*.csv")),
            key=os.path.getmtime,
            reverse=True,
        )
        if not files:
            return pd.DataFrame(), ""
        path = files[0]
        return pd.read_csv(path), os.path.basename(path)
    except Exception:
        return pd.DataFrame(), ""


def quarantine_panel(config: dict, live_df: pd.DataFrame | None = None) -> None:
    """Always-visible quarantine section (live run rows or latest saved file)."""
    section("Quarantine", "Rows that failed critical validation rules")
    df = live_df if live_df is not None and not live_df.empty else None
    source = "current run"
    if df is None:
        df, name = load_latest_quarantine(config)
        source = name or "saved quarantine"

    if df is None or df.empty:
        empty_state(
            "No quarantined rows",
            "When validation fails critical rules, bad rows land here for review.",
            compact=True,
        )
        return

    st.caption(f"Showing {len(df)} rows · {source}")
    with st.expander(f"Quarantined rows ({len(df)})", expanded=False):
        themed_table(df, max_rows=100)


def page_footer() -> None:
    st.markdown(
        '<div class="ui-footer">DataSentinel · Enterprise data quality</div>',
        unsafe_allow_html=True,
    )
