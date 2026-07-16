"""Design tokens — single source of truth for the DataSentinel UI."""

from __future__ import annotations

SP = {4: 4, 8: 8, 12: 12, 16: 16, 20: 20, 24: 24, 32: 32, 40: 40, 48: 48, 64: 64}
RADIUS = {10: 10, 12: 12, 14: 14, 18: 18, 24: 24}

BTN_HEIGHT = 48
BTN_PAD_X = 20
INPUT_HEIGHT = 48
INPUT_PAD_X = 16
CONTAINER_MAX = 1600
PAGE_GUTTER_MIN = 20
PAGE_GUTTER_MAX = 32
SPACE = SP

TYPE = {
    "display": 40,
    "h1": 32,
    "h2": 24,
    "h3": 18,
    "body": 15,
    "small": 14,
    "caption": 12,
}

DURATION = "200ms"
EASING = "cubic-bezier(0.4, 0, 0.2, 1)"
SPRING = "cubic-bezier(0.34, 1.5, 0.64, 1)"

# Ink + frost: dark ambient surfaces with soft light panels (not flat black cells)
THEMES: dict[str, dict[str, str]] = {
    "light": {
        "--ui-bg": "#E8EEF6",
        "--ui-surface": "#F8FAFC",
        "--ui-card": "#FFFFFF",
        "--ui-elevated": "#FFFFFF",
        "--ui-muted": "#Eef2F7",
        "--ui-input": "#FFFFFF",
        "--ui-glass": "rgba(255,255,255,0.88)",
        "--ui-text": "#0B1220",
        "--ui-text-2": "#334155",
        "--ui-text-3": "#475569",
        "--ui-border": "rgba(15,23,42,0.10)",
        "--ui-border-strong": "rgba(15,23,42,0.18)",
        "--ui-primary": "#0F6E8C",
        "--ui-primary-hover": "#0A5670",
        "--ui-secondary": "#1B4F72",
        "--ui-accent": "#C45C26",
        "--ui-accent-soft": "rgba(15,110,140,0.12)",
        "--ui-success": "#0F9F6E",
        "--ui-success-soft": "rgba(15,159,110,0.12)",
        "--ui-danger": "#C43C4A",
        "--ui-danger-soft": "rgba(196,60,74,0.10)",
        "--ui-gradient": "linear-gradient(135deg,#0F6E8C 0%,#1B4F72 52%,#C45C26 100%)",
        "--ui-mesh": (
            "radial-gradient(ellipse 70% 50% at 12% 8%,rgba(15,110,140,0.16),transparent 55%),"
            "radial-gradient(ellipse 55% 45% at 88% 92%,rgba(196,92,38,0.10),transparent 60%),"
            "linear-gradient(180deg,#E8EEF6 0%,#F4F7FB 100%)"
        ),
        "--ui-shadow-sm": "0 1px 2px rgba(15,23,42,0.05)",
        "--ui-shadow-md": "0 8px 28px rgba(15,23,42,0.08)",
        "--ui-shadow-lg": "0 18px 48px rgba(15,23,42,0.12)",
        "--ui-focus": "0 0 0 3px rgba(15,110,140,0.22)",
        "--ui-chart-bg": "rgba(0,0,0,0)",
        "--ui-chart-text": "#0B1220",
        "--ui-chart-muted": "#334155",
        "--ui-chart-grid": "rgba(15,23,42,0.14)",
        "--ui-chart-colors": "#0F6E8C,#C45C26,#1B4F72,#0F9F6E,#B45309,#475569",
        "--ui-table": "#FFFFFF",
        "--ui-table-head": "#Eef2F7",
        "--ui-table-row": "#FFFFFF",
        "--ui-table-row-alt": "#F7FAFC",
        "--ui-toggle-track": "linear-gradient(135deg,#E2E8F0 0%,#CBD5E1 100%)",
        "--ui-toggle-knob": "#FFFFFF",
        "--ui-toggle-icon": "#0B1220",
    },
    "dark": {
        "--ui-bg": "#0A1220",
        "--ui-surface": "#121C2E",
        "--ui-card": "#162236",
        "--ui-elevated": "#152033",
        "--ui-muted": "#1A2740",
        "--ui-input": "#1A2740",
        "--ui-glass": "rgba(18,28,46,0.82)",
        "--ui-text": "#F1F5F9",
        "--ui-text-2": "#CBD5E1",
        "--ui-text-3": "#94A3B8",
        "--ui-border": "rgba(148,163,184,0.18)",
        "--ui-border-strong": "rgba(148,163,184,0.32)",
        "--ui-primary": "#38BDF8",
        "--ui-primary-hover": "#0EA5E9",
        "--ui-secondary": "#67E8F9",
        "--ui-accent": "#F0A06A",
        "--ui-accent-soft": "rgba(56,189,248,0.14)",
        "--ui-success": "#34D399",
        "--ui-success-soft": "rgba(52,211,153,0.14)",
        "--ui-danger": "#FB7185",
        "--ui-danger-soft": "rgba(251,113,133,0.14)",
        "--ui-gradient": "linear-gradient(135deg,#0EA5E9 0%,#0369A1 45%,#C45C26 100%)",
        "--ui-mesh": (
            "radial-gradient(ellipse 70% 55% at 15% 0%,rgba(14,165,233,0.22),transparent 55%),"
            "radial-gradient(ellipse 50% 40% at 90% 85%,rgba(196,92,38,0.14),transparent 55%),"
            "linear-gradient(165deg,#070B14 0%,#0A1220 45%,#0E1A2E 100%)"
        ),
        "--ui-shadow-sm": "0 1px 2px rgba(0,0,0,0.35)",
        "--ui-shadow-md": "0 8px 28px rgba(0,0,0,0.40)",
        "--ui-shadow-lg": "0 20px 56px rgba(0,0,0,0.50)",
        "--ui-focus": "0 0 0 3px rgba(56,189,248,0.28)",
        "--ui-chart-bg": "rgba(0,0,0,0)",
        "--ui-chart-text": "#E2E8F0",
        "--ui-chart-muted": "#94A3B8",
        "--ui-chart-grid": "rgba(148,163,184,0.16)",
        "--ui-chart-colors": "#38BDF8,#F0A06A,#67E8F9,#34D399,#FBBF24,#FB7185",
        "--ui-table": "#162236",
        "--ui-table-head": "#1A2740",
        "--ui-table-row": "#162236",
        "--ui-table-row-alt": "#132033",
        "--ui-toggle-track": "linear-gradient(135deg,#0EA5E9 0%,#0369A1 100%)",
        "--ui-toggle-knob": "#FFFFFF",
        "--ui-toggle-icon": "#FFFFFF",
    },
}


def get_theme_name() -> str:
    import streamlit as st

    return st.session_state.get("theme", "dark")


def get_vars() -> dict[str, str]:
    return THEMES[get_theme_name()]


def get_chart_colors() -> list[str]:
    return get_vars()["--ui-chart-colors"].split(",")
