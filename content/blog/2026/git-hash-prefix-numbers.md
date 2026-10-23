+++
author = "Toni Sagrista Selles"
categories = ["vcs"]
tags = ["git", "programming", "hash", "curiosities", "english"]
date = 2026-09-29
linktitle = ""
title = "Git hash prefix or cellphone number?"
description = "What is the probability of getting an all-numbers Git hash prefix?"
featuredpath = "date"
type = "post"
js = ["/js/mathjax3.js"]
+++

Today, I was playing around with a new feature in [Gaia Sky](https://gaiasky.space), and I created a new release from master. Immediately, I noticed something unusual in the generated package name:

```
packages-3.8.0.066962508
```

The 3.8.0 part is the release version, while the last 9 characters are the abbreviated Git commit hash.
Usually, that last part looks something like:

```
packages-3.8.0.a31f7c92e
```

This time, however, every single one of the hash characters is a number, `066962508`. My first stupid reaction was thinking that something had gone wrong. However, `git log` confirmed the hash was fine.

```
➜ git log

commit 066962508de536403a185471344ba83801d45a88 (HEAD -> master, origin/master, origin/HEAD, gitlab/master, gitlab/HEAD, github/master, github/HEAD)
Author: langurmonkey <tsagrista_AT_ari.uni-heidelberg.de>
Date:   Tue Sep 29 10:10:15 2026 +0200

    feat: Handle gaiasky:// URLs forwarded from second instances and macOS open events. Part of #935.
    
    - Scope dataset URL dedup to the startup path only, so re-sent URLs are always processed by the running instance.
    - Register install4j StartupNotification listener for macOS open-URL events, with pending-URL queue for pre-UI arrival.
    - Add --enable-native-access=ALL-UNNAMED to launcher VM parameters - Add compileOnly install4j-runtime dependency.
```


Obviously, I asked myself, **"how likely is that"**? So I did some digging.

<!--more-->

Git commit hashes are hexadecimal. That means each character can be one of 16 possible values:

```
0 1 2 3 4 5 6 7 8 9 a b c d e f
```

So there's nothing special about a hash starting with `066962508`. It's just a hexadecimal string that happens to contain no `a`–`f` characters in its first nine positions.

But how unlikely is that?

There are 10 numerical characters out of 16 possible hexadecimal characters, so the probability of a single character being a number is:

$$
\frac{10}{16} = 0.625
$$

For nine consecutive characters to all be numbers:

$$
\left(\frac{10}{16}\right)^9 \approx 0.0145
$$

That's about 1.45%, or roughly 1 in 69.

So it's not particularly likely, but it's certainly not extraordinary either. Given enough commits, you're bound to run into one eventually. It looks even stranger because of the leading zero, and a quick glance at the number may even make someone mistake it for a Spanish cellphone number.

I then asked myself what the probability of **all** hash characters being numbers is. Well, if we assume ~40 characters (this is the default for SHA-1 hashes, even though git also supports SHA-256 with ~64 characters), the probability of every single one being a number is:

$$
\left(\frac{10}{16}\right)^{40} \approx 7.89 \times 10\^{-9}
$$

That's about 1 in 126.7 million. Much more unlikely, but still not totally outlandish. But I digress.

Back to the case, I checked whether this was the first time this had happened in the Gaia Sky repository:
```bash
➜ git log --all --format='%H'
    | grep -E '^[0-9]{9}'
    | wc -l

123
```

Nope. It has happened over a hundred and twenty times, and I had simply never noticed it before. I'm pretty sure this is the first time I package a build from one of those commits though.
