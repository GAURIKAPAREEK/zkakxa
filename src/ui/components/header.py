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
        # Required order: Theme | Profile | Logout — tight auto widths
        theme_c, profile_c, logout_c = st.columns(
            [0.55, 1.45, 1.0],
            gap="small",
            vertical_alignment="center",
        )
        with theme_c:
            render_theme_toggle(theme_key)
        with profile_c:
            with st.popover(short_name, key="hdr_profile_v7", use_container_width=False):
                profile_html = (
                    f'<div class="ui-profile-card" style="display:flex!important;flex-direction:row!important;align-items:flex-start!important;gap:16px!important;padding:8px 4px 4px!important;min-width:300px!important;">'
                    f'<div class="ui-profile-avatar" style="width:48px!important;height:48px!important;border-radius:14px!important;background:var(--ui-gradient)!important;color:#ffffff!important;display:flex!important;align-items:center!important;justify-content:center!important;font-weight:700!important;font-size:18px!important;flex-shrink:0!important;margin-top:2px!important;box-shadow:0 4px 12px rgba(0,0,0,0.2)!important;">{html.escape(initials)}</div>'
                    f'<div class="ui-profile-body" style="flex:1!important;min-width:0!important;">'
                    f'<table style="width:100%!important;border-collapse:collapse!important;margin:0!important;padding:0!important;border:none!important;background:transparent!important;">'
                    f'<tr style="height:26px!important;background:transparent!important;">'
                    f'<td style="width:82px!important;font-size:11px!important;font-weight:700!important;text-transform:uppercase!important;color:var(--ui-text-3)!important;padding:2px 0!important;vertical-align:middle!important;border:none!important;background:transparent!important;">Name:</td>'
                    f'<td style="font-size:15px!important;font-weight:700!important;color:var(--ui-text)!important;padding:2px 0!important;vertical-align:middle!important;border:none!important;background:transparent!important;">{html.escape(safe_name)}</td>'
                    f'</tr>'
                    f'<tr style="height:26px!important;background:transparent!important;">'
                    f'<td style="width:82px!important;font-size:11px!important;font-weight:700!important;text-transform:uppercase!important;color:var(--ui-text-3)!important;padding:2px 0!important;vertical-align:middle!important;border:none!important;background:transparent!important;">Email:</td>'
                    f'<td style="font-size:13px!important;font-weight:600!important;color:var(--ui-text)!important;padding:2px 0!important;vertical-align:middle!important;word-break:break-all!important;border:none!important;background:transparent!important;">{html.escape(display_email)}</td>'
                    f'</tr>'
                    f'<tr style="height:26px!important;background:transparent!important;">'
                    f'<td style="width:82px!important;font-size:11px!important;font-weight:700!important;text-transform:uppercase!important;color:var(--ui-text-3)!important;padding:2px 0!important;vertical-align:middle!important;border:none!important;background:transparent!important;">Username:</td>'
                    f'<td style="font-size:13px!important;font-weight:600!important;color:var(--ui-primary)!important;padding:2px 0!important;vertical-align:middle!important;border:none!important;background:transparent!important;">@{html.escape(username or "user")}</td>'
                    f'</tr>'
                    f'</table>'
                    f'<div class="ui-profile-chips" style="display:flex!important;flex-wrap:wrap!important;gap:6px!important;margin-top:12px!important;padding-top:10px!important;border-top:1px solid var(--ui-border)!important;">'
                    f'<span>Workspace member</span>'
                    f'<span>Quality pipeline access</span>'
                    f'</div>'
                    f'</div>'
                    f'</div>'
                )
                if hasattr(st, "html"):
                    st.html(profile_html)
                else:
                    st.markdown(profile_html, unsafe_allow_html=True)
                if st.session_state.get("confirm_delete_desktop"):
                    st.warning("⚠️ Delete account permanently? This cannot be undone.")
                    col1, col2, col3, col4 = st.columns([0.5, 2, 2, 0.5])
                    with col2:
                        if st.button("Yes, delete", key="confirm_delete_desktop_btn", type="primary"):
                            from src.auth import delete_user_permanently
                            delete_user_permanently(username)
                    with col3:
                        if st.button("Cancel", key="cancel_delete_desktop_btn", type="primary"):
                            st.session_state.confirm_delete_desktop = False
                            st.rerun()
                else:
                    if st.button("Delete account permanently", key="hdr_delete_account_btn", type="primary"):
                        st.session_state.confirm_delete_desktop = True
                        st.rerun()

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

    # Mobile dropdown panel — only rendered when open. Contains ONLY the 3 nav links.
    # Profile info, theme toggle, and logout stay in the header row (theme + profile visible on
    # mobile; logout accessible from inside the profile popover).
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

        # 4th option: Theme toggle
        is_dark = st.session_state.get("theme", "dark") == "dark"
        theme_btn_label = "Change theme ☀️" if is_dark else "Change theme 🌙"
        if st.button(
            theme_btn_label,
            key="mnav_theme_toggle",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state.theme = "light" if is_dark else "dark"
            st.rerun()

        # 5th option: Logout
        if st.button(
            "Logout",
            key="mnav_logout_btn",
            type="secondary",
            use_container_width=True,
        ):
            from src.auth import logout_user
            logout_user()
