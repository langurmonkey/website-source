+++
author = "Toni Sagrista Selles"
categories = []
tags = []
date = 2021-04-30
linktitle = ""
title = "QNAP meltdown: Qlocker"
description = "QNAP shows incompetence in an unprecedented level"
featuredpath = "date"
type = "post"
+++

If you are not interested in tech in general and in NAS manufacturers in particular you may have missed the latest news on the shiny new exploit affecting QNAP NAS systems: the Qlocker. Basically, the attackers gained access to QNAP systems and used 7-zip to move the user's files to password-protected archives. Then, they started a massive ransomware campaign asking for 0.01 BTC (around 500 USD) for the password to unlock the files.

<!--more-->

Well, it turns out there's a hardcoded password in one of QNAP's shitty apps for QTS (their operating system), called HBS 3 Hybrid Backup Sync. According to [this thread](https://forum.qnap.com/viewtopic.php?f=45&t=160849&start=450#p788325), an engineer called Walter Shao, who is the Technical Manager of QNAP since 2013, added a backdoor using the admin password "walter". Very nice. This story talks to us about the non-existing standards followed at QNAP when it comes to software auditing and review. 

It's a good thing that I decided to strip my [NAS](/blog/2021/ts-351-review/) of all this rubbish software a while ago, but the device itself will remain switched off as a precautionary measure until this matter is cleared up. This just adds a cherry on top of my already sizable distrust for that company.

For a little bit of comic relief look at [this reddit thread discussing the issue](https://old.reddit.com/r/qnap/comments/n14rr0/whos_walter_shao/). Some comments are real funny.
