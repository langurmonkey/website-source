#!/bin/sh
echo "Minifying CSS"

if [[ $# -eq 1 ]]; then
    THEME=$1
else
    THEME=theme-pink-blue
fi
echo "   using theme $THEME"

LOC=$WEB/static/css
uglifycss $LOC/$THEME.css $LOC/main.css $LOC/add-on.css $LOC/fork-awesome.min.css > $LOC/site-bundle.css
