"""Generates icon.ico for the rpguide exe — d20 dice with AI sparkle aesthetic."""
import math
import os
from PIL import Image, ImageDraw, ImageFont


def _hex_points(cx: float, cy: float, r: float, rotation_deg: float = 0):
    pts = []
    for i in range(6):
        angle = math.radians(rotation_deg + 60 * i)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return pts


def _draw_star(draw: ImageDraw.ImageDraw, cx: float, cy: float,
               r_outer: float, r_inner: float, n: int, color):
    pts = []
    for i in range(n * 2):
        r = r_outer if i % 2 == 0 else r_inner
        angle = math.radians(-90 + i * 180 / n)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    if len(pts) >= 3:
        draw.polygon(pts, fill=color)


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    font_size = max(8, int(size * 0.30))
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/verdanab.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, font_size)
            except Exception:
                continue
    return ImageFont.load_default()


def _create_at_size(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = cy = size / 2

    BG       = (18,  8,  45, 255)
    HEX_FILL = (35, 15,  75, 255)
    GOLD     = (255, 190,  35, 255)
    GOLD_DIM = (200, 145,  28, 130)
    TEXT_CLR = (255, 232, 150, 255)
    SPARKLE  = (255, 240, 190, 230)

    # Background circle
    bg_r = size * 0.48
    draw.ellipse([cx - bg_r, cy - bg_r, cx + bg_r, cy + bg_r], fill=BG)

    if size < 24:
        draw.ellipse(
            [cx - bg_r + 1, cy - bg_r + 1, cx + bg_r - 1, cy + bg_r - 1],
            outline=GOLD,
        )
        return img

    # Hexagon (flat-top, rotation=0 puts a vertex at the top)
    hex_r = size * 0.41
    pts = _hex_points(cx, cy, hex_r, rotation_deg=0)
    draw.polygon(pts, fill=HEX_FILL)

    lw = max(2, size // 48)

    # Outer hexagon border in gold
    for i in range(6):
        draw.line([pts[i], pts[(i + 1) % 6]], fill=GOLD, width=lw)

    # Inner spokes from centre (d20 facet lines)
    for pt in pts:
        draw.line([(cx, cy), pt], fill=GOLD_DIM, width=max(1, lw - 1))

    # "20" label
    if size >= 48:
        font = _load_font(size)
        text = "20"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = cx - tw / 2 - bbox[0]
        ty = cy - th / 2 - bbox[1]

        # Drop-shadow
        draw.text((tx + max(1, lw - 1), ty + max(1, lw - 1)),
                  text, fill=(0, 0, 0, 160), font=font)
        draw.text((tx, ty), text, fill=TEXT_CLR, font=font)

    # Sparkle accents on alternate edge midpoints (only for ≥ 128 px)
    if size >= 128:
        sr = size * 0.038
        for i in range(0, 6, 2):
            p1, p2 = pts[i], pts[(i + 1) % 6]
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            dx, dy = mx - cx, my - cy
            dist = math.hypot(dx, dy)
            if dist:
                factor = 1.13
                sx, sy = cx + dx * factor, cy + dy * factor
                _draw_star(draw, sx, sy, sr, sr * 0.38, 4, SPARKLE)

    return img


def main():
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = {s: _create_at_size(s) for s in sizes}
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    # Pillow ICO: pass a dict of {size: image} via the icon_size parameter,
    # or save with explicit sizes list.  The most reliable method is to let
    # Pillow resize from the largest canvas using the `sizes` keyword.
    base = images[256]
    base.save(
        out,
        format="ICO",
        sizes=[(s, s) for s in sizes],
    )
    print(f"Icon saved: {out}")


if __name__ == "__main__":
    main()
