# ============================================================
# SAVE THIS FILE AS: src/auth.py
# (the CORE logic file — SMTP, database, password hashing)
# ============================================================
import os
import re
import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from urllib.parse import urlencode

import bcrypt
import sqlalchemy
import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from src.paths import resolve_path

AUTH_CONFIG_PATH = resolve_path("config/auth_config.yaml")
RESET_TOKEN_MINUTES = 15


@st.cache_resource
def _get_db_engine():
    """Connect to the persistent Supabase/Postgres database, if configured."""
    try:
        if hasattr(st, "secrets") and "database" in st.secrets:
            db_url = st.secrets["database"]["url"]
            return sqlalchemy.create_engine(db_url, pool_pre_ping=True)
    except (FileNotFoundError, KeyError, TypeError):
        pass
    return None


def _table_columns(conn, table_name: str) -> set[str]:
    dialect = conn.dialect.name
    if dialect == "sqlite":
        rows = conn.execute(sqlalchemy.text(f"PRAGMA table_info({table_name})")).fetchall()
        return {row[1] for row in rows}
    rows = conn.execute(
        sqlalchemy.text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name = :table"
        ),
        {"table": table_name},
    ).fetchall()
    return {row[0] for row in rows}


@st.cache_resource
def _ensure_users_table_once(engine):
    """Run schema creation/migration only once per app process (not on every rerun)."""
    create_query = """
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text(create_query))
        conn.commit()
        columns = _table_columns(conn, "users")
        if "reset_token" not in columns:
            conn.execute(sqlalchemy.text("ALTER TABLE users ADD COLUMN reset_token TEXT"))
        if "reset_expiry" not in columns:
            conn.execute(sqlalchemy.text("ALTER TABLE users ADD COLUMN reset_expiry TEXT"))
        conn.commit()
    return True


def _ensure_users_table(engine):
    _ensure_users_table_once(engine)


def _load_from_secrets():
    """Legacy: static credentials block in secrets (kept for backward compatibility)."""
    try:
        if hasattr(st, "secrets") and "auth" in st.secrets:
            auth = st.secrets["auth"]
            return {
                "credentials": dict(auth["credentials"]),
                "cookie": dict(auth["cookie"]),
            }
    except (FileNotFoundError, KeyError, TypeError):
        pass
    return None


@st.cache_data(ttl=5)
def _fetch_users_from_db(_engine) -> dict:
    with _engine.connect() as conn:
        rows = conn.execute(
            sqlalchemy.text("SELECT username, name, email, password FROM users")
        ).fetchall()
    return {
        row[0]: {"name": row[1], "email": row[2], "password": row[3]}
        for row in rows
    }


def load_auth_config():
    """Load auth from the database if configured, else local YAML or secrets."""
    engine = _get_db_engine()
    if engine is not None:
        _ensure_users_table(engine)
        usernames = _fetch_users_from_db(engine)
        return {
            "credentials": {"usernames": usernames},
            "cookie": {
                "name": "datasentinel_auth",
                "key": "datasentinel_secret_key_change_this",
                "expiry_days": 7,
            },
        }

    secrets_config = _load_from_secrets()
    if secrets_config is not None:
        return secrets_config

    os.makedirs(os.path.dirname(AUTH_CONFIG_PATH), exist_ok=True)
    if not os.path.exists(AUTH_CONFIG_PATH):
        default_config = {
            "credentials": {"usernames": {}},
            "cookie": {
                "name": "datasentinel_auth",
                "key": "datasentinel_secret_key_change_this",
                "expiry_days": 7,
            },
        }
        with open(AUTH_CONFIG_PATH, "w") as f:
            yaml.dump(default_config, f)

    with open(AUTH_CONFIG_PATH) as f:
        config = yaml.load(f, Loader=SafeLoader)
    return config


def save_auth_config(config):
    """Only used for the local-YAML fallback path; DB writes happen in register_user."""
    if _get_db_engine() is not None:
        return True
    if _load_from_secrets() is not None:
        return False
    with open(AUTH_CONFIG_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    return True


def is_cloud_deployment():
    return _load_from_secrets() is not None


def hash_password(plain_password: str) -> str:
    """Hash password with bcrypt (compatible with streamlit-authenticator)."""
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()


def _username_exists(username: str) -> bool:
    engine = _get_db_engine()
    if engine is not None:
        with engine.connect() as conn:
            existing = conn.execute(
                sqlalchemy.text("SELECT 1 FROM users WHERE username = :u"),
                {"u": username},
            ).fetchone()
        return existing is not None
    config = load_auth_config()
    return username in config["credentials"]["usernames"]


def register_user(
    name: str,
    email: str,
    username: str,
    password: str,
) -> tuple[bool, str]:
    """Validate and persist a new account (to the database if configured, else local YAML)."""
    name = (name or "").strip()
    email = (email or "").strip()
    username = (username or "").strip()
    password = password or ""

    if not all([name, email, username, password]):
        return False, "All fields are required."

    if not re.fullmatch(r"[A-Za-z ]+", name):
        return False, "Full name can only contain alphabets."

    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        return False, "Username can only contain letters, numbers, and underscores."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if not re.search(r"\d", password) or not re.search(
        r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password
    ):
        return False, "Password must contain at least one number and one special symbol."

    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Enter a valid email address."

    if _username_exists(username):
        return False, "Username already exists. Choose another or sign in."

    hashed = hash_password(password)
    engine = _get_db_engine()
    if engine is not None:
        _ensure_users_table(engine)
        with engine.connect() as conn:
            conn.execute(
                sqlalchemy.text(
                    "INSERT INTO users (username, name, email, password) VALUES (:u, :n, :e, :p)"
                ),
                {"u": username, "n": name, "e": email, "p": hashed},
            )
            conn.commit()
        return True, "Account created. Sign in with your username and password."

    config = load_auth_config()
    usernames = config["credentials"]["usernames"]
    usernames[username] = {"name": name, "email": email, "password": hashed}
    if save_auth_config(config):
        return True, "Account created. Sign in with your username and password."
    return False, "Could not save account. Contact your administrator."


def get_authenticator():
    config = load_auth_config()
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )
    return authenticator, config


def validate_signup_fields(name: str, email: str, username: str, password: str) -> dict:
    """Live validation for signup fields."""
    errors = {}
    name = (name or "").strip()
    email = (email or "").strip()
    username = (username or "").strip()
    password = password or ""

    if name and not re.fullmatch(r"[A-Za-z ]+", name):
        errors["name"] = "Full name can only contain alphabets."

    if username:
        if len(username) < 3:
            errors["username"] = "Username must be at least 3 characters."
        elif not re.fullmatch(r"[A-Za-z0-9_]+", username):
            errors["username"] = "Username can only contain letters, numbers, and underscores."
        elif _username_exists(username):
            errors["username"] = "Username already exists. Choose another or sign in."

    if password:
        if len(password) < 6:
            errors["password"] = "Password must be at least 6 characters."
        elif not re.search(r"\d", password) or not re.search(
            r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password
        ):
            errors["password"] = "Password must contain at least one number and one special symbol."

    if email and ("@" not in email or "." not in email.split("@")[-1]):
        errors["email"] = "Enter a valid email address."

    return errors


def authenticate_user(username: str, password: str) -> tuple[bool, str]:
    """Authenticate with a fresh config load to avoid stale credentials after signup."""
    username = (username or "").strip()
    if not username or not password:
        return False, "Enter your username and password."

    config = load_auth_config()
    usernames = config["credentials"]["usernames"]
    user_record = usernames.get(username)
    if not user_record:
        return False, "Invalid username or password."

    stored_hash = user_record.get("password") or ""
    if isinstance(stored_hash, str) and stored_hash.startswith("$2"):
        try:
            valid = bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))
        except (ValueError, TypeError):
            valid = False
    else:
        valid = False

    if not valid:
        return False, "Invalid username or password."
    return True, user_record.get("name") or username


def logout_user() -> None:
    """Clear session state and return to login (unified with custom auth)."""
    keys_to_clear = [
        "authentication_status",
        "name",
        "username",
        "email",
        "auth_error",
        "auth_loading",
        "auth_page",
        "forgot_success",
        "reset_success",
        "signup_success",
        "_workspace_hydrated",
        "_auth_paint_done",
        "app_page",
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)
    st.query_params.clear()
    st.rerun()


def _app_base_url() -> str:
    try:
        if hasattr(st, "secrets") and "smtp" in st.secrets:
            return st.secrets["smtp"].get("app_url", "http://localhost:8501").rstrip("/")
    except (FileNotFoundError, KeyError, TypeError):
        pass
    return "http://localhost:8501"


def _build_reset_link(token: str) -> str:
    base = _app_base_url()
    query = urlencode({"reset_token": token})
    return f"{base}/?{query}"


def _reset_email_html(reset_link: str) -> str:
    from src.logo import logo_email_html

    logo_block = logo_email_html(48)
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F8FAFC;font-family:Inter,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 16px;">
    <tr><td align="center">
      <table width="100%" style="max-width:520px;background:#FFFFFF;border-radius:12px;border:1px solid #E2E8F0;overflow:hidden;">
        <tr><td style="padding:32px 32px 16px;text-align:center;">
          <div style="margin-bottom:16px;">{logo_block}</div>
          <div style="font-size:18px;font-weight:700;color:#0F172A;letter-spacing:-0.02em;">DataSentinel</div>
          <h1 style="margin:24px 0 8px;font-size:24px;color:#0F172A;">Reset your password</h1>
          <p style="margin:0 0 24px;font-size:15px;line-height:1.6;color:#64748B;">
            We received a request to reset your password. Click the button below to choose a new one.
            This link expires in {RESET_TOKEN_MINUTES} minutes.
          </p>
          <a href="{reset_link}" style="display:inline-block;padding:12px 24px;background:linear-gradient(135deg,#5B5CEB,#8B5CF6);color:#FFFFFF;text-decoration:none;border-radius:10px;font-weight:600;font-size:14px;">
            Reset password
          </a>
          <p style="margin:24px 0 0;font-size:13px;line-height:1.6;color:#94A3B8;">
            If you did not request this, you can safely ignore this email.
          </p>
        </td></tr>
        <tr><td style="padding:16px 32px 32px;border-top:1px solid #E2E8F0;">
          <p style="margin:0;font-size:12px;color:#94A3B8;text-align:center;">DataSentinel · Enterprise data quality</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


def _password_changed_email_html() -> str:
    from src.logo import logo_email_html

    logo_block = logo_email_html(48)
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#F8FAFC;font-family:Inter,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 16px;">
    <tr><td align="center">
      <table width="100%" style="max-width:520px;background:#FFFFFF;border-radius:12px;border:1px solid #E2E8F0;overflow:hidden;">
        <tr><td style="padding:32px 32px 16px;text-align:center;">
          <div style="margin-bottom:16px;">{logo_block}</div>
          <div style="font-size:18px;font-weight:700;color:#0F172A;letter-spacing:-0.02em;">DataSentinel</div>
          <h1 style="margin:24px 0 8px;font-size:24px;color:#0F172A;">Password updated successfully</h1>
          <p style="margin:0 0 24px;font-size:15px;line-height:1.6;color:#64748B;">
            Your DataSentinel account password was just changed. You can now sign in
            with your new password.
          </p>
          <p style="margin:24px 0 0;font-size:13px;line-height:1.6;color:#94A3B8;">
            If you did not make this change, please contact your administrator immediately.
          </p>
        </td></tr>
        <tr><td style="padding:16px 32px 32px;border-top:1px solid #E2E8F0;">
          <p style="margin:0;font-size:12px;color:#94A3B8;text-align:center;">DataSentinel · Enterprise data quality</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


def _smtp_send_password_changed_email(to_email: str) -> None:
    """Best-effort confirmation email; never blocks the password-reset flow."""
    try:
        if not hasattr(st, "secrets") or "smtp" not in st.secrets or not to_email:
            return
        smtp_cfg = st.secrets["smtp"]
        host = smtp_cfg["host"]
        port = int(smtp_cfg.get("port", 587))
        username = smtp_cfg["username"]
        password = smtp_cfg["password"]
        sender = smtp_cfg.get("sender_email", username)

        msg = EmailMessage()
        msg["Subject"] = "Your DataSentinel password was changed"
        msg["From"] = sender
        msg["To"] = to_email
        msg.set_content(
            "Your DataSentinel account password was just changed. "
            "You can now sign in with your new password.\n\n"
            "If you did not make this change, contact your administrator immediately."
        )
        msg.add_alternative(_password_changed_email_html(), subtype="html")

        if port == 465:
            with smtplib.SMTP_SSL(host, port, timeout=20) as server:
                server.login(username, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port, timeout=20) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
    except Exception:
        import traceback
        print("SMTP Error sending password-changed confirmation email:")
        traceback.print_exc()


def _smtp_send_reset_email(to_email: str, token: str) -> tuple[bool, str]:
    try:
        if not hasattr(st, "secrets") or "smtp" not in st.secrets:
            return False, "Email is not configured. Contact your administrator."
        smtp_cfg = st.secrets["smtp"]
        host = smtp_cfg["host"]
        port = int(smtp_cfg.get("port", 587))
        username = smtp_cfg["username"]
        password = smtp_cfg["password"]
        sender = smtp_cfg.get("sender_email", username)
        reset_link = _build_reset_link(token)

        msg = EmailMessage()
        msg["Subject"] = "Reset your DataSentinel password"
        msg["From"] = sender
        msg["To"] = to_email
        msg.set_content(
            f"Reset your DataSentinel password using this link (expires in {RESET_TOKEN_MINUTES} minutes):\n\n"
            f"{reset_link}\n\n"
            "If you did not request this, ignore this email."
        )
        msg.add_alternative(_reset_email_html(reset_link), subtype="html")

        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        return True, "Password reset email sent."
    except Exception as e:
        return False, f"Could not send reset email. Debug: {type(e).__name__}: {e}"


def _store_reset_token(email: str, token: str, expiry: str) -> bool:
    engine = _get_db_engine()
    if engine is not None:
        _ensure_users_table(engine)
        with engine.connect() as conn:
            row = conn.execute(
                sqlalchemy.text("SELECT username FROM users WHERE lower(email) = lower(:e)"),
                {"e": email},
            ).fetchone()
            if not row:
                return False
            conn.execute(
                sqlalchemy.text(
                    "UPDATE users SET reset_token = :t, reset_expiry = :x WHERE lower(email) = lower(:e)"
                ),
                {"t": token, "x": expiry, "e": email},
            )
            conn.commit()
        return True

    config = load_auth_config()
    for uname, data in config["credentials"]["usernames"].items():
        if (data.get("email") or "").strip().lower() == email.lower():
            data["reset_token"] = token
            data["reset_expiry"] = expiry
            return save_auth_config(config)
    return False


def request_password_reset(email: str) -> tuple[bool, str]:
    email = (email or "").strip()
    if not email:
        return False, "Enter your registered email."
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Enter a valid email address."

    token = secrets.token_urlsafe(32)
    expiry = (datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_MINUTES)).isoformat()
    found = _store_reset_token(email, token, expiry)

    # Always return the same message to prevent email enumeration.
    generic_ok = "If this email is registered, you will receive a reset link shortly."
    if not found:
        return True, generic_ok

    sent, message = _smtp_send_reset_email(email, token)
    if not sent:
        return False, message
    return True, generic_ok


def reset_password_with_token(token: str, new_password: str) -> tuple[bool, str]:
    token = (token or "").strip()
    if not token:
        return False, "Invalid reset link."
    if len(new_password or "") < 6:
        return False, "Password must be at least 6 characters."
    if not re.search(r"\d", new_password) or not re.search(
        r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", new_password
    ):
        return False, "Password must include at least one number and one special symbol."

    now = datetime.now(timezone.utc)
    engine = _get_db_engine()
    if engine is not None:
        _ensure_users_table(engine)
        with engine.connect() as conn:
            row = conn.execute(
                sqlalchemy.text(
                    "SELECT username, email, reset_expiry FROM users WHERE reset_token = :t"
                ),
                {"t": token},
            ).fetchone()
            if not row:
                return False, "This reset link is invalid or has already been used."
            expiry_raw = row[2]
            if not expiry_raw:
                return False, "This reset link has expired. Request a new one."
            expiry = datetime.fromisoformat(expiry_raw.replace("Z", "+00:00"))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if expiry < now:
                return False, "This reset link has expired. Request a new one."
            conn.execute(
                sqlalchemy.text(
                    "UPDATE users SET password = :p, reset_token = NULL, reset_expiry = NULL "
                    "WHERE username = :u"
                ),
                {"p": hash_password(new_password), "u": row[0]},
            )
            conn.commit()
        _smtp_send_password_changed_email(row[1])
        return True, "Password updated successfully."

    config = load_auth_config()
    for uname, data in config["credentials"]["usernames"].items():
        if data.get("reset_token") != token:
            continue
        expiry_raw = data.get("reset_expiry")
        if not expiry_raw:
            return False, "This reset link has expired. Request a new one."
        expiry = datetime.fromisoformat(expiry_raw.replace("Z", "+00:00"))
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if expiry < now:
            return False, "This reset link has expired. Request a new one."
        data["password"] = hash_password(new_password)
        data.pop("reset_token", None)
        data.pop("reset_expiry", None)
        if save_auth_config(config):
            _smtp_send_password_changed_email(data.get("email", ""))
            return True, "Password updated successfully."
        return False, "Could not update password."
    return False, "This reset link is invalid or has already been used."
