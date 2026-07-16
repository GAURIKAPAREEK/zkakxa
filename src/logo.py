"""Backward-compatible logo shim — use src.ui.logo."""

from src.ui.logo import LOGO_CSS as LOGO_ANIMATION_CSS
from src.ui.logo import brand_html as logo_brand_html
from src.ui.logo import crystal_svg as logo_svg

__all__ = ["LOGO_ANIMATION_CSS", "logo_brand_html", "logo_email_html", "logo_svg", "render_logo", "render_logo_brand"]


def logo_email_html(size: int = 40) -> str:
    return logo_svg(size, animated=False, glow=True)


def render_logo(**kwargs) -> None:
    import streamlit as st
    st.markdown(logo_svg(**kwargs), unsafe_allow_html=True)


def render_logo_brand(**kwargs) -> None:
    import streamlit as st
    st.markdown(logo_brand_html(**kwargs), unsafe_allow_html=True)
