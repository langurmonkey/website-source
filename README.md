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
scripts/minify-all.sh
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

In order to generate the static gallery you will need [thumbsup](https://thumbsup.github.io) and also [exiftool-json-db](https://github.com/thumbsup/exiftool-json-db) in your path (for EXIF data). Additionally, install the following packages with pacman.

```bash
npm install thumbsup exiftool-json-db --unsafe-perm=true
pacman -S gifsicle dcraw imagemagick perl-image-exiftool ffmpeg
```

The gallery theme is in the ``gallery-theme/`` directory of this repository. Generate the gallery from a set of static files using the provided configuration file:

```bash
$  thumbsup --input ./folder-with-photos --output ./output-folder --config $WEB/thubmsup-config.json
```

Or use the full version with all the attributes:

```bash
$  thumbsup --input ./folder-with-photos --output ./output-folder --embed-exif --title "Toni Sagrista Selles - Photo gallery" --theme-path $WEB/gallery-theme --photo-preview link --photo-download link --link-prefix "http://wwwstaff.ari.uni-heidelberg.de/gaiasandbox/personal/images/gallery/" --sort-albums-by end-date --sort-albums-direction desc --sort-media-direction desc
```

The original photos are hosted in `gaiasandbox`'s ARI page.
Since HUGO in Codeberg Pages does not allow any folder called `/public` within `/static`, rename it to `/assets`. The generated `index.html` file already points to the renamed folder, so no need to replace any strings.

You can then copy the contents of ``./output-folder`` to ``$WEB/static/photo-gallery/`` and commit.

Mathematical formulas
---------------------

The MathJax JavaScript library is not included by default in the pages. If you need to use Latex-like formulas in a post, you must include the JavaScript file in the post source like this:

```html
<!-- Loading MathJax -->
<script type="text/javascript" id="MathJax-script" async src="/js/mathjax3.js"></script>
```
