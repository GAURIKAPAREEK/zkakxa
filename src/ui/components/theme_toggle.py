from __future__ import annotations

import streamlit as st


def render_theme_toggle(key: str = "ui_theme_toggle") -> None:
    """Shared ghost theme control: dark→sun, light→moon (destination icon)."""
    is_dark = st.session_state.get("theme", "dark") == "dark"
    tip = "Switch to light theme" if is_dark else "Switch to dark theme"
    # Destination icon: sun enters light, moon enters dark
    label = "☀️" if is_dark else "🌙"
    if st.button(label, key=key, type="secondary", help=tip):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()
