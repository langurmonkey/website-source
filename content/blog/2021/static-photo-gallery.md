+++
author = "Toni Sagrista Selles"
categories = ["Website"]
tags = ["website", "privacy", "programming", "html", "english", "thumbsup"]
date = 2021-11-05
linktitle = ""
title = "Create your static photo gallery with thumbsup"
description = "Do not post your photos in online services that do not respect your rights, create your own static HTML photo gallery for your website with thumbsup"
featuredpath = "date"
type = "post"
+++

It is nowadays commonplace to upload your valued photos to online services that don't respect your rights like Flickr, Google Photos or Instagram. While these sites have a social component that may help you build an audience and have a wider reach, usually their terms and conditions are abusive to end users. In this post I'll be discussing how to create your own static HTML photo gallery that you can host on your website using [`thumbsup`](https://thumbsup.github.io/), a static gallery generator written in Python that produces totally customizable photo galleries. You can host your high resolution photos in your private server and have the gallery link to them. The [photo gallery on this very site](/photo-gallery) is generated using this method.

<!--more-->

## Installing `thumbsup`

`thumbsup` is a Python package that is able to generate a static HTML gallery from a directory full of photos and videos. In their own words, it takes care of resizing photos, generating the thumbnails, re-encoding the videos and much more.

In order to generate the static gallery you will need [thumbsup](https://thumbsup.github.io) and also [exiftool-json-db](https://github.com/thumbsup/exiftool-json-db) in your path (for EXIF data retrieval). You can install them with `npm` as shown below. Additionally, you will need `dcdraw`, `imagemagick` and some other utilities. Install them with pacman as shown below (Arch Linux only).

```bash
npm install thumbsup exiftool-json-db --unsafe-perm=true
pacman -S gifsicle dcraw imagemagick perl-image-exiftool ffmpeg
```

## Generating your first gallery


First, you need to curate a selection of your photos that will go into the gallery. In my case, I typically maintain a directory containing the photos I want to share organized into sub-directories by theme. You have already guessed right, each of these is to become a photo 'album'. I have, for instance, `gallery/animals`, `gallery/scenary`, `gallery/turkey-2012`, `gallery/nepal-2013` and so on. Each directory contains the photos that will go into the album with the same name.

### Choosing a theme

Before generating the gallery, you need a theme. You can either choose one of the [built-in themes](https://thumbsup.github.io/docs/4-themes/built-in/) or you can [create your own](https://thumbsup.github.io/docs/4-themes/create/). Creating your own theme is out of the scope of this tutorial, but I just want to mention that the theme I am using is customized to have the same look'n'feel as the main website, and it is publicly available [in this directory of the repository](https://gitlab.com/langurmonkey/langurmonkey.gitlab.io/-/tree/master/gallery-theme).

### Running the script

You are now ready to run the `thumbsup` script. If you have your own theme, you would use the `--theme-path` argument followed by the path of your theme, like this:

```bash
$  thumbsup --input ./folder-with-photos --output ./output-folder \
--embed-exif --title "Title of your gallery" --theme-path $PATH_TO_YOUR_THEME \
--photo-preview link --photo-download link \
--link-prefix "http://where-your-photos-are-hosted.online/"
```

If you want to use a built-in theme, you use the `--theme` flag with the name of the theme. For example, if you like the *cards* theme, you run:

```bash
$  thumbsup --input ./folder-with-photos --output ./output-folder \
--embed-exif --title "Title of your gallery" --theme cards \
--photo-preview link --photo-download link \
--link-prefix "http://where-your-photos-are-hosted.online/"
```

Find the available built-in with screenshots and demo sites [here](https://thumbsup.github.io/docs/4-themes/built-in/).

Once the script is run, you need to copy the contents of `./output-folder` to your preferred server location for it to be available online.

## Linking vs including the photos

Since my website is hosted in Gitlab Pages, I choose to have the full-resolution version of the photos hosted somewhere else and have the gallery link to these. The gallery contains lower resolution versions and thumbnails. This is achieved with `--photo-preview link` and `--photo-download link`. You need to enter the base URL of the location of the full resolution photos using the `--link-prefix` argument. 

If you do not use any of these, `thumbsup` will include the full resolution versions in the output folder directly. Much easier.

## Conclusion

In this post we have seen how `thumbsup` can help us generating a static photo gallery that can be shared online very easily. Keeping the gallery up to date is as easy as re-running the script when the photos in the input folder change, and copying the output to the server.
