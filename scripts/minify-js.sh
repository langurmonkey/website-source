#!/bin/sh
echo "Minifying JS"
LOC=$WEB/static/js
minify -b -o $LOC/site-bundle.js $LOC/cash.min.js $LOC/skel.min.js $LOC/codeblock.js $LOC/util.js $LOC/main.js
