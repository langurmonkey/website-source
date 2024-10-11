+++
author = "Toni Sagrista Selles"
categories = ["texteditor"]
tags = ["vim","helix","kakoune","modal","English"]
date = 2024-10-11
linktitle = ""
title = "On Neovim and Helix"
description = "A subjective look at these two modal text editors"
featuredpath = "date"
type = "post"
+++

Today I have updated my `$EDITOR` variable to point to Helix instead of Neovim. I have used [Neo]vim since forever, so what made me switch editors? In this post, I discuss some of the ups and downs of both editors and what ultimately made me decide for Helix.

<!--more-->

Neovim is a modal text editor that is notoriously barebones by default. It includes the bare minimum to act as capalbe, general-purpose text editor. Any additional functionality is provided by **plugins**. Whie Neovim can be configured in vimscript to make it compatible with Vim, the native way of doing it is with Lua. Due to the high reliance on plugins and their sometimes complex configuration, starting with Neovim typically involves copying someone else's configuration entirely, or even better, just using one of the multiple pre-packaged distributions like LunarVim, AstroNVim, or CosmicNVim. These projects exist only to mitigate the complexity of creating a functional and modern Neovim configuration, and to ease its maintenance.

This approach tends to work well, but it is time-consuming. Not even talking about writing and maintaining your own configuration. Need cool syntax highlighting? Use the treesitter plugin. Need to use LSP? It is included in Neovim (not in Vim), but configuring it is hell, so you may want to use a plugin just for its configuration. Wait, I have so many plugins, this is getting difficult to maintain! Don't fret, use a *plugin manager* plugin, like `lazy.nvim`, to simplify the process. And so on. 

So, now that we are here, we must ask ourselves, what else is there?

## Modal Text Editors

Modal text editors are typically used inside a terminal window, and are operated (almost) entirely using the keyboard. The two most well-known candidates are [Vim](https://www.vim.org) and [Neovim](https://neovim.io), together with their ancestor `vi`. Some more recent additions to the roster include [Kakoune](https://kakoune.org) and [Helix](https://helix-editor.com), which vary the editing model slightly. 

Out of all of these, I picked **Helix** as a possible replacement of Neovim. You see, Helix has a different approach to functionality, as it ships with LSP, autocompletion, treesitter, fuzzy search, surround, multiple selections and much more by default. This means that it strives to offer a much more complete experience off-the-shelf, when compared to the others, with minimal configuration.

## Editing Modes

In **Neovim**, the editing mode is `action → object`, or `action → selection`. This means that we first specify the **action** to perform, like `y`ank, `d`elete, `c`hange, etc., and then we specify the object[s] to which the action applies, also called selection, like `w`ord, end of line `$`, etc. This model of action first, and selection last has its problems. For instance, you can't see your objects until the action has already been performed. If there were errors, you are forced to undo and then try again. In [Neo]vim, you can do `diw` to delete the current word. This is action, `d` for delete, and selection `iw`, for "in word".

In contrast, borrowing from Kakoune's model, **Helix** inverts the paradigm. Instead of action followed by object, we first specify the object and then the action, `object → action`, or `selection → action`. This enables **seeing** what will be changed by the action before actually executing the action. This model is much more interactive and, in my opinion, intuitive. In Helix you'd do `ebd` (`eb` for end-beginning selection, as in Helix movements imply selections, and `d` to delete).

In both Neovim and Helix we have **`NORMAL`**,  **`INSERT`**, and **`VISUAL`** modes, with the `:` command mode on top. Additionally, Helix has some minor modes, or sub-modes, that are accessible from normal mode and revert back to it after one command. These are **`GOTO`** mode, **`MATCH`** mode, **`VIEW`** mode or **`SPACE`** mode. For instance, space mode, accessed by typing <kbd>SPACE</kbd>, offers a set of mappings to different actions, shown in a popup, such as a fuzzy file picker (akin to `telescope.nvim`), a buffer picker, or a jumplist picker. It is similar to what you achieve in Neovim by using `whichkey.nvim`. But in Helix, all of this is built in.

## Configuration

We have already established that configuring Neovim is **not simple**. What about Helix? Well, it uses TOML and the configuration tends to be much shorter than your regular Neovim configuration, thanks to the sane defaults and built-in functionality. My Helix configuration file currently looks like this:

```toml
theme = "onedark"

[editor]
line-number = "relative"
cursorline = true
mouse = true
color-modes = true

[editor.cursor-shape]
insert = "bar"
normal = "block"
select = "underline"

# File explorer configuration
[editor.file-picker]
hidden = false
parents = false

[editor.soft-wrap]
enable = true

# Do not render white spaces
[editor.whitespace]
render = "none"

[editor.indent-guides]
render = false
character = "╎" # Some characters that work well: "▏", "┆", "┊", "⸽"
skip-levels = 1

# LSP Server configuration
[editor.lsp]
display-messages = true
auto-signature-help	= true
display-signature-help-docs	= true

# Key mappings
[keys.normal]
D = "kill_to_line_end"
```

## Plugins

As far as I know, Helix does not still have a plugin infrastructure in place. This limits a lot what can be done with the editor, but it also keeps it simple. Arguably, a lot of the functionality expected from a text editor is included in the base package.


## Technology

The core of Neovim is written in C, with a lot of Lua and Vimscript thrown in for additional features. Helix, in contrast, is written in Rust, which is a more modern language that emphasizes safety and produces more **correct** and **memory-safe** programs by default. I'm not saying that Rust is better than C, I'm just stating that Rust forces you to write code that tends to be safer.


## Conclusions

As of today, I'm comfortable enough with Helix so that I'm now using it as my default editor. I also configured Yazi to open text files with Helix by default. Still, I'm still much more comfortable with vim keybindings, but I hope that in a few days/weeks I can be as productive with Helix as I am now in Neovim.
