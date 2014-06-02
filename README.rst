colorise v0.1.3
===============

.. image:: https://travis-ci.org/MisanthropicBit/colorise.svg?branch=master
    :target: https://travis-ci.org/MisanthropicBit/colorise

.. image:: https://pypip.in/license/colorise/badge.png
    :target: https://pypi.python.org/pypi/colorise/

Provides cross-platform text coloring for consoles, useful functions and a nestable color format syntax.

``colorise`` has been tested with Python 2.6, 2.7, 3.2 and 3.3.

Installation:
-------------
You can install via `pip <https://pip.pypa.io/en/latest/>`_::

    pip install colorise

Alternatively, if you downloaded the source files, just run the following command from the
download directory::

    python setup.py install

Usage:
------

There are a number of ways to color the foreground- and background colors of the output to the console.
You can find additional examples in the ``/examples`` folder.

You can directly set the color:

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/screenshots/set_color_usage.png
    :alt: Using the set_color function

You can print some text in a predefined color

.. code::

    >>> colorise.cprint("Error: Expected a string, found int", fg='red', bg='darkgreen')

``colorise`` has a special color format syntax that allows for nested expressions as well:

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/screenshots/fprint_usage.png
    :alt: Print color formatted text

There are a few useful tools as well:

.. code::

    >>> colorise.formatcolor("Format me, please!", bg='darkred')
    "<bg=darkred:Format me, please!>"
    >>> colorise.formatbyindex("Format me as well!", fg='blue', indices=[4, 17, 3, 5, 10])
    "For<fg=blue:mat> me <fg=blue:a>s well<fg=blue:!>"

``colorise.highlight`` behaves like ``colorise.formatbyindex``, but will write the output instead
of returning a string:

.. image:: https://raw.githubusercontent.com/MisanthropicBit/colorise/master/screenshots/highlight_usage.png
    :alt: Highlighting select characters in a string

If you have a ``<`` or ``>`` in your string, you can escape it with a backslash ``\``. The backslash
is automatically removed. Colons, escaped or not, ``:`` are ignored if they appear as text.

.. code::

    >>> colorise.fprint("<fg=darkpurple:Some : \> silly \< string>")

Implementation notes
--------------------
On Linux and Unix there are no 'dark' themed backgrounds, so calling

.. code::

    >>> colorise.cprint("Isn't this wrong?", bg='darkred')

will just set the background color to red. Also, 'normal' and 'dark' colors are either normal/bright colors,
or normal/dark depending on the underlying platform, and may not necessarily appear as very dark.

Due to the many different termnial/console types, it is virtually impossible to correctly map color names to
their actual colors. You may see variations (like 'yellow' showing up as brownish) or other discrepancies. ``colorise``
assumes the following available colors:

- Black
- Red
- Green
- Yellow
- Blue
- Magenta
- Cyan
- White

It is therefore best to stick to colors which are more likely to be present and correct, like 'red', 'blue' and 'green'.