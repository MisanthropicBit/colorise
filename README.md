<center>
    <img src="colorise-logo.png" />
    <h3 align="center">v1.0.0</h3>
    <div align="center">
        <a href="https://travis-ci.org/MisanthropicBit/colorise">
            <img src="https://travis-ci.org/MisanthropicBit/colorise.svg?branch=rgb_256_exts" />
        </a>
        <a href="/LICENSE">
            <img src="https://img.shields.io/github/license/MisanthropicBit/colorise.svg" />
        </a>
        <a href="https://pypi.org/project/colorise/">
            <img src="https://img.shields.io/pypi/v/colorise.svg" />
        </a>
        <a href="https://pypi.org/project/colorise/">
            <img src="https://img.shields.io/pypi/wheel/colorise" />
        </a>
        <img src="https://img.shields.io/pypi/pyversions/colorise.svg" />
    </div>
</center>

---

`colorise` provides easy cross-platform text coloring for terminals/consoles and
has [been tested](/TESTED_ON.md) on different platforms/terminals.

## Features

* Supports 8, 16, 88, 256 colors and true-color.
* Colors can be specified by name, index, hexadecimal, HLS, HSV or RGB formats.

```python
>>> colorise.cprint('Hello', fg='red')
>>> colorise.cprint('Hello', fg=201)
>>> colorise.cprint('Hello', fg='#a696ff')
>>> colorise.cprint('Hello', fg='0xa696ff')
>>> colorise.cprint('Hello', fg='hls(0.6923;0.7960;1.0)')
>>> colorise.cprint('Hello', fg='hsv(249;41;100)')
>>> colorise.cprint('Hello', fg='rgb(167;151;255)')
```

* Custom color format akin to Python 3.0 [string formatting](https://docs.python.org/3.7/library/stdtypes.html#str.format).

```python
>>> colorise.fprint('{fg=red}Hello {bg=blue}world!')
```

* Automatically find the closest color based on the terminal's
  capabilities. Below is sprite of a [familiar plumber](/examples/mario.py).
  Pixels are specified as RGB so `colorise` automatically approximates colors
  for 256 and 16 color indices in the two right-most images.

<div align="center">
    <img src="/screenshots/mario-true-color.png" width="150" />
    <img src="/screenshots/mario-256-color.png" width="150" />
    <img src="/screenshots/mario-16-color.png" width="150" />
</div>
<div align="center">
    <i>From left to right: True-color, 256 color and 16 color.</i>
</div>
<br />

* Useful functions like [`highlight`](/examples/highlighting.py) that highlights
  individual characters in a string given a list of indices.
* Support for attributes such as bold, italic, underline etc.

```python
>>> colorise.highlight('Hello world', indices=[0, 2, 3, 7, 9], attributes=[Attr.Italic])
```

## Installation

Install `colorise` via [`pip`](https://pip.pypa.io/en/latest/).

```bash
pip install colorise
```

To get started check out the [tutorial](), [docs]() or the [examples]().
