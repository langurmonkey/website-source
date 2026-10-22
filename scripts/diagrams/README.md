# Diagram generators

Small Python scripts that emit the hand-drawn SVG figures used in blog posts.
Each one writes straight into `static/img/` and is safe to re-run; the output is
deterministic and version-controlled, so the source of truth is the script, not
the SVG.

| Script | Output | Used by |
|---|---|---|
| `make-splatting-svg.py` | `static/img/2026/10/galaxy-rendering-splatting.svg` | `content/blog/2026/galaxy-rendering.md`, section "Splatting" |
| `make-smoothing-svg.py` | `static/img/2026/10/galaxy-rendering-smoothing.svg` | same post, section "Smoothing without inventing detail" |

Run them from the repo root (or via `just diagrams`):

```sh
python3 scripts/diagrams/make-splatting-svg.py
python3 scripts/diagrams/make-smoothing-svg.py
```

Conventions, so the figures stay consistent with each other and with the site:

- 900 px wide canvas, white background (the figures are not theme-aware).
- System font stacks only, no embedded fonts, no external references.
- Text uses numeric entities (`&#963;`), never named ones: SVG is parsed as XML,
  where `&sigma;` is undefined and kills the file.
- Hues mirror the post's palette: cyan/amber/pink for the particle colours.
