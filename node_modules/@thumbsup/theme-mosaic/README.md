# @thumbsup/theme-mosaic

[![NPM](https://img.shields.io/npm/v/@thumbsup/theme-mosaic.svg?style=flat)](https://www.npmjs.com/package/@thumbsup/theme-mosaic)
[![Travis CI](https://travis-ci.org/thumbsup/theme-mosaic.svg?branch=master)](https://travis-ci.org/thumbsup/theme-mosaic)

One of the built-in themes for https://github.com/thumbsup/thumbsup.

---

## Usage

```bash
thumbsup --theme mosaic
```

## Screenshots

![albums](docs/albums.png)
![media](docs/media.png)

## Options

You can use override the following variables to customise this theme:

```less
@body-background: #fff;
@highlight-color: #17baef;
```

You can add them to your own LESS file, and run thumbsup with `--theme-style custom.less`.

## Developing

Testing the theme

```bash
thumbsup --input /photos --output ./tmp --theme-path ./theme
```

Publishing the theme:

```bash
npm publish --access=public
```
