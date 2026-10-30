"""
Generate two PWA manifest screenshots with ONLY the Python stdlib (no Pillow,
no network). These are simple branded placeholders at the required aspect
ratios so the "richer install UI" warnings clear — swap for real app captures
when convenient.

  screenshot-wide.png    1280x720  (form_factor: wide  -> desktop)
  screenshot-narrow.png   720x1280 (form_factor: narrow -> mobile)

Run:  python make-screenshots.py
"""
import struct, zlib, os

HERE = os.path.dirname(os.path.abspath(__file__))

C0 = (91, 141, 239)    # #5b8def
C1 = (63, 111, 214)    # #3f6fd6
DARK = (15, 20, 32)    # #0f1420 app bg
CARD = (26, 33, 48)    # #1a2130


def lerp(a, b, t):
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t), int(a[2] + (b[2] - a[2]) * t))


def make(w, h):
    rows = [bytearray(w * 3) for _ in range(h)]

    def setpx(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            i = x * 3
            rows[y][i] = c[0]; rows[y][i + 1] = c[1]; rows[y][i + 2] = c[2]

    def fill(x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(h, y1)):
            for x in range(max(0, x0), min(w, x1)):
                i = x * 3
                rows[y][i] = c[0]; rows[y][i + 1] = c[1]; rows[y][i + 2] = c[2]

    # app-style dark background
    fill(0, 0, w, h, DARK)
    # gradient banner across the top (like the app header)
    band = int(h * 0.16)
    for y in range(band):
        c = lerp(C0, C1, y / max(1, band))
        for x in range(w):
            setpx(x, y, c)
    # a couple of "cards" to hint at the event list
    pad = int(w * 0.06)
    cy = int(band + h * 0.08)
    ch = int(h * 0.12)
    gap = int(h * 0.05)
    for _ in range(3):
        fill(pad, cy, w - pad, cy + ch, CARD)
        # left accent bar
        fill(pad, cy, pad + max(4, int(w * 0.006)), cy + ch, C0)
        cy += ch + gap
        if cy + ch > h:
            break
    return rows


def write_png(path, rows, w, h):
    def chunk(typ, data):
        body = typ + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += rows[y]
    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    out += chunk(b"IEND", b"")
    full = os.path.join(HERE, path)
    with open(full, "wb") as f:
        f.write(out)
    print("wrote", full, w, "x", h)


def main():
    write_png("screenshot-wide.png", make(1280, 720), 1280, 720)
    write_png("screenshot-narrow.png", make(720, 1280), 720, 1280)


if __name__ == "__main__":
    main()
