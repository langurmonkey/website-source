+++
author = "Toni Sagrista Selles"
categories = ["vcs"]
tags = ["git", "jj", "jujutsu", "programming", "tooling", "english"]
date = 2024-10-23
linktitle = ""
title = "Jujutsu, a modern version control system"
description = "Jujutsu improves and simplifies on current version control systems"
featuredpath = "date"
type = "post"
+++

I first discovered [Jujutsu](https://github.com/martinvonz/jj) a few weeks ago, and I was immediately intrigued. At first glance, it looked like a simple wrapper around Git, but the deeper I looked, the more impressed I became with its capabilities. In reality, Jujutsu transforms the usual distributed version control system paradigm, by offering a new design that leads to *cleaner* and simpler workflows.

In this post, I have a look at what Jujutsu has to offer, and I dive into its command line interface and usage workflows. My goal is that, by the end of this post, you can understand a little bit why I find this tool so cool.

<!--more-->

## Best Resources

I haven't found many user guides or tutorials on Jujutsu so far. Even the official repository of the project contains a *getting started* tutorial that is outdated (as per their own notice). However, there is an excellent guide written by Steve Klabnik, the author behind no starch press' *The Rust Programming Language*[^1] book, which I [read](/blog/2021/rust-devenv) and enjoyed a few years ago. Anyway, it seems like Steve's guide on Jujutsu is the go-to tutorial to read if you want get started, so here it is:

- [Steve's Jujutsu Tutorial](https://steveklabnik.github.io/jujutsu-tutorial)

If you are the kind of person that would rather watch a video than read a text, there are a couple of good ones:

- [Jujutsu: A Git-Compatible VCS](https://youtu.be/bx_LGilOuE4) -- by Martin von Zweigbergk, the creator of Jujutsu himself.
- [What is version control was AWESOME?](https://youtu.be/2otjrTzRfVk) -- a tutorial series with (so far) only one part.

## Jujutsu Overview

Jujutsu is a simple, modern, easy to use, and change-centric distributed control system that is compatible with Git. This means that it *currently* uses Git as a backend, and you can start using it now with your pre-existing Git repositories. 

This is similar to what Git did in its early days with the `git svn` bridge. This drove initial adoption because it was easy to communicate changesets between Subversion and Git. However, it is also different, because Git never used SVN as a backend, like Jujutsu does with Git. This last part is probably driven by the immense adoption of GitHub and similar services, and by Git being the *de facto* standard as <acronym title="Distributed Version Control System">DVCS</acronym>es go.

More interesting is Jujutsu's design, which contains some interesting points. 

- **Changes** -- we have *changes* in addition to our usual *revisions*. The *change model* is borrowed from Mercurial, and identify units of work that may span several revisions. 
- **Committed working copy** -- everything within a change is committed automatically, so you don't actually need to explicitly run a counterpart to `git commit`. This is achieved in other ways, as we'll see in a moment. 
- **Branches are anonymous** -- branches are identified by the descriptions in their commits, but they are anonymous by default. However, since the backend is Git, there exist named *bookmarks*, which can act as branch names.
- **Automatic conflict resolution** -- conflicts are not scary here. In Git, conflicts are something that you need to get rid of before going on with your life, but in Jujutsu, they are accepted and even committed to the repository. You get an annotation on the change reminding you that the conflict is there, and that you probably need to address it at some point. But in your own time, no need to panic.
- **No staging** -- there is no index or staging area. The working copy itself is committed as it evolves, and amended on every change.
- **Awesome CLI** -- the command line interface is so damn comfy to use. If using the Git CLI is bumping into a wall with your shoulder at full speed, using `jj` is like getting a gentle and pleasant back massage. 


Before you ask, yes, the name 'Jujutsu' is weird indeed. My understanding is that this is purely anecdotical. The binary was first, and it was named `jj` because it is easy to type and remember. They then assigned the name Jujutsu simply because it matches `jj`.

For the rest of this post I'll be using both Jujutsu and `jj` interchangeably.

## The Jujutsu Workflow

Let's get our hands dirty. In this section we'll be creating a repository and performing some operations to illustrate a typical workflow. Before starting, install and setup `jj`. More info on how to do so for your operating system can be found [here](https://martinvonz.github.io/jj/latest/install-and-setup/). 

### Initialize a Repository

First, we need to create an initialize a repository. We create a directory, let's call it `jjtest`, and then `cd` into it. The native `jj` backend is there, but it is disallowed by default, as it is still being worked on, so we'll create a new repository backed by Git:

```sh
$ jj git init
Initialized repor in "."
```

Looks good. If we had a pre-existing Git repository that we want to use `jj` with, we'd use `--git-repo`. For instance, I can do this in my Gaia Sky repository:

```sh
$ cd $GS && jj git init --git-repo
Done importing changes from the underlying Git repo.
Hint: The following remote bookmarks aren't associated with the existing local bookmarks:
  master@gitlab
  master@origin
Hint: Run `jj bookmark track master@gitlab master@origin` to keep local bookmarks updated on future pulls.
Initialized repo in "."
```

As you can see, `jj` detects the existing remotes (`origin` at Codeberg and `gitlab` at GitLab), and informs us that we need to track the master branch. But since we're starting from scratch, this is not necessary.


### Our First Change

We have now a new empty repository. We can see the current status of the repository with `jj st`.

```sh
$ jj st
The working copy is clean
Working copy : swkvvrku a47b8f33 (empty) (no description set)
Parent commit: zzzzzzzz 00000000 (empty) (no description set)
```
In the response we see that our current working copy is empty. In the same line, we see the current change ID (`swkvvrku`) and the current commit ID (`a47b8f33`). The change ID won't change until we create a new change with `jj new`, but the commit ID changes every time we modify something in the working copy. As we mentioned earlier, the working copy is **committed by default**.

In the second line we see the parent of our current change. Every repository starts with a root commit with the same change ID (`zzzzzzzz`) and commit ID (`00000000`). This root commit is present in every repository.

We also see that none of the changes have a description. In `jj`, descriptions are super important because they are (almost) the only way we have to identify our changes. We can add a description to our current change with `jj describe`, or its alias `jj desc`:

```sh
$ jj desc -m "Create the file a.txt"
Working copy now at: swkvvrku ee981442 (empty) Create the file a.txt
Parent commit      : zzzzzzzz 00000000 (empty) (no description set)
```

Interesting. Now, our change is still empty, but it lists the description we just entered. This makes sense. Also, note that since we added a description, which requires amending a commit, we get a new commit ID, from `a47b8f33` to `ee981442`.
In the last command, we could have used `jj desc` without the `-m` argument. Then, a new editor would pop up to edit the description. In my case, this editor is [Helix](/blog/2024/on-neovim-and-helix), and this is what it would have shown:
```hx

JJ: This commit contains the following changes:
JJ:     A a.txt

JJ: Lines starting with "JJ: " (like this one) will be removed.
```
Write the description in the first line, save, and you are done.

Let's now actually do the work and create `a.txt`, and then check the status again.

```sh
$ echo "This is A." > a.txt
$ jj st
Working copy changes:
A a.txt
Working copy : swkvvrku b53a1563 Create the file a.txt
Parent commit: zzzzzzzz 00000000 (empty) (no description set)
```

Right. Our working copy (current change) is not empty anymore. We got yet another commit ID, and now we see that we `A`dded the file `a.txt`, below `Working copy changes:`.

At this point we are done with our first change. We can start a new one with `jj new`.

```sh
$ jj new
Working copy now at: nxlokovw 1afd48be (empty) (no description set)
Parent commit      : swkvvrku b53a1563 Create the file a.txt
```

There is also a `jj commit -m "desc"` command, but internally it only updates the description and then creates a new change, so it does `jj desc -m "desc"` followed by `jj new`. I like the `desc`/`new` workflow better than the `commit` one, as it enables us to first describe what we're doing and then do the actual work. We'll stick with that. 


### Editing Changes

At any time, we can see the repository log by using `jj log`.

```sh
$ jj log
@  nxlokovw me@tonisagrista.com 2024-10-23 13:23:58 1afd48be
│  (empty) (no description set)
○  swkvvrku me@tonisagrista.com 2024-10-23 13:14:23 b53a1563
│  Create the file a.txt
◆  zzzzzzzz root() 00000000
```

Woah, this is nice. This is the default output log format, and it is so much nicer than most other CLI tools. Wee see three changes:

- The first belongs to the root commit (`zzzzzzzz`)
- The second, the one we just made, where we added `a.txt` (`swkvvrku`)
- The current (empty) change (`nxlokovw`)

Something else to note is that the current change is always annotated with `@`. Moreover, the highlight script in this website does not show this, but if I show you a screenshot of my terminal, you may notice something cool:

{{< fig src="/img/2024/10/jj-log-1.jpg" type="image/jpg" class="fig-center" width="85%" title="A screenshot of a terminal showing the output of `jj log`." loading="lazy" >}}

See the purple letters at the beginning of each change ID? These highlight the minimum prefix that can be used to identify this particular change. In this case, `z` identifies the first change, `s` the second and `n` the third. Once the repository grows, this won't be one-letter prefixes anymore, but they will keep reasonably short for an average number of changes.

What if we want to go and edit the change where we created `a.txt`? Easy, we just use `jj edit`, followed by the change identifier. In this case, the minimum prefix for that change is `s`, so we use that.

```sh
$ jj edit s
Working copy now at: swkvvrku b53a1563 Create the file a.txt
Parent commit      : zzzzzzzz 00000000 (empty) (no description set)
```

The output suggests that our working copy now is the change `swkvvrku`. If we show the log, we see that the `@` has changed, but the top change is no more:

```sh
$ jj log
@  swkvvrku me@tonisagrista.com 2024-10-23 13:14:23 b53a1563
│  Create the file a.txt
◆  zzzzzzzz root() 00000000
``` 

Of course, we had an empty change with no description, so it was discarded. We effectively reverted the `jj new` we ran before. Let's re-run it, and add a description.

```sh
$ jj new
Working copy now at: orytlsoz 3905ce5e (empty) (no description set)
Parent commit      : swkvvrku b53a1563 Create the file a.txt

$ jj desc -m "Create the file b.txt"
Working copy now at: orytlsoz 1c4c385a (empty) Create the file b.txt
Parent commit      : swkvvrku b53a1563 Create the file a.txt
```

Now we have an empty change with a description that reads `Create a file b.txt`.

```sh
$ jj log
@  orytlsoz me@tonisagrista.com 2024-10-23 13:53:27 1c4c385a
│  (empty) Create the file b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 13:14:23 b53a1563
│  Create the file a.txt
◆  zzzzzzzz root() 00000000
```

Let's actually create the file.

```sh
echo "This is B." > b.txt
$ jj st
Working copy changes:
A b.txt
Working copy : orytlsoz d3e8a557 Create the file b.txt
Parent commit: swkvvrku b53a1563 Create the file a.txt
```
Our current working change contains a new file (which was automatically committed) and a description. Let's try to redo the `jj edit s`.

```sh
$ jj edit s
Working copy now at: swkvvrku b53a1563 Create the file a.txt
Parent commit      : zzzzzzzz 00000000 (empty) (no description set)
Added 0 files, modified 0 files, removed 1 files
```
If we check the log now, we see that the `@` is in the middle change.

```sh
$ jj log 
○  orytlsoz me@tonisagrista.com 2024-10-23 13:56:09 d3e8a557
│  Create the file b.txt
@  swkvvrku me@tonisagrista.com 2024-10-23 13:14:23 b53a1563
│  Create the file a.txt
◆  zzzzzzzz root() 00000000
```

We are now in the middle change. If we do `ls`, we'll see that our file `b.txt` is not there. This makes sense, as we are back at the previous change. We can now even edit this change and get away with it! Let's do it.

```sh
$ echo "More content for A." >> a.txt
```
And we check the status.

```sh
$ jj st
Rebased 1 descendant commits onto updated working copy
Working copy changes:
A a.txt
Working copy : swkvvrku 214154bf Create the file a.txt
Parent commit: zzzzzzzz 00000000 (empty) (no description set)
```

Wild! The output suggests that the descendant commit, where we created `b.txt`, was automatically rebased. Of course, we modified its parent, so the commits that follow need to be rebased, but `jj` did this automatically for us. Just like that, what a champ.

```sh
$ jj log
○  orytlsoz me@tonisagrista.com 2024-10-23 14:01:58 bb3d48dc
│  Create the file b.txt
@  swkvvrku me@tonisagrista.com 2024-10-23 14:01:58 214154bf
│  Create the file a.txt
◆  zzzzzzzz root() 00000000
```
Maybe, now that we're at it, we can also change the description of this change to reflect a little bit better what happended.

```sh
$ jj desc -m "Create the file a.txt, and then edit it"
Rebased 1 descendant commits
Working copy now at: swkvvrku b1f00d10 Create the file a.txt, and then edit it
Parent commit      : zzzzzzzz 00000000 (empty) (no description set)
```
Again, a rebase was needed, because we amended a description.

```sh
$ jj log
○  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
│  Create the file b.txt
@  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
◆  zzzzzzzz root() 00000000
```
The log reflects the new description. Awesome. We can now go back to our previous change, where we created `b.txt`, and continue from there. To do so, we move our current change (marked by `@`) in the graph, to `orytlsoz`. We can just use the minimum unique prefix, which is `o` in this case.

```sh
$ jj edit o
Working copy now at: orytlsoz 186df778 Create the file b.txt
Parent commit      : swkvvrku b1f00d10 Create the file a.txt, and then edit it
Added 1 files, modified 0 files, removed 0 files
```
Let's check the log for completion. This time around we'll use the `-s` flag, for 'summary'. This shows a listing of the actions in each change, with `A` for additions and `E` for edits.

```sh
$ jj log -s
@  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
│  Create the file b.txt
│  A b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
│  A a.txt
◆  zzzzzzzz root() 00000000
```

Ok. Our repository now has two files, `a.txt` and `b.txt`, and two changes (plus the root one).

### Branches and Bookmarks

As we mentioned already, `jj` has anonymous branches by default. We create branches by creating new changes with non-leaf commits as parents. First of all, we need an empty change, so we do `jj new`.

```sh
$ jj new
Working copy now at: nztukyrp 8da68904 (empty) (no description set)
Parent commit      : orytlsoz 186df778 Create the file b.txt
```
Now, we'll create a new change with `swkvvrku` as parent. This is our first change, where we created `a.txt`. We use the minimum unique prefix `s`.

```sh
$ jj new s
Working copy now at: ulvzlnov 2f751477 (empty) (no description set)
Parent commit      : swkvvrku b1f00d10 Create the file a.txt, and then edit it
Added 0 files, modified 0 files, removed 1 files
```

Seems like it went through. I wonder what the change graph looks like now...

```sh
$ jj log
@  ulvzlnov me@tonisagrista.com 2024-10-23 14:15:46 2f751477
│  (empty) (no description set)
│ ○  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
├─╯  Create the file b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
◆  zzzzzzzz root() 00000000
```
`jj` detected that the parent `swkvvrku` is not a leaf, so it created the new change `orytlsoz` in a branch. Now `swkvvrku` has two children. Let's describe the new work on this branch.

```sh
$ jj desc -m "Create branch.txt"
Working copy now at: ulvzlnov da16ac88 (empty) Create branch.txt
Parent commit      : swkvvrku b1f00d10 Create the file a.txt, and then edit it

$ jj log
@  ulvzlnov me@tonisagrista.com 2024-10-23 14:18:24 da16ac88
│  (empty) Create branch.txt
│ ○  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
├─╯  Create the file b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
◆  zzzzzzzz root() 00000000
```

And now we could create the file with some content in it.

```sh
$ echo "This is BRANCH\!" > branch.txt
$ jj st
Working copy changes:
A branch.txt
Working copy : ulvzlnov 2d5b6567 Create branch.txt
Parent commit: swkvvrku b1f00d10 Create the file a.txt, and then edit it
```

Now we have our working copy, where we created `branch.txt`, and the other branch, where we created `b.txt`. If `ls` now, we should see only `a.txt` and `branch.txt`.

```sh
$ ls -l
drwxr-xr-x  - tsagrista 23 Oct 12:58  .jj
.rw-r--r-- 31 tsagrista 23 Oct 14:01  a.txt
.rw-r--r-- 16 tsagrista 23 Oct 14:19  branch.txt
```

To switch branches we need to move our working copy `@`. We already know how to do it, with `jj edit`!

```sh
$ jj edit o
Working copy now at: orytlsoz 186df778 Create the file b.txt
Parent commit      : swkvvrku b1f00d10 Create the file a.txt, and then edit it
Added 1 files, modified 0 files, removed 1 files

$ ls -l
drwxr-xr-x  - tsagrista 23 Oct 12:58  .jj
.rw-r--r-- 31 tsagrista 23 Oct 14:01  a.txt
.rw-r--r-- 11 tsagrista 23 Oct 14:23  b.txt
```

Just as we predicted, this branch has `a.txt` and `b.txt`, but no `branch.txt`.

Let's say that we are finished with our work in the `branch.txt` branch and need to merge it. There is no `jj merge` (actually, there is, but it is deprecated), but we can use `jj new` instead! You see, `jj new` creates a new change, and by default it acts on `@`. However, you can give it a different change, or even more than one change. And what is a merge commit, but a commit with two or more parents?
Let's remember where we are.

```sh
$ jj log
○  ulvzlnov me@tonisagrista.com 2024-10-23 14:20:03 2d5b6567
│  Create branch.txt
│ @  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
├─╯  Create the file b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
◆  zzzzzzzz root() 00000000
```
We need to merge `orytlsoz` (`o`) and `ulvzlnov` (`u`), so we just create a new change with these two as parents:

```sh
$ jj new o u
Working copy now at: stzsvkul 5eaeba85 (empty) (no description set)
Parent commit      : orytlsoz 186df778 Create the file b.txt
Parent commit      : ulvzlnov 2d5b6567 Create branch.txt
Added 1 files, modified 0 files, removed 0 files

$ ls -l
drwxr-xr-x  - tsagrista 23 Oct 12:58  .jj
.rw-r--r-- 31 tsagrista 23 Oct 14:01  a.txt
.rw-r--r-- 11 tsagrista 23 Oct 14:23  b.txt
.rw-r--r-- 16 tsagrista 23 Oct 14:28  branch.txt
```

Awesome, totally painless. We created a new change on top of two parents, effectively creating a merge commit.

```sh
$ jj log
@    stzsvkul me@tonisagrista.com 2024-10-23 14:28:21 5eaeba85
├─╮  (empty) (no description set)
│ ○  ulvzlnov me@tonisagrista.com 2024-10-23 14:20:03 2d5b6567
│ │  Create branch.txt
○ │  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
├─╯  Create the file b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
◆  zzzzzzzz root() 00000000
```

This merge commit has no description, so we can add it to make it explicit.

```sh
$ jj desc -m "My merge"
```

Now, my merge is an empty change with a description, but no actual file changes. I like to leave it like this, so that my graph is nice and clean. Let's create a new change on top of it.

```sh
$ jj new
Working copy now at: rvmypmmr f9d87a00 (empty) (no description set)
Parent commit      : stzsvkul 5c5f3930 (empty) My merge

$ jj log
@  rvmypmmr me@tonisagrista.com 2024-10-23 14:31:13 f9d87a00
│  (empty) (no description set)
○    stzsvkul me@tonisagrista.com 2024-10-23 14:30:26 5c5f3930
├─╮  (empty) My merge
│ ○  ulvzlnov me@tonisagrista.com 2024-10-23 14:20:03 2d5b6567
│ │  Create branch.txt
○ │  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
├─╯  Create the file b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
◆  zzzzzzzz root() 00000000
```

I hope you are beginning to see how powerful and simple this is. To finish this little tutorial, I'll cover how `jj` manages conflicts.

### Conflicts

Conflicts are a common pain point in most DVCS. In `jj` they are still annoying, but much more pleasant to work with. Let's create some conflicts in our test repository. First, let's add a description to our current change, edit `branch.txt`, and add some text to it.

```sh
$ echo "This is SPARTA." >> branch.txt 
$ jj desc -m "Add sparta to branch.txt"
Working copy now at: rvmypmmr 22ff369c Add sparta to branch.txt
Parent commit      : stzsvkul 5c5f3930 (empty) My merge
```
Now, let's add a new change below `stzsvkul` (`st`) that also modifies `branch.txt`.

```sh
$ jj new st
Working copy now at: mnrotqpk 82d15389 (empty) (no description set)
Parent commit      : stzsvkul 5c5f3930 (empty) My merge
Added 0 files, modified 1 files, removed 0 files

$ jj desc -m "Add athens to branch.txt"
Working copy now at: mnrotqpk 2d65e858 (empty) Add athens to branch.txt
Parent commit      : stzsvkul 5c5f3930 (empty) My merge

$ echo "This is ATHENS." >> branch.txt
```

And now let's have a look at our graph.

```sh
$ jj log
@  mnrotqpk me@tonisagrista.com 2024-10-23 14:44:23 b4f9dc97
│  Add athens to branch.txt
│ ○  rvmypmmr me@tonisagrista.com 2024-10-23 14:41:24 22ff369c
├─╯  Add sparta to branch.txt
○    stzsvkul me@tonisagrista.com 2024-10-23 14:30:26 5c5f3930
├─╮  (empty) My merge
│ ○  ulvzlnov me@tonisagrista.com 2024-10-23 14:20:03 2d5b6567
│ │  Create branch.txt
○ │  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
├─╯  Create the file b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
◆  zzzzzzzz root() 00000000
```

Now, we'll create a new change on top of Sparta (`rvmypmmr`, or just `r`) and Athens (`mnrotqpk`, or just `m`).

```sh
$ jj new r m
Working copy now at: mmwylxnr 7efe8ac0 (conflict) (empty) (no description set)
Parent commit      : mnrotqpk b4f9dc97 Add athens to branch.txt
Parent commit      : rvmypmmr 22ff369c Add sparta to branch.txt
Added 0 files, modified 1 files, removed 0 files
There are unresolved conflicts at these paths:
branch.txt    2-sided conflict
```

`jj` promptly informs us that we have a conflict, since we modified `branch.txt` from both `rvmypmmr` and `mnrotqpk`. Our log also shows the conflict, and marks it read (not visible with this web's highlighting).

```sh
$ jj log
@    mmwylxnr me@tonisagrista.com 2024-10-23 14:45:51 7efe8ac0 conflict
├─╮  (empty) (no description set)
│ ○  rvmypmmr me@tonisagrista.com 2024-10-23 14:41:24 22ff369c
│ │  Add sparta to branch.txt
○ │  mnrotqpk me@tonisagrista.com 2024-10-23 14:44:23 b4f9dc97
├─╯  Add athens to branch.txt
○    stzsvkul me@tonisagrista.com 2024-10-23 14:30:26 5c5f3930
├─╮  (empty) My merge
│ ○  ulvzlnov me@tonisagrista.com 2024-10-23 14:20:03 2d5b6567
│ │  Create branch.txt
○ │  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
├─╯  Create the file b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
◆  zzzzzzzz root() 00000000
```

Now we could just describe this, and keep doing work. `jj` won't complain, it will simply take note that we have a conflict at that change.

```sh
$ jj desc -m "Conflict between Athens and Sparta"
Working copy now at: mmwylxnr 0fbc6b52 (conflict) (empty) Conflict between Athens and Sparta
Parent commit      : mnrotqpk b4f9dc97 Add athens to branch.txt
Parent commit      : rvmypmmr 22ff369c Add sparta to branch.txt
There are unresolved conflicts at these paths:
branch.txt    2-sided conflict

$ jj new
Working copy now at: kxsmtptp 0c87696c (conflict) (empty) (no description set)
Parent commit      : mmwylxnr 0fbc6b52 (conflict) (empty) Conflict between Athens and Sparta
There are unresolved conflicts at these paths:
branch.txt    2-sided conflict
```

When we are ready to resolve the conflict, we need to go back and edit the merge change, `mmwylxnr` (`mm`).

```sh
$ jj edit mm
Working copy now at: kxsmtptp 0c87696c (conflict) (empty) (no description set)
Parent commit      : mmwylxnr 0fbc6b52 (conflict) (empty) Conflict between Athens and Sparta
There are unresolved conflicts at these paths:
branch.txt    2-sided conflict
```

And then just edit the conflicted file `branch.txt`. It looks like this:

```sh
$ cat branch.txt
This is BRANCH!
<<<<<<< Conflict 1 of 1
%%%%%%% Changes from base to side #1
+This is ATHENS.
+++++++ Contents of side #2
This is SPARTA.
>>>>>>> Conflict 1 of 1 ends
```

This is a bit different from Git. Here `<<<<<<<` and `>>>>>>>` indicate the start and end of the conflict, and `%%%%%%%` and `+++++++` indicate the changes from either side. In order to resolve this, we edit the file to look like this:

```branch.txt
This is BRANCH!
This is ATHENS.
This is SPARTA.
```

When we save, we can check the status of the repository:

```sh
$ jj st
Working copy changes:
M branch.txt
Working copy : mmwylxnr 96f65e19 Conflict between Athens and Sparta
Parent commit: mnrotqpk b4f9dc97 Add athens to branch.txt
Parent commit: rvmypmmr 22ff369c Add sparta to branch.txt
```
No more conflicts! `jj` automatically resolved the conflict when it detected that we edited it in-file. This is so nice. Let's make sure our conflict is gone by looking at the log.

```sh
$ jj log 
@    mmwylxnr me@tonisagrista.com 2024-10-23 14:53:16 96f65e19
├─╮  Conflict between Athens and Sparta
│ ○  rvmypmmr me@tonisagrista.com 2024-10-23 14:41:24 22ff369c
│ │  Add sparta to branch.txt
○ │  mnrotqpk me@tonisagrista.com 2024-10-23 14:44:23 b4f9dc97
├─╯  Add athens to branch.txt
○    stzsvkul me@tonisagrista.com 2024-10-23 14:30:26 5c5f3930
├─╮  (empty) My merge
│ ○  ulvzlnov me@tonisagrista.com 2024-10-23 14:20:03 2d5b6567
│ │  Create branch.txt
○ │  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
├─╯  Create the file b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
◆  zzzzzzzz root() 00000000
```
Right, gone for good.


In the next few sections I will touch on other aspects of `jj`, but without entering in much detail. First, we'll have a look at the revsets feature, then we'll see how to create named branches with bookmarks, and then we'll touch on the operations log.

### Revsets

We can pass change or commit IDs to most `jj` commands. In addition, `jj` has "revsets", short for "revision sets". Revsets can be expressed with symbols, operators or functions.

For instance, the **symbol** `@` describes the current working change. 

**Operators** describe relationships between changes. We can use logical operators like `&` or `|`, but also things like `::x` to describe the ancestors of `x`.
 
**Functions** are where most of the strength resides. We have `root()` to get the root change, or `all()` to get all of them. But also `ancestors(x)` to get all ancestors of a change, or `description(x)`, to get all changes with `x` in their description.

You can use revsets with any `jj` command. For instance, we can use this in our test repo:

```sh
$ jj log -r 'description(Create)'
○  ulvzlnov me@tonisagrista.com 2024-10-23 14:20:03 2d5b6567
│  Create branch.txt
│ ○  orytlsoz me@tonisagrista.com 2024-10-23 14:05:11 186df778
├─╯  Create the file b.txt
○  swkvvrku me@tonisagrista.com 2024-10-23 14:05:11 b1f00d10
│  Create the file a.txt, and then edit it
~
```

### Bookmarks

Bookmarks are a way to attach *named* tags to changes. They are most typically used to mimic named branches. We can `create`, `delete`, `list`, `move` and `rename` bookmarks (and more).

If we want to create a bookmark on the current change, we just do this.

```sh
$ jj bookmark create my-bookmark
Created 1 bookmarks pointing to mmwylxnr 96f65e19 my-bookmark | Conflict between Athens and Sparta
```

The log also represents the bookmark.

```sh
$ jj log --limit 3
@    mmwylxnr me@tonisagrista.com 2024-10-23 14:53:16 my-bookmark 96f65e19
├─╮  Conflict between Athens and Sparta
│ ○  rvmypmmr me@tonisagrista.com 2024-10-23 14:41:24 22ff369c
│ │  Add sparta to branch.txt
○ │  mnrotqpk me@tonisagrista.com 2024-10-23 14:44:23 b4f9dc97
├─╯  Add athens to branch.txt
```

### Operation Log

Finally, I want to show off a very cool feature. This is the operation log. `jj` records every operation performed in a repository (commits, pulls, statuses, etc.) in a log that can be listed. To show it, do:

```sh
$ jj op log
@  3f2c2cfcef27 tsagrista@hidalgo 2 minutes ago, lasted 1 millisecond
│  create bookmark my-bookmark pointing to commit 96f65e197e0c6a0f00dd12f9997d01c5c92da1b1
│  args: jj bookmark create my-bookmark
○  ff0c76c87309 tsagrista@hidalgo 22 minutes ago, lasted 236 milliseconds
│  snapshot working copy
│  args: jj st
○  8a9de7322915 tsagrista@hidalgo 25 minutes ago, lasted less than a microsecond
│  edit commit 0fbc6b529843406e738b1f4797a31c0a9ce47e41
│  args: jj edit mm
○  cf6ef8049f34 tsagrista@hidalgo 26 minutes ago, lasted 227 milliseconds
│  new empty commit
│  args: jj new
○  78c72f845d2d tsagrista@hidalgo 26 minutes ago, lasted 227 milliseconds
│  describe commit 7efe8ac031cee611a16363d4d8585fd8988d5556
│  args: jj desc -m 'Conflict between Athens and Sparta'
○  71072e960de2 tsagrista@hidalgo 29 minutes ago, lasted 231 milliseconds
│  new empty commit
│  args: jj new m r
○  43acab9baa1e tsagrista@hidalgo 31 minutes ago, lasted 226 milliseconds
│  snapshot working copy
│  args: jj log
○  c8d850d703e1 tsagrista@hidalgo 31 minutes ago, lasted 225 milliseconds
[...]
```

This allows `jj` to undo and redo operations with easy to go back and forth in the repo history, with the help of `jj undo`. Super handy.

## Conclusions

[^1]: https://doc.rust-lang.org/book
