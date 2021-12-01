+++
author = "Toni Sagrista Selles"
categories = ["Git"]
tags = ["programming", "git", "vcs", "english"]
date = 2021-12-01
linktitle = ""
title = "Git bisect"
description = ""
featuredpath = "date"
type = "post"
+++

When I started using git as my VCS I skimmed the docs and `git-bisect` caught my eye. I got acquainted with it rather quickly and have been using it rather heavily ever since. [`git-bisect`](https://git-scm.com/docs/git-bisect) is a little handy git sub-command typically used to quickly narrow down the commit where a bug was introduced in a code base. It uses a simple binary search tree algorithm (BST) to test out different revisions by parting the remaining search space in *half*.

<!--more-->

Basically, one needs just one thing to start bisecting: the last known version that works---where the bug was **not** there. Then, we start bisecting with:

```bash
git bisect start             # start bisecting
git bisect bad               # current revision is bad
git bisect good good-commit  # good-commit revision is last known to work
```

The system will automatically start the BST and sequentially check out different commits for you to test. Once a commit has been tested we can mark it *bad* if the bug is still there:

```bash
git bisect bad
```

Or *good*, if the bug was not yet present:
```bash
git bisect good
```

When we have exhausted the search the system will inform us that we've found the offending commit. Then, we can end the process with:

```bash
git bisect reset
```

We can also visualize the current bisect progress with `gitk` using:

```bash
git bisect visualize
```
Note that this last command only works if a bisect is in progress in the current directory.

<!-- Loading MathJax -->
<script type="text/javascript" id="MathJax-script" async src="/js/mathjax3.js"></script>

The number of steps needed to locate a bug within a list of \\(n\\) commits is roughly ~\\(\mathcal{O}(\log{}n)\\). This is very good news, especially with projects with long histories and lots of commits. In the following example, we have in the history commits A to I, while main is the current head. In that case, we would find the culprit in 3 steps.

```

Visiting order:             3     2        1
                                             
Commits:               A -> B -> C -> D -> E -> F -> G -> H -> I -> main
                       ^    *                                        ^
                       |                                             |
                     good                                           bad
```
