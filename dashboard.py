import os
import sys

import pandas as pd
import streamlit as st

sys.path.append(os.path.dirname(__file__))

_FAVICON = os.path.join(os.path.dirname(__file__), "assets", "brand", "favicon.png")

from src.anomaly_detector import detect_statistical_anomalies
from src.auth import get_authenticator
from src.azure_sql import save_pipeline_run
from src.cleaning import count_null_cells, save_clean_data, verify_clean_data
from src.ui.chart import render_quality_trend_charts
from src.ingestion import load_config, load_file
from src.paths import resolve_path
from src.profiler import profile_dataframe
from src.quality_trend import get_quality_trend
from src.quarantine import quarantine_bad_rows, save_quarantine
from src.schema_drift import detect_schema_drift, save_schema_snapshot
from src.dashboard_ui import (
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
from src.app_shell import init_theme, inject_css, render_app_header
from src.auth_ui import render_auth_page
from src.validator import apply_validation_rules

st.set_page_config(
    page_title="DataSentinel",
    page_icon=_FAVICON if os.path.exists(_FAVICON) else "🔷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

authenticator, _auth_config = get_authenticator()
init_theme("dark")

# ══════════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════════
if st.session_state.get("authentication_status") is not True:
    inject_css(login=True)
    if "auth_page" not in st.session_state:
        st.session_state["auth_page"] = "login"
    render_auth_page()
    st.stop()

# ══════════════════════════════════════════════════════════════════
# APP SHELL
# ══════════════════════════════════════════════════════════════════
inject_css(login=False)

if "app_page" not in st.session_state:
    st.session_state["app_page"] = "dashboard"

current_user = st.session_state.get("username", "")
user_name = st.session_state.get("name", current_user)
user_email = st.session_state.get("email", "")
app_page = st.session_state.get("app_page", "dashboard")

# Paint shell first so Streamlit can replace the login DOM before Azure I/O
render_app_header(user_name, current_user, user_email, "main_theme", "main_logout")

if not st.session_state.get("_workspace_hydrated"):
    st.markdown(
        '<div class="ui-boot-panel" role="status">'
        '<div class="ui-boot-card"><p>Loading workspace…</p></div>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.session_state["_workspace_hydrated"] = True
    st.rerun()

config = load_config("config/pipeline_config.yaml")
trend_df = get_quality_trend(config, current_user)
has_history = not trend_df.empty


def _run_pipeline(uploaded_file):
    temp_path = resolve_path(os.path.join("data", "raw", uploaded_file.name))
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded **{uploaded_file.name}**")

    try:
        with st.spinner("Running validation pipeline…"):
            df, metadata = load_file(temp_path)
            profile = profile_dataframe(df, config)
            violations, summary = apply_validation_rules(df, config)
            clean_df, quarantined_df = quarantine_bad_rows(df, violations, config)
            row_pass_rate = (len(clean_df) / len(df) * 100.0) if len(df) > 0 else 100.0
            profile["overall_quality_score"] = round(min(profile["overall_quality_score"], row_pass_rate), 1)
            clean_report = verify_clean_data(clean_df, config)
            save_quarantine(quarantined_df, config, uploaded_file.name)
            save_clean_data(clean_df, config, uploaded_file.name)
            anomalies = detect_statistical_anomalies(df, profile, config)
            df_dtypes = {col: str(df[col].dtype) for col in df.columns}
            drift_result = detect_schema_drift(
                list(df.columns), df_dtypes, uploaded_file.name, current_user
            )
            save_schema_snapshot(
                list(df.columns), df_dtypes, config, uploaded_file.name, current_user
            )
            save_pipeline_run(
                metadata=metadata,
                profile=profile,
                validation_summary=summary,
                anomalies=anomalies,
                drift_result=drift_result,
                config=config,
                username=current_user,
            )
    except Exception as exc:
        st.error(f"Pipeline failed: {exc}")
        return

    section("Validation results", f"Quality score: {profile['overall_quality_score']}%")
    stat_grid([
        ("Quality score", f"{profile['overall_quality_score']}%", "Overall health"),
        ("Clean rows", clean_report["rows"], "Passed validation"),
        ("Quarantined", len(quarantined_df), "Failed rules"),
        ("Null cells", clean_report["null_cells"], "In clean output"),
    ])

    if clean_report["is_fully_clean"]:
        st.success("Dataset verified — no nulls in required columns.")
    else:
        st.warning(f"{clean_report['null_cells']} null cells remain in clean output.")

    section("Column health", "Null rates and status for every column")
    col_df = pd.DataFrame([
        {
            "Column": col,
            "Type": d["data_type"],
            "Null %": f"{round(d['null_percentage'] * 100, 1)}%",
            "Status": d["severity"],
        }
        for col, d in profile["column_profiles"].items()
    ])
    themed_table(col_df, max_rows=50)

    section("Cleaning summary")
    before_nulls = count_null_cells(df, config, required_only=True)
    stat_grid([
        ("Input rows", len(df), "Original dataset"),
        ("Nulls before", before_nulls, "Required columns"),
        ("Nulls after", clean_report["null_cells"], "After cleaning"),
        ("Removed", len(quarantined_df), "Quarantined rows"),
    ])

    if anomalies:
        section("Anomalies detected")
        themed_table(pd.DataFrame(anomalies)[["column", "value", "z_score", "column_mean"]], max_rows=50)

    # Always show quarantine after a run (empty state if none)
    quarantine_panel(config, live_df=quarantined_df)

    if drift_result.get("drift_detected"):
        st.warning("Schema drift detected since last upload.")
        if drift_result.get("added_columns"):
            st.write("Added:", drift_result["added_columns"])
        if drift_result.get("removed_columns"):
            st.write("Removed:", drift_result["removed_columns"])

    st.download_button(
        "Download clean CSV",
        clean_df.to_csv(index=False).encode("utf-8"),
        file_name=f"clean_{uploaded_file.name}",
        mime="text/csv",
        use_container_width=True,
        type="primary",
    )


def render_dashboard_page() -> None:
    # Top section: Upload dataset (Left) and Hero Command Center (Right) side-by-side
    upload_col, hero_col = st.columns([1, 1], gap="large")

    with upload_col:
        panel_start()
        uploaded_file = st.file_uploader(
            "Upload",
            type=["csv", "json", "xlsx"],
            label_visibility="collapsed",
            key="main_uploader",
        )

    with hero_col:
        dashboard_hero(has_data=has_history)

    # How it works is only shown when idle
    if uploaded_file is None:
        how_it_works()

    # Metrics grid
    if has_history:
        stat_grid([
            ("Total runs", len(trend_df), "Pipeline executions"),
            ("Avg quality", f"{trend_df['quality_score'].mean():.1f}%", "Across all runs"),
            ("Datasets", trend_df["file_name"].nunique(), "Unique files"),
            ("Anomalies", int(trend_df["anomalies_found"].sum()), "Detected total"),
        ])
    else:
        stat_grid([
            ("Total runs", "0", "Upload to begin"),
            ("Avg quality", "—", "No data yet"),
            ("Datasets", "0", "Unique files"),
            ("Anomalies", "0", "Detected"),
        ])

    # Idle dashboard quarantine panel (shows blank/empty state if no active validation run)
    if uploaded_file is None:
        quarantine_panel(config)

    if uploaded_file is not None:
        _run_pipeline(uploaded_file)


def render_analytics_page() -> None:
    page_intro("Analytics", "Quality trends across previous datasets and runs.")
    if not has_history:
        empty_state("No analytics yet", "Upload a dataset from Dashboard to build your first trend charts.")
        return

    try:
        selected = st.selectbox(
            "Filter by dataset",
            ["All datasets"] + sorted(trend_df["file_name"].unique()),
            key="analytics_dataset_filter",
        )
        chart_df = trend_df if selected == "All datasets" else trend_df[trend_df["file_name"] == selected]
        threshold = config.get("quality", {}).get("min_quality_score", 70)
        render_quality_trend_charts(chart_df, threshold=threshold, key_prefix="analytics_trend")
    except Exception as exc:
        st.warning(f"Could not load analytics: {exc}")


def render_history_page() -> None:
    page_intro("History", "Full pipeline run history for your workspace.")
    if not has_history:
        empty_state("No history yet", "Runs will appear here after you upload and validate a dataset.")
        return

    selected = st.selectbox(
        "Filter by dataset",
        ["All datasets"] + sorted(trend_df["file_name"].unique()),
        key="history_dataset_filter",
    )
    history_df = trend_df if selected == "All datasets" else trend_df[trend_df["file_name"] == selected]
    display = history_df.sort_values("run_timestamp", ascending=False).copy()
    themed_table(display, max_rows=100)


if app_page == "analytics":
    render_analytics_page()
elif app_page == "history":
    render_history_page()
else:
    render_dashboard_page()

page_footer()
