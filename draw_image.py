#!/usr/bin/env python3
"""Overlay front-page text on the generated news image.

Reads base.png (1024x1024), draws a masthead, a headline and four
short news lines on dark translucent bands, and writes entry.png
(1024x1024, under 1 MiB).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base.png")
OUT = os.path.join(HERE, "entry.png")
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MASTHEAD = "26 NOVEMBER 2026"
HEADLINE = "THE WORLD IN ONE DAY"
LINES = [
    "US TARIFFS: UP TO 25% ON INDIA, 14 NATIONS",
    "UKRAINE STRIKES RUSSIAN AIR BASE, 5 PLANES HIT",
    "N. KOREA CALLS FOR WIDER NUCLEAR DEPLOYMENT",
    "STORM POSTPONES MACY'S THANKSGIVING PARADE",
]
FOOTER = "make.fun news-image"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((1024 - w) / 2, y), text, font=fnt, fill=fill)


def main():
    img = Image.open(BASE).convert("RGB")
    if img.size != (1024, 1024):
        img = img.resize((1024, 1024), Image.LANCZOS)

    # Darken the whole picture slightly so overlaid text pops.
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # Top masthead band.
    d.rectangle([0, 0, 1024, 150], fill=(8, 12, 24, 235))
    d.rectangle([0, 150, 1024, 154], fill=(212, 175, 55, 255))
    # Bottom headlines band.
    d.rectangle([0, 812, 1024, 1024], fill=(8, 12, 24, 225))
    d.rectangle([0, 812, 1024, 816], fill=(212, 175, 55, 255))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    centered(draw, 18, MASTHEAD, font(FONT_BOLD, 58), (255, 255, 255))
    centered(draw, 88, HEADLINE, font(FONT_BOLD, 40), (212, 175, 55))

    y = 834
    for i, line in enumerate(LINES, start=1):
        draw.text((44, y), f"{i}.", font=font(FONT_BOLD, 30),
                  fill=(212, 175, 55))
        draw.text((84, y), line, font=font(FONT_BOLD, 30),
                  fill=(255, 255, 255))
        y += 40

    fw = draw.textlength(FOOTER, font=font(FONT_REG, 20))
    draw.text((1024 - 44 - fw, 996), FOOTER, font=font(FONT_REG, 20),
              fill=(200, 200, 200))

    # Palette PNG: the photo is noisy, so plain RGB PNG exceeds 1 MiB.
    # Adaptive 256-colour palette with dithering keeps it well under.
    pal = img.convert("RGB").convert(
        "P", palette=Image.ADAPTIVE, colors=256)
    pal.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}, {size} bytes")
    assert size <= 1048576, "entry.png over 1 MiB"


if __name__ == "__main__":
    main()
