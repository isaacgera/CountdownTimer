"""
Generate square PNG app icons for Countdown Timer using ONLY the Python stdlib
(no Pillow, no network — works behind a corporate proxy).

Keeps it simple and fast: a diagonal brand-blue gradient background with a white
calendar mark built from plain filled rectangles (body outline, header strip,
two binding rings). Square + opaque, which is what the PWA manifest requires.

Run:  python make-png-icons.py   (from this folder)
Produces: icon-192.png, icon-512.png, icon-maskable-192.png, icon-maskable-512.png
"""
import struct, zlib, os

HERE = os.path.dirname(os.path.abspath(__file__))

C0 = (91, 141, 239)    # #5b8def
C1 = (63, 111, 214)    # #3f6fd6
WHITE = (255, 255, 255)


def lerp(a, b, t):
    return (int(a[0] + (b[0] - a[0]) * t),
            int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t))


def make_icon(size, scale):
    # flat row buffer of (r,g,b); gradient background
    rows = []
    maxd = (size - 1) * 2 or 1
    for y in range(size):
        row = bytearray(size * 3)
        for x in range(size):
            c = lerp(C0, C1, (x + y) / maxd)
            i = x * 3
            row[i] = c[0]; row[i + 1] = c[1]; row[i + 2] = c[2]
        rows.append(row)

    unit = size / 512.0

    def sc(v):  # scale about centre (256) for maskable safe zone
        return 256 + (v - 256) * scale

    def P(v):
        return int(sc(v) * unit)

    w = max(2, int(22 * unit * scale))  # stroke thickness

    def fill(x0, y0, x1, y1):
        if x1 < x0: x0, x1 = x1, x0
        if y1 < y0: y0, y1 = y1, y0
        for y in range(max(0, y0), min(size, y1)):
            row = rows[y]
            for x in range(max(0, x0), min(size, x1)):
                i = x * 3
                row[i] = 255; row[i + 1] = 255; row[i + 2] = 255

    # calendar body as four edges (a rectangle outline 112,150 -> 400,408)
    bx0, by0, bx1, by1 = P(112), P(150), P(400), P(408)
    fill(bx0, by0, bx1, by0 + w)          # top edge
    fill(bx0, by1 - w, bx1, by1)          # bottom edge
    fill(bx0, by0, bx0 + w, by1)          # left edge
    fill(bx1 - w, by0, bx1, by1)          # right edge
    # header divider (across the body at y=222)
    fill(bx0, P(222) - w // 2, bx1, P(222) + w // 2)
    # two binding rings above the body
    fill(P(190) - w // 2, P(112), P(190) + w // 2, P(170))
    fill(P(322) - w // 2, P(112), P(322) + w // 2, P(170))
    # a simple blocky "7": top bar + a thick near-vertical stroke
    sx0, sx1 = P(205), P(315)
    sy0 = P(258)
    fill(sx0, sy0, sx1, sy0 + w)                      # top bar of the 7
    fill(P(268), sy0, P(268) + w + 2, P(372))         # descending stroke
    return rows


def write_png(path, rows, size):
    def chunk(typ, data):
        body = typ + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)

    raw = bytearray()
    for y in range(size):
        raw.append(0)          # filter byte
        raw += rows[y]
    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))  # RGB, 8-bit
    out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    out += chunk(b"IEND", b"")
    full = os.path.join(HERE, path)
    with open(full, "wb") as f:
        f.write(out)
    print("wrote", full, size, "x", size)


def main():
    for name, size, scale in [
        ("icon-192.png", 192, 1.0),
        ("icon-512.png", 512, 1.0),
        ("icon-maskable-192.png", 192, 0.8),
        ("icon-maskable-512.png", 512, 0.8),
    ]:
        write_png(name, make_icon(size, scale), size)


if __name__ == "__main__":
    main()
