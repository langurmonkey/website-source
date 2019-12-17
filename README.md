tonisagrista.com
================

My website project. Visit it in [tonisagrista.com](https://tonisagrista.com).

Letsencrypt certificate renewal
-------------------------------

To renew the certificate, just do:

```bash
$  sudo certbot certonly --manual -d tonisagrista.com
```

Then go to the [repo configuration](https://gitlab.com/jumpinglangur/jumpinglangur.gitlab.io/pages)
and update the certificate and key with `/etc/letsencrypt/live/tonisagrista.com/fullchain.pem` and
`/etc/letsencrypt/live/tonisagrista.com/privkey.pem` respectively.


Gallery
-------

In order to generate the static gallery you will need [thumbsup](thumbsup.github.io) and also [exiftool-json-db](github.com/thumbsup/exiftool-json-db) in your path (for EXIF data).

Generate the gallery from a set of static files using:

```bash
$  thumbsup --input ./folder-with-photos --output ./photo-gallery --embed-exif --title "Toni Sagristà Sellés - Photo gallery" --theme flow --photo-preview link --photo-download link --link-prefix "http://wwwstaff.ari.uni-heidelberg.de/gaiasandbox/personal/images/gallery/"
```

The original photos are hosted in `gaiasandbox`'s ARI page.
Since HUGO in Gitlab caps any folder called `/public` within `/static`, rename it to `/assets` and replace any string `public/` with `assets/` in `photo-gallery/index.html`.

