+++
author = "Toni Sagrista Selles"
categories = ["programming"]
tags = ["c","c++","rust","make","just","commandline","linux","english"]
date = 2024-10-04
linktitle = ""
title = "Just ``make`` use of ``just``"
description = "Organize your project-specific commands with ``just``"
featuredpath = "date"
type = "post"
+++

Nowadays, makefiles are ubiquitous in software. Most C and C++ projects have used them historically, and still use them as a build system. Nowadays, lots of projects written in other languages which have their own build tools also use them, not to make files, but to store and run commands in an organized manner. If this is you, you are doing it wrong. However, there is a tool designed to do just that: ``just``.

<!--more-->

## What is ``make``

[``make``](https://www.gnu.org/software/make/manual/make.html) is a GNU utility mainly used to **make** files. It automatically determines which parts of a build are outdated and need remaking (recompiling), and runs the commands to make them. ``make`` uses a makefile, which is a user-written file that specifies the targets (files) and the rules to make them. Usually, the makefile informs make as to how to compile and link a program written in C or C++, even though it is also extensively used in other well-suited languages like LaTeX.

However, targets in a makefile are by default files. This means that they build other files. Let's see a very simple example.

```makefile
foo: bar
    cat bar bar > foo
```

In this makefile, we have one file target, ``foo``. To make the file ``foo``, we need a file ``bar``. What appears after the colon in the first line are the requirements to make that file. The command appears below, and it just concatenates ``bar`` 2 times and outputs the result to ``foo``.

Let's try it. First, let's create a file named ``bar``.

```bash
echo "this is bar" > bar
```

Then, make sure you have a file named ``makefile`` with the contents shown above. Then, run ``make foo``.

```bash
$  make foo
cat bar bar > foo
```

If you ``ls``, you will see that now you have a new file named ``foo``, with the contents of ``bar`` repeated twice. Now, try ``make foo`` again.

```bash
$  make foo
make: 'foo' is up to date.
```

Indeed, nothing was made because ``make`` determined that ``foo`` is already up to date.

This is essentially the main purpose of ``make``. However, ``make`` is often used to store and run arbitrary commands that do not really make any file. For example, in a C codebase you often find a ``clean`` target which removes all object (*.o) files. In our example, we can add a ``clean`` target that removes ``foo``. To do that, you *can* explicitly tell ``make`` that the target is not linked to a file. We do so by annotating the target with ``.PHONY``:

```makefile
.PHONY clean
clean: 
    rm -rf foo
```

After that, ``make clean`` with run even if you do not have a file with the name ``clean``. However, this target will not work if a file named ``clean`` is in the same directory. To overcome this, we need ``.PHONY``. A phony target is, in essence, a target that is always out of date.

This is why, conceptually, ``make`` is not very well-suited to only organize and run arbitrary commands. To that purpose, there exists another tool, ``just``.

## What is ``just``

[``just``](https://just.systems) ([github](https://github.com/casey/just)) is a command runner written in Rust. It is **not** a build system. It steps in in those occasions when you have a project and need to keep your commands (that do not build the project!) nicely organized. ``just`` stores the commands (called *recipes*) in a file named ``justfile``, with a syntax very similar to makefiles. For example, the ``justfile`` for this website's project is the following:

```justfile
minify:
  $WEB/scripts/minify-all.sh theme-bw

deploy: minify
  $WEB/deploy.sh

hugo:
  hugo server
```

It has three targets and none of them build files. They do random stuff like minifying and the CSS and the JavaScript files, deploying the website to the server by running the ``deploy.sh`` script, or starting a local server. See that targets can still have dependencies (``deploy`` depends on ``minify``), so that they are run in order.

``just`` has many more features though. 

- It is a command runner, not a build system, so there's no need for ``.PHONY`` recipes.
- Multi-platform.
- Aliases.
- Can be invoked from any subdirectory.
- Recipes can be listed with ``just -l``.
- Specific and informative errors.
- Errors are resolved statically.
- Recipes can be written in any arbitrary language.
- [Much more](https://just.systems/man/en).

The next time you need to store and organize commands for your project, think again before using ``make``. ``just`` might just be what you need!
