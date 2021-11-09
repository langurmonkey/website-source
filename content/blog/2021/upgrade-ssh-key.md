+++
author = "Toni Sagrista Selles"
categories = ["Security"]
tags = ["security", "privacy", "linux", "rsa", "ed25519", "ssh", "english"]
date = 2021-11-09
linktitle = ""
title = "Upgrade your old RSA SSH key to ED25519"
description = "The RSA algorithm has some problems and you should update to Ed25519"
featuredpath = "date"
type = "post"
+++

If you work regularly with remote machines or use online services like Gitlab, you are probably using an SSH key. And if you have not updated it recently, chances are you are using an RSA key, or, god forbid, an ECDSA or DSA key. Well, bad news: in order to be on the safe side, you should probably upgrade. A presentation at [BlackHat 2013](https://isecpartners.com/media/105564/ritter_samuel_stamos_bh_2013_cryptopocalypse.pdf) reported significant advances in solving the problems on which DSA and some other key types are based. The presentation suggested that keys based on elliptic curve cryptography (ECC) should be used instead: ECDSA or Ed25519. Additionally, ECDSA and DSA have nasty additional issues, so you should probably just stick to Ed25519. Here's how to upgrade.

<!--more-->

But before we start, here's a short summary of the types of keys you may encounter in the wild:
-  **DSA** --- unsafe and unsupported. It requires a parameters *k* to be completely random, secret and unique. This can make discovering your private key *easy*. **DO NOT USE**.
-  **ECDSA** --- a tad better than DSA but has the same parameter problem. **DO NOT USE**.
-  **RSA** --- it's still alright, especially with 2048-bit an over. It is supported everywhere, but it is slower than Ed25519 though. You should upgrade if you can.
-  **Ed25519** --- the strongest key type mathematically, and also the fastest. The public key is very compact, at around 68 characters only. However, it may not be supported on embedded or aging systems. For your everyday use with your desktop and laptop computers, this is your best bet.

## Generating an Ed25519 key

First, you way want to check what keys are actually installed on your computer:

```bash
for key in ~/.ssh/id_*; do ssh-keygen -l -f "${key}"; done | uniq
```

If you found out that you already have an Ed25519 key, then you are done. Otherwise, read on.

Fire up a terminal and generate the key with `ssh-keygen`:

```bash
ssh-keygen -t ed25519 -C "your@email.com"
```

Enter a strong passphrase when asked. Congrats! Your key is already generated. Now, let's use it.

## Using your Ed25519 key

First, you need to copy your key to all the servers you need to SSH into:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@host
```

Then, you may want to add the key to your SSH agent so that it is cached during your session and you only need to enter the passphrase once. First, make sure your SSH agent is up and running:

```bash
eval "$(ssh-agent -s)"
```

This should return the pid of the agent if it is running.

Run the following to add the key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

If you want a long-running SSH agent, you may want to use `keychain` to manager your keys. This program runs the SSH agent and makes sure that it keeps on running even after your session is closed. This may come in handy to easily share a single SSH agent process for all your shells and cron jobs.

To add the keys to the SSH agent managed by `keychain`, add the following to your shell startup script (`~/.bashrc`, `~/.zshrc` or whatever):

```zshrc
eval $(keychain --quiet --eval ~/.ssh/id_rsa ~/.ssh/id_ed25519)
```

The first time you open your terminal, you will be prompted for a passphrase. Then, the keys are cached and ready to use.

I have included the RSA key because I am keeping mine around for compatibility purposes. Sometimes I need to log into systems that use very old Operating Systems where Ed25519 is not supported. In this cases, having an RSA key around is good.

## Conclusion

In this post we have seen why all key types other than Ed25519 are considered unsafe and should be avoided if possible. We have shown how we can quickly and easily generate a new Ed25519 key and how to put it to good use.
