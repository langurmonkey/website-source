#!/bin/sh
BASEDIR=$(dirname "$0")
sh $BASEDIR/minify-css.sh "$@"
sh $BASEDIR/minify-js.sh
