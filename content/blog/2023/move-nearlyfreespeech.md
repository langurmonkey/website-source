+++
author = "Toni Sagristà Sellés"
title = "I'm moving"
description = "From Codeberg Pages to NearlyFreeSpeech.NET."
date = "2023-01-22"
linktitle = ""
featured = ""
featuredpath = ""
featuredalt = ""
categories = ["Website"]
tags = ["website", "hosting", "english"]
type = "post"
+++

Just a short note. I have moved this site from [Codeberg Pages](/blog/2022/codeberg-setup/) to [nearlyfreespeech.net](https://nearlyfreespeech.net). By the time you are reading this the move should already be finished. This hosting service is dirt-cheap for low-traffic static sites like mine. Right now, my estimated total sits at $0.31 per month, which is $3.72 per year. Less than the cheapest price **per month** offered by most other hosting providers. But they also only offer starting packages allocating many more resources than what is needed for simple static websites.

What I really like about NearlyFreeeSpeech.NET is that it is super-barebones and they opt for a clear no-nonsense approach. Their [website](https://nearlyfreespeech.net) has a very refreshing web-1.0 look and feel. The services are simple and reliable (so far). You need to set up your own site and transfer it via SSH (or FTP, meh). There is no cPanel or other nonsense interfaces. They offer no support by default (you have to pay for it separately), which is probably why they can keep the prices so low. In short, they expect you to know your stuff.

Setting up **Let's Encrypt** is also a breeze. After adding your aliases to your site ([tonisagrista.com](https://tonisagrista.com) and [sagrista.info](https://sagrista.info) in my case), you can just ssh into your server and run `tls-setup.sh`. This is a 170-line shell script which sets up TLS with Let's Encrypt for you, and it is available by default in your server under `/usr/local/bin/tls-setup.sh`.

I also simplified the [deploy.sh](https://codeberg.org/langurmonkey/website-source/src/commit/ddb3ec73cba02f0a05d275b96f2a1785d1f9b129/deploy.sh) script for this site, which used to build the site and commit it to different branches in the Codeberg repository for the different aliases. Now, it just builds the site and `rsync`s it to the server:

```deploy.sh
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
build_directory="public"

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
rsync -avh ${build_directory}/* ${ssh_server}:${server_dir}/

echo "## Finished deploying site to ${ssh_server}:${server_dir}."
```

So far, I'm very happy with the change.
