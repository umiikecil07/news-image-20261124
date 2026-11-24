"""Drawing toolkit for the front page.

Fonts ship in fonts/ beside this file so rendering is identical in any
sandbox; system paths are only a fallback. Everything is measured with the
font actually loaded, so text wraps adapt instead of overflowing.
"""

import os

from PIL import ImageDraw, ImageFont

_HERE = os.path.dirname(os.path.abspath(__file__))

_FONT_FILES = {
    "black": "NotoSans-Black.ttf",
    "regular": "NotoSans-Regular.ttf",
}

_SYSTEM_DIRS = [
    "/usr/share/fonts/truetype/noto",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
]

_SYSTEM_NAMES = {
    "black": ["NotoSans-Black.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"],
    "regular": ["NotoSans-Regular.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"],
}


def load_font(kind, size):
    """Load a font of the given kind and size, with fallbacks."""
    name = _FONT_FILES[kind]
    for path in (os.path.join(_HERE, "fonts", name),):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    for folder in _SYSTEM_DIRS:
        for candidate in _SYSTEM_NAMES[kind]:
            path = os.path.join(folder, candidate)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, text, font, fill, max_width, leading, max_lines=None):
    """Draw wrapped text; returns the y just below the last line.

    When max_lines is set, extra lines are dropped and the last shown
    line gets an ellipsis.
    """
    lines = wrap(draw, text, font, max_width)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(". ") + "…"
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def rising_chart(draw, box, colour, ink):
    """Draw a rising candlestick chart with an arrow inside box.

    box is (x0, y0, x1, y1). Candles climb left to right; a bold arrow
    rides above them.
    """
    x0, y0, x1, y1 = box
    n = 7
    slot = (x1 - x0) / n
    base = y1 - 14
    tops = [base - 8, base - 22, base - 18, base - 42, base - 34, base - 62, base - 88]
    bottoms = [base, base - 6, base - 2, base - 24, base - 16, base - 44, base - 70]
    for i in range(n):
        cx = x0 + slot * i + slot / 2
        w = slot * 0.42
        draw.line([(cx, tops[i] - 8), (cx, bottoms[i] + 6)], fill=ink, width=2)
        draw.rectangle([cx - w / 2, tops[i], cx + w / 2, bottoms[i]], fill=colour)
    # axis
    draw.line([(x0, y1 - 8), (x1, y1 - 8)], fill=ink, width=2)
    # arrow
    ax0, ay0 = x0 + 6, base - 84
    ax1, ay1 = x1 - 10, y0 + 16
    draw.line([(ax0, ay0), (ax1, ay1)], fill=colour, width=5)
    draw.polygon(
        [(ax1, ay1), (ax1 - 16, ay1 + 2), (ax1 - 2, ay1 + 16)],
        fill=colour,
    )


def icon(draw, kind, cx, cy, r, colour, ink):
    """Draw a small pictogram centred on (cx, cy) with radius r."""
    if kind == "tanker":
        # hull
        draw.polygon(
            [(cx - r, cy + r * 0.15), (cx + r, cy + r * 0.15),
             (cx + r * 0.75, cy + r * 0.65), (cx - r * 0.75, cy + r * 0.65)],
            fill=colour,
        )
        # containers
        for i, h in enumerate((0.5, 0.75, 0.55)):
            x = cx - r * 0.8 + i * r * 0.55
            draw.rectangle(
                [x, cy - r * h, x + r * 0.45, cy + r * 0.1], fill=ink
            )
        # funnel
        draw.rectangle([cx + r * 0.45, cy - r * 0.9, cx + r * 0.8, cy - r * 0.1], fill=ink)
        # waves
        for dx in (-0.7, 0.0, 0.7):
            draw.arc(
                [cx + dx * r - r * 0.28, cy + r * 0.72, cx + dx * r + r * 0.28, cy + r * 1.05],
                0, 180, fill=ink, width=3,
            )
    elif kind == "ship":
        draw.polygon(
            [(cx - r, cy + r * 0.2), (cx + r, cy + r * 0.2),
             (cx + r * 0.7, cy + r * 0.7), (cx - r * 0.7, cy + r * 0.7)],
            fill=colour,
        )
        draw.line([(cx, cy - r), (cx, cy + r * 0.2)], fill=ink, width=4)
        draw.polygon([(cx, cy - r), (cx, cy - r * 0.25), (cx + r * 0.55, cy - r * 0.25)], fill=ink)
        draw.line([(cx - r * 0.9, cy + r * 0.85), (cx + r * 0.9, cy + r * 0.85)], fill=ink, width=3)
    elif kind == "shield":
        pts = [
            (cx, cy - r), (cx + r * 0.85, cy - r * 0.55), (cx + r * 0.85, cy + r * 0.1),
            (cx, cy + r), (cx - r * 0.85, cy + r * 0.1), (cx - r * 0.85, cy - r * 0.55),
        ]
        draw.polygon(pts, fill=colour)
        # star
        sx, sy, sr = cx, cy - r * 0.05, r * 0.42
        star = []
        for i in range(10):
            ang = -90 + i * 36
            rad = sr if i % 2 == 0 else sr * 0.45
            import math
            star.append((sx + rad * math.cos(math.radians(ang)),
                         sy + rad * math.sin(math.radians(ang))))
        draw.polygon(star, fill=(255, 255, 255))
    elif kind == "chip":
        draw.rectangle(
            [cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7],
            fill=colour,
        )
        draw.rectangle(
            [cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35],
            outline=(255, 255, 255), width=3,
        )
        for i in range(3):
            off = -r * 0.4 + i * r * 0.4
            draw.line([(cx + off, cy - r), (cx + off, cy - r * 0.7)], fill=ink, width=3)
            draw.line([(cx + off, cy + r * 0.7), (cx + off, cy + r)], fill=ink, width=3)
            draw.line([(cx - r, cy + off), (cx - r * 0.7, cy + off)], fill=ink, width=3)
            draw.line([(cx + r * 0.7, cy + off), (cx + r, cy + off)], fill=ink, width=3)
