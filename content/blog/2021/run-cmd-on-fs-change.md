+++
author = "Toni Sagrista Selles"
categories = ["Linux"]
tags = [ "cli", "programming"]
date = "2021-02-11"
description = "Learn about entr and how it can help you"
linktitle = ""
title = "Run a command when files change"
type = "post"
+++


Sometimes it is necessary to run a command or a collection of commands whenever a file or a group of files is modified. ['entr'](https://github.com/eradman/entr) is a small event notify test runner which might just be what you need in your development environment. 

<!--more-->

`entr` is super easy to use. It gets a list of files from the standard input and runs an arbitrary command whenever any of the files change. For example, you can pair it with [`ripgrep`](https://github.com/BurntSushi/ripgrep) to watch your whole home and print something whenever a file change.

```bash
cd ~
rg --files ~ | entr echo "A file just changed in $HOME"
```

## Practical uses

The example above is cool, it lets you know whenever a file changes in home. However, if a new file is added you won't notice as it was not initially listed by `rg --files ~`. `entr` shines brightest when you need to track changes in a limited number of files. For example, a code base. In my Rust development environment, I usually have a window in a corner where I run the following command.

```bash
ls src/**/*.rs | entr cargo build
```

This tracks changes in all Rust source code `*.rs` files in the `src/` directory and its sub-directories, and builds the Rust project whenever a change happens.

I also use it to automatically rebuild my latex papers and documents when editing them. This enables immediate feedback and automatic building. Open the document in a minimal document viewer like [`zathura`](https://pwmt.org/projects/zathura/) and you have an automatic display which is always in sync with your code.


