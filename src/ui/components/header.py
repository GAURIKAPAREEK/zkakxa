"""Enterprise application header."""

from __future__ import annotations

import html

import streamlit as st

from src.ui.components.theme_toggle import render_theme_toggle
from src.ui.logo import crystal_svg

NAV_PAGES = (
    ("dashboard", "Dashboard"),
    ("analytics", "Analytics"),
    ("history", "History"),
)


def _set_page(page: str) -> None:
    st.session_state["app_page"] = page
    st.session_state["mobile_menu_open"] = False
    st.rerun()


def _toggle_mobile_menu() -> None:
    st.session_state["mobile_menu_open"] = not st.session_state.get("mobile_menu_open", False)


def render_header(
    name: str,
    username: str,
    email: str,
    *,
    theme_key: str = "hdr_theme",
    logout_key: str = "hdr_logout",
    search_key: str = "hdr_search",
) -> None:
    del search_key, logout_key
    display_email = email or f"{username}@workspace.local"
    safe_name = name or "User"
    initials = "".join(p[0].upper() for p in safe_name.split()[:2]) or "U"
    active = st.session_state.get("app_page", "dashboard")
    short_name = safe_name.split()[0] if safe_name else "User"
    menu_open = st.session_state.get("mobile_menu_open", False)

    st.markdown('<div class="ui-hdr-anchor" aria-hidden="true"></div>', unsafe_allow_html=True)
    # Four groups on the same row: brand | nav (desktop) | actions (theme+profile+logout) | hamburger (mobile)
    # On mobile CSS hides only the desktop nav column and the logout button; theme + profile remain
    # visible next to the hamburger.
    brand_c, nav_c, actions_c, burger_c = st.columns(
        [1, 1.15, 1, 0.35],
        gap="small",
        vertical_alignment="center",
    )

    with brand_c:
        st.markdown(
            f'<div class="ui-brand">'
            f'<a class="ui-brand-link" href="#" aria-label="DataSentinel home">'
            f'{crystal_svg(30, animated=True, glow=True, interactive=True)}'
            f'<span class="ui-wordmark">DataSentinel</span></a></div>',
            unsafe_allow_html=True,
        )

    with nav_c:
        st.markdown('<div class="ui-nav-row" aria-hidden="true"></div>', unsafe_allow_html=True)
        cols = st.columns([1, 1, 1], gap="small", vertical_alignment="center")
        for col, (page_id, label) in zip(cols, NAV_PAGES):
            with col:
                is_active = active == page_id
                btn_type = "primary" if is_active else "secondary"
                if st.button(label, key=f"nav_{page_id}", type=btn_type, use_container_width=False):
                    if not is_active:
                        _set_page(page_id)

    with actions_c:
        st.markdown('<div class="ui-hdr-actions" aria-hidden="true"></div>', unsafe_allow_html=True)
        # Required order: Profile | Theme | Logout — profile first, then sun/moon
        profile_c, theme_c, logout_c = st.columns(
            [1.45, 0.55, 1.0],
            gap="small",
            vertical_alignment="center",
        )
        with profile_c:
            with st.popover(short_name, key="hdr_profile", use_container_width=False):
                st.markdown(
                    f"""
<div class="ui-profile-card">
  <div class="ui-profile-avatar">{html.escape(initials)}</div>
  <div class="ui-profile-body">
    <p class="ui-profile-label">Name</p>
    <p class="ui-profile-name">{html.escape(safe_name)}</p>
    <p class="ui-profile-label">Email</p>
    <p class="ui-profile-meta">{html.escape(display_email)}</p>
    <p class="ui-profile-label">Username</p>
    <p class="ui-profile-meta">@{html.escape(username or "user")}</p>
    <div class="ui-profile-chips">
      <span>Workspace member</span>
      <span>Quality pipeline access</span>
    </div>
  </div>
</div>
""",
                    unsafe_allow_html=True,
                )
                # Mobile-only logout inside profile popover (desktop logout button is separate)
                if st.button("Logout", key="ui_logout_btn_profile", type="secondary", use_container_width=True):
                    from src.auth import logout_user

                    logout_user()
        import streamlit as st
        with theme_c:
             if not st.session_state.get("is_mobile", False):
                  render_theme_toggle(theme_key)
        with logout_c:
            if st.button("Logout", key="ui_logout_btn", type="secondary", help="Log out"):
                from src.auth import logout_user

                logout_user()

    with burger_c:
        st.markdown('<div class="ui-hdr-burger" aria-hidden="true"></div>', unsafe_allow_html=True)
        burger_label = "✕" if menu_open else "☰"
        if st.button(burger_label, key="ui_burger_btn", type="secondary", help="Menu"):
            _toggle_mobile_menu()
            st.rerun()

    # Mobile dropdown panel — only rendered when open. Contains the 3 nav links
    # PLUS a 4th "Change theme" option (sun / moon) so phone users can toggle
    # the theme from inside the hamburger. Profile + logout stay accessible via
    # the profile popover in the header row.
    if menu_open:
        st.markdown('<div class="ui-mobile-panel" aria-hidden="true"></div>', unsafe_allow_html=True)
        for page_id, label in NAV_PAGES:
            is_active = active == page_id
            btn_type = "primary" if is_active else "secondary"
            if st.button(
                label,
                key=f"mnav_{page_id}",
                type=btn_type,
                use_container_width=True,
            ):
                if not is_active:
                    _set_page(page_id)
       st.divider()
       st.markdown("### Appearance")
       render_theme_toggle("mobile_theme_toggle")

        # 4th option — Change theme (destination icon: sun for light, moon for dark)
        is_dark = st.session_state.get("theme", "dark") == "dark"
        theme_icon = "☀️" if is_dark else "🌙"
        if st.button(
            f"Change theme  {theme_icon}",
            key="mnav_theme",
            type="secondary",
            use_container_width=True,
            help="Switch to light theme" if is_dark else "Switch to dark theme",
        ):
            st.session_state.theme = "light" if is_dark else "dark"
            st.session_state["mobile_menu_open"] = False
            st.rerun()
