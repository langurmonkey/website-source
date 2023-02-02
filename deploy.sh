#!/usr/bin/env bash

# This script deploys a Hugo website to the specified server
# via SSH. SSH keys are assumed to be already configured and 
# active.
# Just run it without arguments and it will do its thing.

clean_deploy=false

# colon after var means it has a value rather than it being a bool flag
while getopts 'c' OPTION; do
  case "$OPTION" in
    c)
      clean_deploy=true
      ;;
    ?)
      echo "Script usage: $(basename $0) [-c]" >&2
      exit -1
      ;;
  esac
done

# the local hugo build directory.
build_directory="./public/"
# the ssh server name.
# please, add an entry with the given name to ~/.ssh/config
# Host nfs
#     HostName ssh.phx.nearlyfreespeech.net
#     TCPKeepAlive yes
#     ServerAliveInterval 300
#     User langurmonkey_tonisagristacom
ssh_server="nfs"
# the public directory in the server where the site is.
server_dir="/home/public"

echo "## Running minify script."
# First, minify using the default theme (theme-bw)
scripts/minify-all.sh theme-bw

# DEPLOY
echo "## Deploying site to ${ssh_server}:${server_dir}."

if [ ${clean_deploy} = true ]; then
  echo "## Cleaning public directory in server."
  # if clean-deploy, delete previous build.
  ssh ${ssh_server} "rm -rf ${server_dir}/*" 
fi

echo "## Generating static site."
# generate hugo static site to `build` directory.
hugo --destination "${build_directory}" --minify --quiet

echo "## Copying data to server."
# copy contents of ${build_directory} to server
rsync -avhtu --delete ${build_directory}/ ${ssh_server}:${server_dir}/

echo "## Finished deploying site to ${ssh_server}:${server_dir}."
