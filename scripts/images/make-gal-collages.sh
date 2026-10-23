#!/usr/bin/env bash
# Build side-by-side collages (top | side | wide) for each galNN set.
# Writes a full-resolution and a small version next to the sources.
#
# Usage: scripts/images/make-gal-collages.sh [dir] [small-width]
#   dir         directory holding galNN-{top,side,wide}.jpg (default: static/img/2026/10)
#   small-width total width of the small collage in px (default: 1600)

set -euo pipefail

DIR="${1:-static/img/2026/10}"
SMALL_W="${2:-1600}"

cd "$(dirname "$0")/../.."

shopt -s nullglob
for top in "$DIR"/gal*-top.jpg; do
    base="${top%-top.jpg}"
    side="$base-side.jpg"
    wide="$base-wide.jpg"
    [ -f "$side" ] && [ -f "$wide" ] || { echo "skip $base: incomplete set"; continue; }

    out="$base-collage.jpg"
    montage "$top" "$side" "$wide" -tile 3x1 -geometry +0+0 -quality 92 "$out"

    small="$base-collage-small.jpg"
    magick "$out" -resize "${SMALL_W}x" -quality 88 "$small"

    printf '%s\n  %s\n  %s\n' "$out" \
        "$(identify -format '%wx%h %b' "$out")" \
        "$(identify -format '%wx%h %b' "$small")"
done
