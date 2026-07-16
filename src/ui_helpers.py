"""Lightweight UI helpers."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from src.ui.components.theme_toggle import render_theme_toggle


def render_theme_switch(key: str) -> None:
    render_theme_toggle(key)


def toggle_theme(key: str) -> None:
    render_theme_toggle(key)


def suppress_enter_hint() -> None:
    components.html(
        """
        <script>
        const doc = window.parent.document;
        function patch() {
            doc.querySelectorAll('input[type="text"],input[type="password"],input[type="email"]').forEach(el => {
                el.setAttribute("autocomplete", "off");
            });
            doc.querySelectorAll('[data-testid="InputInstructions"]').forEach(el => {
                el.style.display = "none";
            });
        }
        patch();
        new MutationObserver(patch).observe(doc.body, { childList: true, subtree: true });
        </script>
        """,
        height=0,
        width=0,
    )
