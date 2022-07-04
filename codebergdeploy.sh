#!/usr/bin/env bash

# Deploy the website to codeberg.

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Source.
if [ -z ${WEB+x} ]; then
  WEB=$SCRIPT_DIR
fi

# Destination.
if [ -z ${WEBDEPLOY+x} ]; then
  WEBDEPLOY=$PROJ/website-deploy/
fi

# Check destination exists and is a git repo.
if [ ! -d "$WEBDEPLOY" ]; then
  echo "Deploy directory $WEBDEPLOY does not exist!"
  exit 1
fi

# Generate site.
cd $WEB
hugo --minify

# Copy over to $WEBDEPLOY.
rsync -avh $WEB/public/ $WEBDEPLOY/

# Add, commit, push.
cd $WEBDEPLOY
git add .
git commit -m "none: new deployment."
git push -f --all

echo "Done!"

