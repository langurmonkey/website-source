#!/usr/bin/bash


# Set the target directory where new folders will be created.
# We use a directory with the current date.
DATE_STR=$(date +"%Y%m%d")
GALLERY_DIR=/home/tsagrista/Pictures/photo-gallery/$DATE_STR

# Create the directory if it doesn't already exist
mkdir -p "$GALLERY_DIR"

docker run -t \
  -v /home/tsagrista/Pictures/my-selection:/input:ro \
  -v $GALLERY_DIR:/output \
  -v /home/tsagrista/Projects/website-source:/web:ro \
  -u $(id -u):$(id -g) \
  ghcr.io/thumbsup/thumbsup \
  thumbsup --input /input --output /output --theme-path /web/gallery-theme --config /web/thumbsup-config.json
