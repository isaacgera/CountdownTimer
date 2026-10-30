"""
Generate PNG app icons for Countdown to Date, matching icon.svg:
a white stopwatch mark on a blue brand gradient with rounded corners.

Requires Pillow:  python -m pip install --user Pillow
Run from this folder:  python generate-icons.py

Produces: icon-192.png, icon-512.png, icon-maskable-192.png, icon-maskable-512.png
"""
import math
from PIL import Image, ImageDraw

# Brand gradient endpoints (top-left -> bottom-right)
C0 = (91, 141, 239)   # #5b8def
C1 = (63, 111, 214)   # #3f6fd6
WHITE = (255, 255, 255)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(size):
    """Diagonal gradient image."""
    img = Image.new("RGB", (size, size), C0)
    px = img.load()
    maxd = (size - 1) * 2 or 1
    for y in range(size):
        for x in range(size):
            t = (x + y) / maxd
            px[x, y] = lerp(C0, C1, t)
    return img


def rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return m


def draw_stopwatch(draw, size, scale=1.0):
    """Draw the white stopwatch mark centred, scaled to `scale` of the canvas.

    Mirrors icon.svg (512 viewbox): circle r150 @ (256,286), stem + hand.
    """
    # work in 512 space then map to size
    def P(x, y):
        # scale about centre (256,266), then map 512 -> size
        cx, cy = 256, 266
        x = cx + (x - cx) * scale
        y = cy + (y - cy) * scale
        return (x / 512 * size, y / 512 * size)

    lw = max(2, round(26 * scale * size / 512))
    # dial
    c = P(256, 286)
    r = 150 * scale * size / 512
    draw.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], outline=WHITE, width=lw)
    # top button bar
    draw.line([P(220, 72), P(292, 72)], fill=WHITE, width=lw)
    # stem
    draw.line([P(256, 72), P(256, 112)], fill=WHITE, width=lw)
    # hand (vertical)
    draw.line([P(256, 286), P(256, 196)], fill=WHITE, width=lw)
    # hand (to lower-right)
    draw.line([P(256, 286), P(320, 328)], fill=WHITE, width=lw)


def make(size, maskable=False):
    bg = gradient(size).convert("RGBA")
    draw = ImageDraw.Draw(bg)
    # artwork scale: maskable keeps inside ~80% safe zone
    draw_stopwatch(draw, size, scale=0.8 if maskable else 1.0)
    if maskable:
        # full-bleed square background (no rounded corners)
        return bg
    # standard icon: rounded corners
    radius = round(size * 112 / 512)
    mask = rounded_mask(size, radius)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(bg, (0, 0), mask)
    return out


def main():
    jobs = [
        ("icon-192.png", 192, False),
        ("icon-512.png", 512, False),
        ("icon-maskable-192.png", 192, True),
        ("icon-maskable-512.png", 512, True),
    ]
    for name, size, maskable in jobs:
        img = make(size, maskable)
        img.save(name)
        print("wrote", name)


if __name__ == "__main__":
    main()
