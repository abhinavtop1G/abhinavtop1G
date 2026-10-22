"""Render the ASCII globe frames for the profile card.

The Earth is the same 60,000-point Fibonacci sphere my portfolio's globe uses
(land.b64 is a bitset: bit i is set when point i lies on land, from Natural
Earth 1:110m). Each frame turns the planet a little; Patiala is marked, and five
satellites, one per project, orbit it. Run once; the output (globe.json) is
static and read by build_profile.py.

    python scripts/make_globe.py
"""

import base64
import json
import math
from pathlib import Path

HERE = Path(__file__).parent

N = 60_000
FRAMES = 24
COLS, ROWS = 54, 25
# A monospace cell is about half as wide as it is tall (8.4 x 17 px at 14 px).
ASPECT = 8.4 / 17
R_ROWS = 11.4
R_COLS = R_ROWS / ASPECT
CX, CY = COLS / 2, ROWS / 2
PITCH = 0.42  # north tilted toward the viewer
LIGHT = (-0.45, 0.55, 0.7)
PATIALA = (30.34, 76.39)
RAMP = ":-=+*#%@"


def unit(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.sin(lo), math.sin(la), math.cos(la) * math.cos(lo))


def land_points():
    bits = base64.b64decode((HERE / "land.b64").read_text().strip())
    golden = math.pi * (3 - math.sqrt(5))
    pts = []
    for i in range(N):
        if bits[i >> 3] & (1 << (i & 7)):
            y = 1 - (i + 0.5) * 2 / N
            r = math.sqrt(1 - y * y)
            t = i * golden
            pts.append((math.cos(t) * r, y, math.sin(t) * r))
    return pts


def build_index(pts, step=4):
    """Bucket land points by 4-degree lat/lon cells for fast neighbourhood queries."""
    grid = {}
    for p in pts:
        lat = math.degrees(math.asin(max(-1, min(1, p[1]))))
        lon = math.degrees(math.atan2(p[0], p[2]))
        grid.setdefault((int((lat + 90) // step), int((lon + 180) // step)), []).append(p)
    return grid, step


def coverage(m, index, radius=0.045):
    """Share of the sphere within `radius` of model point m that is land (0..1)."""
    grid, step = index
    lat = math.degrees(math.asin(max(-1, min(1, m[1]))))
    lon = math.degrees(math.atan2(m[0], m[2]))
    bi, bj = int((lat + 90) // step), int((lon + 180) // step)
    cos_r = math.cos(radius)
    near = 0
    span = 1 if abs(lat) < 70 else 4
    for di in (-1, 0, 1):
        for dj in range(-span, span + 1):
            for p in grid.get((bi + di, (bj + dj) % (360 // step)), ()):
                if p[0] * m[0] + p[1] * m[1] + p[2] * m[2] >= cos_r:
                    near += 1
    expected = N * (1 - cos_r) / 2  # points in a cap of that radius
    return min(1.0, near / expected)


def to_view(m, yaw):
    """Model -> view: yaw about y, then pitch about x."""
    cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(PITCH), math.sin(PITCH)
    x = cy * m[0] + sy * m[2]
    z = -sy * m[0] + cy * m[2]
    y = cp * m[1] - sp * z
    z = sp * m[1] + cp * z
    return (x, y, z)


def to_model(v, yaw):
    cy, sy, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(PITCH), math.sin(PITCH)
    y = cp * v[1] + sp * v[2]
    z = -sp * v[1] + cp * v[2]
    x = cy * v[0] - sy * z
    z = sy * v[0] + cy * z
    return (x, y, z)


def cell_of(v):
    return round(CX + v[0] * R_COLS - 0.5), round(CY - v[1] * R_ROWS - 0.5)


def ring_point(theta, radius=1.17, incl=0.24, tilt=-0.2):
    """A satellite orbit in view space: nearly edge-on, a little tilted."""
    x = radius * math.cos(theta)
    y = radius * math.sin(theta) * math.sin(incl)
    z = radius * math.sin(theta) * math.cos(incl)
    ct, st = math.cos(tilt), math.sin(tilt)
    return (x * ct - y * st, x * st + y * ct, z)


def main():
    index = build_index(land_points())
    lx, ly, lz = LIGHT
    ln = math.sqrt(lx * lx + ly * ly + lz * lz)
    light = (lx / ln, ly / ln, lz / ln)
    patiala = unit(*PATIALA)
    # Start with India facing the viewer, then turn east to west.
    yaw0 = -math.atan2(patiala[0], patiala[2]) - 0.6
    frames = []
    for k in range(FRAMES):
        yaw = yaw0 + k * 2 * math.pi / FRAMES
        land = [[" "] * COLS for _ in range(ROWS)]
        sea = [[" "] * COLS for _ in range(ROWS)]
        orbit = [[" "] * COLS for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                nx = (c + 0.5 - CX) / R_COLS
                ny = (CY - (r + 0.5)) / R_ROWS
                d = nx * nx + ny * ny
                if d > 1:
                    continue
                nz = math.sqrt(1 - d)
                lam = max(0.0, nx * light[0] + ny * light[1] + nz * light[2])
                cov = coverage(to_model((nx, ny, nz), yaw), index)
                if cov > 0.3:
                    land[r][c] = RAMP[min(len(RAMP) - 1, int((0.25 + 0.75 * lam) * cov * len(RAMP)))]
                else:
                    # Ocean: dots on the lit face, ticks toward the limb.
                    sea[r][c] = "." if nz > 0.3 else "'"
        # The orbit, hidden where the planet stands in front of it.
        for s in range(360):
            v = ring_point(math.radians(s))
            if v[2] < 0 and v[0] ** 2 + v[1] ** 2 < 1:
                continue
            c, r = cell_of(v)
            if 0 <= r < ROWS and 0 <= c < COLS and land[r][c] == " ":
                orbit[r][c] = "."
                sea[r][c] = " "
        marks = []
        pv = to_view(patiala, yaw)
        if pv[2] > 0.12:
            c, r = cell_of(pv)
            marks.append({"c": c, "r": r, "ch": "@", "kind": "home"})
        # Five project satellites, evenly spaced, moving a little faster than the planet turns.
        for j in range(5):
            theta = j * 2 * math.pi / 5 + k * 1.5 * 2 * math.pi / FRAMES
            v = ring_point(theta)
            if v[2] < 0 and v[0] ** 2 + v[1] ** 2 < 1:
                continue
            c, r = cell_of(v)
            if 0 <= r < ROWS and 0 <= c < COLS:
                marks.append({"c": c, "r": r, "ch": "o", "kind": f"sat{j}"})
        frames.append(
            {
                "land": ["".join(row) for row in land],
                "sea": ["".join(row) for row in sea],
                "orbit": ["".join(row) for row in orbit],
                "marks": marks,
            }
        )
        print(f"frame {k + 1}/{FRAMES}")
    out = {"cols": COLS, "rows": ROWS, "frames": frames}
    (HERE / "globe.json").write_text(json.dumps(out, separators=(",", ":")))
    print("\n".join(frames[0]["land"]))


if __name__ == "__main__":
    main()
