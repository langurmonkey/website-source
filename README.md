tonisagrista.com
================

My website project. Visit it in [tonisagrista.com](https://tonisagrista.com).

Letsencrypt certificate renewal
-------------------------------

To renew the certificate, just do:

```bash
certbot certonly --manual -d tonisagrista.com
```

Then go to the [repo configuration](https://gitlab.com/jumpinglangur/jumpinglangur.gitlab.io/pages)
and update the certificate and key with `/etc/letsencrypt/live/tonisagrista.com/fullchain.pem` and
`/etc/letsencrypt/live/tonisagrista.com/privkey.pem` respectively.

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

To minify everything, do:

```bash
scripts/minify-all.sh
```

Note that you **need** to run this script in order for the CSS to be applied, as the website itself only links the minified bundle file!

Gallery
-------

In order to generate the static gallery you will need [thumbsup](https://thumbsup.github.io) and also [exiftool-json-db](https://github.com/thumbsup/exiftool-json-db) in your path (for EXIF data). Additionally, install the following packages with pacman.

```bash
npm install thumbsup exiftool-json-db --unsafe-perm=true
pacman -S gifsicle dcraw imagemagick perl-image-exiftool ffmpeg
```

The gallery theme is in the ``gallery-theme/`` directory of this repository. Generate the gallery from a set of static files using:

```bash
$  thumbsup --input ./folder-with-photos --output ./output-folder --embed-exif --title "Toni Sagrista Selles - Photo gallery" --theme-path $WEB/gallery-theme --photo-preview link --photo-download link --link-prefix "http://wwwstaff.ari.uni-heidelberg.de/gaiasandbox/personal/images/gallery/" --sort-albums-by end-date
```

The original photos are hosted in `gaiasandbox`'s ARI page.
Since HUGO in Gitlab Pages does not allow any folder called `/public` within `/static`, rename it to `/assets`. The generated `index.html` file already points to the renamed folder, so no need to replace any strings.

You can then copy the contents of ``./output-folder`` to ``$WEB/static/photo-gallery/`` and commit.
