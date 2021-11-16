+++
author = "Toni Sagrista Selles"
categories = ["Computers"]
tags = ["emulator", "computer architecture", "programming", "english"]
date = 2021-07-14
linktitle = ""
title = "Implementing a CHIP-8 emulator"
description = "Writing a simple emulator from scratch is fun: rCHIP8"
featuredpath = "date"
type = "post"
+++

I've written about the [CHIP-8](https://en.wikipedia.org/wiki/Chip-8) machine [before](/blog/2021/chip8-spec). It is a very simple interpreted programming language that can be implemented without much hassle by anyone interested in getting their feet wet with emulators. It is commonly regarded as the "hello world" of emulators.

Some time ago I decided to implement a CHIP-8 emulator in Rust as my second project written in that language. My first foray into the language was the porting of the [Gaia Sky LOD catalog generation](https://gitlab.com/gaiasky/gaiasky-catgen) tool from Java. This allowed us to substantially increase the generation speed and dramatically (really) decrease the memory consumption of the processing, to the point where a processing that previously needed more than 2 TB of RAM could now be done with less than a hundred gigs. Back to the topic at hand, I called my implementation [`rchip8`](https://gitlab.com/langurmonkey/rchip8) (very creative). This post describes the process and structure of such an emulator with more or less detail.

<!--more-->

If you know nothing about CHIP-8 I would recommend you to at least skim-read the [specification](/blog/2021/chip8-spec). This post will be more fun if you know a little about the machine itself.

I implemented the full emulator in two sessions of approximately one hour each. After the first session the basic structure and functionality (display, internal clock, registers, interpreter) was already there, but some of the instructions were still missing. In the second session I implementing these instructions, ironed out some of the bugs and added a few command line options to make it more flexible.

You can find the **source repository** for this implementation [here](https://gitlab.com/langurmonkey/rchip8).

## Basic structure

My emulator is organized into 8 main modules:

- Main module: `main.rs`
- Machine: `chip8.rs`
- Display: `display.rs`
- Audio: `audio.rs`
- Keyboard input: `keyboard.rs`
- Time: `time.rs`
- Debug utils: `debug.rs`

## The main module

The main module controls and uses the rest. It implements the CLI argument parsing, initializes the machine with all its modules, and it also implements the **main loop**. The main loop contains the event loop, and the call to the machine cycle. The main loop also updates the display module if needed, and uses the `Beep` utility in the audio module to sound the beeper when needed.

The implementation accepts a few CLI arguments, which are parsed using [clap](https://docs.rs/clap/2.33.3/clap/). The arguments are well documented when running the program with `-h`.

```
R-CHIP-8 0.1.0
Toni Sagrsità Sellés <me@tonisagrista.com>
CHIP-8 emulator

USAGE:
    rchip8 [FLAGS] [OPTIONS] <input>

FLAGS:
    -d, --debug      Run in debug mode. Pauses after each instruction, prints info to stdout
    -h, --help       Prints help information
    -V, --version    Prints version information

OPTIONS:
    -b, --bgcol <bgcol>    Background (off) color as a hex code, defaults to 101020
    -c, --fgcol <fgcol>    Foreground (on) color as a hex code, defaults to ABAECB
    -i, --ips <ips>        Emulation speed in instructions per second, defaults to 1000
    -s, --scale <scale>    Integer display scale factor, defaults to 10 (for 640x320 upscaled resolution)

ARGS:
    <input>    ROM file to load and run
```


The initialization happens immediately after the CLI arguments have been parsed, and goes over the main modules and creates the relevant structures: the SDL2 context, the `Display` manager, the `Beep` (audio), and the actual `Chip8` machine:

{{< highlight rust "linenos=table,linenostart=135" >}}
// Init SDL2
let sdl_context = sdl2::init().unwrap();

// Create the display
let mut display = Display::new(&sdl_context, "R-CHIP-8", scale, fgcol, bgcol);

// Create audio beep
let beep = Beep::new(&sdl_context);

// Create the machine
let debug_mode = matches.occurrences_of("debug") > 0;
println!("Debug: {}", debug_mode);
let mut chip8 = Chip8::new(rom, start, instruction_time_ns, debug_mode);
{{</ highlight >}}

Once that's done everything is ready to start the main loop. It is actually very, very simple:

{{< highlight rust "linenos=table,linenostart=149" >}}
// Main loop
'mainloop: loop {
    let t: u128 = time::time_nanos();

    // Event loop
    for event in display.event_pump.poll_iter() {
        match event {
            Event::Quit { .. }
            | Event::KeyDown {
                keycode: Some(Keycode::Escape),
                ..
            }
            | Event::KeyDown {
                keycode: Some(Keycode::CapsLock),
                ..
            } => break 'mainloop,
            _ => {}
        }
    }

    // Run the machine
    chip8.cycle(t, &mut display.event_pump);

    // Clear/update display if needed
    if chip8.display_clear_flag {
        display.clear();
    }
    if chip8.display_update_flag {
        display.render(chip8.display);
    }

    // Play/pause the beep
    if chip8.beep_flag {
        beep.play();
    } else {
        beep.pause();
    }
}
{{</ highlight >}}

Even though the main loop is in the main module, the actual timing of the machine is controlled by the machine module. We'll see that later.
The machine also sets some flags that are used in the main loop to operate the display and audio modules. These flags are the following:

- `display_clear_flag` -- if up, the display must be cleared
- `dispaly_update_flag` -- if up, the display must be updated using the `chip8.display` buffer
- `beep_flag` -- if this flag is up, the machine must beep


## The machine

This module contains the machine data structures, is in charge of initializing the registers, memory and counters, and also implements the interpreter that parses and executes instructions and times them correctly according to the instructions per second setting.

The `Chip8` struct contains the data structures:

- RAM -- a 4 kB (4096 bits) array of `u8`, initialized to 0, implemented as `[u8; 4096]`
- Registers -- sixteen one-byte registers, implemented as `[u8; 16]`
- The index register `I` -- a 16-bit register used to store memory addresses, implemented as `u16`
- The stack -- a LIFO array of 16-bit values used for subroutines, implemented as a `[u16; constants::STACK_SIZE]`
- The program counter `PC` -- the memory location of the current instruction, implemented as an `usize` used to index the RAM
- The delay and sound timers `DT` and `ST` -- two 8-bit registers used for timing and sound, implemented as a couple of `u8` fields
- The display buffer -- the buffer used to store the on/off state of each pixel in the display, implemented as a `[u8; constants::DISPLAY_LEN]`, where `DISPLAY_LEN` is 64*32=2048

The CHIP-8 machine does not really specify this, but it is common to use the first 80 bytes of RAM to store sprite fonts for the HEX characters from 0 to F. My implementation does this too:

{{< highlight rust "linenos=true" >}}
// Initialize the fonts
let fonts: [u8; 80] = [
    0xF0, 0x90, 0x90, 0x90, 0xF0, // 0
    0x20, 0x60, 0x20, 0x20, 0x70, // 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0, // 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0, // 3
    0x90, 0x90, 0xF0, 0x10, 0x10, // 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0, // 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0, // 6
    0xF0, 0x10, 0x20, 0x40, 0x40, // 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0, // 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0, // 9
    0xF0, 0x90, 0xF0, 0x90, 0x90, // A
    0xE0, 0x90, 0xE0, 0x90, 0xE0, // B
    0xF0, 0x80, 0x80, 0x80, 0xF0, // C
    0xE0, 0x90, 0x90, 0x90, 0xE0, // D
    0xF0, 0x80, 0xF0, 0x80, 0xF0, // E
    0xF0, 0x80, 0xF0, 0x80, 0x80, // F
];
ram[..80].copy_from_slice(&fonts);
{{< /highlight >}}

The ROMs (programs) to be executed are just a series of bytes that will be interpreted as instructions. Some ROMs also contain data or sprites. By default, the ROM should be copied to the machine RAM at the address `0x200`. The program counter `PC` is, then, initialized to the same address, since that's where the first program instruction resides.

{{< highlight rust "linenos=true" >}}
// Copy ROM to memory
let bytes = rom.len();
let ppos = constants::PROGRAM_LOC + bytes;
ram[constants::PROGRAM_LOC..ppos].copy_from_slice(&rom[0..bytes]);
{{< /highlight >}}

### The `cycle()` method

The `cycle()` method in the `Chip8` structure of `chip8.rs` is called in every iteration of the main loop. This method does a few things:

1. Updates the delay timer `DT` and the sound time `ST`. These timers must be decreased 60 times per second if their value is greater than 0. To do so, the `cycle()` method gets a time as argument (`t: u128` is the current time in nanoseconds), which is then compared against the *last time* that the method was called. If this value is over 16.666.666 (1/60 seconds in nanoseconds), then the timers are updated if needed.
2. Interprets the next instruction if the timing is right. The `Chip8` has the instruction time in nanoseconds. This is the number of nanoseconds between instructions. So, if the current time minus the *last time* is greater than this value, the next instruction is interpreted. 
3. Updates the *last time* record with the current time, in preparation for the next call to `cycle()`.

Each instruction is **2 bytes long** (4 hexadeciaml digits) and are stored with the most-significant byte first. Instructions have the one of the format `CXYN`, `CXNN` or `CNNN`, where each of the characters is 4 bits, or a hexadecimal digit. `C` is the code or group. `X` and `Y` are typically used to refer to register numbers. `N`, `NN` and `NNN` are 4, 8 and 12-bit literal numbers used to set values or for further instruction identification within a group (since 4 bits would only allow for 16 instructions). Instructions are decoded by splitting them into chunks and grouping them accordingly.

First, we need to get the instruction from the RAM address of `PC`, and increase the `PC` two words:

{{< highlight rust "linenos=true" >}}
let instr: u16 = ((self.ram[self.pc] as u16) << 8) | self.ram[self.pc + 1] as u16;
self.pc += 2;
{{</ highlight >}}

Then we decode the current instruction into `C`, `X`, `Y` and `N`, `NN` and `NNN`. This is easy with some bit shifting:

{{< highlight rust "linenos=true" >}}
let code = instr & 0xF000;
let x = ((instr & 0x0F00) >> 8) as usize;
let y = ((instr & 0x00F0) >> 4) as usize;
let n = instr & 0x000F;
let nn = instr & 0x00FF;
let nnn = instr & 0x0FFF;
{{</ highlight >}}

Finally, we need to match the instruction code and optionally `N`, and perform whatever actions defined by the instruction. Find a precise description of each CHIP-8 instruction in my [previous CHIP-8 specification post](/blog/2021/chip8-spec/#instruction-set). My implementation of these instructions is [here](https://gitlab.com/langurmonkey/rchip8/-/blob/master/src/chip8.rs#L177).

In this post we discuss in detail only `0xDXYN`, which is the **draw instruction**. Its definition is this:

`0xDXYN`: `DRW VX, VY, N` -- draw the sprite at position VX, VY with N bytes of sprite data at the address stored in `I`. Set `VF` to 01 if any pixels are changed to unset, and 00 otherwise. [^drw]

The interpreter must read `N` bytes from the `I` address in RAM. These `N` bytes are interpreted as a sprite and drawn at the display coordinates [`VX`, `VY`]. The bits are set using an XOR with the current state. This is my implementation of the instruction:

{{< highlight rust "linenos=true">}}
// DXYN - DRW  VX, VY, N
0xD000 => {
    self.registers[0x0F] = 0;
    let xpos: usize = self.registers[x] as usize % constants::DISPLAY_WIDTH;
    let ypos: usize = self.registers[y] as usize % constants::DISPLAY_HEIGHT;
    for row in 0..n {
        // Fetch bits
        let bits: u8 = self.ram[(self.index + row) as usize];
        // Current Y
        let cy = (ypos + row as usize) % constants::DISPLAY_HEIGHT;
        // Loop over bits
        for col in 0..8_usize {
            // Current X
            let cx = (xpos + col) % constants::DISPLAY_WIDTH;
            let current_color = self.display[cy * constants::DISPLAY_WIDTH + cx];
            let mask: u8 = 0x01 << 7 - col;
            let color = bits & mask;
            // XOR
            // 0 0 -> 0
            // 0 1 -> 1
            // 1 0 -> 1
            // 1 1 -> 0
            if color > 0 {
                // color is on
                if current_color > 0 {
                    // current color is on
                    self.display[cy * constants::DISPLAY_WIDTH + cx] = 0;
                    self.registers[0x0F] = 1;
                } else {
                    // current color is off
                    self.display[cy * constants::DISPLAY_WIDTH + cx] = 1;
                }
            } else {
                // Bit is off
                // Do nothing
            }
            if cx == constants::DISPLAY_WIDTH - 1 {
                // Reached the right edge
                break;
            }
        }
        if cy == constants::DISPLAY_HEIGHT - 1 {
            // Reached the bottom edge
            break;
        }
    }
    self.display_update_flag = true;
}
{{</ highlight >}}

Note that at the end we set the display flag to true so that the main module can update the display module with the modified display buffer. Let's have a look at the display module next.

## The display

{{< fig src="/img/2021/07/rchip8-test-results.jpg" title="rCHIP8 display output with test ROM." width="50%" class="fig-center" loading="lazy" >}}

The display is in charge of drawing stuff. It is implemented with [SDL2](https://www.libsdl.org) using the [`sdl2` Rust bindings](https://docs.rs/sdl2/0.32.2/sdl2/). 

The base CHIP-8 display has only two colors (monochrome), and works with a resolution of 64x32 pixels. [0, 0] is at the top-left corner, while [63,31] is at the bottom-right.

```
  [0,0]                      [63,0]     
  ┌───────────────────────────────┐
  │                               │
  │                               │
  │         64x32 DISPLAY         │
  │                               │
  │                               │
  └───────────────────────────────┘
  [0,31]                    [63,31]   
```

The graphics are drawn using 8x15 sprites, but this module knows nothing about this. Its only responsibilities are creating the window, drawing a buffer to the canvas, and clearing the canvas when requested. There are two main functions in this module: 

- `clear()` -- clears the display to the configured background color
- `draw(buffer: [u8; DISPLAY_LEN])` -- which draws the contents of the given buffer to the canvas using the configured foreground color

Additionally, the display takes in as parameters the foreground color, the background color, and a scale factor. The scale factor is used to increase the size of the display. The default size is 640x320, which corresponds to a scale factor of 10.

```rust
pub struct Display {
    pub canvas: Canvas<Window>,
    pub event_pump: EventPump,
    pub scale: u32,
    pub fgcol: Color,
    pub bgcol: Color,
}
```

## Audio

This module is very simple. It contains a single struct called `Beep`, which connects to an audio device. The module emulates the beep produced by the system beeper. It contains the `play()` method, which starts the beeper, and the `pause()` method, which stops it. It is called in the main loop.

## Keyboard

This module only contains a couple of functions to convert bytes into SDL2 scan codes and vice-versa. This is used to map the CHIP-8 input keypad to the left chunk of the QUERTY keyboard:

<kbd>1</kbd><kbd>2</kbd><kbd>3</kbd><kbd>4</kbd>\
<kbd>Q</kbd><kbd>W</kbd><kbd>E</kbd><kbd>R</kbd>\
<kbd>A</kbd><kbd>S</kbd><kbd>D</kbd><kbd>F</kbd>\
<kbd>Z</kbd><kbd>X</kbd><kbd>C</kbd><kbd>V</kbd>

The `map()` method is simple, and contains a single `match`:

{{< highlight rust "linenos=true">}}
// Converts bytes into scan codes
// The mapping is done with the following keys:
// 1 2 3 C      1 2 3 4
// 4 5 6 D      Q W E R
// 7 8 9 E  =>  A S D F
// A 0 B F      Z X C V
pub fn map(code: u8) -> Scancode {
    match code {
        0x00 => Scancode::X,
        0x01 => Scancode::Num1,
        0x02 => Scancode::Num2,
        0x03 => Scancode::Num3,
        0x04 => Scancode::Q,
        0x05 => Scancode::W,
        0x06 => Scancode::E,
        0x07 => Scancode::A,
        0x08 => Scancode::S,
        0x09 => Scancode::D,
        0x0A => Scancode::Z,
        0x0B => Scancode::C,
        0x0C => Scancode::Num4,
        0x0D => Scancode::R,
        0x0E => Scancode::F,
        0x0F => Scancode::V,
        _ => Scancode::Escape,
    }
}
{{</ highlight >}}

The `unmap()` method is equally simple, this time in the opposite direction.

## Time

Nothing to see here, really. This module only contains a single method to get the current system time in nanoseconds.

## Debug

This module contains some debugging utilities that are used when `rchip8` is started wit the `-d` or `--debug` flags. In that case, the execution is paused after each instruction and the contents of the main data structures (counters, registers, etc.) are printed out. This is a good mode to enable if you need to study how the internal state of the machine changes with each instruction.

## Conclusion

In this post I have presented a Rust implementation of the CHIP-8 machine. We have seen each of the different modules and their responsibilities. There are many extensions and variations that could be added, like the CHIP-8X, the CHIP-8X or the S-CHIP (also called Super-Chip). These add different features like new instructions or additional display modes. I may implement some of them into `rchip8` in the future.

[^drw]: [Drawing sprites to the screen](https://github.com/mattmikolay/chip-8/wiki/Mastering-CHIP‐8#drawing-sprites-to-the-screen)
