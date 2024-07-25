+++
title = "Privacy Policy"
categories = ["Privacy"]
tags = ["website","privacy","principles"]
date = "2021-04-06"
+++

This site strives to be as bloat-free as possible. It does not use cookies, tracking codes, analytics scripts or anything else that can be used to invade personal privacy. We use, however, the privacy-respecting `sessionStorage`[^dark-theme-blog] to store the user's theme preference, if any.

This site serves, along with the HTML page, 2 JavaScript files (theme manager, which loads at the top of the `body` element, and a bundle with the rest, loaded in the footer), 1 font file (fork awesome) and 1 CSS file. Some special pages, like the [search page](/search), may need an additional JS file fetch. The posts that contain mathematical formulas are less than a handful, and they get the MathJax 3 JavaScript from this very domain without requiring an external CDN.

All content is served from this domain, and is hosted on [NearlyFreeSpeech.NET](https://nearlyfreespeech.net). The source code of this website is available under the MIT license[^webrepo].

[^webrepo]: Website source repository: https://codeberg.org/langurmonkey/website-source
[^dark-theme-blog]: See this post for more information: [/blog/2021/dark-theme-redesign/](/blog/2021/dark-theme-redesign/)
