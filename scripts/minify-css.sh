#!/bin/sh
echo "Minifying CSS"

if [[ $# -eq 1 ]]; then
    THEME=$1
else
    THEME=theme-pink-blue
fi
echo "   using theme $THEME"

LOC=$WEB/static/css
minify -b -o $LOC/site-bundle.css $LOC/$THEME.css $LOC/main.css $LOC/add-on.css $LOC/fork-awesome.min.css
