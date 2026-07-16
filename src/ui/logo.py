"""Hexagonal Crystal Core — animated SVG logo (no letters, no initials)."""

from __future__ import annotations

import uuid

SIZE_MAP = {"xs": 16, "sm": 24, "md": 40, "lg": 56, "xl": 80, "2xl": 128}

LOGO_CSS = """
.ui-crystal { display: inline-block; vertical-align: middle; line-height: 0; flex-shrink: 0; }
.ui-crystal.is-interactive { cursor: pointer; transition: transform 280ms cubic-bezier(0.34,1.56,0.64,1); }
.ui-crystal.is-interactive:hover { transform: scale(1.08); }
@keyframes ui-logo-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes ui-logo-float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
@keyframes ui-logo-breathe { 0%,100% { opacity: 0.45; } 50% { opacity: 0.85; } }
@keyframes ui-logo-pulse { 0%,100% { opacity: 0.8; transform: scale(1); } 50% { opacity: 1; transform: scale(1.06); } }
@keyframes ui-logo-shine { 0% { transform: translateX(-80px) skewX(-12deg); opacity: 0; } 50% { transform: translateX(80px) skewX(-12deg); opacity: 0.35; } 100% { opacity: 0; } }
@keyframes ui-logo-sparkle { 0%,88%,100% { opacity: 0; transform: scale(0); } 90% { opacity: 0.9; transform: scale(1.3); } }
.ui-crystal.is-animated .ui-logo-float { animation: ui-logo-float 4s ease-in-out infinite; }
.ui-crystal.is-animated .ui-logo-spin { animation: ui-logo-spin 10s linear infinite; transform-origin: 50px 50px; }
.ui-crystal.is-animated .ui-logo-glow { animation: ui-logo-breathe 3s ease-in-out infinite; }
.ui-crystal.is-animated .ui-logo-core { animation: ui-logo-pulse 3s ease-in-out infinite; transform-origin: 50px 50px; }
.ui-crystal.is-animated .ui-logo-shine { animation: ui-logo-shine 5.5s ease-in-out infinite; }
.ui-crystal.is-animated .ui-logo-sparkle { animation: ui-logo-sparkle 7s ease-in-out infinite; }
.ui-brand-row { display: flex; align-items: center; gap: 12px; }
.ui-brand-text { font-size: 16px; font-weight: 700; letter-spacing: -0.02em; color: var(--ui-text); }
.ui-brand-text--light { color: #fff !important; }
@media (prefers-reduced-motion: reduce) {
  .ui-crystal.is-animated .ui-logo-float,
  .ui-crystal.is-animated .ui-logo-spin,
  .ui-crystal.is-animated .ui-logo-glow,
  .ui-crystal.is-animated .ui-logo-core,
  .ui-crystal.is-animated .ui-logo-shine,
  .ui-crystal.is-animated .ui-logo-sparkle { animation: none !important; }
}
"""


def _uid() -> str:
    return uuid.uuid4().hex[:8]


def crystal_svg(
    size: str | int = "md",
    *,
    animated: bool = True,
    glow: bool = True,
    interactive: bool = False,
    uid: str | None = None,
) -> str:
    px = SIZE_MAP[size] if isinstance(size, str) else int(size)
    uid = uid or _uid()
    cls = ["ui-crystal"]
    if animated:
        cls.append("is-animated")
    if interactive:
        cls.append("is-interactive")
    glow_filter = f'filter="url(#glow-{uid})"' if glow else ""
    bg_opacity = "0.55" if glow else "0.2"

    return f"""<span class="{' '.join(cls)}" style="width:{px}px;height:{px}px" role="img" aria-label="DataSentinel">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="{px}" height="{px}" fill="none">
  <defs>
    <linearGradient id="edge-{uid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8B5CF6"/><stop offset="45%" stop-color="#5B5CEB"/><stop offset="100%" stop-color="#38BDF8"/>
    </linearGradient>
    <linearGradient id="face-{uid}" x1="30%" y1="0%" x2="70%" y2="100%">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.35"/><stop offset="100%" stop-color="#5B5CEB" stop-opacity="0.12"/>
    </linearGradient>
    <radialGradient id="core-{uid}" cx="50%" cy="45%" r="45%">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.95"/>
      <stop offset="55%" stop-color="#38BDF8" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#5B5CEB" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="shine-{uid}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <filter id="glow-{uid}" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g class="ui-logo-float">
    <g class="ui-logo-spin">
      <ellipse class="ui-logo-glow" cx="50" cy="54" rx="30" ry="9" fill="rgba(91,92,235,{bg_opacity})"/>
      <polygon points="50,6 88,27 88,69 50,90 12,69 12,27" fill="url(#face-{uid})" stroke="url(#edge-{uid})" stroke-width="1.4" stroke-linejoin="round"/>
      <polygon points="50,16 78,31 78,65 50,80 22,65 22,31" fill="none" stroke="#38BDF8" stroke-width="0.7" stroke-opacity="0.45" stroke-linejoin="round"/>
      <polygon points="50,26 68,36 68,60 50,70 32,60 32,36" fill="url(#core-{uid})" stroke="#00E5FF" stroke-width="0.6" stroke-opacity="0.7" class="ui-logo-core" {glow_filter}/>
      <line x1="50" y1="16" x2="50" y2="80" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="0.5"/>
      <rect class="ui-logo-shine" x="0" y="0" width="22" height="100" fill="url(#shine-{uid})" opacity="0.4" style="mix-blend-mode:overlay"/>
    </g>
    <circle class="ui-logo-sparkle" cx="74" cy="20" r="1.8" fill="#FFFFFF"/>
  </g>
</svg>
</span>"""


def brand_html(
    size: str = "md",
    *,
    animated: bool = True,
    glow: bool = True,
    light_text: bool = False,
    show_wordmark: bool = True,
    interactive: bool = False,
) -> str:
    text_cls = "ui-brand-text ui-brand-text--light" if light_text else "ui-brand-text"
    wordmark = f'<span class="{text_cls}">DataSentinel</span>' if show_wordmark else ""
    return f'<div class="ui-brand-row">{crystal_svg(size, animated=animated, glow=glow, interactive=interactive)}{wordmark}</div>'
