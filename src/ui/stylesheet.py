"""Assembles the global stylesheet from design tokens."""

from __future__ import annotations

from src.ui.tokens import (
    BTN_HEIGHT,
    BTN_PAD_X,
    CONTAINER_MAX,
    DURATION,
    EASING,
    INPUT_HEIGHT,
    INPUT_PAD_X,
    PAGE_GUTTER_MAX,
    PAGE_GUTTER_MIN,
    RADIUS,
    SP,
    TYPE,
    get_theme_name,
    get_vars,
)


def _vars() -> str:
    lines = [f"  {k}: {v};" for k, v in get_vars().items()]
    return ":root {\n" + "\n".join(lines) + "\n}"


def _base() -> str:
    return f"""
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap');
#MainMenu, footer, [data-testid="stToolbar"] {{ visibility: hidden; height: 0; }}
*, *::before, *::after {{ box-sizing: border-box; }}
:root {{
  --page-max-width: {CONTAINER_MAX}px;
  --page-gutter: clamp({PAGE_GUTTER_MIN}px, 2vw, {PAGE_GUTTER_MAX}px);
}}
html, body, [class*="css"] {{
    font-family: 'Outfit', system-ui, sans-serif;
    font-size: {TYPE['body']}px;
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
}}
[data-testid="stAppViewContainer"] {{
    background: var(--ui-bg);
    background-image: var(--ui-mesh);
    color: var(--ui-text);
    overflow-x: hidden;
}}
.block-container {{
    max-width: var(--page-max-width) !important;
    width: 100% !important;
    padding: {SP[12]}px var(--page-gutter) {SP[32]}px !important;
    margin-inline: auto !important;
}}
/* Kill Streamlit auto heading permalinks (chain/link icons) */
[data-testid="stHeaderActionElements"],
a[aria-label="Link to heading"],
.stMarkdown a.headerlink {{
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
}}
header[data-testid="stHeader"] {{
    background: transparent !important;
    border: none !important;
    pointer-events: none !important;
}}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display: none !important; }}
@keyframes ui-fade {{ from {{ opacity:0; transform:translateY(8px); }} to {{ opacity:1; transform:none; }} }}
@keyframes ui-drift {{ 0%,100% {{ transform: translate3d(0,0,0); }} 50% {{ transform: translate3d(0,-10px,0); }} }}
@keyframes ui-shimmer {{ 0% {{ background-position: 0% 50%; }} 100% {{ background-position: 100% 50%; }} }}
@keyframes ui-theme-morph {{
  0% {{
    opacity: 0.15;
    transform: rotate(-140deg) scale(0.5);
    filter: blur(1.5px);
  }}
  100% {{
    opacity: 1;
    transform: rotate(0deg) scale(1);
    filter: none;
  }}
}}
@keyframes ui-auth-enter {{
  from {{ opacity: 0; transform: translateY(12px); }}
  to {{ opacity: 1; transform: none; }}
}}
.ui-fade {{ animation: ui-fade 320ms {EASING} both; }}
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
.stCaption {{ color: var(--ui-text-3) !important; }}
.ui-panel-card:empty, .ui-auth-wrap:empty, header.ui-bar:empty {{ display: none !important; }}
@media (prefers-reduced-motion: reduce) {{
  .ui-fade, .ui-auth-enter {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
}}
"""


def _buttons() -> str:
    h, r = BTN_HEIGHT, RADIUS[12]
    return f"""
[data-testid="stButton"] button[kind="primary"],
[data-testid="stBaseButton-primary"],
[data-testid="stDownloadButton"] button,
[data-testid="stFormSubmitButton"] button {{
    width: 100% !important;
    height: {h}px !important;
    min-height: {h}px !important;
    padding: 0 {BTN_PAD_X}px !important;
    border: none !important;
    border-radius: {r}px !important;
    background: var(--ui-gradient) !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: {TYPE['small']}px !important;
    box-shadow: var(--ui-shadow-sm) !important;
    transition: transform {DURATION} {EASING}, box-shadow {DURATION} {EASING} !important;
}}
[data-testid="stButton"] button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover,
[data-testid="stDownloadButton"] button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(14,165,233,0.28) !important;
}}
[data-testid="stButton"] button[kind="primary"]:focus-visible,
[data-testid="stBaseButton-primary"]:focus-visible,
[data-testid="stDownloadButton"] button:focus-visible {{
    box-shadow: var(--ui-focus) !important;
}}
[data-testid="stButton"] button[kind="primary"] p,
[data-testid="stBaseButton-primary"] p,
[data-testid="stDownloadButton"] button p {{ color: #fff !important; margin: 0 !important; }}

[data-testid="stButton"] button[kind="secondary"],
[data-testid="stBaseButton-secondary"] {{
    width: 100% !important;
    height: {h}px !important;
    min-height: {h}px !important;
    padding: 0 {BTN_PAD_X}px !important;
    border-radius: {r}px !important;
    border: 1px solid var(--ui-border) !important;
    background: var(--ui-elevated) !important;
    color: var(--ui-text) !important;
    font-weight: 600 !important;
    font-size: {TYPE['small']}px !important;
    box-shadow: var(--ui-shadow-sm) !important;
    transition: background {DURATION} {EASING}, border-color {DURATION} {EASING}, transform {DURATION} {EASING} !important;
}}
[data-testid="stButton"] button[kind="secondary"]:hover,
[data-testid="stBaseButton-secondary"]:hover {{
    background: var(--ui-muted) !important;
    border-color: var(--ui-border-strong) !important;
    transform: translateY(-1px) !important;
}}
[data-testid="stButton"] button[kind="secondary"]:focus-visible,
[data-testid="stBaseButton-secondary"]:focus-visible {{ box-shadow: var(--ui-focus) !important; }}
[data-testid="stButton"] button[kind="secondary"] p,
[data-testid="stBaseButton-secondary"] p {{ color: var(--ui-text) !important; margin: 0 !important; }}
[data-testid="stButton"] button:disabled,
[data-testid="stBaseButton-secondary"]:disabled {{ opacity: 0.45 !important; transform: none !important; cursor: not-allowed !important; }}
"""


def _ctrl_buttons() -> str:
    keys = ["ui_theme_toggle", "main_theme", "hdr_theme"]
    wrappers = []
    for k in keys:
        wrappers.append(f".st-key-{k}")
        wrappers.append(f".stKey-{k}")
    container_sel = ", ".join(wrappers)
    btn_selectors = []
    for w in wrappers:
        btn_selectors.append(f"{w} button")
        btn_selectors.append(f"{w} [data-testid='stBaseButton-secondary']")
    btn_sel = ", ".join(btn_selectors)
    # Critical: never append " p" to a comma-joined list — that only suffixes the last item
    # and incorrectly targets every preceding button. Build label selectors explicitly.
    label_sel = ", ".join(
        f"{w} button p, {w} button span, {w} [data-testid='stBaseButton-secondary'] p, "
        f"{w} [data-testid='stBaseButton-secondary'] span"
        for w in wrappers
    )

    return f"""
/* Theme — standalone ghost icon (no permanent box); morph on theme change */
{container_sel} {{
    width: 42px !important;
    min-width: 42px !important;
    max-width: 42px !important;
    height: 42px !important;
    flex: 0 0 42px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    overflow: visible !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    position: relative !important;
    z-index: 5 !important;
}}
{container_sel} [data-testid="stElementContainer"],
{container_sel} [data-testid="element-container"],
{container_sel} [data-testid="stButton"] {{
    margin: 0 !important;
    width: 42px !important;
    max-width: 42px !important;
    height: 42px !important;
    max-height: 42px !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    position: relative !important;
    z-index: 5 !important;
}}
{btn_sel} {{
    box-sizing: border-box !important;
    position: relative !important;
    width: 42px !important;
    max-width: 42px !important;
    height: 42px !important;
    min-height: 42px !important;
    max-height: 42px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    border-radius: 999px !important;
    background: transparent !important;
    background-image: none !important;
    color: var(--ui-text) !important;
    font-size: 22px !important;
    line-height: 1 !important;
    box-shadow: none !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    transform: none !important;
    overflow: visible !important;
    visibility: visible !important;
    opacity: 1 !important;
    transition: background-color 200ms {EASING}, box-shadow 200ms {EASING}, transform 200ms {EASING} !important;
}}
{btn_sel}:hover {{
    background: var(--ui-accent-soft) !important;
    background-image: none !important;
    border: none !important;
    transform: scale(1.05) !important;
    box-shadow: 0 0 18px rgba(56,189,248,0.22) !important;
    filter: none !important;
    opacity: 1 !important;
}}
{btn_sel}:focus-visible {{
    outline: none !important;
    box-shadow: var(--ui-focus) !important;
    background: var(--ui-accent-soft) !important;
    opacity: 1 !important;
}}
{label_sel} {{
    display: block !important;
    visibility: visible !important;
    margin: 0 !important;
    padding: 0 !important;
    font-size: 22px !important;
    line-height: 1 !important;
    color: inherit !important;
    opacity: 1 !important;
    animation: ui-theme-morph 420ms {EASING};
    transform-origin: center center;
}}
@media (prefers-reduced-motion: reduce) {{
  {label_sel} {{ animation: none !important; opacity: 1 !important; transform: none !important; filter: none !important; }}
  {btn_sel}:hover {{ transform: none !important; }}
}}

/* Nav pills — premium size; equal padding; never collapse (letter-wrap guard) */
.st-key-nav_dashboard, .st-key-nav_analytics, .st-key-nav_history,
.stKey-nav_dashboard, .stKey-nav_analytics, .stKey-nav_history {{
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: max-content !important;
}}
.st-key-nav_dashboard [data-testid="stButton"],
.st-key-nav_analytics [data-testid="stButton"],
.st-key-nav_history [data-testid="stButton"],
.stKey-nav_dashboard [data-testid="stButton"],
.stKey-nav_analytics [data-testid="stButton"],
.stKey-nav_history [data-testid="stButton"] {{
    width: auto !important;
    min-width: max-content !important;
}}
.st-key-nav_dashboard [data-testid="stButton"] button,
.st-key-nav_analytics [data-testid="stButton"] button,
.st-key-nav_history [data-testid="stButton"] button,
.stKey-nav_dashboard [data-testid="stButton"] button,
.stKey-nav_analytics [data-testid="stButton"] button,
.stKey-nav_history [data-testid="stButton"] button,
.st-key-nav_dashboard [data-testid="stBaseButton-primary"],
.st-key-nav_dashboard [data-testid="stBaseButton-secondary"],
.st-key-nav_analytics [data-testid="stBaseButton-primary"],
.st-key-nav_analytics [data-testid="stBaseButton-secondary"],
.st-key-nav_history [data-testid="stBaseButton-primary"],
.st-key-nav_history [data-testid="stBaseButton-secondary"],
.stKey-nav_dashboard [data-testid="stBaseButton-primary"],
.stKey-nav_dashboard [data-testid="stBaseButton-secondary"],
.stKey-nav_analytics [data-testid="stBaseButton-primary"],
.stKey-nav_analytics [data-testid="stBaseButton-secondary"],
.stKey-nav_history [data-testid="stBaseButton-primary"],
.stKey-nav_history [data-testid="stBaseButton-secondary"] {{
    width: auto !important;
    min-width: max-content !important;
    height: 46px !important;
    min-height: 46px !important;
    max-height: 46px !important;
    padding: 0 26px !important;
    border-radius: 999px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    box-shadow: none !important;
    transform: none !important;
    flex: none !important;
    white-space: nowrap !important;
    word-break: normal !important;
    overflow-wrap: normal !important;
    transition: background 280ms {EASING}, color 280ms {EASING}, box-shadow 280ms {EASING}, border-color 280ms {EASING} !important;
}}
.st-key-nav_dashboard [data-testid="stButton"] button p,
.st-key-nav_analytics [data-testid="stButton"] button p,
.st-key-nav_history [data-testid="stButton"] button p,
.st-key-nav_dashboard [data-testid="stBaseButton-primary"] p,
.st-key-nav_dashboard [data-testid="stBaseButton-secondary"] p,
.st-key-nav_analytics [data-testid="stBaseButton-primary"] p,
.st-key-nav_analytics [data-testid="stBaseButton-secondary"] p,
.st-key-nav_history [data-testid="stBaseButton-primary"] p,
.st-key-nav_history [data-testid="stBaseButton-secondary"] p {{
    white-space: nowrap !important;
    word-break: normal !important;
    overflow-wrap: normal !important;
    margin: 0 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    line-height: 1 !important;
}}
.st-key-nav_dashboard [data-testid="stButton"] button[kind="secondary"],
.st-key-nav_analytics [data-testid="stButton"] button[kind="secondary"],
.st-key-nav_history [data-testid="stButton"] button[kind="secondary"],
.st-key-nav_dashboard [data-testid="stBaseButton-secondary"],
.st-key-nav_analytics [data-testid="stBaseButton-secondary"],
.st-key-nav_history [data-testid="stBaseButton-secondary"],
.stKey-nav_dashboard [data-testid="stBaseButton-secondary"],
.stKey-nav_analytics [data-testid="stBaseButton-secondary"],
.stKey-nav_history [data-testid="stBaseButton-secondary"] {{
    background: transparent !important;
    border: 1px solid transparent !important;
    color: var(--ui-text-2) !important;
}}
.st-key-nav_dashboard [data-testid="stButton"] button[kind="secondary"]:hover,
.st-key-nav_analytics [data-testid="stButton"] button[kind="secondary"]:hover,
.st-key-nav_history [data-testid="stButton"] button[kind="secondary"]:hover,
.st-key-nav_dashboard [data-testid="stBaseButton-secondary"]:hover,
.st-key-nav_analytics [data-testid="stBaseButton-secondary"]:hover,
.st-key-nav_history [data-testid="stBaseButton-secondary"]:hover {{
    background: rgba(148,163,184,0.12) !important;
    border-color: transparent !important;
    color: var(--ui-text) !important;
    transform: none !important;
}}
.st-key-nav_dashboard [data-testid="stButton"] button[kind="primary"],
.st-key-nav_analytics [data-testid="stButton"] button[kind="primary"],
.st-key-nav_history [data-testid="stButton"] button[kind="primary"],
.st-key-nav_dashboard [data-testid="stBaseButton-primary"],
.st-key-nav_analytics [data-testid="stBaseButton-primary"],
.st-key-nav_history [data-testid="stBaseButton-primary"],
.stKey-nav_dashboard [data-testid="stBaseButton-primary"],
.stKey-nav_analytics [data-testid="stBaseButton-primary"],
.stKey-nav_history [data-testid="stBaseButton-primary"] {{
    background: linear-gradient(135deg, #6366F1 0%, #3B82F6 48%, #22D3EE 100%) !important;
    color: #fff !important;
    border: 1px solid transparent !important;
    box-shadow: 0 4px 14px rgba(59,130,246,0.28), inset 0 1px 0 rgba(255,255,255,0.22) !important;
}}
.st-key-nav_dashboard [data-testid="stButton"] button[kind="primary"] p,
.st-key-nav_analytics [data-testid="stButton"] button[kind="primary"] p,
.st-key-nav_history [data-testid="stButton"] button[kind="primary"] p,
.st-key-nav_dashboard [data-testid="stBaseButton-primary"] p,
.st-key-nav_analytics [data-testid="stBaseButton-primary"] p,
.st-key-nav_history [data-testid="stBaseButton-primary"] p {{
    color: #fff !important;
}}

/* Logout — aligned with nav/profile height */
.st-key-ui_logout_btn, .stKey-ui_logout_btn {{
    flex: 0 0 auto !important;
    width: auto !important;
    min-width: max-content !important;
    max-width: none !important;
    height: 44px !important;
    max-height: 44px !important;
}}
.st-key-ui_logout_btn [data-testid="stButton"],
.stKey-ui_logout_btn [data-testid="stButton"],
.st-key-ui_logout_btn [data-testid="stElementContainer"],
.stKey-ui_logout_btn [data-testid="stElementContainer"] {{
    margin: 0 !important;
    width: auto !important;
    max-width: none !important;
    height: 44px !important;
    max-height: 44px !important;
}}
.st-key-ui_logout_btn button,
.stKey-ui_logout_btn button,
.st-key-ui_logout_btn [data-testid="stBaseButton-secondary"],
.stKey-ui_logout_btn [data-testid="stBaseButton-secondary"] {{
    box-sizing: border-box !important;
    width: auto !important;
    max-width: none !important;
    height: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;
    padding: 0 16px !important;
    border-radius: 12px !important;
    border: 1px solid var(--ui-border) !important;
    background: var(--ui-elevated) !important;
    background-image: none !important;
    box-shadow: none !important;
    transform: none !important;
    color: var(--ui-text-2) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    line-height: 1 !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
}}
.st-key-ui_logout_btn button:hover,
.stKey-ui_logout_btn button:hover,
.st-key-ui_logout_btn [data-testid="stBaseButton-secondary"]:hover,
.stKey-ui_logout_btn [data-testid="stBaseButton-secondary"]:hover {{
    background: var(--ui-danger-soft) !important;
    border-color: rgba(251,113,133,0.45) !important;
    color: var(--ui-danger) !important;
    background-image: none !important;
    transform: none !important;
}}
.st-key-ui_logout_btn button p,
.stKey-ui_logout_btn button p,
.st-key-ui_logout_btn [data-testid="stBaseButton-secondary"] p,
.stKey-ui_logout_btn [data-testid="stBaseButton-secondary"] p,
.st-key-ui_logout_btn button span,
.stKey-ui_logout_btn button span {{
    display: block !important;
    visibility: visible !important;
    margin: 0 !important;
    padding: 0 !important;
    color: inherit !important;
    font-size: 14px !important;
    line-height: 1 !important;
    opacity: 1 !important;
    width: auto !important;
    height: auto !important;
}}

/* Forgot-password text link — keep near Remember me */
.st-key-ui_forgot_link {{ display: flex !important; justify-content: flex-start !important; }}
.st-key-ui_forgot_link [data-testid="stButton"] {{ margin: 0 !important; width: auto !important; }}
.st-key-ui_forgot_link [data-testid="stButton"] button,
.st-key-ui_forgot_link [data-testid="stBaseButton-secondary"] {{
    width: auto !important;
    height: auto !important;
    min-height: 0 !important;
    padding: 2px 0 !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    color: var(--ui-primary) !important;
    font-weight: 500 !important;
    font-size: {TYPE['small']}px !important;
    transform: none !important;
}}
.st-key-ui_forgot_link [data-testid="stButton"] button:hover,
.st-key-ui_forgot_link [data-testid="stBaseButton-secondary"]:hover {{
    text-decoration: underline !important; transform: none !important; background: transparent !important;
}}
.st-key-ui_forgot_link [data-testid="stButton"] button p,
.st-key-ui_forgot_link [data-testid="stBaseButton-secondary"] p {{ color: var(--ui-primary) !important; margin: 0 !important; }}

/* Profile popover — matches logout / nav height */
.st-key-hdr_profile, .stKey-hdr_profile {{
    width: auto !important;
    max-width: 180px !important;
    height: 44px !important;
    max-height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 !important;
    overflow: hidden !important;
}}
.st-key-hdr_profile [data-testid="stPopover"],
.stKey-hdr_profile [data-testid="stPopover"],
.st-key-hdr_profile [data-testid="stElementContainer"],
.stKey-hdr_profile [data-testid="stElementContainer"] {{
    width: auto !important;
    max-width: 180px !important;
    height: 44px !important;
    max-height: 44px !important;
    margin: 0 !important;
}}
.st-key-hdr_profile button, .stKey-hdr_profile button {{
    width: auto !important;
    min-width: max-content !important;
    max-width: 180px !important;
    height: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;
    padding: 0 14px 0 6px !important;
    border-radius: 999px !important;
    border: 1px solid var(--ui-border) !important;
    background: var(--ui-elevated) !important;
    box-shadow: none !important;
    transform: none !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 10px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
}}
.st-key-hdr_profile button:hover, .stKey-hdr_profile button:hover {{
    background: var(--ui-muted) !important;
    border-color: var(--ui-border-strong) !important;
    transform: none !important;
}}
.st-key-hdr_profile button p, .stKey-hdr_profile button p {{
    color: var(--ui-text) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    margin: 0 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    line-height: 1 !important;
}}
.st-key-hdr_profile button::before, .stKey-hdr_profile button::before {{
    content: "" !important;
    width: 28px !important;
    height: 28px !important;
    border-radius: 50% !important;
    background: var(--ui-gradient) !important;
    flex-shrink: 0 !important;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.18);
}}
"""


def _inputs() -> str:
    h, r, px = INPUT_HEIGHT, RADIUS[12], INPUT_PAD_X
    return f"""
[data-testid="stWidgetLabel"] p, label {{
    color: var(--ui-text-2) !important;
    font-size: {TYPE['small']}px !important;
    font-weight: 500 !important;
    margin-bottom: {SP[8]}px !important;
}}
[data-testid="stTextInput"] [data-testid="stTextInputRootElement"],
[data-testid="stTextInput"] > div[data-baseweb="input"],
[data-testid="stSelectbox"] > div > div {{
    background: var(--ui-input) !important;
    border: 1px solid var(--ui-border) !important;
    border-radius: {r}px !important;
    min-height: {h}px !important;
    height: {h}px !important;
    display: flex !important;
    align-items: center !important;
    transition: border-color 180ms ease, box-shadow 180ms ease, background-color 180ms ease !important;
}}
[data-testid="stTextInput"] [data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stTextInput"] > div[data-baseweb="input"]:focus-within,
[data-testid="stSelectbox"] > div > div:focus-within {{
    border-color: var(--ui-primary) !important;
    box-shadow: var(--ui-focus) !important;
}}
[data-testid="stTextInput"] [data-baseweb="base-input"],
[data-testid="stTextInput"] > div > div > div {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    height: 100% !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
}}
[data-testid="stTextInput"] input {{
    flex: 1 1 auto !important;
    height: 100% !important;
    min-height: 0 !important;
    padding: 0 {px}px !important;
    color: var(--ui-text) !important;
    font-size: {TYPE['small']}px !important;
    background: transparent !important;
    caret-color: var(--ui-primary) !important;
    border: none !important;
    box-shadow: none !important;
}}
[data-testid="stTextInput"] input::placeholder {{ color: var(--ui-text-3) !important; opacity: 1 !important; }}
[data-testid="stTextInput"] button {{
    flex: 0 0 auto !important;
    width: 32px !important;
    height: 32px !important;
    min-height: 32px !important;
    padding: 0 !important;
    margin-right: 8px !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    color: var(--ui-text-3) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 8px !important;
    transform: none !important;
}}
[data-testid="stTextInput"] button:hover {{
    color: var(--ui-text) !important;
    background: var(--ui-accent-soft) !important;
    transform: none !important;
}}
[data-testid="stTextInput"] button:focus-visible {{ box-shadow: var(--ui-focus) !important; }}
[data-testid="stTextInput"] button p {{ display: none !important; }}
[data-testid="stTextInput"] button svg {{
    width: 18px !important;
    height: 18px !important;
    fill: none !important;
    stroke: currentColor !important;
}}

/* Select / dropdown — semantic text so Baseweb never paints white-on-white */
[data-testid="stSelectbox"] {{ color: var(--ui-text) !important; }}
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stSelectbox"] [data-baseweb="select"] > div {{
    background: var(--ui-input) !important;
    color: var(--ui-text) !important;
}}
[data-testid="stSelectbox"] [data-baseweb="select"] div,
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] input,
[data-testid="stSelectbox"] [data-baseweb="select"] [value],
[data-testid="stSelectbox"] div[aria-live],
[data-testid="stSelectbox"] div[aria-selected] {{
    color: var(--ui-text) !important;
    -webkit-text-fill-color: var(--ui-text) !important;
    opacity: 1 !important;
    caret-color: var(--ui-text) !important;
}}
[data-testid="stSelectbox"] [data-baseweb="select"] svg {{
    color: var(--ui-text-3) !important;
    fill: var(--ui-text-3) !important;
    opacity: 1 !important;
}}
div[data-baseweb="popover"] {{
    color: var(--ui-text) !important;
}}
div[data-baseweb="popover"] ul[role="listbox"],
div[data-baseweb="popover"] ul[role="listbox"] li,
div[data-baseweb="menu"] li,
div[data-baseweb="popover"] [role="option"] {{
    color: var(--ui-text) !important;
    -webkit-text-fill-color: var(--ui-text) !important;
    background-color: var(--ui-elevated) !important;
}}
div[data-baseweb="popover"] ul[role="listbox"] li:hover,
div[data-baseweb="popover"] [role="option"]:hover,
div[data-baseweb="popover"] [aria-selected="true"] {{
    background-color: var(--ui-muted) !important;
    color: var(--ui-text) !important;
    -webkit-text-fill-color: var(--ui-text) !important;
}}
[data-testid="stCheckbox"] label p,
[data-testid="stCheckbox"] span {{
    color: var(--ui-text-2) !important;
}}
"""


def _header() -> str:
    r = RADIUS[14]
    return f"""
.ui-hdr-anchor {{ display: none; }}
.block-container:has(.ui-hdr-anchor) {{ padding-top: {SP[12]}px !important; }}

/* Kill leftover login-page nodes while Streamlit remaps widgets after auth */
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) .ui-auth-texture,
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) .ui-auth-brand,
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) .ui-auth-card-head,
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) .ui-auth-foot,
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) .ui-auth-form-shell,
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) .ui-auth-headline,
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) .ui-auth-lede,
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) .ui-auth-how-box,
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) .ui-auth-features,
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) .ui-auth-anchor,
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) [class*="st-key-login_"],
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) [class*="stKey-login_"],
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) [class*="st-key-goto_signup"],
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) [class*="st-key-goto_login"],
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) [class*="st-key-ui_forgot"],
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) [class*="st-key-signup_"],
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) [class*="st-key-forgot_"],
[data-testid="stAppViewContainer"]:has(.ui-hdr-anchor) [class*="st-key-reset_"] {{
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
    opacity: 0 !important;
    position: absolute !important;
    width: 0 !important;
    height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
}}

/* Kill leftover app-header nodes while Streamlit remaps back to login */
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .ui-hdr-anchor,
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .ui-brand,
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .ui-nav-row,
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .ui-how,
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .ui-hero,
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .ui-stat,
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="st-key-ui_logout"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="st-key-hdr_profile"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="st-key-main_theme"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="st-key-hdr_theme"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="st-key-nav_"] {{
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
    opacity: 0 !important;
}}


.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) {{
    /* Flex 1fr auto 1fr equivalent — avoid CSS grid (collapses Streamlit columns) */
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    justify-content: space-between !important;
    align-items: center !important;
    gap: 16px !important;
    column-gap: 16px !important;
    min-height: 72px !important;
    max-height: none !important;
    height: auto !important;
    overflow: visible !important;
    padding: 12px 18px !important;
    margin-bottom: 12px !important;
    background: var(--ui-glass);
    backdrop-filter: blur(18px);
    border: 1px solid var(--ui-border);
    border-radius: {r}px;
    box-shadow: var(--ui-shadow-sm);
}}
/* Streamlit ≥1.33 uses data-testid="stColumn"; older builds used "column" */
.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) > [data-testid="column"],
.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) > [data-testid="stColumn"] {{
    display: flex !important;
    align-items: center !important;
    min-height: 48px !important;
    max-height: none !important;
    height: auto !important;
    min-width: 0 !important;
    overflow: visible !important;
}}
.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) > [data-testid="column"] > div,
.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) > [data-testid="stColumn"] > div {{
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    min-height: 48px !important;
    overflow: visible !important;
}}
.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) > [data-testid="column"]:nth-child(1),
.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) > [data-testid="stColumn"]:nth-child(1) {{
    justify-content: flex-start !important;
    flex: 1 1 0 !important;
}}
.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) > [data-testid="column"]:nth-child(2),
.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) > [data-testid="stColumn"]:nth-child(2) {{
    justify-content: center !important;
    flex: 0 0 auto !important;
    min-width: max-content !important;
}}
.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) > [data-testid="column"]:nth-child(3),
.block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) > [data-testid="stColumn"]:nth-child(3) {{
    justify-content: flex-end !important;
    flex: 1 1 0 !important;
}}
.ui-hdr-actions {{ display: none !important; height: 0 !important; margin: 0 !important; padding: 0 !important; }}
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-hdr-actions) > div[data-testid="stVerticalBlock"],
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-hdr-actions) > div[data-testid="stVerticalBlock"] {{
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
}}
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-hdr-actions) div[data-testid="stHorizontalBlock"],
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-hdr-actions) div[data-testid="stHorizontalBlock"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
    flex-wrap: nowrap !important;
    gap: 14px !important;
    column-gap: 14px !important;
    width: max-content !important;
    max-width: 100% !important;
    margin-left: auto !important;
    min-height: 44px !important;
}}
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-hdr-actions) div[data-testid="stHorizontalBlock"] > [data-testid="column"],
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-hdr-actions) div[data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-hdr-actions) div[data-testid="stHorizontalBlock"] > [data-testid="column"],
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-hdr-actions) div[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex: 0 0 auto !important;
    flex-grow: 0 !important;
    flex-shrink: 0 !important;
    flex-basis: auto !important;
    width: fit-content !important;
    min-width: max-content !important;
    max-width: fit-content !important;
    padding: 0 !important;
}}
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-hdr-actions) div[data-testid="stHorizontalBlock"] > [data-testid="column"] > div,
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-hdr-actions) div[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div,
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-hdr-actions) div[data-testid="stHorizontalBlock"] > [data-testid="column"] > div,
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-hdr-actions) div[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div {{
    width: auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

/* Nav group — balanced tabs in outer pill (~56px) */
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-nav-row) > div,
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-nav-row) > div {{
    justify-content: center !important;
    width: 100% !important;
}}
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-nav-row) div[data-testid="stHorizontalBlock"],
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-nav-row) div[data-testid="stHorizontalBlock"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-wrap: nowrap !important;
    gap: 4px !important;
    column-gap: 4px !important;
    width: max-content !important;
    max-width: 100%;
    margin: 0 auto !important;
    padding: 5px !important;
    min-height: 56px !important;
    border: 1px solid var(--ui-border) !important;
    border-radius: 999px !important;
    background: var(--ui-muted) !important;
}}
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-nav-row) div[data-testid="stHorizontalBlock"] > [data-testid="column"],
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-nav-row) div[data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-nav-row) div[data-testid="stHorizontalBlock"] > [data-testid="column"],
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-nav-row) div[data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex: 0 0 auto !important;
    flex-grow: 0 !important;
    flex-shrink: 0 !important;
    flex-basis: auto !important;
    width: fit-content !important;
    min-width: max-content !important;
    max-width: fit-content !important;
    min-height: 46px !important;
    gap: 0 !important;
}}
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-nav-row) [data-testid="stButton"],
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-nav-row) [data-testid="stButton"],
.block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-nav-row) [data-testid="element-container"],
.block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-nav-row) [data-testid="element-container"] {{
    width: auto !important;
    min-width: max-content !important;
}}
.ui-brand {{
    display: inline-flex; align-items: center; gap: 10px;
    min-height: 48px; width: auto;
}}
.ui-brand-link {{
    display: inline-flex; align-items: center; gap: 10px;
    text-decoration: none !important; line-height: 1;
    border: none !important;
}}
.ui-brand-link:hover {{ text-decoration: none !important; }}
.ui-brand-link svg {{ display: block; flex-shrink: 0; }}
.ui-wordmark {{
    font-family: 'Outfit', sans-serif;
    font-size: 19px; font-weight: 700; letter-spacing: -0.03em;
    color: var(--ui-text); white-space: nowrap; line-height: 1;
}}
.ui-nav-row {{ display: none; }}
.ui-avatar {{
    width: 36px; height: 36px; border-radius: {RADIUS[10]}px;
    background: var(--ui-gradient); color: #fff; font-size: 13px; font-weight: 700;
    display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0;
}}
.ui-user-meta {{ display: flex; flex-direction: column; gap: 1px; min-width: 0; }}
.ui-user-name {{ font-size: 13px; font-weight: 600; color: var(--ui-text); }}
.ui-user-email {{ font-size: 11px; color: var(--ui-text-3); }}
.ui-profile-card {{
    display: flex; gap: 14px; align-items: flex-start;
    padding: 4px 2px 2px; min-width: 240px;
}}
.ui-profile-avatar {{
    width: 48px; height: 48px; border-radius: 14px;
    background: var(--ui-gradient); color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 16px; flex-shrink: 0;
}}
.ui-profile-body {{ flex: 1; min-width: 0; }}
.ui-profile-label {{
    margin: 8px 0 2px; font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.06em; color: var(--ui-text-3);
}}
.ui-profile-label:first-child {{ margin-top: 0; }}
.ui-profile-name {{ margin: 0; font-size: 16px; font-weight: 700; color: var(--ui-text); }}
.ui-profile-meta {{ margin: 0; font-size: 13px; color: var(--ui-text-2); word-break: break-all; }}
.ui-profile-chips {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }}
.ui-profile-chips span {{
    font-size: 11px; font-weight: 600; color: var(--ui-primary);
    background: var(--ui-accent-soft); border: 1px solid var(--ui-border);
    border-radius: 999px; padding: 4px 10px;
}}
.ui-boot-panel {{
    display: flex; align-items: center; justify-content: center;
    min-height: 42vh; margin-top: {SP[24]}px;
}}
.ui-boot-card {{
    padding: {SP[20]}px {SP[32]}px;
    border-radius: {r}px;
    background: var(--ui-glass);
    border: 1px solid var(--ui-border);
    box-shadow: var(--ui-shadow-sm);
    color: var(--ui-text-2);
    font-weight: 600;
    font-size: {TYPE['small']}px;
}}
.ui-boot-card p {{ margin: 0; color: var(--ui-text-2) !important; }}
@media (max-width: 900px) {{
    .ui-wordmark {{ font-size: 16px; }}
    .block-container:has(.ui-hdr-anchor) [data-testid="column"]:has(.ui-nav-row) div[data-testid="stHorizontalBlock"],
    .block-container:has(.ui-hdr-anchor) [data-testid="stColumn"]:has(.ui-nav-row) div[data-testid="stHorizontalBlock"] {{
        max-width: none;
    }}
    .block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) {{
        gap: 8px !important;
        padding: 8px 12px !important;
    }}
    .st-key-nav_dashboard [data-testid="stButton"] button,
    .st-key-nav_analytics [data-testid="stButton"] button,
    .st-key-nav_history [data-testid="stButton"] button,
    .stKey-nav_dashboard [data-testid="stButton"] button,
    .stKey-nav_analytics [data-testid="stButton"] button,
    .stKey-nav_history [data-testid="stButton"] button {{
        padding: 0 12px !important;
        font-size: 12px !important;
    }}
}}
@media (max-width: 640px) {{
    .block-container:has(.ui-hdr-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-brand) {{
        flex-wrap: wrap !important;
        height: auto !important;
        max-height: none !important;
    }}
    .ui-wordmark {{ display: none; }}
}}

/* Last-wins — keep theme ghost icon fully visible + sized */
.block-container:has(.ui-hdr-anchor) [class*="st-key-main_theme"] button,
.block-container:has(.ui-hdr-anchor) [class*="st-key-hdr_theme"] button,
.block-container:has(.ui-hdr-anchor) [class*="st-key-ui_theme"] button,
.block-container:has(.ui-hdr-anchor) [class*="st-key-main_theme"] [data-testid="stBaseButton-secondary"],
.block-container:has(.ui-hdr-anchor) [class*="st-key-hdr_theme"] [data-testid="stBaseButton-secondary"],
.block-container:has(.ui-hdr-anchor) [class*="st-key-ui_theme"] [data-testid="stBaseButton-secondary"] {{
    box-sizing: border-box !important;
    height: 42px !important;
    min-height: 42px !important;
    max-height: 42px !important;
    width: 42px !important;
    border: none !important;
    background: transparent !important;
    background-image: none !important;
    box-shadow: none !important;
    transform: none !important;
    opacity: 1 !important;
    visibility: visible !important;
    font-size: 22px !important;
    color: var(--ui-text) !important;
}}
.block-container:has(.ui-hdr-anchor) [class*="st-key-main_theme"] button p,
.block-container:has(.ui-hdr-anchor) [class*="st-key-hdr_theme"] button p,
.block-container:has(.ui-hdr-anchor) [class*="st-key-ui_theme"] button p,
.block-container:has(.ui-hdr-anchor) [class*="st-key-main_theme"] button span,
.block-container:has(.ui-hdr-anchor) [class*="st-key-hdr_theme"] button span,
.block-container:has(.ui-hdr-anchor) [class*="st-key-ui_theme"] button span {{
    opacity: 1 !important;
    visibility: visible !important;
    font-size: 22px !important;
    color: inherit !important;
}}
.block-container:has(.ui-hdr-anchor) [class*="st-key-ui_logout"] button,
.block-container:has(.ui-hdr-anchor) [class*="st-key-ui_logout"] [data-testid="stBaseButton-secondary"] {{
    box-sizing: border-box !important;
    height: 44px !important;
    min-height: 44px !important;
    max-height: 44px !important;
    transform: none !important;
}}
"""


def _dashboard() -> str:
    r = RADIUS[14]
    return f"""
.ui-hero {{
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: center;
    gap: 32px;
    margin: 0 !important; padding: 20px 24px !important;
    background: var(--ui-glass); backdrop-filter: blur(16px);
    border: 1px solid var(--ui-border); border-radius: {RADIUS[18]}px; box-shadow: var(--ui-shadow-sm);
    position: relative; overflow: hidden;
    min-height: 0 !important;
}}
@media (max-width: 768px) {{
    .ui-hero {{ grid-template-columns: 1fr; gap: 16px; padding: 16px 18px !important; }}
    .ui-hero-status {{ justify-self: start; }}
}}
[data-testid="stElementContainer"]:has(.ui-hero),
[data-testid="element-container"]:has(.ui-hero),
[data-testid="stElementContainer"]:has(.ui-how),
[data-testid="element-container"]:has(.ui-how),
[data-testid="stMarkdownContainer"]:has(.ui-hero),
[data-testid="stMarkdownContainer"]:has(.ui-how),
[data-testid="stMarkdownContainer"]:has(.ui-section) {{
    width: 100% !important;
    max-width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
}}
[data-testid="stElementContainer"]:has(.ui-hero),
[data-testid="element-container"]:has(.ui-hero) {{
    margin-bottom: 16px !important;
    min-height: 0 !important;
}}
[data-testid="stMarkdownContainer"]:has(.ui-hero) {{
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}}
.ui-hero-copy {{ position: relative; z-index: 1; max-width: 62ch; min-width: 0; }}
.ui-hero-status {{ position: relative; z-index: 1; display: flex; align-items: center; justify-content: flex-end; }}
.ui-hero::before {{
    content: ""; position: absolute; inset: 0;
    background: radial-gradient(ellipse 42% 120% at 100% 0%, var(--ui-accent-soft), transparent 70%);
    pointer-events: none;
}}
.ui-hero-kicker {{
    margin: 0 0 12px; font-size: 11px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase; color: var(--ui-primary) !important;
}}
.ui-hero-title {{
    font-family: 'Outfit', system-ui, sans-serif;
    font-size: clamp(28px, 2.2vw, 40px); font-weight: 700; letter-spacing: -0.03em;
    margin: 0; color: var(--ui-text) !important; line-height: 1.1;
}}
.ui-hero-lede {{
    margin: 16px 0 0; color: var(--ui-text-2) !important;
    font-size: 16px; line-height: 1.6; max-width: 42rem;
}}
.ui-page-intro {{ margin: 8px 0 12px; }}
.ui-page-intro h1 {{
    font-family: 'Outfit', system-ui, sans-serif;
    font-size: clamp(22px,1.8vw,28px); font-weight: 700; letter-spacing: -0.02em;
    margin: 0; color: var(--ui-text) !important; line-height: 1.2;
}}
.ui-page-intro p {{
    margin: 6px 0 0; color: var(--ui-text-2) !important;
    font-size: {TYPE['body']}px; max-width: 58ch;
}}
/* Analytics / History filter rhythm — avoid oversized top air */
.block-container:has(.ui-hdr-anchor) [data-testid="stSelectbox"] {{
    margin-top: 4px !important;
    margin-bottom: 8px !important;
}}
.block-container:has(.ui-hdr-anchor) [data-testid="stVerticalBlockBorderWrapper"] {{
    gap: 0.55rem !important;
}}
.ui-status {{
    display: inline-flex; align-items: center; gap: {SP[8]}px; font-size: {TYPE['small']}px; font-weight: 600;
    color: var(--ui-success) !important; background: var(--ui-success-soft);
    padding: {SP[8]}px {SP[16]}px; border-radius: 9999px; white-space: nowrap; flex-shrink: 0;
    border: 1px solid rgba(52,211,153,0.28); position: relative; z-index: 1;
}}
.ui-status-dot {{ width: 8px; height: 8px; border-radius: 50%; background: var(--ui-success); box-shadow: 0 0 8px var(--ui-success); }}

.ui-how {{
    margin: 0 0 {SP[32]}px; padding: {SP[12]}px {SP[16]}px;
    background: var(--ui-glass); border: 1px solid var(--ui-border);
    border-radius: {RADIUS[18]}px; box-shadow: var(--ui-shadow-sm);
}}
.ui-how-kicker {{
    margin: 0 0 {SP[12]}px; font-size: 11px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase; color: var(--ui-primary) !important;
}}
.ui-how-grid {{
    list-style: none; margin: 0; padding: 0;
    display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: {SP[16]}px; align-items: stretch;
}}
.ui-how-step {{
    display: flex; flex-direction: column; justify-content: center;
    height: 100%; min-height: 118px;
    padding: 20px 18px; border-radius: 12px;
    background: var(--ui-card); border: 1px solid var(--ui-border);
    box-shadow: var(--ui-shadow-sm);
    transition: transform 240ms {EASING}, box-shadow 240ms {EASING}, border-color 240ms {EASING};
}}
.ui-how-step:hover {{
    transform: translateY(-2px);
    border-color: var(--ui-border-strong);
    box-shadow: var(--ui-shadow-md);
}}
.ui-how-inner {{
    display: flex; gap: 12px; align-items: flex-start; min-width: 0;
}}
.ui-how-num {{
    flex: 0 0 auto; font-size: 12px; font-weight: 700; letter-spacing: 0.06em;
    color: var(--ui-accent) !important; line-height: 1.35; padding-top: 3px;
}}
.ui-how-body {{
    display: flex; flex-direction: column; gap: 6px; min-width: 0;
}}
.ui-how-title,
.ui-how-body strong.ui-how-title {{
    font-size: 16px; font-weight: 600; color: var(--ui-text) !important; line-height: 1.25;
}}
.ui-how-desc,
.ui-how-body span.ui-how-desc {{
    font-size: 13.5px; color: var(--ui-text-2) !important; line-height: 1.5;
}}
@media (prefers-reduced-motion: reduce) {{
    .ui-how-step {{ transition: none; }}
    .ui-how-step:hover {{ transform: none; }}
}}
@media (max-width: 1000px) {{
    .ui-how-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
}}
@media (max-width: 640px) {{
    .ui-how-grid {{ grid-template-columns: 1fr; }}
    .ui-how-step {{ min-height: 96px; }}
}}

.ui-stat-anchor {{ display: none; }}
.block-container:has(.ui-stat-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-stat) {{
    display: flex !important; align-items: stretch !important; gap: {SP[16]}px !important;
    width: 100% !important; margin: 0 !important; padding: 0 !important;
}}
.block-container:has(.ui-stat-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-stat) > [data-testid="column"] {{
    display: flex !important; flex: 1 1 0 !important; width: 0 !important; min-width: 0 !important;
    padding: 0 !important;
}}
.ui-stat {{
    flex: 1; width: 100%; min-height: 96px;
    display: flex; flex-direction: column; justify-content: center; gap: {SP[8]}px;
    padding: {SP[16]}px {SP[20]}px; background: var(--ui-card);
    border: 1px solid var(--ui-border); border-radius: {RADIUS[18]}px;
    box-shadow: var(--ui-shadow-sm); position: relative; overflow: hidden;
    color: var(--ui-text) !important;
    transition: transform 260ms {EASING}, box-shadow 260ms {EASING}, border-color 260ms {EASING};
}}
.ui-stat::before {{
    content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 3px;
    background: var(--ui-gradient); opacity: 0.9;
}}
.ui-stat:hover {{ transform: translateY(-2px); box-shadow: var(--ui-shadow-md); border-color: var(--ui-border-strong); }}
.ui-stat-label,
[data-testid="stMarkdownContainer"] .ui-stat-label {{
    font-size: {TYPE['caption']}px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
    color: var(--ui-text-3) !important;
}}
.ui-stat-value,
[data-testid="stMarkdownContainer"] .ui-stat-value {{
    font-size: 26px; font-weight: 700; letter-spacing: -0.02em;
    color: var(--ui-text) !important; line-height: 1.1;
}}
.ui-stat-hint,
[data-testid="stMarkdownContainer"] .ui-stat-hint {{
    font-size: {TYPE['caption']}px; color: var(--ui-text-2) !important;
}}

.ui-panel-anchor {{ display: none; }}
[data-testid="column"]:has(.ui-panel-anchor) > div[data-testid="stVerticalBlock"] {{
    background: var(--ui-glass); backdrop-filter: blur(16px);
    border: 1px solid var(--ui-border); border-radius: {RADIUS[18]}px;
    padding: {SP[20]}px {SP[20]}px {SP[16]}px; box-shadow: var(--ui-shadow-sm); gap: {SP[12]}px !important;
    min-height: 0 !important; height: 100% !important;
}}
[data-testid="column"]:has(.ui-panel-anchor) .ui-section {{ margin: 0 !important; }}
.ui-section {{ margin: {SP[32]}px 0 {SP[8]}px; }}
.ui-section h3 {{ font-family: 'Outfit', system-ui, sans-serif; font-size: {TYPE['h2']}px; font-weight: 700; color: var(--ui-text) !important; margin: 0; letter-spacing: -0.02em; }}
.ui-section p {{ font-size: {TYPE['small']}px; color: var(--ui-text-2) !important; margin: {SP[4]}px 0 0; }}

.ui-empty {{ text-align: center; padding: {SP[24]}px {SP[20]}px; border: 1px dashed var(--ui-border-strong); border-radius: {r}px; background: var(--ui-muted); }}
.ui-empty h4 {{ margin: {SP[8]}px 0 {SP[4]}px; color: var(--ui-text) !important; font-size: {TYPE['h3']}px; }}
.ui-empty p {{ margin: 0; color: var(--ui-text-2) !important; font-size: {TYPE['small']}px; }}
.ui-footer {{ margin-top: {SP[40]}px; padding-top: {SP[24]}px; border-top: 1px solid var(--ui-border); text-align: center; color: var(--ui-text-3) !important; font-size: {TYPE['caption']}px; }}
.ui-field-error {{ color: var(--ui-danger) !important; font-size: {TYPE['small']}px; margin: {SP[4]}px 0; }}
[data-testid="stExpander"] {{
    width: 100% !important;
    margin: {SP[12]}px 0 !important;
    border: 1px solid var(--ui-border) !important;
    border-radius: {r}px !important;
    background: var(--ui-card) !important;
}}
[data-testid="stAlert"] {{ margin: {SP[12]}px 0 !important; }}
[data-testid="stDownloadButton"] {{ margin-top: {SP[8]}px !important; }}
"""


def _tables() -> str:
    r = RADIUS[14]
    up_icon = (
        "%3Csvg xmlns='http://www.w3.org/2000/svg' width='34' height='34' fill='none' "
        "stroke='%2338BDF8' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E"
        "%3Cpath d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/%3E"
        "%3Cpath d='M17 8l-5-5-5 5'/%3E%3Cpath d='M12 3v12'/%3E%3C/svg%3E"
    )
    return f"""
/* Themed HTML tables (activity / history) — no pure black cells */
.ui-table-wrap {{
    width: 100%;
    overflow: auto;
    border: 1px solid var(--ui-border);
    border-radius: {r}px;
    background: var(--ui-table);
    box-shadow: var(--ui-shadow-sm);
}}
.ui-table {{
    width: 100%;
    border-collapse: collapse;
    min-width: 480px;
}}
.ui-table thead th {{
    position: sticky; top: 0; z-index: 1;
    background: var(--ui-table-head);
    color: var(--ui-text-2);
    font-size: {TYPE['caption']}px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    text-align: left;
    padding: 12px 16px;
    border-bottom: 1px solid var(--ui-border-strong);
}}
.ui-table tbody td {{
    padding: 12px 16px;
    font-size: {TYPE['small']}px;
    color: var(--ui-text);
    border-bottom: 1px solid var(--ui-border);
    background: var(--ui-table-row);
}}
.ui-table tbody tr:nth-child(even) td {{ background: var(--ui-table-row-alt); }}
.ui-table tbody tr:hover td {{ background: var(--ui-accent-soft); }}
.ui-table tbody tr:last-child td {{ border-bottom: none; }}

/* Native Streamlit dataframe outer chrome also theme-matched */
[data-testid="stDataFrame"] {{
    background: var(--ui-card) !important;
    border: 1px solid var(--ui-border) !important;
    border-radius: {r}px !important;
    overflow: hidden !important;
    box-shadow: var(--ui-shadow-sm) !important;
}}
[data-testid="stDataFrame"] > div {{
    background: var(--ui-card) !important;
}}
[data-testid="stPlotlyChart"] {{
    background: var(--ui-card); border: 1px solid var(--ui-border);
    border-radius: {r}px; padding: {SP[12]}px; box-shadow: var(--ui-shadow-sm);
    margin: {SP[8]}px 0 {SP[16]}px; width: 100% !important;
    max-width: 100% !important; overflow-x: hidden !important;
    min-height: 340px !important;
}}
[data-testid="stPlotlyChart"] > div {{
    width: 100% !important; max-width: 100% !important;
}}
[data-testid="stPlotlyChart"] iframe {{
    min-height: 320px !important;
    max-width: 100% !important;
}}
[data-testid="stFileUploader"] {{ background: transparent !important; border: none !important; padding: 0 !important; }}
[data-testid="stFileUploader"] label {{ display: none !important; }}
[data-testid="stFileUploaderDropzone"] {{
    flex-direction: column !important; align-items: center !important; text-align: center !important;
    gap: {SP[8]}px !important; padding: {SP[24]}px {SP[20]}px !important;
    min-height: 160px !important;
    background: var(--ui-muted) !important;
    border: 1.5px dashed var(--ui-border-strong) !important; border-radius: {r}px !important;
    transition: border-color {DURATION} {EASING}, background {DURATION} {EASING} !important;
}}
[data-testid="stFileUploaderDropzone"]:hover {{ border-color: var(--ui-primary) !important; background: var(--ui-accent-soft) !important; }}
[data-testid="stFileUploaderDropzone"]::before {{
    content: ""; width: 34px; height: 34px; margin-bottom: {SP[4]}px;
    background: url("data:image/svg+xml,{up_icon}") center/34px no-repeat;
}}
[data-testid="stFileUploaderDropzoneInstructions"] {{ color: var(--ui-text) !important; }}
[data-testid="stFileUploaderDropzoneInstructions"] span {{ font-size: {TYPE['body']}px !important; font-weight: 600 !important; color: var(--ui-text) !important; }}
[data-testid="stFileUploaderDropzoneInstructions"] small {{ font-size: {TYPE['caption']}px !important; color: var(--ui-text-3) !important; }}
[data-testid="stFileUploaderDropzone"] button {{
    width: auto !important; height: 40px !important; min-height: 40px !important;
    padding: 0 {SP[16]}px !important; margin-top: {SP[8]}px !important;
    border-radius: {RADIUS[10]}px !important; border: 1px solid var(--ui-border-strong) !important;
    background: var(--ui-elevated) !important; color: var(--ui-text) !important;
    font-weight: 600 !important; font-size: {TYPE['small']}px !important; box-shadow: none !important;
}}
[data-testid="stFileUploaderDropzone"] button:hover {{ background: var(--ui-card) !important; border-color: var(--ui-primary) !important; transform: none !important; }}
[data-testid="stFileUploaderFile"] {{
    background: var(--ui-card) !important; border: 1px solid var(--ui-border) !important;
    border-radius: {RADIUS[10]}px !important; padding: {SP[8]}px {SP[12]}px !important; margin-top: {SP[12]}px !important;
}}
[data-testid="stFileUploaderFileName"] {{ color: var(--ui-text) !important; font-size: {TYPE['small']}px !important; }}
[data-testid="stAlert"] {{ border-radius: {RADIUS[10]}px !important; border: 1px solid var(--ui-border) !important; }}
"""


def _auth() -> str:
    r = RADIUS[14]
    return f"""
.ui-auth-anchor {{ display: none; }}
/* Hide leftover app chrome while remapping to login (prevents multi logout icons) */
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .ui-brand,
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .ui-hero,
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .ui-how,
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .ui-stat,
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="st-key-ui_logout"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="stKey-ui_logout"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="st-key-hdr_profile"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="st-key-main_theme"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="st-key-hdr_theme"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="st-key-nav_"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [class*="stKey-nav_"] {{
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
    opacity: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}}
.ui-auth-texture {{
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
      radial-gradient(ellipse 55% 45% at 18% 22%, rgba(14,165,233,0.28), transparent 60%),
      radial-gradient(ellipse 45% 40% at 82% 78%, rgba(196,92,38,0.18), transparent 55%),
      linear-gradient(160deg, #060A12 0%, #0B1524 42%, #101E30 100%);
}}
.ui-auth-texture::before {{
    content: ""; position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse 70% 60% at 50% 40%, black 20%, transparent 75%);
    animation: ui-drift 14s ease-in-out infinite;
}}
.ui-auth-texture::after {{
    content: ""; position: absolute; inset: 0; opacity: 0.45;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E");
    mix-blend-mode: soft-light;
}}
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) {{
    overflow: hidden !important; height: 100vh !important;
    background: #060A12 !important;
}}
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) [data-testid="stAppViewBlockContainer"],
[data-testid="stAppViewContainer"]:has(.ui-auth-anchor) .block-container {{
    position: relative; z-index: 1;
}}
.block-container:has(.ui-auth-anchor) {{
    max-width: min(1180px, 94vw) !important; height: 100vh !important; display: flex !important;
    flex-direction: column !important; justify-content: center !important;
    padding: {SP[16]}px {SP[24]}px !important; overflow: hidden !important;
}}
.block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) {{
    align-items: stretch !important; gap: {SP[24]}px !important;
    min-height: clamp(560px, 78vh, 780px) !important;
}}
/* Left: branded ink panel */
.block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) > div:first-child {{
    background:
      linear-gradient(145deg, rgba(14,165,233,0.22) 0%, rgba(3,105,161,0.08) 40%, rgba(196,92,38,0.18) 100%),
      linear-gradient(180deg, rgba(12,22,38,0.55), rgba(8,14,24,0.35)) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: {RADIUS[24]}px !important;
    box-shadow: var(--ui-shadow-lg) !important;
    overflow: hidden !important;
    display: flex !important;
    flex-direction: column !important;
    padding: 0 !important;
    position: relative !important;
    backdrop-filter: blur(10px);
}}
.block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) > div:first-child > div {{
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
}}
.block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) > div:first-child::before {{
    content: ""; position: absolute; inset: 0; pointer-events: none;
    background:
      radial-gradient(circle at 20% 15%, rgba(255,255,255,0.14), transparent 28%),
      linear-gradient(120deg, transparent 40%, rgba(255,255,255,0.05) 50%, transparent 60%);
    background-size: 100% 100%, 220% 100%;
    animation: ui-shimmer 7s linear infinite;
}}
/* Right: light frost form (dark/light combination) */
.block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) > div:last-child {{
    background: linear-gradient(180deg, rgba(248,250,252,0.96), rgba(236,242,248,0.92)) !important;
    backdrop-filter: blur(22px);
    border: 1px solid rgba(255,255,255,0.55) !important;
    border-radius: {RADIUS[24]}px !important;
    box-shadow: var(--ui-shadow-lg) !important;
    padding: clamp(28px,3vw,48px) clamp(24px,2.6vw,44px) !important;
    display: flex !important; flex-direction: column !important; justify-content: center !important;
    color: #0B1220 !important;
}}
.block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) > div:last-child div[data-testid="stVerticalBlock"] {{
    gap: {SP[16]}px !important;
}}
/* Force light-form controls on auth right panel */
.block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) > div:last-child {{
    --ui-text: #0B1220;
    --ui-text-2: #3D4F66;
    --ui-text-3: #64748B;
    --ui-input: #FFFFFF;
    --ui-border: rgba(15,23,42,0.12);
    --ui-border-strong: rgba(15,23,42,0.20);
    --ui-elevated: #FFFFFF;
    --ui-muted: #Eef2F7;
    --ui-primary: #0F6E8C;
    --ui-gradient: linear-gradient(135deg,#0F6E8C 0%,#1B4F72 52%,#C45C26 100%);
}}
.ui-auth-brand {{
    padding: clamp(22px, 2.6vw, 36px) clamp(20px, 2.4vw, 36px);
    position: relative; z-index: 1;
    display: flex; flex-direction: column; height: 100%;
    gap: 0;
    overflow: auto;
}}
.ui-auth-enter {{
    animation: ui-auth-enter 560ms {EASING} both;
}}
.ui-auth-enter--1 {{ animation-delay: 40ms; }}
.ui-auth-enter--2 {{ animation-delay: 110ms; }}
.ui-auth-enter--3 {{ animation-delay: 180ms; }}
.ui-auth-enter--4 {{ animation-delay: 260ms; }}
.ui-auth-enter--5 {{ animation-delay: 340ms; }}
.ui-auth-enter--6 {{ animation-delay: 400ms; }}
.ui-auth-enter--7 {{ animation-delay: 460ms; }}
.ui-auth-enter--8 {{ animation-delay: 520ms; }}
.ui-auth-brand-logo {{ margin-bottom: 18px; }}
.ui-auth-headline {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: clamp(24px, 2.2vw, 34px);
    font-weight: 600;
    line-height: 1.2;
    letter-spacing: -0.02em;
    margin: 0 0 12px;
    color: #F8FAFC !important;
    max-width: 22ch;
}}
.ui-auth-lede {{
    font-size: 14px; line-height: 1.55;
    color: rgba(241,245,249,0.88) !important;
    margin: 0 0 18px; max-width: 46ch;
}}
.ui-auth-how-box {{
    margin: 0 0 16px;
    padding: 14px 14px 12px;
    border-radius: 14px;
    background: rgba(8,14,24,0.38);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
}}
.ui-auth-how-title {{
    margin: 0 0 10px;
    font-size: 12px; font-weight: 700;
    letter-spacing: 0.08em; text-transform: uppercase;
    color: #F0A06A !important;
    display: flex; align-items: center; gap: 8px;
}}
.ui-auth-how-gear {{
    font-size: 14px; line-height: 1; font-weight: 400;
    letter-spacing: 0; text-transform: none;
}}
.ui-auth-how-list {{
    list-style: none; margin: 0; padding: 0;
    display: grid; gap: 8px;
}}
.ui-auth-how-list li {{
    display: flex; gap: 10px; align-items: flex-start;
    font-size: 13px; line-height: 1.45;
    color: rgba(248,250,252,0.90) !important;
}}
.ui-auth-how-n {{
    flex: 0 0 auto;
    width: 20px; height: 20px;
    border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700;
    color: #0B1220 !important;
    background: linear-gradient(135deg, #67E8F9, #F0A06A);
    margin-top: 1px;
}}
.ui-auth-features {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    margin-top: auto;
}}
.ui-auth-feat {{
    padding: 14px 14px;
    min-height: 78px;
    border-radius: 12px;
    background: rgba(8,14,24,0.32);
    border: 1px solid rgba(255,255,255,0.10);
    display: flex; flex-direction: column; justify-content: center; gap: 4px;
    transition: transform 240ms {EASING}, border-color 240ms {EASING}, box-shadow 240ms {EASING}, background 240ms {EASING};
}}
.ui-auth-feat:hover {{
    transform: translateY(-2px);
    border-color: rgba(103,232,249,0.35);
    box-shadow: 0 8px 24px rgba(0,0,0,0.28);
    background: linear-gradient(160deg, rgba(14,165,233,0.18), rgba(8,14,24,0.40));
}}
.ui-auth-feat strong {{
    font-size: 13px; font-weight: 700;
    color: #F8FAFC !important; line-height: 1.2;
}}
.ui-auth-feat span {{
    font-size: 12px; line-height: 1.4;
    color: rgba(226,232,240,0.78) !important;
}}
.ui-auth-card-head {{ margin-bottom: {SP[8]}px; text-align: left; }}
.ui-auth-card-head h2 {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: clamp(26px,2vw,32px); font-weight: 600;
    margin: 0 0 {SP[8]}px; color: #0B1220 !important; letter-spacing: -0.02em;
}}
.ui-auth-card-head p {{ font-size: {TYPE['body']}px; color: #3D4F66 !important; margin: 0; }}
.st-key-login_remember {{ display: flex !important; align-items: center !important; }}
.st-key-login_remember label {{ margin: 0 !important; font-size: {TYPE['small']}px !important; color: #3D4F66 !important; }}
.ui-auth-foot {{
    position: relative; z-index: 1;
    text-align: center; margin-top: {SP[16]}px;
    font-size: {TYPE['caption']}px; color: rgba(226,232,240,0.65) !important;
}}
.ui-loading {{
    position: fixed; inset: 0; z-index: 999999; display: flex; align-items: center; justify-content: center;
    background: rgba(6,10,18,0.92); backdrop-filter: blur(10px);
}}
.ui-loading-card {{
    display: flex; flex-direction: column; align-items: center; gap: {SP[12]}px;
    padding: {SP[24]}px {SP[32]}px; border-radius: {r}px;
    background: #F8FAFC; border: 1px solid rgba(15,23,42,0.1); box-shadow: var(--ui-shadow-lg);
}}
@media (max-width: 1100px) {{
    .ui-auth-headline {{ font-size: clamp(22px, 2.4vw, 28px); max-width: none; }}
    .ui-auth-lede {{ font-size: 13px; }}
}}
@media (max-width: 900px) {{
    .block-container:has(.ui-auth-anchor) {{
        justify-content: flex-start !important; min-height: auto !important; height: auto !important;
        padding: {SP[16]}px {SP[16]}px {SP[24]}px !important; overflow: auto !important;
    }}
    .block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) {{
        flex-direction: column !important;
        min-height: 0 !important;
        gap: {SP[16]}px !important;
    }}
    .block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) > div:first-child,
    .block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) > div:last-child {{
        width: 100% !important;
    }}
    .ui-auth-brand {{ overflow: visible; }}
    [data-testid="stAppViewContainer"]:has(.ui-auth-anchor) {{ height: auto !important; overflow: auto !important; }}
}}
@media (max-width: 480px) {{
    .ui-auth-features {{ grid-template-columns: 1fr; }}
    .ui-auth-headline {{ font-size: 22px; }}
}}
@media (prefers-reduced-motion: reduce) {{
    .ui-auth-texture::before,
    .block-container:has(.ui-auth-anchor) div[data-testid="stHorizontalBlock"]:has(.ui-auth-brand) > div:first-child::before,
    .ui-auth-enter, .ui-auth-feat {{
        animation: none !important;
    }}
    .ui-auth-feat {{ transition: none; }}
    .ui-auth-feat:hover {{ transform: none; }}
}}
"""


def build_global_css(*, login: bool = False) -> str:
    from src.ui.logo import LOGO_CSS

    sections = [
        _vars(),
        _base(),
        LOGO_CSS,
        _buttons(),
        _inputs(),
        _tables(),
        _dashboard(),
        _ctrl_buttons(),
    ]
    sections.append(_auth() if login else _header())
    return "<style>\n" + "\n".join(sections) + "\n</style>"
