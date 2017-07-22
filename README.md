# colorise v1.0.0 ![Build status](https://travis-ci.org/MisanthropicBit/colorise.svg?branch=rgb_256_exts) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/MisanthropicBit/colorise/rgb_256_exts/LICENSE) [![PyPI version](https://badge.fury.io/py/colorise.svg)](https://badge.fury.io/py/colorise)

`colorise` provides cross-platform text coloring for consoles using a nestable color format syntax akin to Python's 2.6+ string formatting.

* Custom string format for colors that integrates with python 2.6+ string formatting
* Automatically tries to find the closest color based on your terminal's capabilities
* Supports 16 colors, 88 colors, 256 colors and true-color
* Supports giving colors by name, index, hexadecimal, HLS, HSV or RGB format
* Useful functions like [`highlight`](/examples/highlighting.py)

`colorise` has been tested with Python 2.6, 2.7, 3.2 and 3.3, and the following terminals:

* iTerm 2.1.4,
* Terminal.app 2.6.1 (361.1)
* The default Windows console

## Installation

You can install via [`pip`](https://pip.pypa.io/en/latest/):

```bash
pip install colorise
```

Or downloaded the repository and run the following command:

```bash
python setup.py install
```

## Usage

![Example of using colorise](/demo.gif?raw=true)

If your terminal does not support a given color, ``colorise`` will attempt to
approximate it. For example, if you specify a color as (255, 0, 0) on a 16-color
terminal, you will still get red. You can find additional examples in the ``/examples``
folder.

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
