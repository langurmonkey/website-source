+++
author = "Toni Sagrista Selles"
categories = ["Privacy"]
tags = ["search", "linux", "privacy", "english", "qutebrowser", "open-source", "archlinux"]
date = 2021-11-04
linktitle = ""
title = "Searx: moving away from DuckDuckGo"
description = "The metasearch engine open source project Searx might be what you are looking for in terms of private web search"
featuredpath = "date"
type = "post"
+++

I have been using DuckDuckGo as my search engine of choice for the last few years. Howerver, DuckDuckGo seems to have [a few problems](https://www.reddit.com/r/degoogle/comments/pwf7q0/twitter_censors_email_correspondence_that_appears/hegyiik/):

1. It is based in the US, arguably not the most privacy-respecting jurisdiction in the world.
2. Only part of their source code is open.
3. Uses Amazon Web Services (AWS) as a cloud provider and Cloudfare CDS.
4. It looks like [their browser was caught tracking visited websites per user](https://www.techworm.net/2020/07/duckduckgo-browser-track-website.html).
5. At the end of the day, you can't really know that they are telling the truth when they promise not to track you.

In this post, I'm discussing Searx, a better alternative to DuckDuckGo that is truly open and driven by the community.

<!--more-->

## Searx

Searx is a metasearch engine that aggregates results from multiple sources and eliminates the tracking. It can be used over the Tor network to also provide search anonymity. Anyone can install and deploy their own Searx instance, either for private use or for everyone to use as a contribution to the community. The user interface is modern and can be customized to a degree. For instance, it provides a couple of UI themes and dark mode is available for both. 

Since you can inspect the project's whole [source code](https://github.com/searx/searx), you can be reasonably sure that tracking does not indeed happen, even though every instance could in principle modify it without notifying its users. In any case, there are many instances to choose from, and if you do not trust anyone, you can just deploy your own for your private local use. This [section of their documentation](https://searx.github.io/searx/user/own-instance.html) contains an interesting discussion of private vs public instance usage. 

## Installing Searx on Arch Linux

Installing your own private instance in Arch Linux is as easy as installing the [`searx`](https://aur.archlinux.org/packages/searx/) AUR package. Then, start it by running the systemd service:

```
systemctl start uwsgi@searx.service
```

If you want to start the service every time at startup, enable it:

```
systemctl enable uwsgi@searx.service
```

Then, point your browser to [localhost:8888](http://localhost:8888) and you should get the default Searx landing page running on your machine:

<p style="text-align: center; width: 70%; margin: 0 auto;">
<a href="/img/2021/11/local-searx-instance.jpg">
<img src="/img/2021/11/local-searx-instance.jpg"
     alt="Searx landing page running on my laptop"
     style="width: 100%" />
</a>
<em style="color: gray;">The default Searx interface as running on my laptop after a fresh install.</em>
</p>

Edit the file `/etc/searx/settings.yml` for some configuration options.

## Qutebrowser setup

You can set up qutebrowser to use your newly installed private Searx instance by replacing the `DEFAULT` search engine in the `config.py` configuration file:

```Python
c.url.searchengines = {'DEFAULT': 'http://localhost:8888?q={}'}
```

If all of this is too much for you, and you are fine trusting someone else, just replace the URL with one of the public instances.

## Final remarks

I myself use the private local installation in all my computers listed above. I'm almost always connected to a VPN via wireguard, which adds a slight anonymity layer (not even very good, but it's there anyways) by hiding my true location and routing all traffic via an encrypted tunnel. In my phone, I just trust [searx.be](https://searx.be), which is currently the top listed instance in the [Searx instance list](https://searx.space/#help-country) page.

All in all, Searx is an awesome project that offers a true private search engine that is, in my opinion, superior to anything else. You do not need to trust third parties to keep you private and not track your every move, which is awesome. Installing a local instance is easy-peasy, but you can also use one of the publicly available instances if you prefer to.

Some Searx resources:

-  [Public instance list](https://searx.space/)
-  [Official documentation](https://searx.github.io/searx/)
-  [Source repository at Github](https://github.com/searx/searx)
