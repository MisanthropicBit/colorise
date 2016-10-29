colorise v1.0.0
===============

.. image:: https://travis-ci.org/MisanthropicBit/colorise.svg?branch=master
    :target: https://travis-ci.org/MisanthropicBit/colorise

.. image:: https://pypip.in/license/colorise/badge.png
    :target: https://pypi.python.org/pypi/colorise/

``colorise`` provides cross-platform text coloring for consoles, some useful functions and a nestable color format syntax that supports Python's (2.6+) string formatting.

``colorise`` has been tested with Python 2.6, 2.7, 3.2 and 3.3, and the following terminals: iTerm 2.1.4, Terminal.app 2.6.1 (361.1) and the Windows console (?).

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/demo/colorise_demo.gif
    :alt: Demo of colorise

Installation:
-------------
You can install via `pip <https://pip.pypa.io/en/latest/>`_::

    pip install colorise

Alternatively, if you downloaded the source files, just run the following command from the
download directory::

    python setup.py install

Usage:
------

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

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/screenshots/set_color_usage_win.png
    :alt: Using the set_color function

You can print some text in a predefined color

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/screenshots/cprint_usage_xubuntu.png
    :alt: Using the cprint function to color a string

``colorise`` has a special color format syntax that allows for nested expressions as well:

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/screenshots/fprint_usage_win.png
    :alt: Print color formatted text

There are a few useful tools as well:

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/screenshots/formatcolor_usage_mac.png
    :alt: Format a string in colors

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/screenshots/formatbyindex_usage_mac.png
    :alt: Format a string in colors using a list of indices

``colorise.highlight`` behaves like ``colorise.formatbyindex``, but will write the output instead
of returning a string:

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/screenshots/highlight_usage_win.png
    :alt: Highlighting select characters in a string

If you have a ``<`` or ``>`` in your string, you can escape it with a backslash ``\``. The backslash
is automatically removed. Colons, escaped or not, ``:`` are ignored if they appear as text.

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/screenshots/fprint_escapes_usage_mac.png
    :alt: Use of escapes in a color format string

Implementation notes
--------------------
On Linux and Unix there are no 'dark' themed backgrounds (perhaps "bolded" or "bright" colors are a better name, but do not truly represnt darkened colors), so calling

    >>> colorise.cprint("Isn't this wrong?", bg='darkred')

will not necessarily give the expected result. This is due to the many different termnial/console types, making it is virtually impossible to correctly map color names to their actual colors. Additionally, some consoles, such as iTerm and the Windows standard console, lets you redefine colors, so that using logical colornames is no guarantee for consistency. ``colorise`` assumes the following available colors on all systems:

- Black
- Red
- Green
- Yellow
- Blue
- Magenta
- Cyan
- White

It is therefore best to stick to these systems colors which are more likely to be present and "correct", like 'red', 'blue' and 'green'.
