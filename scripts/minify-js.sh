#!/bin/sh
echo "Minifying JS"
LOC=$WEB/static/js
minify -b -o "$LOC/site-bundle.js.tmp" "$LOC/codeblock.js" "$LOC/util.js" "$LOC/main.js" \
  && cat "$LOC/cash.min.js" "$LOC/skel.min.js" "$LOC/site-bundle.js.tmp" > "$LOC/site-bundle.js" \
  && rm -f "$LOC/site-bundle.js.tmp"
