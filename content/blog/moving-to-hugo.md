+++
author = "Toni Sagrista Selles"
categories = ["Website"]
tags = [ "programming", "projects", "website", "web", "static site generator", "drupal", "hugo", "ipage" ]
date = "2016-11-10"
description = "Bye bye paid web hosting + Drupal, hello GitLab + Hugo"
linktitle = ""
title = "Moving to Hugo"
featured = "hugo.jpg"
featuredalt = "Hugo SSG"
featuredpath = "date"
type = "post"
+++

The idea of ditching both my web hosting provider and Drupal has been at the back of my mind for a few months.

Bear with me. Since about 2011 I have been maintaining this website using the cheapest hosting tier my hosting offers -- At least it was the cheapest at the time I got it. They call it *The Essential* and it costs over 300 bucks for 2 years. It is not a lot, but it is definitely too much for my purposes of hosting a small blog where I provide occasional updates on my projects, my portfolio and my CV.

Also, loading times are **horribly long** and the complexity of managing the [Drupal](http://drupal.org) installation (upgrades/updates) and also the database takes way too much of my time. Only the thought of updating to Drupal 8 sends shivers down my spine and ultimately got me searching for better options.

<!--more-->

### Static Site Generators

A while ago, while looking for alternatives, I stumbled upon the concept of [Static Site Generator](https://wiki.python.org/moin/StaticSiteGenerator). It is basically a system that produces static `html` + `css` + `js` websites from some configuration and content files. The static websites are ready to be hosted in a web server. There are [**a ton**](https://www.staticgen.com/) of them!
After tinkering around with [Jekyll](http://jekyllrb.com) and some others, I chose [**Hugo**](http://gohugo.io). [GitLab Pages](https://pages.gitlab.io/) supports it, so that whenever I commit changes to my website files GitLab triggers the site generation automatically. I can now update my website from a terminal by just `git commit`ting!

Turns out **most of the features** I had in my Drupal installation **I can also have in Hugo**:

*  Blog
*  Summaries
*  Categories
*  Tags
*  Static pages
*  Nice theming and templating support
*  Markdown -- Hugo supports it natively, Drupal requires a plugin
*  Comments -- Using Disqus
*  Integration with Goolge Analytics

On top of all that, I **gain a few perks** over traditional web hosting:

*  Very fast loading -- No server-side processing required
*  Versioning -- All files are in [GitLab](http://gitlab.com)
*  Free! -- [GitLab Pages](https://pages.gitlab.io/) has a [built-in CI](https://about.gitlab.com/gitlab-ci/) which automatically builds my site whenever I make a commit
*  No more database and backup bull$****$
*  No more Drupal updates or crashes
*  No more tedious web backends to update stuff

So now that I have made the move, I migrated all content from the database to `.md` files and set up a new theme (based on jpescador's [future imperfect](https://github.com/jpescador/hugo-future-imperfect) port for Hugo) I feel like I have regained control of my website and there are no more obscure `cPanel` interfaces or memory limit overflows.

My domain is still in the process of being transferred to another registrar, but I am now a happy man.
