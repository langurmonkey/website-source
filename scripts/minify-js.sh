#!/bin/sh
echo "Minifying JS"
LOC=$WEB/static/js
uglifyjs $LOC/cash.min.js $LOC/skel.min.js $LOC/codeblock.js $LOC/util.js $LOC/main.js > $LOC/site-bundle.js

