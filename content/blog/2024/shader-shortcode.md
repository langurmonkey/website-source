+++
author = "Toni Sagrista Selles"
categories = ["Graphics"]
tags = ["glsl","shaders","hugo","shortcode","website"]
date = 2024-07-10
linktitle = ""
title = "Shader Canvas Hugo Shortcode"
description = "A Hugo shortcode to render GLSL in real time on your site"
featuredpath = "date"
type = "post"
js = ["/js/glslcanvas.min.js"]
+++

Do you want to add a canvas with a shader running in real time to your Hugo site? In this post I show how to create a Hugo shortcode to display a shader.

<!--more-->

You need two ingredients for this recipe:

1. The [glslCanvas](https://github.com/patriciogonzalezvivo/glslCanvas) Javascript library (single file) originally written for [The Book of Shaders](http://thebookofshaders.com/) website. Save it in your `/js` directory. Download it with:
    ```bash
    wget https://github.com/patriciogonzalezvivo/glslCanvas/raw/4d5e073bf135692178d7cb62b5cc32dac2dae19f/src/GlslCanvas.js
    ```
    Then, add ``js = ["/js/GlslCanvas.js"]`` to the header of the post/page.

2. The Hugo shortcode. Paste this in a file named ``shader.html`` in `/themes/[your-theme]/layouts/shortcodes/`: 
    ```html
        <!-- 
        Embed a shader into a webpage. You need to add:

        js = ["/js/GlslCanvas.js"]

        in the header of the page for this to work.

        Attributes:
        - src      - path to the fragment shader
        - width    - width img attribute
        - height   - height img attribute
        - title    - description/caption
        - class    - figure class
        -->
        <figure{{ with .Get "class" }} class="{{ . }}"{{ end }}>
            <canvas class="glslCanvas" 
                  data-fragment-url="{{ .Get "src" }}"
                 {{- with .Get "width" }} width="{{ . }}"{{ end -}}
                 {{- with .Get "height" }} height="{{ . }}"{{ end -}}></canvas>
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
 
    ```

3. Once that's set up, embed your shader in your post, like so:

    ```html
    {{</* shader src="/shader/2024/spiked-star.glsl" 
                 class="fig-center" 
                 width="400" 
                 height="400" 
                 title="A spiked star that changes color and size." */>}}
    ```

That's it. Run your site and open your browser to admire your shader in all its WebGL splendor. My original implementation for the shader below is in [Shadertoy](https://www.shadertoy.com/view/3slBD8). The actual code used in this website is shown below the canvas.

{{< shader src="/shader/2024/spiked-star.glsl" 
             class="fig-center" 
             width="400" 
             height="400" 
             title="A spiked star that changes color and size." >}}


{{< collapsedcode file="/static/shader/2024/spiked-star.glsl" language="glsl" summary="spiked-star.glsl" >}}
