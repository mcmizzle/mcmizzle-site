#!/usr/bin/env python3
"""Generate a per-post Open Graph card.

A link shared to LinkedIn or Slack is mostly its preview image. Every post
pointing at the same generic monogram makes two different posts look like the
same post, so each one gets a card carrying its own title.

Usage:
    python3 tools/og-image.py <slug> "Post title"

Writes assets/og-<slug>.png at 1200x630. Requires Pillow:

    python3 -m venv .venv && .venv/bin/pip install Pillow
    .venv/bin/python tools/og-image.py <slug> "Post title"

This is a local authoring tool, not part of serving the site — the site still
has no build step, and the PNG it produces is committed like any other asset.
If Pillow isn't available, skip it: the post template falls back to the shared
assets/og-image.png, which is worse but not broken.
"""

import sys
import pathlib

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow not installed — see the usage note at the top of this file.")

W, H = 1200, 630

# Light-theme palette from assets/style.css. Cards are always light: most
# social clients show previews on a white surface regardless of user theme.
BG = "#fdf6ec"
FG = "#2e2418"
MUTED = "#7e6f5a"
ACCENT = "#b95238"

MARGIN = 80
BAR_H = 14                     # accent bar across the top
TITLE_SIZE = 62
FOOTER_SIZE = 28
LINE_SPACING = 1.22
MAX_LINES = 4

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"


def wrap(text, font, draw, max_width):
    """Greedy wrap. Returns lines, truncating with an ellipsis past MAX_LINES."""
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)

    if len(lines) > MAX_LINES:
        lines = lines[:MAX_LINES]
        while lines[-1] and draw.textlength(lines[-1] + "…", font=font) > max_width:
            lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else lines[-1][:-1]
        lines[-1] += "…"
    return lines


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip().split("\n\n")[2])

    slug, title = sys.argv[1], sys.argv[2]
    root = pathlib.Path(__file__).resolve().parent.parent
    out = root / "assets" / f"og-{slug}.png"

    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, BAR_H], fill=ACCENT)

    title_font = ImageFont.truetype(BOLD, TITLE_SIZE)
    footer_font = ImageFont.truetype(REGULAR, FOOTER_SIZE)

    lines = wrap(title, title_font, draw, W - MARGIN * 2)
    line_h = int(TITLE_SIZE * LINE_SPACING)
    block_h = line_h * len(lines)

    # Sit the title block slightly above centre so it doesn't crowd the footer.
    y = (H - block_h) // 2 - 30
    for line in lines:
        draw.text((MARGIN, y), line, font=title_font, fill=FG)
        y += line_h

    footer_y = H - MARGIN - FOOTER_SIZE
    draw.text((MARGIN, footer_y), "mcmizzle.com", font=footer_font, fill=ACCENT)
    kicker = "Engineering notes"
    kicker_w = draw.textlength(kicker, font=footer_font)
    draw.text((W - MARGIN - kicker_w, footer_y), kicker, font=footer_font, fill=MUTED)

    img.save(out, "PNG", optimize=True)
    print(f"wrote {out.relative_to(root)}  ({out.stat().st_size // 1024} KB, {len(lines)} line(s))")


if __name__ == "__main__":
    main()
