+++
author = "Toni Sagrista Selles"
categories = ["website"]
tags = ["git", "repository", "codeberg", "english"]
date = 2022-07-04
linktitle = ""
title = "Hello, Codeberg Pages"
description = "Moving this site from Gitlab Pages to Codeberg Pages"
featuredpath = "date"
type = "post"
+++

In their own words, taken from [the docs](https://docs.codeberg.org/getting-started/what-is-codeberg/), *"Codeberg is a democratic community-driven, non-profit software development platform operated by Codeberg e.V. and centered around Codeberg.org, a Gitea-based software forge."*. Essentially, it is a non-profit platform run on donations for sharing free and open source software by providing a collaborative VCS environment based on [Gitea](gitea.io). One good day I decided to move all my open source repositories from GitLab over to Codeberg, and that includes the hosting of this very website. This is the story of this migration.

<!--more-->

## Why Codeberg pages?

Codeberg offers a [Pages](https://codeberg.page) component where users can deploy, publish and host their own static sites, just like GitHub or GitLab pages. However, the configuration right now is a bit more barebones than in those other proprietary options, as you can't rely on a CI system to deploy the site for you. I like that, as I feel like I'm more in control of the whole process. I can produce the static site locally and then push it to the remote host. Codeberg also supports HTTPS via certificates provided by *Let's Encrypt*. The process of setting this up is totally transparent and, to be frank, surprised me for the better. In my particular case, I need the site to be available at my two domains (tonisagrista.com and sagrista.info), which adds a grain of complexity to the whole thing. 


## Start with the docs

As always, a very good starting point is the official documentation. In this case, a quick visit to [codeberg.page](https://codeberg.page) provides the essential information at a glance:

1. Create a public repository named `pages`, **or** create a `pages` branch in an existing public repository.
2. Push your static webiste content into that repo or branch.
3. Done! Your repository should be accessible at `https://USER.codeberg.page/[/REPO][/@BRANCH]`. However, if you want to use your own domain you need (a) a `.domains` file with the domain name, and (b), the following DNS configuration:

    - `A 217.197.91.145`
    - `@ TXT [[BRANCH.]REPO.]USER.codeberg.page`

That works pretty well. In my experience, the DNS records took a while to update and the HTTPS certificate (via Let's Encrypt) returned certificate errors for a while. After that short period, all worked just fine.

## More than one domain, no redirection

However, the issue comes when trying to add two domains without redirection. You see, the `.domains` file contains a domain name in each line. The first domain name is the main one, while all the others are redirected to the first. What if you do not want redirection? The solution is to deploy your site to different branches, one for each domain. This involves pushing a different `.domains` file to each of the branches, and using a different `TXT` record for each domain name, pointing to the relevant branch. 

Again, in my case, I generate my static site using Hugo from a repository that contains the source files (which lives in the `master` branch). To actually generate it, I need to invoke the CLI program `hugo`. This generates the static site in a sub-directory (named `public` by default), which I need to push to a different branch for each of my domains. I'm using the following branches for the listed domains:

| Domain               | Branch        |
|----------------------|---------------|
| [tonisagrista.com]() | `pages`       |
| [sagrista.info]()    | `pagesmirror` |

I have written a shell script which deploys the sites according to the configuration at the top. A list of domain/branch pairs is provided, the rest is handled automatically.

{{< highlight bash "linenos=table" >}}
#!/usr/bin/env bash

# This script deploys a Hugo website to the specified branches
# with the given domains, using the given codeberg repository under
# the 'remote_name' variable.
# Just run it without arguments and it will do its thing.

# Original source: https://codeberg.org/adam/website/src/branch/main/deploy.sh

# the hugo build directory.
build_directory="public"
# the branch to deploy to.
build_branches=("pages" "pagesmirror")
# domains, number must match the branches.
domains=("https://tonisagrista.com" "https://sagrista.info")
# name of the codeberg remote.
remote_name="cb"

len=${#build_branches[@]}
len_dom=${#domains[@]}

if [ $len -ne $len_dom ]; then
  echo "The length of the 'build_branches' array does not match that of 'domains'."
  echo "Please check the variables at the top of the file."
  exit 1
fi

  echo "Running minify script."
# First, minify using the default theme (theme-bw)
scripts/minify-all.sh theme-bw

# iterate over all branches and deploy to each one with the matching domain.
for i in ${!build_branches[@]}; do
  step=0

  build_branch=${build_branches[$i]}
  domain=${domains[$i]}

  echo "($((i+1))/$len)   Deploying site to branch '$build_branch' with domain '$domain'."

  # delete previous site built, if it exists.
  if [ -d "$build_directory" ]; then
    step=$(($step+1))
    echo "    ($step) Deleting previous build."
    rm -rf $build_directory
  fi

  # get remote codeberg url.
  remote_origin_url=$(git config --get remote."${remote_name}".url)

  step=$(($step+1))
  echo "    ($step) Building Hugo site."

  # generate hugo static site to `build` directory.
  hugo --destination "${build_directory}" --minify --quiet

  # initialize a git repo in build_directory and checkout to build_branch.
  step=$(($step+1))
  echo "    ($step) Initializing new git repository, checking out branch '${build_branch}'."
  git -C "${build_directory}" init || echo "   Can't git init."
  git -C "${build_directory}" checkout -b "${build_branch}" || echo "    ERROR: Can't git checkout."

  # add your domain
  step=$(($step+1))
  echo "    ($step) Adding '.domains' file with '${domain}'."
  echo "${domain}" > "${build_directory}"/.domains

  # stage all files except .gitignore (don't want it in the static site).
  step=$(($step+1))
  echo "    ($step) Staging all files but '.gitignore'."
  git -C "${build_directory}" add -- . ':!.gitignore' || echo "    ERROR: Can't git add."

  # commit static site files and force push to build_branch of the origin.
  step=$(($step+1))
  echo "    ($step) Committing files."
  git -C "${build_directory}" commit -m "build: update static site." || echo "    ERROR: Can't git commit."

  # add remote.
  step=$(($step+1))
  echo "    ($step) Adding remote '${remote_name}' pointing to ${remote_origin_url}."
  git -C "${build_directory}" remote add "${remote_name}" "${remote_origin_url}" || echo "    ERROR: Can't add origin."

  # force-push branch.
  step=$(($step+1))
  echo "    ($step) Force-pushing to remote '${remote_name}', branch '${build_branch}'."
  git -C "${build_directory}" push --force "${remote_name}" "${build_branch}" || echo "    ERROR: Can't git push."

  echo "($((i+1))/$len)   Finished deploying ${build_branch}."
done
{{</ highlight >}}

Line 13 contains the list of branches. Line 15 contains the domains. These are matched by position, so take that into account.
Some parts are specific to my configuration, like the call to `minify-all` on line 30. You can ignore those. As for the rest, I only need to edit the sources of my site and then run the script. The site is automatically deployed to both my domains.

