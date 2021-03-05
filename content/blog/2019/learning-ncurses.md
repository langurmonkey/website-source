+++
author = "Toni Sagrista Selles"
categories = ["Programming", "Linux"]
tags = [ "snake", "terminal", "linux", "ncurses", "programming", "c++"]
date = "2019-03-16"
description = "Implementing a snake game in the terminal"
linktitle = ""
title = "Learning ncurses"
featured = "tsnake.gif"
featuredalt = "tsnake, a snake game in the terminal"
featuredpath = "date"
type = "post"
+++

Lately, I have been kicking the dust off my C++ skills, and decided to start by learning to use a library which I have been eyeing for a while, `ncurses`. `ncurses` is a C library which lets you create text-based UI programs for the terminal, in the same fashion as the gif above. Basically, you can use the terminal to implement text-based user interfaces. Since I seem to have an [obsession with snake games](/project/snake), I figured I'd create a snake game for the terminal.

<!--more-->

The project I'm sharing today is [`tsnake`](https://gitlab.com/langurmonkey/tsnake), a terminal-based snake game which supports maps, different difficulties, and interactive resizing, all rendered in a terminal window using `ncurses`.

## How to start

Let's see how it works. The game itself is initialised and run within the function `start_game(int, int)`. This function gets two paramters: the starting length of the snake and the map identifier. When a game finishes either because the user won or because she crashed, a window pops up displaying the final score and the user is given a couple of options. Either quit or keep playing. If she chooses to keep playing, the game resets with a new map. That is implemented in a simple loop in the main function:

{{< highlight cpp "linenos=table" >}}
int ret;
while(ret != R_QUIT){
    ret = start_game(start_length, ++map_id);
}
{{< /highlight >}}

The first thing we do when starting a new game is creating the game window. To do so, we use the `newwin(nlines, ncols, y, x)` ncurses call. This returns a `WINDOW` type object, which we keep in the game state structure, along with its width and height as cols and lines. The window has a size of  [`LINES-1`, `COLS`], leaving the last line for the status bar, where we print some useful information like the key bindings, the current score or the speed of the snake.

Here is a sketch of what this very simple setup looks like.

```bash
+-------------------------------------------+
|                                           |
|                                           |
|                                           |
|         SNAKE GAME IS                     |
|              RENDERED IN THIS WINDOW      | 
|                                           |
|                                           |
|                                           |
+-------------------------------------------+
STATUS BAR GOES HERE
```

Then we draw the map identified by the given id and after that we start the actual game loop.

In the following sections we will mostly use the function variants which take in a window as one of the arguments. These functions contain a `w` somewhere in the name, and are counterparts to the ones without `w`, which act on the default canvas. For example, `mvinch(y, x)` gets the character at a given position in the main canvas, while `mvwinch(*win, y, x)` gets the character at a given position of a given window.

## Drawing maps with ncurses

The code snippet that follows draws the initial map, which contains a pool with a fence surrounding it.

{{< highlight cpp "linenos=table" >}}
// pool
wattroff(state->gamew, COLOR_PAIR(C_WALL));
wattron(state->gamew, COLOR_PAIR(C_WATER));
for(int y = state->gw_h * 0.4; y <= state->gw_h * 0.6; y++){
    mvwhline(state->gamew, y, state->gw_w / 3, WATER, state->gw_w / 3); 
}
wattroff(state->gamew, COLOR_PAIR(C_WATER));
wattron(state->gamew, COLOR_PAIR(C_WALL));

// 5 fences
int tx = state->gw_w * 0.2; 
int ty = state->gw_h * 0.2;
int bx = state->gw_w * 0.8;
int by = state->gw_h * 0.8;

mvwvline(state->gamew, ty, tx, WALL, by - ty);
mvwvline(state->gamew, ty, bx, WALL, by - ty);

mvwhline(state->gamew, by, tx, WALL, bx - tx + 1);
mvwhline(state->gamew, ty, tx, WALL, state->gw_w * 0.21);
mvwhline(state->gamew, ty, state->gw_w * 0.6, WALL, state->gw_w * 0.21);
{{< /highlight >}}

Let's break it down a little. The variable `state` holds the game state, and contains the game windoe (`gamew`), the window width and height (`gw_w` and `gw_h`), the current score, the snake position and a few more pieces of information. In this snippet, we use `wattroff(*win, attr)` and `wattron(*win, attr)` to control the colors with which the characters will be printed. We use defines to link color location integers with meaningful names like `C_WATER` (blue) or `C_WALL` (red).

Then, we can use `mvwhline(*win, y, x, char, num)` and/or `mvwvline(*win, y, x, char, num)` to create vertical and horizontal lines of length `num` starting at `[x, y]` with the character `char` in the window `win`. We also use defines for the character types. In this spirit, water tiles are `#define WATER '^'` and the walls are `#define  WALL '#'`. With all this, building the maps is just a matter of putting the right tiles at the right places.
We only ever draw the map in two situations: when the game starts and when the window is resized. We will query the window state with `char mvwinch(*win, y, x)`, which returns the character at a given position in a window.


This is what the map produced by the code above looks like:

<p style="text-align: center; width: 70%; margin: 0 auto;">
<a href="/img/2019/03/tsnake-map-0.jpg">
<img src="/img/2019/03/tsnake-map-0.jpg"
     alt="tsnake map 0"
     style="width: 100%" />
</a>
<p style="text-align: center;" class="caption">The first map of tsnake, a simple pool surrounded by a few walls.</p>
</p>

## The game loop

Once we have printed the map, we start with the main loop. The main loop manages the resize events (even though they are not really events), manages the input and updates the state. 

In order to support terminal resizing, we need to check whether the variables COLS and LINES have changed. If so, we redraw the map, reposition the snake and the food using interpolation and refresh the window.

Then, we use `getch()` to get input keys. Usually, this function blocks the program until a new character is received.

{{< highlight cpp "linenos=table" >}}
// This function will block until a new input is received 
char ch = getch();
{{< /highlight >}}

However, ncurses allows the getch function to be non-blocking by using the `nodelay()` function:

{{< highlight cpp "linenos=table" >}}
// In this case, getch() does not block the
// execution and returns ERR if no input is ready
nodelay(stdscr, TRUE);
char ch = getch();
{{< /highlight >}}

After managing the user input, we do the collision checking using the state stored in the game window by ncurses. Basically, if we hit any character other than a whitespace we have a collision. This results in a very simple collision check function:

{{< highlight cpp >}}
int collision_check(game_state* state, int y, int x)
{
    int testch = mvwinch(state->gamew, y, x) & A_CHARTEXT;
    return testch == SNAKE || testch == WALL || out_of_bounds(state, y, x);
}
{{< /highlight >}}

At the end of the loop, we need to refresh both the standard screen and the window in order for the buffers to be applied to the terminal:

{{< highlight cpp "linenos=table" >}}
refresh();
wrefresh(state.gamew);
{{< /highlight >}}

## Conclusion

There are obviously many more aspects to the implementation of tsnake which have not been presented here. This article only gives a very rough bird's eye view on how to use ncurses and the possibilities that the library offers.

Feel free to check the full source code in the [gitlab repository](https://gitlab.com/langurmonkey/tsnake). You can install the [tsnake aur package](https://aur.archlinux.org/packages/tsnake) if you are on Arch or derivatives. 
