+++
author = "Toni Sagrista Selles"
categories = ["Gaia Sky"]
tags = ["gaia sky", "website", "tech", "web", "html", "css", "js"]
date = 2025-02-19
linktitle = ""
title = "Gaia Sky gets new website"
description = "A brand new website and a brand new domain"
featuredpath = "date"
type = "post"
+++

Over the past few weeks I've been working on a new standalone website for Gaia Sky. It uses the same technology stack as my personal website (essentially [Hugo](https://gohugo.io)), so it is a static website generated from templates and content. This is enough for Gaia Sky. I am no graphic designer or UX person, but I tried my best to make it look *potable*.

{{< fig src="/img/2025/02/gaiasky-website.jpg" class="fig-center" width="75%" title="The new Gaia Sky website, [gaiasky.space](https://gaiasky.space)" loading="lazy" >}}

Why did I create a standalone website instead of keeping the old section in the [ZAH](https://zah.uni-heidelberg.de) site? A few reasons:

1. It is **much easier** to update and maintain.
2. We now have a [**news section**](https://gaiasky.space/news) to make announcements of new releases, datasets, and whatnot. People can follow it with [RSS](https://gaiasky.space/index.xml).
3. We can **use our own domain**, [`gaiasky.space`](https://gaiasky.space). This was in the back of my mind for a long time.
4. We can **verify our Flathub package**. The [impossibility](https://github.com/flathub/de.uni_heidelberg.zah.GaiaSky/issues/57) to get Gaia Sky [verified](https://github.com/flathub-infra/website/issues/3844) in Flathub is what prompted it all, as we obviously do not control the domain [`uni-heidelberg.de`](https://uni-heidelberg.de) associated with the old app ID `de.uni_heidelberg.zah.GaiaSky`. The new ID `space.gaiasky.GaiaSky` is already [verified](https://flathub.org/apps/space.gaiasky.GaiaSky).

As an extra perk, the new site allowed us to integrate things that were previously scattered in several places. I have written scripts to generate pages for:

- [gaiasky.space/downloads/releases](https://gaiasky.space/downloads/releases) -- old releases, together with their packages and release notes.
- [gaiasky.space/resources/datasets](https://gaiasky.space/resources/datasets) -- a full listing of the datasets available in Gaia Sky, with their descriptions and additional metadata.


The site is responsive and should render fine on PC and mobile. If you are interested, give it a visit: [gaiasky.space](https://gaiasky.space).
