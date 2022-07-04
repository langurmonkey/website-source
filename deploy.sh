#!/usr/bin/env bash

# This script deploys a Hugo website to the specified branches
# with the given domains, using the given codeberg repository under
# the 'remote_name' variable.
# Just run it without arguments and it will do its thing.

# Original source: https://codeberg.org/adam/website/src/branch/main/deploy.sh

# the hugo build directory.
build_directory="public"
# the branch to deploy to.
build_branches=("pages" "pages-1")
# domains, number must match the branches.
domains=("https://sagrista.info" "https://tonisagrista.com")
# name of the codeberg remote.
remote_name="cb"

len=${#build_branches[@]}
len_dom=${#domains[@]}

if [ $len -ne $len_dom ]; then
  echo "The length of the 'build_branches' array does not match that of 'domains'."
  echo "Please check the variables at the top of the file."
  exit 1
fi

# iterate over all branches and deploy to each one with the matching domain.
for i in ${!build_branches[@]}; do
  step=0

  build_branch=${build_branches[$i]}
  domain=${domains[$i]}

  echo "$((i+1)) / $len : Deploying site to branch '$build_branch' with domain '$domain'"

  # delete previous site built, if it exists.
  if [ -d "$build_directory" ]; then
    step=$(($step+1))
    echo "   ($step) Deleting previous build."
    rm -rf $build_directory
  fi

  # get remote codeberg url.
  remote_origin_url=$(git config --get remote."${remote_name}".url)

  step=$(($step+1))
  echo "   ($step) Building Hugo site..."

  # generate hugo static site to `build` directory.
  hugo --destination "${build_directory}" --minify --quiet

  # initialize a git repo in build_directory and checkout to build_branch.
  step=$(($step+1))
  echo "   ($step) Initializing new git repository, checking out branch '${build_branch}'."
  git -C "${build_directory}" init || echo "   Can't git init."
  git -C "${build_directory}" checkout -b "${build_branch}" || echo "   Can't git checkout."

  # add your domain
  step=$(($step+1))
  echo "   ($step) Adding '.domains' file with '${domain}'."
  echo "${domain}" > "${build_directory}"/.domains

  # stage all files except .gitignore (don't want it in the static site).
  step=$(($step+1))
  echo "   ($step) Staging all files but '.gitignore'."
  git -C "${build_directory}" add -- . ':!.gitignore' || echo "   Can't git add."

  # commit static site files and force push to build_branch of the origin.
  step=$(($step+1))
  echo "   ($step) Committing files."
  git -C "${build_directory}" commit -m "build: update static site." || echo "   Can't git commit."

  # add remote.
  step=$(($step+1))
  echo "   ($step) Adding remote '${remote_name}' pointing to ${remote_origin_url}."
  git -C "${build_directory}" remote add "${remote_name}" "${remote_origin_url}" || echo "   Can't add origin."

  # force-push branch.
  step=$(($step+1))
  echo "   ($step) Force-pushing to remote '${remote_name}', branch '${build_branch}."
  git -C "${build_directory}" push --force "${remote_name}" "${build_branch}" || echo "   Can't git push."

  echo "$((i+1)) / $len : Finished deploying ${build_branch}."
done

