+++
author = "Toni Sagrista Selles"
categories = ["website"]
tags = ["html5", "hugo", "english"]
date = 2021-11-15
linktitle = ""
title = "HTML lazy image loading"
description = "Adding lazy image loading to Hugo's figure shortcode"
featuredpath = "date"
type = "post"
+++

The HTML `<img />` tag has this handy attribute `loading="lazy"` that enables lazy image loading, so that images are only loaded whenever the user scrolls all the way down to their position. This makes page loading super-fast, and reduces the amount of wasted bandwidth, especially when browsing from page to page. In the past this was achieved by a few lines of custom JavaScript code, but it is supported by all major browsers, both for PC and mobile. It should *always* be used unless there's a very good reason not to, to the point where it can probably be argued that it should be the default behavior of images.

<!--more-->

Well, [Hugo](https://gohugo.io), the static site generator that I happen to use for this very website has a very handy built-in `figure` [shortcode](https://gohugo.io/content-management/shortcodes/) (shortcodes are snippets of code that call built-in or custom templates), but unfortunately it does not support lazy image loading. Do not panic! We'll see how to add support for it right away.

First, we need to get the built-in shortcode source code and import it into our project to be able to tweak it. Since the 'figure' name is already taken, we'll call it 'fig'. The original shortcode source can be found [here](https://github.com/gohugoio/hugo/blob/master/tpl/tplimpl/embedded/templates/shortcodes/figure.html). Copy it into your Hugo site, to `$WEB/themes/$THEME_NAME/layouts/shortcodes/fig.html`. Now you should be able to call this shortcode with something like this:

```html
{{</* fig src="/path/to/img.jpg" link="/link/url/here" title="Image tile" width="80%" */>}}
```

Now, let's add the `loading` attribute to the shortcode. To do so, we can just print its value in the output if the parameter is passed in in the shortcode call, like this:

```html
{{</* fig src="/path/to/img.jpg" link="/link/url/here" title="Image tile" width="80%" loading="lazy" */>}}
```

We also need to modify the shortcode source, the `fig.html` file. The snippet below contains the whole file. I added line 11, which accepts the `loading` attribute and passes it on to the image tag. I also added some extra styling for the attribution data, but other than that it is Hugo's default `figure` shortcode.


{{< highlight html "linenos=table" >}}
<figure{{ with .Get "class" }} class="{{ . }}"{{ end }}>
    {{- if .Get "link" -}}
        <a href="{{ .Get "link" }}"
        {{ with .Get "target" }}
            target="{{ . }}"
        {{ end }}
        {{ with .Get "rel" }}
            rel="{{ . }}"
        {{ end }}>
    {{- end -}}
    <img src="{{ .Get "src" }}"
         {{- if or (.Get "alt") (.Get "caption") }}
            alt="{{ with .Get "alt" }}{{ . }}
         {{ else }}
            {{ .Get "caption" | markdownify | plainify }}
         {{ end }}"
         {{- end -}}
         {{- with .Get "width" }} width="{{ . }}"{{ end -}}
         {{- with .Get "height" }} height="{{ . }}"{{ end -}}
         {{- with .Get "loading" }} loading="{{ . }}"{{ end -}}
    /><!-- Closing img tag -->
    {{- if .Get "link" }}</a>{{ end -}}
    {{- if or (or (.Get "title") (.Get "caption")) (.Get "attr") -}}
        <figcaption
         {{- with .Get "width" }} style="margin: 0 auto; width:{{ . }};"{{ end -}}
            >
            {{ with (.Get "title") -}}
                <h4>{{ . }}</h4>
            {{- end -}}
            {{- if or (.Get "caption") (.Get "attr") -}}<p class="fig-attribution">
                {{- .Get "caption" | markdownify -}}
                {{- with .Get "attrlink" }}
                    <a href="{{ . }}">
                {{- end -}}
                {{- .Get "attr" | markdownify -}}
                {{- if .Get "attrlink" }}</a>{{ end }}</p>
            {{- end }}
        </figcaption>
    {{- end }}
</figure>
{{</ highlight >}}

That's it. With this little trick the images on your site can be set to load lazily. The results are shown in the gif below.

{{< fig src="/img/2021/11/lazy-img-loading.gif" class="fig-center" width="500px" title="Lazy image loading at work using the shortcode above. Note how images are requested on demand as the user scrolls down the page." loading="lazy" >}}
