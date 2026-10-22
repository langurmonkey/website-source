#!/usr/bin/env python3
"""Generate static/img/2026/10/galaxy-rendering-splatting.svg.

Figure for content/blog/2026/galaxy-rendering.md, section "Splatting": each
particle adds its weight to the voxel it falls in, so a voxel ends up with the
summed weight and the weight-averaged colour.

Run from the repo root:  python3 scripts/diagrams/make-splatting-svg.py
"""

import os

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

INK = "#222"
DIM = "#888"
FAINT = "#c9c9c9"
PANEL = "#ffffff"
EDGE = "#dedede"

CYAN = "#1a8fd1"
AMBER = "#e08a1e"
PINK = "#d6317f"

# (x, y, weight, colour) in grid units
P = [
    (0.85, 4.55, 0.40, CYAN),
    (1.30, 2.30, 0.80, AMBER),
    (1.62, 2.72, 0.50, PINK),
    (2.35, 4.35, 0.45, CYAN),
    (2.90, 1.10, 0.25, AMBER),
    (3.10, 3.55, 0.90, PINK),
    (3.80, 2.10, 0.30, AMBER),
    (4.30, 0.85, 0.55, PINK),
    (4.55, 4.15, 0.65, CYAN),
    (5.20, 2.90, 1.00, AMBER),
    (5.85, 1.35, 0.40, CYAN),
    (6.35, 3.80, 0.35, PINK),
]

CELL = 50.0
COLS, ROWS = 7, 5

# panel A
AX, AY = 40.0, 326.0          # bottom-left of the interior
# panel B
BX, BY = 512.0, 326.0

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgb2hex(c):
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in c)

# accumulate the particles into voxels
vox = {}
for x, y, w, col in P:
    key = (int(x), int(y))
    r, g, b = hex2rgb(col)
    acc = vox.setdefault(key, [0.0, 0.0, 0.0, 0.0])
    acc[0] += w * r
    acc[1] += w * g
    acc[2] += w * b
    acc[3] += w

rho_max = max(v[3] for v in vox.values())

out = []
A = out.append

A('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 600" width="900" height="600" '
  'role="img" aria-labelledby="splat-title">')
A('<title id="splat-title">Splatting a particle field into a voxel grid: each particle adds '
  'its weight to the nearest voxel, and the voxel stores the summed weight and the '
  'weight-averaged colour.</title>')
A('<defs>')
A('<marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
  'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#999"/></marker>')
A('</defs>')
A('<rect width="900" height="600" fill="#ffffff"/>')

# ── panel frames ──────────────────────────────────────────────────────────────
for x0, x1, label, sub in ((28, 402, "particles", "continuous: position, weight w, colour c"),
                           (500, 874, "voxel grid", "each particle lands in its nearest voxel")):
    A(f'<rect x="{x0}" y="64" width="{x1 - x0}" height="274" rx="10" '
      f'fill="{PANEL}" stroke="{EDGE}"/>')
    A(f'<text x="{x0 + 2}" y="50" font-family="{SANS}" font-size="14.5" font-weight="600" '
      f'fill="{INK}">{label}</text>')
    A(f'<text x="{x0 + 2}" y="32" font-family="{SANS}" font-size="12" fill="{DIM}">'
      f'{sub.upper()}</text>')

# ── panel A: the particles ────────────────────────────────────────────────────
for x, y, w, col in P:
    px, py = AX + CELL * x, AY - CELL * y
    r = 5 + 9 * w
    A(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="{col}" fill-opacity="0.30"/>')
for x, y, w, col in P:
    px, py = AX + CELL * x, AY - CELL * y
    A(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="{col}"/>')

# ── arrow ─────────────────────────────────────────────────────────────────────
A('<line x1="416" y1="201" x2="486" y2="201" stroke="#999" stroke-width="1.6" '
  'marker-end="url(#arw)"/>')
A(f'<text x="451" y="190" text-anchor="middle" font-family="{MONO}" font-size="12.5" '
  f'fill="{DIM}">splat</text>')

# ── panel B: the voxels ───────────────────────────────────────────────────────
for cx in range(COLS):
    for cy in range(ROWS):
        A(f'<rect x="{BX + cx * CELL:.0f}" y="{BY - (cy + 1) * CELL:.0f}" '
          f'width="{CELL:.0f}" height="{CELL:.0f}" fill="none" stroke="{FAINT}" stroke-width="1"/>')

for (cx, cy), (sr, sg, sb, sw) in sorted(vox.items()):
    col = rgb2hex((sr / sw, sg / sw, sb / sw))
    op = 0.10 + 0.72 * (sw / rho_max)
    x = BX + cx * CELL
    y = BY - (cy + 1) * CELL
    A(f'<rect x="{x:.0f}" y="{y:.0f}" width="{CELL:.0f}" height="{CELL:.0f}" fill="{col}" '
      f'fill-opacity="{op:.2f}"/>')

# highlighted voxel (1, 2)
hx, hy = BX + CELL, BY - 3 * CELL
A(f'<rect x="{hx:.0f}" y="{hy:.0f}" width="{CELL:.0f}" height="{CELL:.0f}" fill="none" '
  f'stroke="{INK}" stroke-width="2"/>')

# ── callout connector ─────────────────────────────────────────────────────────
BX0, BY0, BSZ = 560.0, 400.0, 160.0
A(f'<line x1="{hx:.0f}" y1="{hy + CELL:.0f}" x2="{BX0}" y2="{BY0}" stroke="#ccc" '
  f'stroke-width="1" stroke-dasharray="4 4"/>')
A(f'<line x1="{hx + CELL:.0f}" y1="{hy + CELL:.0f}" x2="{BX0 + BSZ}" y2="{BY0}" stroke="#ccc" '
  f'stroke-width="1" stroke-dasharray="4 4"/>')

# ── legend row ────────────────────────────────────────────────────────────────
A(f'<text x="28" y="356" font-family="{SANS}" font-size="11.5" fill="{DIM}">'
  f'circle area &#8733; w &#183; colour = emission c</text>')
A(f'<text x="874" y="356" text-anchor="end" font-family="{SANS}" font-size="11.5" '
  f'fill="{DIM}">voxel opacity &#8733; &#961;</text>')

# ── zoom of voxel (1, 2) ──────────────────────────────────────────────────────
A(f'<rect x="{BX0}" y="{BY0}" width="{BSZ}" height="{BSZ}" fill="{PANEL}" stroke="{INK}" '
  f'stroke-width="2" rx="4"/>')

inner = [(x, y, w, col) for x, y, w, col in P if (int(x), int(y)) == (1, 2)]
for x, y, w, col in inner:
    px = BX0 + (x - 1) * BSZ
    py = BY0 + BSZ - (y - 2) * BSZ
    r = (5 + 9 * w) * BSZ / CELL
    A(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="{col}" fill-opacity="0.30"/>')
    A(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{col}"/>')

A(f'<text x="{BX0 + BSZ + 14}" y="{BY0 + 16}" font-family="{SANS}" font-size="11.5" '
  f'fill="{DIM}">one voxel,<tspan x="{BX0 + BSZ + 14}" dy="15">magnified</tspan></text>')

# ── arithmetic ────────────────────────────────────────────────────────────────
TX = 70.0
A(f'<text x="{TX}" y="{BY0 + 14}" font-family="{SANS}" font-size="11.5" fill="{DIM}">'
  f'WHAT THE VOXEL ACCUMULATES</text>')

A(f'<text x="{TX}" y="{BY0 + 52}" xml:space="preserve" font-family="{MONO}" font-size="14.5" fill="{INK}">'
  f'&#961; = w<tspan font-size="10" dy="3">1</tspan><tspan dy="-3"> + w</tspan>'
  f'<tspan font-size="10" dy="3">2</tspan><tspan dy="-3"> = </tspan>'
  f'<tspan fill="{AMBER}">0.80</tspan><tspan> + </tspan><tspan fill="{PINK}">0.50</tspan>'
  f'<tspan> = 1.30</tspan></text>')

A(f'<text x="{TX}" y="{BY0 + 84}" xml:space="preserve" font-family="{MONO}" font-size="14.5" fill="{INK}">'
  f'c = (w<tspan font-size="10" dy="3">1</tspan><tspan dy="-3">c</tspan>'
  f'<tspan font-size="10" dy="3">1</tspan><tspan dy="-3"> + w</tspan>'
  f'<tspan font-size="10" dy="3">2</tspan><tspan dy="-3">c</tspan>'
  f'<tspan font-size="10" dy="3">2</tspan><tspan dy="-3">) / &#961;</tspan></text>')

A(f'<text x="{TX}" y="{BY0 + 112}" xml:space="preserve" font-family="{MONO}" font-size="13" fill="{DIM}">'
  f'&#160;&#160;&#160;= (<tspan fill="{AMBER}">0.80</tspan><tspan>c</tspan>'
  f'<tspan font-size="9" dy="2.7">1</tspan><tspan dy="-2.7"> + </tspan>'
  f'<tspan fill="{PINK}">0.50</tspan><tspan>c</tspan>'
  f'<tspan font-size="9" dy="2.7">2</tspan><tspan dy="-2.7">)/1.30</tspan></text>')

mean = [vox[(1, 2)][i] / vox[(1, 2)][3] for i in range(3)]
A(f'<rect x="{TX}" y="{BY0 + 128}" width="30" height="30" rx="3" fill="{rgb2hex(mean)}"/>')
A(f'<text x="{TX + 42}" y="{BY0 + 148}" font-family="{SANS}" font-size="11.5" fill="{DIM}">'
  f'the three bytes stored for that voxel</text>')

A('</svg>')

svg = "\n".join(out)
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(root, "static/img/2026/10/galaxy-rendering-splatting.svg")
open(path, "w", encoding="utf-8").write(svg + "\n")
print("wrote", path, len(svg), "bytes")
print("voxels:", len(vox), "rho_max:", rho_max)
print("mean colour of (1,2):", rgb2hex(mean))
