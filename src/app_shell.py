"""App shell — theme init, CSS injection, header."""

from __future__ import annotations

import streamlit as st

from src.ui.components.header import render_header
from src.ui.components.theme_toggle import render_theme_toggle
from src.ui.stylesheet import build_global_css


def init_theme(default: str = "dark") -> None:
    if "theme" not in st.session_state:
        st.session_state.theme = default


import importlib
import src.ui.stylesheet

def inject_css(*, login: bool = False) -> None:
    importlib.reload(src.ui.stylesheet)
    css = src.ui.stylesheet.build_global_css(login=login)
    if hasattr(st, "html"):
        st.html(css)
    else:
        st.markdown(css, unsafe_allow_html=True)


def render_app_header(
    name: str,
    username: str,
    email: str = "",
    theme_key: str = "hdr_theme",
    logout_key: str = "hdr_logout",
) -> None:
    import importlib
    import src.ui.components.header
    importlib.reload(src.ui.components.header)
    src.ui.components.header.render_header(name, username, email, theme_key=theme_key, logout_key=logout_key)


def toggle_theme(key: str) -> None:
    render_theme_toggle(key)


def render_sidebar(_name: str) -> None:
    pass
