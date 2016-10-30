# colorise v1.0.0 ![Build status](https://travis-ci.org/MisanthropicBit/colorise.svg?branch=rgb_256_exts) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/MisanthropicBit/colorise/rgb_256_exts/LICENSE)

`colorise` provides cross-platform text coloring for consoles, some useful functions and a nestable color format syntax that supports Python's (2.6+) string formatting.

* Custom string format for colors that integrates with python 2.6+ string formatting
* Useful functions like [`highlight`](/examples/highlighting.py)
* Automatically matches the closest color based on your terminal's capabilities
* Supports 16 colors, 88 colors, 256 colors and true-color
* Supports colors by name, index, hexadecimal, HLS, HSV or RGB format

`colorise` has been tested with Python 2.6, 2.7, 3.2 and 3.3, and the following terminals:

* iTerm 2.1.4,
* Terminal.app 2.6.1 (361.1)
* The default Windows console (?).

![Example of using colorise](/demo.gif?raw=true)

## Installation:

You can install via [`pip`](https://pip.pypa.io/en/latest/):

```bash
pip install colorise
```

Or downloaded the repository and run the following command:

```bash
python setup.py install
```

## Usage:

The color format is defined as follows: <(i|rgb|hex|hsv|hsl):text> where

    * i is an index of a 88- or 256-color in the terminal, e.g. "<fg=106:...>"
    * rgb is a tuple of red, green and blue channel intensities, e.g. "<bg=255,128,34:...>"
    * hex is a hexadecimal representation of a color, e.g. "<fg=#c3ef41:...>"
    * hsl is a hue, saturation and luminence representation of a color, e.g. "<fg=hsv(?,?,?):...>"
    * hsv is a hue, saturation and ? representation of a color, e.g. "<fg=hsl(?,?,?):...>"

If your terminal does not support a given color, ``colorise`` will attempt to approximate it. For example, if
you specify a 256-color index on a terminal that supports only 88 colors.

There are a number of ways to color the foreground- and background colors of the output to the console.
You can find additional examples in the ``/examples`` folder.

You can directly set the color:

![Using the set_color function](/screenshots/set_color_usage_win.png)

You can print some text in a predefined color:

![Using the cprint function to color a string](/screenshots/cprint_usage_xubuntu.png)

`colorise` has a special color format syntax that allows for nested expressions as well:

![Print color formatted text](/screenshots/fprint_usage_win.png)

There are a few useful tools as well:

![Format a string in colors](/screenshots/formatcolor_usage_mac.png)

![Format a string in colors using a list of indices](/screenshots/formatbyindex_usage_mac.png)

`colorise.highlight` behaves like `colorise.formatbyindex`, but will write the colored output instead
of returning a formatted string:

![Highlighting select characters in a string](/screenshots/highlight_usage_win.png)

If you have a `<` or `>` in your string, you can escape it with a backslash `\\`. The backslash
is automatically removed. Colons, escaped or not, `:` are ignored if they appear as text.

![Use of escapes in a color format string](/screenshots/fprint_escapes_usage_mac.png)

## Implementation notes
On Linux and Unix there are no 'dark' themed backgrounds (perhaps "bolded" or "bright" colors are a better name, but do not truly represnt darkened colors), so calling

```bash
>>> colorise.cprint("Isn't this wrong?", bg='darkred')
```

will not necessarily give the expected result. This is due to the many different termnial/console types, making it is virtually impossible to correctly map color names to their actual colors. Additionally, some consoles, such as iTerm and the Windows standard console, lets you redefine colors, so that using logical colornames is no guarantee for consistency. ``colorise`` assumes the following available colors on all systems:

* Black
* Red
* Green
* Yellow
* Blue
* Magenta
* Cyan
* White

It is therefore best to stick to these systems colors which are more likely to be present and "correct", like 'red', 'blue' and 'green'.
