+++
author = "Toni Sagrista Selles"
categories = ["Programming"]
tags = ["git", "svn", "programming", "development", "english"]
date = 2021-11-28
linktitle = ""
title = "Semantic commit messages"
description = "Use your git history like a pro and reap the benefits (almost) instantly"
featuredpath = "date"
type = "post"
+++

Do you often find yourself using "New feature", "More" or similar short, useless and generic strings as your git commit messages? I know I did. Until I learned about semantic commit messages, that is. What are they and how can they exponentially improve your commit history and make it actually useful? I'm discussing it in this post.

<!--more-->

[Semantic commit messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716) are intended to bring some structure and order to your git history---or whatever VCS you happen to use. Essentially, they define a format that all your commit messages should be in, so that they can be easily parsable and processed automatically. I think they bring very many benefits to your regular developer's workflow:

1. You will actually need think about what is in your commit.
2. Your commits will be unitary---each covering a single topic (bug fix, feature, etc.).
3. Your git history will be better structured and you don't need to *read* too hard to find stuff.
4. You can use your git history for neat things, like auto-generating change logs.
5. Once you have used it for a couple of weeks, you'll find yourself doing it effortlessly almost without thinking!

So, the commit format you need to use is this:

```
type: desription

body (optional)

footer (optional)
```

-  The **type** can typically be one of:

    - `feat` -- new feature or improvement.
    - `fix` -- bug fix, should possibly reference the issue id in footer or body.
    - `docs` -- changes to the documentation (`README`, `ACKNOWLEDGEMENTS`, etc.).
    - `style` -- changes that don't affect functionality or such as cosmetic changes or formatting.
    - `refactor` -- code refactoring which does not modify functionality or fix a bug, class changes, name changes, moves, etc.
    - `perf` -- changes that improve or address performance issues.
    - `build` -- changes to the build and continuous integration systems, or to run scripts and installer files.
    - `none` -- minor changes that do not fit in any other category, or partial, non-finished commits.
- The **description** is a summary written in **present tense**. This is important to keep a consistent format and avoid mixing tenses, which looks and *feels* very bad and sloppy once you read all commit messages one after the other. "`refactor: move render system to render package`" is a correct description, while "`refactor: render system moved to render package`" is not. You'll thank me later.
 - In the **body** you can develop the topic to your heart's content, if you want.
- The **footer** is usually reserved for annotations and references such as the issue number it fixes or the new feature it references.

For example, this would be a valid commit message:

```
fix: super annoying bug

Fix the stars getting obliterated when the user clicks on 'help'

Fixes #234
```

I'm using this format in pretty much all my repositories and the histories are understandable, at least to a degree, even by people that do not know anything about the projects. See the [Gaia Sky repository history](https://gitlab.com/langurmonkey/gaiasky/-/commits/master/), my [dotfiles](https://gitlab.com/langurmonkey/dotfiles/-/commits/master/) or even the [repository for this very site](https://gitlab.com/langurmonkey/langurmonkey.gitlab.io/-/commits/master/).

The format I use in Gaia Sky is described [here](https://gitlab.com/langurmonkey/gaiasky/-/blob/master/CONTRIBUTING.md). One of the major benefits is that I actually generate the [change log file](https://gitlab.com/langurmonkey/gaiasky/-/blob/master/CHANGELOG.md) automatically using [`git-chglog`](https://github.com/git-chglog/git-chglog).


I find myself using the types `fix`, `feat`, `none` and `build` a lot. 
