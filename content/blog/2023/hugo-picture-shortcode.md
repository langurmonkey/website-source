+++
author = "Toni Sagristà Sellés"
title = "Hugo picture shortcode with multiple sources"
description = "A Hugo shortcode using the HTML picture element to enable different formats for the same image"
date = "2023-05-10"
linktitle = ""
featured = ""
featuredpath = "date"
featuredalt = ""
categories = ["website"]
tags = ["html5", "hugo", "jpeg xl", "english"]
type = "post"
+++

A while ago I published [this post](/blog/2021/lazy-image-load-hugo) about a better figure shortcode for Hugo that enabled lazy loading. Today, I bring you yet another update on the same shortcode. This time around, the focus is on leveraging the HTML [`picture`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture) element, which enables alternative versions of the same image in different formats, leaving the browser to decide which one to use. You can serve the same image in, for instance, JPEG-XL and plain old JPEG at the same time. The browser will read the tag, and select the appropriate image depending on its capabilities. If you use a JPEG-XL-capable browser (Thorium, Pale Moon, Basilisk, Waterfox, LibreWolf, Firefox Nightly), you will be served the smaller JPEG-XL version, otherwise you will get the plain JPEG version.

Here is how to use the shortcode in your Hugo posts and pages:

```html
{{</* fig 
        src1="/img/2023/02/jxl-avif/support-jxl-yes.jxl"
        type1="image/jxl" 
        src="/img/2023/02/jxl-avif/support-jxl-no.jpg" 
        class="fig-center" 
        width="50%" 
        loading="lazy" */>}}
```

The above snippet results in the following, once rendered. You should either see "Your browser does not support JPEG-XL" in black, or "Your browser supports JPEG-XL" in green:

{{< fig src1="/img/2023/02/jxl-avif/support-jxl-yes.jxl" type1="image/jxl" src="/img/2023/02/jxl-avif/support-jxl-no.jpg" class="fig-center" width="50%" loading="lazy" >}}

You can include up to four sources (``src1``, ``src2``, etc.), with their corresponding types. Here is the Hugo shortcode file. You need to save it in the file ``themes/[themename]/layouts/shortcodes/fig.html``.

{{< highlight fig.html "linenos=table" >}}
<!-- 
    Same as Hugo's base 'figure' shortcode with the image loading attribute.
    This enables lazy loading of images. Additionally, this uses the 'picture'
    tag to enable multiple versions of the same image with different formats.
    The browser selects the image with the first supported format.

    Attributes:
    - src      - path to default source image
    - width    - width img attribute
    - height   - height img attribute
    - loading  - loading img attribute
    - title    - description/caption
    - src1     - alternative source (1)
    - type1    - type of src1
    - src2     - alternative source (2)
    - type2    - type of src2
    - src3     - alternative source (3)
    - type3    - type of src3
    - src4     - alternative source (4)
    - type4    - type of src4
-->
<figure{{ with .Get "class" }} class="{{ . }}"{{ end }}>
    {{- if .Get "link" -}}
        <a href="{{ .Get "link" }}"{{ with .Get "target" }} target="{{ . }}"{{ end }}{{ with .Get "rel" }} rel="{{ . }}"{{ end }}>
    {{- end -}}
    <picture>
      {{- if .Get "src1" }}
      <source srcset="{{ .Get "src1" }}"{{ with .Get "type1" }} type="{{ . }}"{{ end }} />
      {{ end -}}
      {{- if .Get "src2" }}
      <source srcset="{{ .Get "src2" }}"{{ with .Get "type2" }} type="{{ . }}"{{ end }} />
      {{ end -}}
      {{- if .Get "src3" }}
      <source srcset="{{ .Get "src3" }}"{{ with .Get "type3" }} type="{{ . }}"{{ end }} />
      {{ end -}}
      {{- if .Get "src4" }}
      <source srcset="{{ .Get "src4" }}"{{ with .Get "type4" }} type="{{ . }}"{{ end }} />
      {{ end -}}
      <img src="{{ .Get "src" }}"
         {{- if or (.Get "alt") (.Get "caption") }}
         alt="{{ with .Get "alt" }}{{ . }}{{ else }}{{ .Get "caption" | markdownify| plainify }}{{ end }}"
         {{- end -}}
         {{- with .Get "width" }} width="{{ . }}"{{ end -}}
         {{- with .Get "height" }} height="{{ . }}"{{ end -}}
         {{- with .Get "loading" }} loading="{{ . }}"{{ end -}}
         decoding="async" />
    </picture>
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

Here is a link to the source file: [fig.html](https://codeberg.org/langurmonkey/website-source/src/branch/master/themes/langurmonkey/layouts/shortcodes/fig.html).
