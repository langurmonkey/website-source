tonisagrista.com
================

My website project, online at [tonisagrista.com](https://tonisagrista.com).

Deployment
----------

The `master` branch of this repository contains the Hugo sources. These need to be generated into the static website using the `hugo` CLI program (i.e. `hugo --minify`).

The site is deployed to a [nearlyfreespeech](https://nearlyfreespeech.net) server. The `/deploy.sh` script deploys the site to the server. The `deploy-codeberg.sh` is the old deploy script, which deployed the site to different branches in Codeberg Pages.

Minify
------

In order to minify the JS and CSS, you need `uglifycss` and `uglify-js`.

```bash
npm install -g uglify-js uglifycss
```

If any of the CSS files are modified, re-generate the bundle with:

```bash
cd $WEB/themes/langurmonkey/static/css
uglifycss theme-pink-blue.css main.css add-on.css fork-awesome.css > site-bundle.css
```

Same with the JavaScript files:

```bash
cd $WEB/themes/langurmonkey/static/js
uglifyjs darkmode.js jquery.min.js skel.min.js codeblock.js util.js main.js > site-bundle.js
```

To minify everything at once, do:

```bash
just minify
```

Note that you **need** to run this script in order for the CSS to be applied, as the website itself only links the minified bundle file!

Choose CSS theme
----------------

The minifcation step includes the theme. By default, `theme-pink-blue` is used. If you want to change it, just pass it as an argument to `minify-all.sh`:

```bash
# The theme is the file name without the .css extension
scripts/minify-all.sh theme-name
```

Gallery
-------

In order to generate the static gallery I use [thumbsup](https://thumbsup.github.io). To run it, I use the docker method. Make sure that you have docker installed first, and then start the service.

```bash
pacman -S docker
systemctl start docker
```

Then, just run the provided `thumbsup-run.sh` script. If you get a permission error, you need to add your user to the docker group:

```bash
sudo usermod -aG $USER
newgrp docker
````

Now you can run the script.

```bash
./thumbsup-run.sh
```

The original photos are hosted in `gaiasandbox`'s ARI page.
Since HUGO in Codeberg Pages does not allow any folder called `/public` within `/static`, rename it to `/assets`. The generated `index.html` file already points to the renamed folder, so no need to replace any strings.

You can then copy the contents of ``./output-folder`` to ``$WEB/static/photo-gallery/`` and commit.

Mathematical formulas
---------------------

The MathJax JavaScript library is not included by default in the pages. If you need to use Latex-like formulas in a post, you must include the JavaScript file in the post source.

Either do it in the header,

```html
js = ["/js/mathjax3.js"]
```

or using the script tag in the body,

```html
<!-- Loading MathJax -->
<script type="text/javascript" id="MathJax-script" async src="/js/mathjax3.js"></script>
```
