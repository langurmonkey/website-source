#!/usr/bin/env python3
"""Generate static/img/2026/10/galaxy-rendering-smoothing.svg.

Figure for content/blog/2026/galaxy-rendering.md, section "Smoothing without
inventing detail": the blur width is a length measured on the particles, so the
same kernel covers more voxels on a finer grid.

Run from the repo root:  python3 scripts/diagrams/make-smoothing-svg.py
"""

import math
import os

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

INK = "#1d1d1f"
DIM = "#8a8a8e"
FAINT = "#dcdcde"
EDGE = "#e3e3e5"
PANEL = "#ffffff"

CYAN = "#1a8fd1"
AMBER = "#e0801e"
PINK = "#d6317f"

# Particle field, panel-relative (0..1, y down): (x, y, weight, colour)
P = [
    (0.12, 0.24, 0.55, CYAN),
    (0.31, 0.62, 0.80, AMBER),
    (0.44, 0.18, 0.45, CYAN),
    (0.61, 0.54, 0.95, PINK),
    (0.78, 0.22, 0.35, CYAN),
    (0.90, 0.66, 0.60, AMBER),
    (0.21, 0.84, 0.40, PINK),
    (0.55, 0.88, 0.65, CYAN),
    (0.34, 0.08, 0.30, AMBER),
    (0.72, 0.86, 0.50, PINK),
]

SIGMA = 30.0                      # kernel width on screen, px (both panels)
REF = 3                           # the particle whose neighbours are measured

# ── layout ────────────────────────────────────────────────────────────────────
W, H = 900, 628
M = 30                            # page margin
PA = (M, 66, 440, 332)            # panel A: x0, y0, x1, y1
PB = (460, 66, 870, 332)          # panel B
PC = (M, 404, 870, 612)           # panel C
PAD = 16                          # panel inner padding

FIELD_A = (PA[0] + PAD, 84, PA[2] - PAD, 296)
FIELD_B = (PB[0] + PAD, 96, PB[2] - PAD, 288)


def pt(field, fx, fy):
    x0, y0, x1, y1 = field
    return x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)


def dist(a, b):
    """Distance between two particles, in px of panel A's field."""
    x0, y0, x1, y1 = FIELD_A
    return math.hypot((a[0] - b[0]) * (x1 - x0), (a[1] - b[1]) * (y1 - y0))


def mix(a, b, t):
    """Blend two hex colours, t = 0 gives a and t = 1 gives b."""
    ca = [int(a.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(ca, cb))


def glow(col):
    """A radial gradient that falls off like a Gaussian to the eye."""
    return (f'<radialGradient id="g{col.lstrip("#")}">'
            f'<stop offset="0" stop-color="{col}" stop-opacity="1"/>'
            f'<stop offset="0.28" stop-color="{col}" stop-opacity="0.62"/>'
            f'<stop offset="0.52" stop-color="{col}" stop-opacity="0.28"/>'
            f'<stop offset="0.76" stop-color="{col}" stop-opacity="0.09"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')


out = []
A = out.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
  f'height="{H}" role="img" aria-labelledby="sm-title">')
A('<title id="sm-title">Gaussian smoothing of a particle field. The kernel width is a length '
  'measured on the particles (the median distance to the 4th neighbour), so the same physical '
  'blur is covered by twice as many voxels on a grid of twice the resolution.</title>')
A('<defs>')
for c in (CYAN, AMBER, PINK):
    A(glow(c))
A(f'<clipPath id="clipA"><rect x="{FIELD_A[0]}" y="{FIELD_A[1]}" '
  f'width="{FIELD_A[2] - FIELD_A[0]}" height="{FIELD_A[3] - FIELD_A[1]}"/></clipPath>')
A(f'<clipPath id="clipB"><rect x="{PB[0] + 1}" y="{PB[1] + 1}" width="{PB[2] - PB[0] - 2}" '
  f'height="{PB[3] - PB[1] - 2}" rx="11"/></clipPath>')
A('<marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
  'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#6b6b70"/></marker>')
A('</defs>')
A(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

# ── panels ────────────────────────────────────────────────────────────────────
for x0, y0, x1, y1 in (PA, PB, PC):
    A(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="12" '
      f'fill="{PANEL}" stroke="{EDGE}"/>')


def heading(x, y, title, sub):
    A(f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="14.5" font-weight="600" '
      f'fill="{INK}">{title}</text>')
    A(f'<text x="{x}" y="{y + 19}" font-family="{SANS}" font-size="12" fill="{DIM}">{sub}</text>')


heading(M, 34, "before the blur", "particles: position, weight w, emission colour c")
heading(460, 34, "after a Gaussian of width &#963;", "every particle spread by the same kernel, so the gaps fill in")
heading(M, 364, "the same kernel, two grids",
        "&#963; is a length in world units, so a finer grid spends more voxels on the same blur")

# ── panel A: the particles, and how ℓ is measured ─────────────────────────────
A('<g clip-path="url(#clipA)">')
for fx, fy, w, col in P:
    px, py = pt(FIELD_A, fx, fy)
    A(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{7 + 10 * w:.1f}" fill="{col}" '
      f'fill-opacity="0.18"/>')
A('</g>')
for fx, fy, w, col in P:
    px, py = pt(FIELD_A, fx, fy)
    A(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{2.8 + 3.0 * w:.1f}" fill="{col}"/>')

order = sorted((dist(P[REF], P[j]), j) for j in range(len(P)) if j != REF)
four = [j for _, j in order[:4]]
farthest = max(four, key=lambda j: dist(P[REF], P[j]))
for j in four:
    px, py = pt(FIELD_A, *P[j][:2])
    A(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="12" fill="none" stroke="{DIM}" '
      f'stroke-opacity="0.55" stroke-width="1"/>')
rx, ry = pt(FIELD_A, *P[REF][:2])
tx, ty = pt(FIELD_A, *P[farthest][:2])
A(f'<line x1="{rx:.1f}" y1="{ry:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="#5a5a60" '
  f'stroke-width="1.3" stroke-dasharray="4 3"/>')
mx, my = (rx + tx) / 2, (ry + ty) / 2
A(f'<rect x="{mx - 10:.1f}" y="{my - 11:.1f}" width="20" height="20" rx="4" fill="#ffffff" '
  f'fill-opacity="0.92"/>')
A(f'<text x="{mx:.1f}" y="{my + 5:.1f}" text-anchor="middle" font-family="{MONO}" '
  f'font-size="14" fill="{INK}">&#8467;</text>')

A(f'<text x="{PA[0] + PAD}" y="{PA[3] - 16}" font-family="{SANS}" font-size="11.5" '
  f'fill="{DIM}">&#8467; = median distance from a particle to its 4th neighbour</text>')

# ── panel B: the same field, blurred by one Gaussian of width σ ───────────────
A('<g clip-path="url(#clipB)">')
for fx, fy, w, col in sorted(P, key=lambda p: p[2]):
    px, py = pt(FIELD_B, fx, fy)
    A(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{2.35 * SIGMA:.1f}" '
      f'fill="url(#g{col.lstrip("#")})" fill-opacity="{0.34 + 0.44 * w:.2f}"/>')
A('</g>')

bx, by = pt(FIELD_B, *P[REF][:2])
by = min(max(by, FIELD_B[1] + 20), FIELD_B[3] - 34)
A(f'<line x1="{bx - SIGMA:.1f}" y1="{by:.1f}" x2="{bx + SIGMA:.1f}" y2="{by:.1f}" '
  f'stroke="#3a3a40" stroke-opacity="0.65" stroke-width="1.3" marker-start="url(#arw)" '
  f'marker-end="url(#arw)"/>')
A(f'<text x="{bx + SIGMA + 9:.1f}" y="{by + 5:.1f}" font-family="{MONO}" font-size="14" '
  f'fill="#3a3a40">2&#963;</text>')

A(f'<text x="{PB[0] + PAD}" y="{PB[3] - 16}" font-family="{SANS}" font-size="11.5" '
  f'fill="{DIM}">&#963; = 0.85 &#8467;, in world units of the box</text>')

# ── panel C: the identical kernel over a coarse and a fine voxel grid ────────
SIGMA_C = 30.0                    # px; 2 cells on the coarse grid, 4 on the fine one
CY = 498.0
GRID = 150.0

A(f'<line x1="450" y1="{PC[1] + 16}" x2="450" y2="{PC[3] - 24}" stroke="{EDGE}" '
  f'stroke-width="1"/>')

for cx, cell, span, res, note in ((240.0, 15.0, 10, "400&#179;", "&#963; &#8776; 2 voxels"),
                                  (660.0, 7.5, 20, "800&#179;", "&#963; &#8776; 4 voxels")):
    half = cell * span / 2
    x0, y0 = cx - half, CY - half
    A(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{GRID:.1f}" height="{GRID:.1f}" '
      f'fill="#ffffff" stroke="{FAINT}"/>')
    # One flat value per voxel: sample the Gaussian at the cell centre.
    for j in range(span):
        for k in range(span):
            d = math.hypot((k + 0.5) * cell - half, (j + 0.5) * cell - half)
            a = 0.9 * math.exp(-(d * d) / (2 * SIGMA_C * SIGMA_C))
            A(f'<rect x="{x0 + k * cell:.1f}" y="{y0 + j * cell:.1f}" width="{cell:.1f}" '
              f'height="{cell:.1f}" fill="{mix("#ffffff", AMBER, a)}"/>')
    for k in range(span + 1):
        x, y = x0 + k * cell, y0 + k * cell
        A(f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y0 + GRID:.1f}" '
          f'stroke="#2b2b30" stroke-opacity="0.16" stroke-width="1"/>')
        A(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x0 + GRID:.1f}" y2="{y:.1f}" '
          f'stroke="#2b2b30" stroke-opacity="0.16" stroke-width="1"/>')
    # 2 sigma, drawn over the grid in cells
    ay = y0 + GRID - 15
    A(f'<line x1="{cx - SIGMA_C:.1f}" y1="{ay:.1f}" x2="{cx + SIGMA_C:.1f}" y2="{ay:.1f}" '
      f'stroke="#2b2b30" stroke-opacity="0.75" stroke-width="1.3" marker-start="url(#arw)" '
      f'marker-end="url(#arw)"/>')
    A(f'<rect x="{cx + SIGMA_C - 5:.1f}" y="{ay - 20:.1f}" width="24" height="15" rx="3" '
      f'fill="#ffffff" fill-opacity="0.9"/>')
    A(f'<text x="{cx + SIGMA_C + 7:.1f}" y="{ay - 9:.1f}" text-anchor="middle" '
      f'font-family="{MONO}" font-size="11.5" fill="#3a3a40">2&#963;</text>')
    # caption, centred under the grid
    A(f'<text x="{cx:.1f}" y="{y0 + GRID + 26:.1f}" text-anchor="middle" font-family="{SANS}" '
      f'font-size="12" fill="{DIM}"><tspan font-weight="600" fill="{INK}">{res} grid</tspan>'
      f'<tspan> &#183; {note} &#183; 2&#963; = {int(round(2 * SIGMA_C / cell))} voxels</tspan></text>')

A('</svg>')

svg = "\n".join(out)
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.join(root, "static/img/2026/10/galaxy-rendering-smoothing.svg")
open(path, "w", encoding="utf-8").write(svg + "\n")
print("wrote", path, len(svg), "bytes")
