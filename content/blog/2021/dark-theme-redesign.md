+++
author = "Toni Sagrista Selles"
categories = ["Website"]
tags = [ "website", "design"]
date = "2021-03-03"
description = "How to implement a dark theme for your website, plus a small discussion on the recent redesign that aims at simplifying the experience"
linktitle = ""
title = "Dark theme and redesign"
type = "post"
+++

If you are like me and you like your user interfaces to be as dark as possible, you have the dark mode preference of your browser enabled. You may have noted that this site has now a dark mode which is activated by default. This is done by querying the ``prefers-color-scheme`` setting in the browser. This post describes how this is done, and it discusses a few tweaks I have implemented design-wise to simplify things and remove useless visual elements.

<!--more-->

Dark theme
==========

All major browsers nowadays support dark themes by default. I'm not talking about the interface of the browser itself, but the setting where the browser *informs* the website that the user *prefers* dark themes. This has the upside of being totally seamless for the user. Just set the flag in the browser configuration and websites that do support a dark mode should honor it. Additionally, we may want to provide a visual control to override the default behavior in the form of a button or a checkbox. 

How is this implemented practically? Well, in my case, I have written a very small javascript file (``darkmode.js``) which checks whether the browser setting is available and enabled. If so, then the dark mode CSS class ``"dark-mode"`` is added to a few DOM elements (namely the ``<body>``, the ``<header>`` and ``#menu``). If the setting is not set or not available, we fall back to the [``sessionStorage``](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage). 

Session storage
---------------

The ``sessionStorage`` is a privacy-respecting alternative to the ``localStorage`` or the browser cookies that expires when the page session ends (i.e. the page is closed). So, if a named setting for the current domain (I call it ``"dark-mode"``) is set to ``true``, then we apply the dark theme. If it is unset, or it is set to false, we don't. 

The last piece of the puzzle is a UI control <i class="fa fa-lightbulb-o"></i> which lets the user set the ``sessionStorage`` ``"dark-mode"`` property, and we've got it all covered.

The ``darkmode.js`` file
------------------------

By default, the browser preference is queried and honored. If the user chooses to override the default behavior via the UI button, then the ``sessionStorage`` is used. Below is the ``darkmode.js`` file I'm using.

{{< highlight javascript "linenos=table" >}}
if(sessionStorage.getItem("dark-mode") == "true") {
    // Toggle dark-mode class if "dark-mode" property of sessionStorage is true
    darkModeAdd();
} else if (window.matchMedia && 
    window.matchMedia('(prefers-color-scheme: dark)').matches && 
    sessionStorage.getItem("dark-mode") == null) {
    // Otherwise, check browser setting "prefers-color-scheme" is set to "dark"
    darkModeAdd();
}

function darkModeAdd() {
    document.body.classList.add("dark-mode");
    document.getElementsByTagName('header')[0].classList.add("dark-mode");
    document.getElementById('menu').classList.add("dark-mode");
}
function darkModeToggle() {
    document.body.classList.toggle("dark-mode");
    document.getElementsByTagName('header')[0].classList.toggle("dark-mode");
    document.getElementById('menu').classList.toggle("dark-mode");
    hasDark = document.body.classList.contains("dark-mode");
    sessionStorage.setItem("dark-mode", hasDark);
}
{{< /highlight >}}

It contains two functions and an initial setup. The second function, ``darkModeToggle()``, is run whenever the user clicks on the dark mode UI control (the little light bulb <i class="fa fa-lightbulb-o"></i> at the top of the page). It sets the ``"dark-mode"`` property in the ``sessionStorage``. 

{{< highlight html "linenos=table" >}}
<li class="menu">
    <a href="javascript:darkModeToggle()" style="border: none;" title="Toggle dark mode">
        <i class="fa fa-lightbulb-o" aria-hidden="true"></i>
    </a>
</li>
{{< /highlight >}}


All that's left is actually implementing the dark mode style in your CSS files. In my case, it is very minimal. I just change the background and text color defaults and call it a day.

Dark mode in qutebrowser
------------------------

Qutebrowser really makes things easy. You just need to add the line

```python
c.colors.webpage.prefers_color_scheme_dark = True
```
to your ``config.py``, or look for the setting ``prefers_color_scheme_dark`` in ``:set`` and set it to ``true``.

Dark mode in firefox
--------------------

The setting in Firefox is a bit more obscure. I found many places which pointed to settings to be set in ``about:config``, but none of these worked for me. What worked, however, is the extension [Dark Website Forcer](https://addons.mozilla.org/en-US/firefox/addon/dark-mode-website-switcher). I don't use Firefox very often, and I'm not too fond of filling it up with extensions/add-ons, so there's that.

Website redesign
================

On another note, I have also been making some tweaks to the website to make it more usable. 

I have removed the sidebar, which contained superfluous information, I have made the default font size larger, I have adjusted the fonts, the margins, and the paddings, and I have added a small "Latest posts" at the bottom of the welcome page. I have also removed all font files (except for fork awesome) in favor of the default font families (``monospace``, ``serif``, etc.) and I have moved the social items to the footer. All of this on top of the already discussed new dark mode.

The result is, in my opinion, a much cleaner and less cluttered site, which is easier to read, more gentle to the eyes, and weighs less.
