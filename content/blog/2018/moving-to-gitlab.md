+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = [ "programming", "projects", "git", "vcs", "github", "gitlab" ]
date = "2018-06-05"
description = "In light of the new GitHub acquisition by Microsoft"
linktitle = ""
title = "Moving Gaia Sky to GitLab"
featured = "gitlab-github.jpg"
featuredalt = "GitHub to GitLab"
featuredpath = "date"
type = "post"
+++


I'll shortly be moving the Gaia Sky repository from GitHub to GitLab ([link here](https://gitlab.com/langurmonkey/gaiasky)) due
to the former being acquired by Microsoft.

If you have cloned the repository and wonder how to update your remote reference, here's what to do:

<pre><code>$  cd path/to/gaiasky
$  git remote set-url origin https://gitlab.com/langurmonkey/gaiasky
</code></pre>

That's all it takes. All pulls from now on should be directed to the gitlab repo.
