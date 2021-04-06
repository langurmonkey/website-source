#!/bin/sh
echo "Minifying CSS"
LOC=$WEB/themes/langurmonkey/static/css
uglifycss $LOC/theme-pink-blue.css $LOC/main.css $LOC/add-on.css $LOC/fork-awesome.css > $LOC/site-bundle.css
