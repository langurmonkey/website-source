+++
author = "Toni Sagrista Selles"
categories = ["Website"]
tags = [ "programming", "projects", "website", "web" ]
date = "2016-11-10"
description = "Bye bye paid web hosting + Drupal, hello GitLab + Hugo"
linktitle = ""
title = "Moving to Hugo"
type = "post"
+++

It has been a few months now (maybe years?) that the idea of ditching both my web hosting provider and Drupal has been at the back of my mind.

Bear with me. Since about 2011 I have been maintaining this website using the cheapest hosting tier -- At least it was the cheapest at the time I got it. They call it *The Essential* and it costs over 300 bucks for 2 years. It is not a lot, but it is definitely too much for my purposes of hosting a small blog where I provide occasional updates on my projects, my portfolio and my CV.

Also, loading times are **horribly long** and the complexity of managing the database and [Drupal](http://drupal.org) upgrades/updates takes way too much of my time. The thought of having to update again to Drupal 8 sent shivers down my spine and got me searching for better options.

<!--more-->

### Static Site Generators

A while ago, while looking for alternatives, I stumbled upon the concept of [Static Site Generator](https://www.staticgen.com/), which is basically a system that generates static `html` + `css` + `js` websites from some configuration and content files. There are **a ton** of them!
After tinkering around with [Jekyll](http://jekyllrb.com) and some others, I chose [**Hugo**](http://gohugo.io).

Turns out most of the features I had in my Drupal installation I can also have in Hugo:

*  Blog
*  Summaries
*  Categories
*  Tags
*  Static pages
*  Nice theming and templating support
*  Markdown (Hugo supports it natively, Drupal requires a plugin)
*  Comments -- Using Disqus
*  Integration with Goolge Analytics

On top of all that, I **gain a few perks** over traditional web hosting:

*  Very fast loading -- No server-side processing required
*  Versioning -- All files are in [GitLab](http://gitlab.com)
*  Free! -- [GitLab Pages](https://pages.gitlab.io/) has a [built-in CI](https://about.gitlab.com/gitlab-ci/) which automatically builds my site whenever I commit changes. GitLab offers free public and private repositories
*  No more database and backup bull$****$
*  No more Drupal updates or crashes
*  No more tedious web admin back-ends

So now that I have made the move, I migrated all content from the database to `.md` files and set up a new theme (based on jpescador's [future imperfect](https://github.com/jpescador/hugo-future-imperfect) port for Hugo) I feel like I have regained control of my website and there are no more obscure `cPanel` interfaces or memory limit overflows when I want to update something.

My domain is still in the process of being transferred to another registrar, but I am a happy man.
