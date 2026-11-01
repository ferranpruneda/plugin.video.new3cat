#!/usr/bin/env python3
"""Draw original, childlike artwork for the Infantil section.

Shapes only: sun, clouds, hills, balloons, stars and numerals.
No channel logos and no characters from any show.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resources" / "media" / "kids"
FONT = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Bold.ttf"

NAVY = (43, 58, 92, 255)
CREAM = (255, 250, 236, 255)
SUN = (255, 196, 54, 255)
CORAL = (255, 107, 107, 255)
SKY = (77, 166, 255, 255)
MINT = (78, 205, 163, 255)
LILAC = (176, 140, 255, 255)
PINK = (255, 143, 191, 255)
ORANGE = (255, 149, 77, 255)
WHITE = (255, 255, 255, 255)
HILL = (110, 207, 122, 255)
HILL_DARK = (72, 176, 112, 255)


def _blank(w, h, color=(0, 0, 0, 0)):
    return Image.new("RGBA", (w, h), color)


def _gradient(w, h, top, bottom):
    column = Image.new("RGB", (1, h))
    pixels = column.load()
    for y in range(h):
        mix = y / max(1, h - 1)
        pixels[0, y] = tuple(int(top[i] * (1 - mix) + bottom[i] * mix) for i in range(3))
    return column.resize((w, h), Image.Resampling.NEAREST).convert("RGBA")


def _circle(draw, cx, cy, radius, fill, outline=None, width=0):
    box = (cx - radius, cy - radius, cx + radius, cy + radius)
    draw.ellipse(box, fill=fill, outline=outline, width=width)


def _star(cx, cy, outer, inner, points=5, rotation=-math.pi / 2):
    coords = []
    for index in range(points * 2):
        radius = outer if index % 2 == 0 else inner
        angle = rotation + index * math.pi / points
        coords.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return coords


def _cloud(draw, cx, cy, scale=1.0, fill=WHITE):
    radii = (34 * scale, 26 * scale, 22 * scale)
    offsets = ((-28 * scale, 6 * scale), (8 * scale, -8 * scale), (30 * scale, 8 * scale))
    for (dx, dy), radius in zip(offsets, radii):
        _circle(draw, cx + dx, cy + dy, radius, fill)
    draw.rounded_rectangle(
        (cx - 48 * scale, cy + 4 * scale, cx + 52 * scale, cy + 28 * scale),
        radius=16 * scale,
        fill=fill,
    )


def _balloon(draw, cx, cy, color, scale=1.0):
    rx, ry = 28 * scale, 36 * scale
    draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=color, outline=NAVY, width=max(3, int(4 * scale)))
    knot = [(cx, cy + ry + 10 * scale), (cx - 8 * scale, cy + ry - 2 * scale), (cx + 8 * scale, cy + ry - 2 * scale)]
    draw.polygon(knot, fill=color, outline=NAVY)
    draw.line((cx, cy + ry + 8 * scale, cx + 10 * scale, cy + ry + 70 * scale), fill=NAVY, width=max(2, int(3 * scale)))
    # shine
    _circle(draw, cx - 8 * scale, cy - 10 * scale, 6 * scale, (255, 255, 255, 180), outline=None)


def _sun(draw, cx, cy, radius):
    for index in range(12):
        angle = index * math.pi / 6
        x1 = cx + math.cos(angle) * (radius + 8)
        y1 = cy + math.sin(angle) * (radius + 8)
        x2 = cx + math.cos(angle) * (radius + 28)
        y2 = cy + math.sin(angle) * (radius + 28)
        draw.line((x1, y1, x2, y2), fill=ORANGE, width=8)
    _circle(draw, cx, cy, radius, SUN, NAVY, 6)
    _circle(draw, cx - 14, cy - 4, 6, NAVY)
    _circle(draw, cx + 14, cy - 4, 6, NAVY)
    draw.arc((cx - 16, cy - 2, cx + 16, cy + 18), 20, 160, fill=NAVY, width=5)


def _rainbow(draw, cx, cy, radius):
    bands = (CORAL, ORANGE, SUN, MINT, SKY, LILAC)
    for index, color in enumerate(bands):
        inset = index * 16
        box = (cx - radius + inset, cy - radius + inset, cx + radius - inset, cy + radius - inset)
        draw.arc(box, 200, 340, fill=color, width=14)


def _card(base_color):
    image = _blank(512, 512, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((16, 16, 496, 496), radius=96, fill=base_color, outline=NAVY, width=12)
    draw.rounded_rectangle((48, 48, 464, 464), radius=78, fill=CREAM)
    return image, ImageDraw.Draw(image)


def _poster(base_color, draw_symbol):
    image = _gradient(480, 720, base_color[:3], (255, 248, 230))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((18, 18, 462, 702), radius=48, outline=NAVY, width=10)
    _circle(draw, 240, 280, 150, CREAM, NAVY, 8)
    draw_symbol(draw, 240, 280, 1.15)
    draw.polygon([(0, 620), (140, 540), (280, 640), (480, 520), (480, 720), (0, 720)], fill=HILL)
    draw.polygon([(180, 640), (360, 560), (480, 640), (480, 720), (180, 720)], fill=HILL_DARK)
    return image


def symbol_home(draw, cx, cy, scale):
    _rainbow(draw, cx, cy + 30 * scale, 120 * scale)
    _sun(draw, cx, cy + 10 * scale, 42 * scale)


def symbol_live(draw, cx, cy, scale):
    draw.rounded_rectangle(
        (cx - 90 * scale, cy - 70 * scale, cx + 90 * scale, cy + 60 * scale),
        radius=24 * scale,
        fill=SKY,
        outline=NAVY,
        width=int(8 * scale),
    )
    draw.polygon(
        [
            (cx - 24 * scale, cy - 36 * scale),
            (cx - 24 * scale, cy + 32 * scale),
            (cx + 40 * scale, cy - 2 * scale),
        ],
        fill=SUN,
        outline=NAVY,
    )
    draw.polygon(_star(cx + 78 * scale, cy - 78 * scale, 28 * scale, 12 * scale), fill=CORAL)


def symbol_programmes(draw, cx, cy, scale):
    colors = (PINK, SKY, SUN)
    offsets = (-46, -8, 30)
    for color, dx in zip(colors, offsets):
        draw.rounded_rectangle(
            (cx - 70 * scale + dx, cy - 80 * scale, cx + 50 * scale + dx, cy + 80 * scale),
            radius=18 * scale,
            fill=color,
            outline=NAVY,
            width=int(6 * scale),
        )


def symbol_ages(draw, cx, cy, scale):
    _balloon(draw, cx - 70 * scale, cy - 10 * scale, CORAL, scale * 0.85)
    _balloon(draw, cx + 10 * scale, cy - 40 * scale, SKY, scale)
    _balloon(draw, cx + 78 * scale, cy, SUN, scale * 0.75)


def symbol_petits(draw, cx, cy, scale):
    _circle(draw, cx, cy + 10 * scale, 70 * scale, PINK, NAVY, int(7 * scale))
    _circle(draw, cx - 22 * scale, cy - 4 * scale, 8 * scale, NAVY)
    _circle(draw, cx + 22 * scale, cy - 4 * scale, 8 * scale, NAVY)
    draw.arc(
        (cx - 28 * scale, cy + 4 * scale, cx + 28 * scale, cy + 40 * scale),
        20,
        160,
        fill=NAVY,
        width=int(5 * scale),
    )
    draw.ellipse(
        (cx - 18 * scale, cy - 78 * scale, cx + 18 * scale, cy - 48 * scale),
        fill=CORAL,
        outline=NAVY,
        width=int(4 * scale),
    )


def symbol_tots(draw, cx, cy, scale):
    colors = (CORAL, ORANGE, SUN, MINT, SKY, LILAC)
    for index, color in enumerate(colors):
        angle = -math.pi / 2 + index * math.pi / 3
        _circle(draw, cx + math.cos(angle) * 62 * scale, cy + math.sin(angle) * 62 * scale, 28 * scale, color, NAVY, int(5 * scale))
    _circle(draw, cx, cy, 22 * scale, WHITE, NAVY, int(5 * scale))


def symbol_number(draw, cx, cy, scale, label, color):
    font = ImageFont.truetype(FONT, int(150 * scale))
    draw.text((cx, cy), label, font=font, fill=color, anchor="mm", stroke_width=int(8 * scale), stroke_fill=NAVY)


def symbol_7(draw, cx, cy, scale):
    symbol_number(draw, cx, cy + 8 * scale, scale, "7", ORANGE)


def symbol_10(draw, cx, cy, scale):
    symbol_number(draw, cx, cy + 8 * scale, scale, "10", SKY)


def symbol_highlights(draw, cx, cy, scale):
    draw.polygon(_star(cx, cy, 100 * scale, 44 * scale), fill=SUN, outline=NAVY)
    draw.polygon(_star(cx, cy, 48 * scale, 20 * scale), fill=CORAL)


SYMBOLS = {
    "home": (CORAL, symbol_home),
    "live": (SKY, symbol_live),
    "programmes": (MINT, symbol_programmes),
    "ages": (LILAC, symbol_ages),
    "petits": (PINK, symbol_petits),
    "tots": (SUN, symbol_tots),
    "age7": (ORANGE, symbol_7),
    "age10": (SKY, symbol_10),
    "highlights": (SUN, symbol_highlights),
}


def _icon(kind):
    color, symbol = SYMBOLS[kind]
    image, draw = _card(color)
    symbol(draw, 256, 268, 1.15)
    return image


def _save(image, name):
    path = OUT / name
    image.save(path, "PNG", optimize=True)
    print(path.relative_to(ROOT), image.size, path.stat().st_size)


def fanart():
    image = _gradient(1280, 720, (126, 214, 255), (255, 236, 168))
    draw = ImageDraw.Draw(image)
    _rainbow(draw, 250, 430, 220)
    _sun(draw, 1040, 150, 70)
    _cloud(draw, 260, 120, 1.4)
    _cloud(draw, 620, 90, 1.0)
    _cloud(draw, 860, 160, 0.8)
    for cx, cy, color, scale in (
        (180, 250, CORAL, 1.1),
        (420, 210, LILAC, 0.8),
        (700, 240, SKY, 1.0),
        (980, 300, PINK, 0.9),
        (1160, 360, MINT, 0.7),
    ):
        _balloon(draw, cx, cy, color, scale)
    for cx, cy, outer in ((90, 80, 18), (500, 180, 12), (760, 50, 16), (1180, 80, 14)):
        draw.polygon(_star(cx, cy, outer, outer * 0.45), fill=SUN)
    draw.polygon([(0, 520), (220, 430), (460, 560), (760, 400), (1040, 540), (1280, 420), (1280, 720), (0, 720)], fill=HILL)
    draw.polygon([(0, 620), (300, 540), (640, 660), (980, 560), (1280, 640), (1280, 720), (0, 720)], fill=HILL_DARK)
    return image


def banner():
    image = fanart().crop((0, 80, 1280, 360)).resize((1000, 220), Image.Resampling.LANCZOS)
    return image


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    _save(fanart(), "fanart.png")
    _save(banner(), "banner.png")
    for kind in SYMBOLS:
        _save(_icon(kind), "icon-%s.png" % kind)
        color, symbol = SYMBOLS[kind]
        _save(_poster(color, symbol), "poster-%s.png" % kind)


if __name__ == "__main__":
    main()
