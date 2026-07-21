"""Generate PNG favicon sizes from the static crystal SVG."""

from __future__ import annotations

import math
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "brand")

# Hexagon vertices in 100x100 viewBox space (from logo-static.svg)
OUTER = [(50, 6), (88, 27), (88, 69), (50, 90), (12, 69), (12, 27)]
INNER = [(50, 26), (68, 36), (68, 60), (50, 70), (32, 60), (32, 36)]


def _scale(points: list[tuple[float, float]], size: int, pad: float = 0.08) -> list[tuple[float, float]]:
    scale = size * (1 - pad * 2) / 100
    offset = size * pad
    return [(x * scale + offset, y * scale + offset) for x, y in points]


def _lerp_color(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def _draw_hex(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    outer = _scale(OUTER, size)
    inner = _scale(INNER, size)
    cx = size / 2
    cy = size * 0.48

    # Background glow ellipse
    glow_h = max(2, int(size * 0.09))
    glow_w = max(6, int(size * 0.58))
    draw.ellipse(
        (cx - glow_w / 2, cy - glow_h / 2, cx + glow_w / 2, cy + glow_h / 2),
        fill=(91, 92, 235, int(90 * (size / 128))),
    )

    # Outer face fill (purple tint)
    draw.polygon(outer, fill=(91, 92, 235, 38))

    # Outer stroke gradient approximation
    for i in range(len(outer)):
        p1 = outer[i]
        p2 = outer[(i + 1) % len(outer)]
        t = i / len(outer)
        color = _lerp_color((139, 92, 246), (56, 189, 248), t)
        draw.line([p1, p2], fill=(*color, 255), width=max(1, size // 64))

    # Inner core — cyan glow
    core_fill = (0, 229, 255, 220 if size >= 32 else 200)
    draw.polygon(inner, fill=core_fill)
    draw.polygon(inner, outline=(0, 229, 255, 180), width=max(1, size // 80))

    # Center highlight
    r = max(1, size // 16)
    draw.ellipse((cx - r, cy - r - size * 0.04, cx + r, cy + r - size * 0.04), fill=(255, 255, 255, 180))

    return img


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    sizes = [16, 32, 64, 128, 256, 512]
    for size in sizes:
        path = os.path.join(OUT_DIR, f"favicon-{size}.png")
        _draw_hex(size).save(path, "PNG")
        print(f"Wrote {path}")

    favicon = os.path.join(OUT_DIR, "favicon.png")
    _draw_hex(32).save(favicon, "PNG")
    print(f"Wrote {favicon}")


if __name__ == "__main__":
    sys.exit(main())
