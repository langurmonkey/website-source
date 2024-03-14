+++
author = "Toni Sagrista Selles"
categories = ["linux"]
tags = ["programming", "english", "linux", "cli", "technical"]
date = 2024-03-14
linktitle = ""
title = "Creating and applying patches"
description = "Use diff and patch to create and apply patches to files"
featuredpath = "date"
type = "post"
+++

The POSIX ``diff``, ``cmp`` and ``patch`` commands are very versatile. Sometimes, you need to edit a part of a file and send only your changes to somebody else to apply. This is where these handy commands can help. This post describes concisely how to use them to compare files, create patches and apply them.

<!--more-->

Before starting, I need to point you to the GNU documentation on the subject, which is quite extensive and well written:

- [GNU -- Comparing and Merging Files](https://www.gnu.org/software/diffutils/manual/html_node/index.html#Comparing-and-Merging-Files).

To start, let's imagine we have a file named ``main.rs``, taken from the [Hello, World!](https://doc.rust-lang.org/stable/book/ch01-02-hello-world.html) section of the Rust Programming Language book.

```main.rs
fn main() {
    println!("Hello, world!");
}
```

Now, edit it so that it prints something else out, and save it to ``main-truth.rs``:

```main-truth.rs
fn main() {
    println!("The original Total Recall (1990) is amazing!");
    println!("Let's watch it!");
}
```

We absolutely need to distribute these essential changes we have just made to our peers, for they also need to know the truth. To figure out how the two files, ``main.rs`` and ``main-truth.rs`` differ, we use the ``diff`` command:

```shell
diff -u main.rs main-truth.rs
```

The output of this command lists the differences between the files:

```shell
--- main.rs	2024-03-14 10:02:53.816592246 +0100
+++ main-truth.rs	2024-03-14 10:03:06.803258829 +0100
@@ -1,3 +1,4 @@
 fn main() {
-    println!("Hello, world!");
+    println!("The original Total Recall (1990) is amazing!");
+    println!("Let's watch it!");
 }
```

We want to use those differences to create a patch file. The contents of the patch file are exactly the same as the output of ``diff -u``, so we just redirect the output to the ``truth.patch`` file:

```shell
diff -u main.rs main-truth.rs > truth.patch
```

We distribute the ``truth.patch`` file amongst our naive coworkers, who still think Total Recall (2011) is a good film. They can apply the patch using the ``patch`` command, like so:

```shell
patch -u main.rs truth.patch
```

That should be it. We can also automatically create a backup of the original file with ``-b``. In that case, the backup file is renamed with the ``.orig`` suffix.

As always, ``man`` is your pal to learn about all the wonderful options that [``diff``](https://linux.die.net/man/1/diff) and [``patch``](https://linux.die.net/man/1/patch) offer.
