# ============================================================
# SAVE THIS FILE AS: src/ui/components/auth.py
# (the UI pages file — login/signup/forgot/reset screens)
# ============================================================
"""Authentication pages — unified layout for login, signup, forgot, reset."""

from __future__ import annotations

import streamlit as st

from src.auth import (
    authenticate_user,
    is_cloud_deployment,
    load_auth_config,
    register_user,
    request_password_reset,
    reset_password_with_token,
    validate_signup_fields,
)
from src.ui.logo import brand_html, crystal_svg
from src.ui_helpers import suppress_enter_hint


def _page() -> str:
    if st.query_params.get("reset_token"):
        return "reset"
    return st.session_state.get("auth_page", "login")


def _goto(page: str) -> None:
    st.session_state["auth_page"] = page
    if page != "reset":
        st.query_params.clear()


def _head(title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="ui-auth-card-head"><h2>{title}</h2><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def _error(msg: str) -> None:
    st.markdown(f'<p class="ui-field-error" role="alert">{msg}</p>', unsafe_allow_html=True)


def _login() -> None:
    if st.session_state.pop("show_password_changed_toast", False):
        st.toast("Password changed successfully!")
    _head("Welcome back", "Sign in to your workspace to continue.")
    suppress_enter_hint()
    username = st.text_input("Username", key="login_username", placeholder="your_username")
    password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
    remember, forgot = st.columns([1.6, 1], vertical_alignment="center")
    with remember:
        st.checkbox("Remember me", key="login_remember", value=True)
    with forgot:
        if st.button("Forgot password?", key="ui_forgot_link", type="secondary"):
            _goto("forgot")
            st.rerun()
    loading = st.session_state.get("auth_loading", False)
    if st.button("Signing in…" if loading else "Sign in", key="login_submit", type="primary", use_container_width=True, disabled=loading):
        if not username.strip() or not password:
            st.session_state["auth_error"] = "Enter your username and password."
        else:
            st.session_state["auth_loading"] = True
            st.session_state.pop("auth_error", None)
            st.session_state.pop("_auth_paint_done", None)
            st.rerun()

    if st.session_state.get("auth_error"):
        _error(st.session_state["auth_error"])
    if st.session_state.pop("signup_success", None):
        st.success("Account created successfully! Sign in with your credentials below.")
        st.markdown(
            '<div style="margin:-4px 0 14px 0;padding:10px 14px;background:var(--ui-accent-soft);'
            'border:1px solid var(--ui-primary-border);border-radius:10px;text-align:center;">'
            '<span style="color:var(--ui-text);font-size:13px;">Sign in now </span>'
            '<a href="?" target="_self" style="color:var(--ui-primary);font-weight:600;text-decoration:none;">'
            ' Go to Login</a>'
            '</div>',
            unsafe_allow_html=True,
        )
    if st.button("Create an account", key="goto_signup", type="secondary", use_container_width=True, disabled=loading):
        _goto("signup")
        st.rerun()


def _finish_login_if_pending() -> None:
    """Verify credentials after the loading veil has already been painted."""
    if not st.session_state.get("auth_loading"):
        return
    if st.session_state.get("authentication_status"):
        st.session_state["auth_loading"] = False
        st.session_state.pop("_auth_paint_done", None)
        return
    if _page() != "login":
        st.session_state["auth_loading"] = False
        st.session_state.pop("_auth_paint_done", None)
        return

    pending_user = (st.session_state.get("login_username") or "").strip()
    pending_pw = st.session_state.get("login_password") or ""
    ok, value = authenticate_user(pending_user, pending_pw)
    st.session_state["auth_loading"] = False
    st.session_state.pop("_auth_paint_done", None)
    if ok:
        st.session_state.update({
            "authentication_status": True,
            "name": value,
            "username": pending_user,
            "email": load_auth_config().get("credentials", {}).get("usernames", {}).get(pending_user, {}).get("email", ""),
            "app_page": "dashboard",
            "_workspace_hydrated": False,
        })
        st.session_state.pop("auth_error", None)
        st.rerun()
    st.session_state["auth_error"] = value
    st.rerun()


def _signup() -> None:
    _head("Create your account", "Start monitoring data quality in minutes.")
    suppress_enter_hint()
    if is_cloud_deployment():
        st.info("Account creation is managed by your administrator.")
        if st.button("Back to sign in", key="signup_back_cloud", use_container_width=True):
            _goto("login")
            st.rerun()
        return

    val_name = st.session_state.get("signup_name", "")
    val_email = st.session_state.get("signup_email", "")
    val_username = st.session_state.get("signup_username", "")
    val_password = st.session_state.get("signup_password", "")
    errors = validate_signup_fields(val_name, val_email, val_username, val_password)

    name = st.text_input("Full name", key="signup_name", placeholder="Jane Doe")
    if val_name and "name" in errors:
        _error(errors["name"])

    email = st.text_input("Email", key="signup_email", placeholder="you@company.com")
    if val_email and "email" in errors:
        _error(errors["email"])

    username = st.text_input("Username", key="signup_username", placeholder="jane_doe")
    if val_username and "username" in errors:
        _error(errors["username"])

    password = st.text_input("Password", type="password", key="signup_password", placeholder="8+ chars, number & symbol")
    if val_password and "password" in errors:
        _error(errors["password"])

    loading = st.session_state.get("auth_loading", False)
    submit_disabled = loading or bool(errors) or not (val_name.strip() and val_email.strip() and val_username.strip() and val_password)

    if st.button("Creating account…" if loading else "Create account", key="signup_submit", type="primary", use_container_width=True, disabled=submit_disabled):
        st.session_state["auth_loading"] = True
        ok, message = register_user(name, email, username, password)
        st.session_state["auth_loading"] = False
        if ok:
            st.session_state["signup_success"] = True
            _goto("login")
            st.rerun()
        st.session_state["auth_error"] = message
    if st.session_state.get("auth_error") and _page() == "signup":
        _error(st.session_state["auth_error"])
    if st.button("Already have an account? Sign in", key="goto_login", type="secondary", use_container_width=True):
        st.session_state.pop("auth_error", None)
        _goto("login")
        st.rerun()


def _forgot() -> None:
    _head("Reset your password", "We'll email you a secure link to choose a new password.")
    suppress_enter_hint()
    email = st.text_input("Registered email", key="forgot_email", placeholder="you@company.com")
    loading = st.session_state.get("auth_loading", False)
    if st.button("Sending…" if loading else "Send reset link", key="forgot_submit", type="primary", use_container_width=True, disabled=loading):
        st.session_state["auth_loading"] = True
        ok, message = request_password_reset(email)
        st.session_state["auth_loading"] = False
        if ok:
            st.session_state["forgot_success"] = message
            st.session_state.pop("auth_error", None)
        else:
            st.session_state["auth_error"] = message
    if st.session_state.get("forgot_success"):
        st.success(st.session_state["forgot_success"])
    if st.session_state.get("auth_error") and _page() == "forgot":
        _error(st.session_state["auth_error"])
    if st.button("← Back to sign in", key="forgot_back", type="secondary", use_container_width=True):
        st.session_state.pop("auth_error", None)
        st.session_state.pop("forgot_success", None)
        _goto("login")
        st.rerun()


def _reset() -> None:
    token = st.query_params.get("reset_token", "")
    _head("Choose a new password", "Enter a strong password for your account.")
    if not token:
        st.error("Invalid or missing reset link.")
        if st.button("Back to sign in", key="reset_invalid_back", use_container_width=True):
            st.query_params.clear()
            _goto("login")
            st.rerun()
        return
    pw = st.text_input("New password", type="password", key="reset_password", placeholder="••••••••")
    confirm = st.text_input("Confirm password", type="password", key="reset_confirm", placeholder="••••••••")
    if confirm and pw != confirm:
        _error("Passwords do not match.")
    loading = st.session_state.get("auth_loading", False)
    if st.button("Updating…" if loading else "Update password", key="reset_submit", type="primary", use_container_width=True, disabled=loading):
        if pw != confirm:
            st.session_state["auth_error"] = "Passwords do not match."
        else:
            st.session_state["auth_loading"] = True
            ok, message = reset_password_with_token(token, pw)
            st.session_state["auth_loading"] = False
            if ok:
                st.session_state["reset_success"] = True
                st.session_state.pop("auth_error", None)
            else:
                st.session_state["auth_error"] = message
    if st.session_state.get("auth_error") and _page() == "reset":
        _error(st.session_state["auth_error"])
    if st.session_state.get("reset_success"):
        st.success("Password updated. Sign in with your new password.")
        st.session_state["show_password_changed_toast"] = True
        st.query_params.clear()
        st.session_state.pop("reset_success", None)
        _goto("login")
        st.rerun()
    if st.button("← Back to sign in", key="reset_back", type="secondary", use_container_width=True):
        st.query_params.clear()
        _goto("login")
        st.rerun()


def _brand_panel() -> None:
    st.markdown(
        f"""
<div class="ui-auth-brand">
  <div class="ui-auth-brand-logo ui-auth-enter ui-auth-enter--1">{brand_html("md", animated=True, glow=True, light_text=True)}</div>
  <h1 class="ui-auth-headline ui-auth-enter ui-auth-enter--2">Turning Every Dataset into a Trusted Asset.</h1>
  <p class="ui-auth-lede ui-auth-enter ui-auth-enter--3">
    DataSentinel automates validation, profiling, and anomaly detection — turning raw files 
    into clean, trusted data in minutes.
  </p>

  <div class="ui-auth-features" role="list">
    <div class="ui-auth-feat ui-auth-enter ui-auth-enter--5" role="listitem">
      <strong>Ingest</strong>
      <span>Load datasets securely after sign-in.</span>
    </div>
    <div class="ui-auth-feat ui-auth-enter ui-auth-enter--6" role="listitem">
      <strong>Validate</strong>
      <span>Null checks, type rules &amp; scoring.</span>
    </div>
    <div class="ui-auth-feat ui-auth-enter ui-auth-enter--7" role="listitem">
      <strong>Quarantine</strong>
      <span>Isolate bad rows; export clean file.</span>
    </div>
    <div class="ui-auth-feat ui-auth-enter ui-auth-enter--8" role="listitem">
      <strong>Monitor</strong>
      <span>Private run history &amp; trend analytics.</span>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_auth_page() -> None:
    st.markdown(
        '<div class="ui-auth-anchor" aria-hidden="true"></div>'
        '<div class="ui-auth-texture" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.08, 1], gap="large", vertical_alignment="center")
    with left:
        _brand_panel()
    with right:
        st.markdown('<div class="ui-auth-form-shell">', unsafe_allow_html=True)
        page = _page()
        if page == "login":
            _login()
        elif page == "signup":
            _signup()
        elif page == "forgot":
            _forgot()
        else:
            _reset()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("auth_loading"):
        st.markdown(
            f'<div class="ui-loading" role="status"><div class="ui-loading-card">'
            f'{crystal_svg("xl", animated=True, glow=True)}'
            f'<p style="margin:0;color:var(--ui-text-2)">Signing you in…</p></div></div>',
            unsafe_allow_html=True,
        )
        # First loading pass only paints the veil; auth runs on the following pass
        # so the previous frame stays covered during password verification.
        if not st.session_state.get("_auth_paint_done"):
            st.session_state["_auth_paint_done"] = True
            st.rerun()
        _finish_login_if_pending()
    st.markdown(
        '<div class="ui-auth-foot">DataSentinel · Enterprise data quality platform</div>',
        unsafe_allow_html=True,
    )
    from src.app_shell import inject_css

    inject_css(login=True)
