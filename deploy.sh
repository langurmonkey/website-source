#!/usr/bin/env bash

# This script deploys a Hugo website to the specified branch (pages)
# of the given codeberg repository, in 'remote_name'.
# Just run it without arguments and it will do its thing.

# Original source: https://codeberg.org/adam/website/src/branch/main/deploy.sh

# the hugo build directory.
build_directory="public"
# the branch to deploy to.
build_branch="pages"
# name of the codeberg remote.
remote_name="cb"

# delete previous site built, if it exists.
if [ -d "$build_directory" ]; then
  echo "Deleting previous build."
  rm -rf $build_directory
fi

# get remote codeberg url.
remote_origin_url=$(git config --get remote.$remote_name.url)

# generate hugo static site to `build` directory.
hugo --destination $build_directory --minify

# initialize a git repo in build_directory and checkout to build_branch
cd $build_directory || exit
git init
git checkout -b $build_branch

# stage all files except .gitignore (don't want it in the static site)
git add -- . ':!.gitignore'

# commit static site files and force push to build_branch of the origin
git commit -m "build: update static site"
git remote add $remote_name "$remote_origin_url"
git push --force $remote_name $build_branch

echo "Done!"
