"""Turn a photo into the ASCII portrait on the profile card.

The wall behind me is removed (bright, colourless pixels connected to the
border), the face is sharpened and contrast-stretched, and every cell becomes
the glyph whose ink coverage in Consolas matches its tone. Two grids are
written, one per theme: on the dark card light is ink, on the light card dark
is. Run once; the photo itself never goes into the repo, only portrait.json.

    python scripts/make_portrait.py path/to/photo.jpg
"""

import json
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).parent

COLS, ROWS = 76, 58
CELL = 0.6  # a cell is 0.6 em wide and 1 em tall
SCALE = 4  # the mask is found on a quarter-size copy
HEIGHT_PER_HEAD = 1.6  # crop height, in head widths: hair to collar
EDGE_PERCENTILE = 86  # the strongest 14% of edges become strokes
# Glyphs in order of how much ink they put down in Consolas (measured: 0, 9,
# 15, 21, 27, 29, 41, 45, 48, 60, 65, 72, 86 percent of the densest).
RAMP = " .:~=+xoa#%&@"
TONES = 3  # brightness bands, each drawn in its own colour
# Ordered dither, so the portrait dissolves at its edges instead of being cut.
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16


def background_mask(rgb):
    """True where the pixel is wall: bright, neutral and reachable from the border."""
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    lum = rgb @ np.array([0.299, 0.587, 0.114])
    sat = (mx - mn) / np.maximum(mx, 1)
    wall = ((lum > 150) & (sat < 0.16)) | ((sat > 0.25) & (rgb[..., 2] > rgb[..., 0] + 30))  # + the teal corner
    h, w = wall.shape
    seen = np.zeros_like(wall)
    q = deque((y, x) for y in range(h) for x in (0, w - 1) if wall[y, x])
    q.extend((y, x) for x in range(w) for y in (0,) if wall[y, x])
    for y, x in q:
        seen[y, x] = True
    while q:
        y, x = q.popleft()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < h and 0 <= nx < w and wall[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    return seen


def largest_component(sub):
    """Only the biggest connected blob is me; anything else is the room."""
    h, w = sub.shape
    label = np.zeros((h, w), dtype=int)
    best, best_n, n = 0, 0, 0
    for y0, x0 in zip(*np.nonzero(sub)):
        if label[y0, x0]:
            continue
        n += 1
        label[y0, x0] = n
        q, size = deque([(y0, x0)]), 0
        while q:
            y, x = q.popleft()
            size += 1
            for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= ny < h and 0 <= nx < w and sub[ny, nx] and not label[ny, nx]:
                    label[ny, nx] = n
                    q.append((ny, nx))
        if size > best_n:
            best, best_n = n, size
    return label == best


def main(photo):
    src = Image.open(photo).convert("RGB")
    # Work at a modest size so the flood fill is quick.
    work = src.resize((src.width // SCALE, src.height // SCALE), Image.LANCZOS)
    rgb = np.asarray(work, dtype=float)
    bg = background_mask(rgb)
    # Close small holes and soften the edge of the silhouette.
    m = Image.fromarray((~bg * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    me = largest_component(np.asarray(m) > 128)
    m = Image.fromarray((me * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))

    # Crop to the head, from just above the hair to the collar.
    sub = np.asarray(m) > 128
    top = max(0, np.nonzero(sub.any(axis=1))[0].min() - 4)
    hx = np.nonzero(sub[top : top + work.height // 3].any(axis=0))[0]
    height = round((hx.max() - hx.min()) * HEIGHT_PER_HEAD)
    width = round(height * COLS * CELL / ROWS)
    left = int(round((hx.min() + hx.max()) / 2 - width / 2))
    box = (left, top, left + width, top + height)
    full = src.crop(tuple(v * SCALE for v in box)).convert("L")

    # Tone: wide unsharp mask for local contrast, then a fine one for detail.
    toned = full.filter(ImageFilter.UnsharpMask(radius=60, percent=90, threshold=0))
    toned = toned.filter(ImageFilter.UnsharpMask(radius=6, percent=120, threshold=2))
    lum = np.asarray(toned.resize((COLS, ROWS), Image.LANCZOS), dtype=float)
    mask = np.asarray(m.crop(box).resize((COLS, ROWS), Image.LANCZOS), dtype=float) / 255

    # Stretch the subject's own tones to the full range (2nd..98th percentile).
    inside = lum[mask > 0.5]
    lo, hi = np.percentile(inside, 2), np.percentile(inside, 98)
    t = np.clip((lum - lo) / (hi - lo), 0, 1)

    # Edges: a structure tensor per cell over a 3x5 grid of samples. Where the
    # gradient is strong and points one way, the cell gets a stroke along it.
    fine = np.asarray(full.filter(ImageFilter.GaussianBlur(5)).resize((COLS * 3, ROWS * 5), Image.LANCZOS), dtype=float)
    gy, gx = np.gradient(fine)
    per_cell = lambda a: a.reshape(ROWS, 5, COLS, 3).sum(axis=(1, 3))
    jxx, jyy, jxy = per_cell(gx * gx), per_cell(gy * gy), per_cell(gx * gy)
    half = np.sqrt(((jxx - jyy) / 2) ** 2 + jxy**2)
    strength = (jxx + jyy) / 2 + half
    coherence = half / np.maximum((jxx + jyy) / 2, 1e-9)
    # The edge runs perpendicular to the gradient; fold its angle into [0, 180).
    edge_angle = (np.degrees(0.5 * np.arctan2(2 * jxy, jxx - jyy)) + 90) % 180
    stroke = np.array(["-", "\\", "|", "/"])[((edge_angle + 22.5) // 45).astype(int) % 4]
    is_edge = (strength > np.percentile(strength[mask > 0.5], EDGE_PERCENTILE)) & (coherence > 0.55)

    levels = len(RAMP)
    # The collar fades out over the bottom rows, dissolving rather than cut.
    rr, cc = np.mgrid[0:ROWS, 0:COLS]
    fade = np.clip((ROWS - 1 - rr) / (ROWS * 0.2), 0, 1) ** 1.2
    # ...and narrows toward the middle as it goes, so the shoulders don't spill.
    low = np.clip((rr - ROWS * 0.72) / (ROWS * 0.28), 0, 1)
    fade *= np.clip(1 - (np.abs(cc - COLS / 2) / (COLS / 2) - (1 - 0.55 * low)) / 0.15, 0, 1)
    keep = mask * fade > 0.12 + 0.82 * BAYER[rr % 4, cc % 4] * (fade < 1)
    out = {"cols": COLS, "rows": ROWS, "ramp": RAMP}
    for theme, tone in (("dark", t ** 0.9), ("light", (1 - t) ** 0.9)):
        chars, bands = [], []
        for r in range(ROWS):
            row_c, row_b = [], []
            for c in range(COLS):
                if mask[r, c] < 0.35 or not keep[r, c]:
                    row_c.append(" ")
                    row_b.append(" ")
                    continue
                if is_edge[r, c]:
                    row_c.append(stroke[r, c])
                    row_b.append(str(TONES - 1))
                    continue
                v = tone[r, c] * min(1.0, mask[r, c] * 1.4)
                # The subject never vanishes entirely: its darkest cells keep a trace.
                level = 1 + int(round(v * (levels - 2)))
                row_c.append(RAMP[level])
                row_b.append(str(min(TONES - 1, int(v * TONES))))
            chars.append("".join(row_c).rstrip())
            bands.append("".join(row_b)[: len(chars[-1])])
        out[theme] = {"chars": chars, "bands": bands}
    (HERE / "portrait.json").write_text(json.dumps(out, indent=0))
    print("\n".join(out["dark"]["chars"]))


if __name__ == "__main__":
    main(sys.argv[1])
