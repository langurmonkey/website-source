+++
author = "Toni Sagrista Selles"
categories = ["Linux", "Privacy"]
tags = [ "security", "anonymity", "privacy", "qutebrowser" ]
date = 2020-06-01
description = "Run qutebrowser with tor by default"
linktitle = ""
title = "Tor with qutebrowser"
featuredpath = "date"
type = "post"
+++

If you are a qutebrowser user and care about privacy and anonymity, you may want to run qutebrowser using the tor network by default. Doing so is easy. This post documents how to set it up. 

<!--more-->

First, bring up a terminal and install and enable/start tor (assuming Arch Linux with systemd):

```bash
pacman -S tor
systemctl enable tor.service
systemctl start tor.service
```

Then, just edit the configuration of qutebrowser (usually `~/.config/qutebrowser/config.py`) to use the tor network as a proxy:

```python
c.content.proxy = 'socks://localhost:9050/'
```

And, if you will, use the onion address of duckduckgo as your default search engine:

```python
c.url.searchengines = {'DEFAULT': 'https://3g2upl4pq6kufc4m.onion/?q={}'} 
```

That's it!
