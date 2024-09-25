#!/usr/bin/env bash

# This script updates the AWStats in the NFS server
# via SSH. SSH keys are assumed to be already configured and 
# active.
# Just run it without arguments and it will do its thing.

# the ssh server name.
# please, add an entry with the given name to ~/.ssh/config
# Host nfs
#     HostName ssh.phx.nearlyfreespeech.net
#     TCPKeepAlive yes
#     ServerAliveInterval 300
#     User langurmonkey_tonisagristacom
ssh_server="nfs"
# stats update script in the server
stats_update="/home/tmp/updatestats"


echo "## Updating stats by running awstats script."
ssh -i /home/tsagrista/.ssh/id_website ${ssh_server} -t "${stats_update}"

echo "## Done."
