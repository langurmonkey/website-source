#!/bin/sh
echo "Minifying JS"
LOC=$WEB/themes/langurmonkey/static/js
uglifyjs $LOC/jquery.min.js $LOC/skel.min.js $LOC/codeblock.js $LOC/util.js $LOC/main.js > $LOC/site-bundle.js

