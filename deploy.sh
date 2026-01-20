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
# stats update script in the server
stats_update="/home/tmp/updatestats"


# DEPLOY
echo "## Deploying site to ${ssh_server}:${server_dir}."

flags=""
if [ ${clean_deploy} = true ]; then
  flags="--delete"
fi

echo "## Copying data to server."
# copy contents of ${build_directory} to server
rsync -avh --cvs-exclude ${flags} ${build_directory}/ ${ssh_server}:${server_dir}/

echo "## Finished deploying site to ${ssh_server}:${server_dir}."
