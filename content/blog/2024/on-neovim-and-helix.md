+++
author = "Toni Sagrista Selles"
categories = ["texteditor"]
tags = ["vim","helix","kakoune","modal","English"]
date = 2024-10-12
lastmod = 2024-10-14 08:48:58
linktitle = ""
title = "On Neovim and Helix"
description = "My thoughts on where Helix stands in the modal text editor landscape"
featuredpath = "date"
type = "post"
+++

Today I have updated my `$EDITOR` variable to point to Helix instead of Neovim, and also configured Yazi to use it as the first option for text. I have used [Neo]vim since forever, so what made me switch? In this post, I discuss some of the ups and downs of both editors and what ultimately made me decide for Helix.

<!--more-->

{{< notice "Note" >}}
This article's purpose is **not at all** to speak ill of Neovim, but rather to appreciate Helix, a relatively new project that does not always get the recognition it deserves. I've used Neovim for many many years, and still use it today. It is one of my favourite tools that helps me be more efficient and productive.
{{</ notice >}}

Neovim is a modal text editor that is notoriously barebones by default. This is a good thing. It includes the bare minimum to act as capalbe, general-purpose text editor. Any additional functionality is provided by **plugins**. Whie Neovim can be configured in vimscript to make it compatible with Vim, the native way of doing it is with Lua. 

When starting with Neovim you are *expected* to copy someone else's configuration, or even better, to just use one of the multiple pre-packaged distributions like LunarVim, AstroNVim, or CosmicNVim. These projects exist only to mitigate the complexity of creating a functional and modern Neovim configuration, and to ease its maintenance. My own [neovim configuration](https://codeberg.org/langurmonkey/dotfiles/nvim) was initially copied from one of those projects (can't remember which) and I've been tailoring it to my needs ever since.

This approach tends to work well though, but it is time-consuming. If you start with a clean slate, things can get complex quickly. Need cool syntax highlighting? Use the treesitter plugin (`nvim-treesitter`). Need to use LSP? It is included by default in Neovim (not in Vim), but configuring it is hell, so you may want to use a plugin (`nvim-lspconfig`) just for its configuration. Wait, I have so many plugins, this is getting difficult to maintain! Don't fret, use a *plugin manager* plugin, like `lazy.nvim`, to simplify the process. And so on and so forth. Sometimes this feels like an amalgamation of plugins duct taped together that barely work.

So, we must ask ourselves, what else is there?

## Other Modal Text Editors

Modal text editors are typically used inside a terminal window, and are operated (almost) entirely using the keyboard. The two most well-known candidates are [Vim](https://www.vim.org) and [Neovim](https://neovim.io), together with their ancestor `vi`. Some more recent additions to the roster include [Kakoune](https://kakoune.org) and [Helix](https://helix-editor.com), which vary the editing model slightly. I'm sure there are more that I'm unaware of.

Out of all of these, I picked **Helix** as a possible replacement of Neovim. You see, Helix has a different approach to functionality, as it ships with LSP, autocompletion, treesitter, fuzzy search, surround, multiple selections and much more by default. This means that it strives to offer a much more complete experience off-the-shelf, when compared to the others, with minimal configuration.

## Editing Modes

In **Neovim**, the editing mode is `action → object`, or `action → selection`. This means that we first specify the **action** to perform, like `y`ank, `d`elete, `c`hange, etc., and then we specify the object[s] to which the action applies, also called selection, like `w`ord, end of line `$`, etc. This model of action first, and selection last has its problems. For instance, you can't see your objects until the action has already been performed. If there were errors, you are forced to undo and then try again. In [Neo]vim, you can do `diw` to delete the current word. This is action, `d` for delete, and selection `iw`, for "in word".

In contrast, borrowing from Kakoune's model, **Helix** inverts the paradigm. Instead of action followed by object, we first specify the object and then the action, `object → action`, or `selection → action`. This enables **seeing** what will be changed by the action before actually executing the action. This model is much more interactive and, in my opinion, intuitive. In Helix you'd do `ebd` (`eb` for end-beginning selection, as in Helix movements imply selections, and `d` to delete).

In both Neovim and Helix we have **`NORMAL`**,  **`INSERT`**, and **`VISUAL`** modes, with the `:` command mode on top. Additionally, Helix has some minor modes, or sub-modes, that are accessible from normal mode and revert back to it after one command. These are **`GOTO`** mode, **`MATCH`** mode, **`VIEW`** mode or **`SPACE`** mode. For instance, space mode, accessed by typing <kbd>Space</kbd>, offers a set of mappings to different actions, shown in a popup, such as a fuzzy file picker (akin to `telescope.nvim`), a buffer picker, or a jumplist picker. It is similar to what you achieve in Neovim by using `whichkey.nvim`. But in Helix, all of this is built in.

Helix has a very discoverable UI, which is quite rare for a terminal application. It does a very good job of communicating the key bindings to the user. When entering space, match or goto modes a popup appears, with the further bindings and a small explanation. This helps a lot with the on-ramp.

{{< fig src="/img/2024/10/helix-gotomode.jpg" class="fig-center" width="55%" title="Goto mode popup in Helix." loading="lazy" >}}


## Configuration

We have already established that configuring Neovim is **not simple**. What about Helix? Well, it uses TOML and the configuration tends to be much shorter than your regular Neovim configuration, thanks to the sane defaults and built-in functionality. My Helix configuration file currently looks like this:

```toml
theme = "onedark"

[editor]
line-number = "relative"
cursorline = true
mouse = true
color-modes = true
bufferline = "always" # Enable tab bar at the top

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
# Use Shift-l and -h to move through tabs
S-l = ":buffer-next"
S-h = ":buffer-previous"
```

## Plugins

As far as I know, Helix does not still have a plugin infrastructure in place. This limits a lot what can be done with the editor, but it also keeps it simple. Arguably, a lot of the functionality expected from a text editor is included in the base package.


## Technology

The core of Neovim is written in C, with a lot of Lua and Vimscript thrown in for additional features. Helix, in contrast, is written in Rust, which is a more modern language that emphasizes safety and produces more **correct** and **memory-safe** programs by default. I'm not saying that Rust is better than C, I'm just stating that Rust forces you to write code that tends to be safer.

## Cool Helix Tricks

Here are some cool and handy tricks you can do with helix. 

- Helix includes LSP (language server) support by default, but the actual language servers for each particular language need to be installed separately in your OS. you can do
  ```bash
  hx --health
  ```
  to get a listing of all the supported languages, and whether their language server is available or not. Below is an excerpt of its output:
  ```bash
  Language                      LSP                           DAP                           Formatter                     Highlight                     Textobject                    Indent                        
  [...]
  c                             ✓ clangd                      ✓ lldb-dap                    None                          ✓                             ✓                             ✓                             
  c-sharp                       ✘ OmniSharp                   ✘ netcoredbg                  None                          ✓                             ✓                             ✘                             
  cabal                         ✘ haskell-language-server-…   None                          None                          ✘                             ✘                             ✘                             
  cairo                         ✘ cairo-language-server       None                          None                          ✓                             ✓                             ✓                             
  capnp                         None                          None                          None                          ✓                             ✘                             ✓                             
  cel                           None                          None                          None                          ✓                             ✘                             ✘                             
  clojure                       ✘ clojure-lsp                 None                          None                          ✓                             ✘                             ✘                             
  cmake                         ✘ cmake-language-server       None                          None                          ✓                             ✓                             ✓                             
  comment                       None                          None                          None                          ✓                             ✘                             ✘                             
  common-lisp                   ✘ cl-lsp                      None                          None                          ✓                             ✘                             ✓                             
  cpon                          None                          None                          None                          ✓                             ✘                             ✓                             
  cpp                           ✓ clangd                      ✓ lldb-dap                    None                          ✓                             ✓                             ✓                             
  [...]
  ```
- You can do `:theme␣` and then use <kbd>Tab</kbd> eo cycle the list of themes that appears, while the selected theme is applied instantly as a preview. Moreover, Helix comes with a wide selection of actually usable themes. Things like acme, github, dracula, onedark, catppuccin, monokay, and all their variants are in that selection.
- `␣` (<kbd>Space</kbd>) enters **Space mode**, which is super handy. It includes a fuzzy search (`␣f`), buffer (`␣b`), jumplist (`␣j`), and symbol pickers (`␣s`), code actions (`␣a`), a rename action (`␣r`), and much more.

  {{< fig src="/img/2024/10/helix-spacemode.jpg" class="fig-center" width="75%" title="Space mode in Helix." loading="lazy" >}}

- `m` enters **Match mode**, which is also quite intuitive. Enter it with `m`. It contains functions to navigate to the matching bracket (`mm`), add surrounding characters to the selection (`ms<char>`), replace the closest surrounding characters (`mr<char><new_char>`), or delete the closest surrounding characters (`mr<char>`). These last functions mimic what is provided by a plugin like `vim-surround` in Neovim. More on [match mode](https://docs.helix-editor.com/master/keymap.html#match-mode) and [surround](https://docs.helix-editor.com/master/surround.html).
- `ma` and `mi` select around and in objects. Objects can be words and paragraphs, but also tree-sitter objects like functions, types, arguments, comments, data structures, etc.
- `[` and `]` let you navigate through tree-sitter objects. Use the brackets followed by the object type (functions `f`, type definition `t`, argument `a`, comment `c`, etc.).
- `C` duplicates the cursor. Yes, helix supports multiple cursors by default to operate on multiple lines. You can also align your cursors (and text) with `&`. Super useful. Collapse the cursors with `,`.
- `gw` lets you jump instantly to a two-character label, similar to what qutebrowser does with links. Write `gw` and then type in the label of the location where you want to jump to. Jump labels appear at almost every word in view.

Of course, there are many more functions and features, but these are the ones I like the most.

## Helix Pain Points

There are a couple of issues with Helix.

- To my knowledge, there is no integrated spell checker yet, so if you want this functionality, you need to configure a spell checker LSP, like `typo-lsp`, in your `languages.toml` file for each language. Clearly a pain point.
- A lot of editors nowadays offer a vim mode, either built-in or as a plugin. I myself use it in IntelliJ IDEA when I need to do some heavy refactoring of Java. If I ever get as comfortable using the Helix editing mode as I am with vim's, this could become a drawback.
- I have the impression that some actions take more key strokes in Helix than they do in Neovim. I'm still not sure about that though.


## Conclusions

As of today, I'm comfortable enough with Helix so that I'm now using it as my default editor. I also configured Yazi to open text files with Helix by default. Still, I'm much more comfortable with vim keybindings, but I hope that in a few days/weeks I can be as productive with Helix as I am now in Neovim. In this post, I have visited some of the most interesting features of Helix, and touched on what ultimately motivated me to switch. That said, I'm not yet sure I'll stick with Helix.
