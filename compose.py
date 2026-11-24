"""Compose the 1024x1024 front page for 24 November 2026.

Layout, top to bottom: navy masthead band, red rule, ticker strip, a
full-width lead (Nvidia comeback) with a drawn share chart, a navy markets
band, a 2x2 grid of story cards with drawn pictograms, a two-story strip,
and a footer. A flowing y cursor keeps every section inside the page.
"""

from PIL import Image, ImageDraw

import data
from toolkit import hline, icon, load_font, rising_chart, text_block, wrap

W = 1024
H = 1024
MARGIN = 28
CW = W - 2 * MARGIN  # content width

INK = (20, 20, 20)
NAVY = (20, 49, 92)
RED = (179, 38, 30)
GREEN = (30, 122, 52)
PAPER = (255, 255, 255)
PANEL = (242, 243, 245)
GREY = (85, 85, 85)
LINE = (205, 205, 205)


def _fonts():
    return {
        "masthead": load_font("black", 54),
        "date_big": load_font("black", 25),
        "date_small": load_font("black", 19),
        "ticker": load_font("regular", 20),
        "kicker": load_font("black", 18),
        "lead_head": load_font("black", 58),
        "lead_body": load_font("regular", 20),
        "chart_big": load_font("black", 56),
        "chart_label": load_font("black", 17),
        "band": load_font("black", 20),
        "card_kicker": load_font("black", 16),
        "card_head": load_font("black", 27),
        "card_body": load_font("regular", 17),
        "strip_kicker": load_font("black", 15),
        "strip_head": load_font("black", 23),
        "strip_body": load_font("regular", 17),
        "foot": load_font("regular", 16),
    }


def _masthead(draw, f):
    draw.rectangle([0, 0, W, 92], fill=NAVY)
    draw.text((MARGIN, 18), data.MASTHEAD, font=f["masthead"], fill=PAPER)
    right = f"24 NOVEMBER 2026"
    tw = draw.textlength(right, font=f["date_big"])
    draw.text((W - MARGIN - tw, 16), right, font=f["date_big"], fill=PAPER)
    sub = "TUESDAY"
    tw2 = draw.textlength(sub, font=f["date_small"])
    draw.text((W - MARGIN - tw2, 50), sub, font=f["date_small"], fill=(200, 210, 225))
    draw.rectangle([0, 92, W, 98], fill=RED)
    return 98


def _lead(draw, f, y):
    lead = data.LEAD
    left_w = 592
    # kicker
    draw.text((MARGIN, y), lead["kicker"], font=f["kicker"], fill=RED)
    y_head = y + 26
    # headline, two lines
    lines = ["HUANG IS BACK", "AT NVIDIA"]
    hy = y_head
    for line in lines:
        draw.text((MARGIN, hy), line, font=f["lead_head"], fill=INK)
        hy += 62
    by = hy + 8
    by = text_block(draw, MARGIN, by, lead["body"], f["lead_body"], INK,
                    left_w, 27, max_lines=5)
    # chart panel on the right
    px0, px1 = 648, W - MARGIN
    py0, py1 = y, by
    draw.rectangle([px0, py0, px1, py1], fill=PANEL, outline=LINE, width=2)
    draw.text((px0 + 18, py0 + 14), "THE COMEBACK, IN SHARES",
              font=f["chart_label"], fill=GREY)
    big = "+31%"
    bw = draw.textlength(big, font=f["chart_big"])
    draw.text((px0 + 18, py0 + 38), big, font=f["chart_big"], fill=GREEN)
    draw.text((px0 + 18 + bw + 12, py0 + 62), "NVIDIA SHARES",
              font=f["chart_label"], fill=INK)
    rising_chart(draw, (px0 + 18, py0 + 108, px1 - 18, py1 - 44),
                 GREEN, INK)
    draw.text((px0 + 18, py1 - 36), "NASDAQ +6.5%  ·  A WEEK AFTER -10%",
              font=f["chart_label"], fill=INK)
    return by


def _markets_band(draw, f, y):
    draw.rectangle([0, y, W, y + 44], fill=NAVY)
    parts = " · ".join(f"{name} {val}" for name, val in data.MARKETS)
    tw = draw.textlength(parts, font=f["band"])
    draw.text(((W - tw) / 2, y + 10), parts, font=f["band"], fill=PAPER)
    return y + 44


def _card(draw, f, x, y, w, h, story):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=LINE, width=2)
    draw.rectangle([x, y, x + w, y + 6], fill=RED)
    ix, iy = x + w - 42, y + 34
    icon(draw, story["icon"], ix, iy, 24, RED, INK)
    tx = x + 16
    tw = w - 100
    draw.text((tx, y + 18), story["kicker"], font=f["card_kicker"], fill=RED)
    hy = y + 44
    for line in wrap(draw, story["headline"], f["card_head"], tw)[:2]:
        draw.text((tx, hy), line, font=f["card_head"], fill=INK)
        hy += 30
    text_block(draw, tx, hy + 4, story["body"], f["card_body"], INK,
               w - 32, 22, max_lines=3)
    return y + h


def _grid(draw, f, y):
    gap = 16
    w = (CW - gap) // 2
    h = 184
    x0 = MARGIN
    x1 = MARGIN + w + gap
    _card(draw, f, x0, y, w, h, data.CARDS[0])
    _card(draw, f, x1, y, w, h, data.CARDS[1])
    _card(draw, f, x0, y + h + gap, w, h, data.CARDS[2])
    _card(draw, f, x1, y + h + gap, w, h, data.CARDS[3])
    return y + 2 * h + gap


def _strip(draw, f, y):
    gap = 16
    w = (CW - gap) // 2
    for i, story in enumerate(data.STRIP):
        x = MARGIN + i * (w + gap)
        draw.text((x, y), story["kicker"], font=f["strip_kicker"], fill=RED)
        hy = y + 22
        for line in wrap(draw, story["headline"], f["strip_head"], w)[:1]:
            draw.text((x, hy), line, font=f["strip_head"], fill=INK)
            hy += 28
        text_block(draw, x, hy + 2, story["body"], f["strip_body"], GREY,
                   w, 22, max_lines=2)
    return y + 88


def _footer(draw, f, y):
    hline(draw, MARGIN, W - MARGIN, y, INK, 2)
    wire = "  |  ".join(data.WIRE)
    tw = draw.textlength(wire, font=f["foot"])
    draw.text(((W - tw) / 2, y + 8), wire, font=f["foot"], fill=GREY)
    fw = draw.textlength(data.FOOTER, font=f["foot"])
    draw.text(((W - fw) / 2, y + 30), data.FOOTER, font=f["foot"], fill=GREY)
    sw = draw.textlength(data.SOURCES, font=f["foot"])
    draw.text(((W - sw) / 2, y + 52), data.SOURCES, font=f["foot"], fill=GREY)
    return y + 68


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    f = _fonts()
    y = _masthead(draw, f)
    y = _lead(draw, f, y + 10)
    y = _markets_band(draw, f, y + 10)
    y = _grid(draw, f, y + 10)
    y = _strip(draw, f, y + 10)
    y = _footer(draw, f, y + 8)
    assert y <= H, f"page overflow: {y} > {H}"
    return img
