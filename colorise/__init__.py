#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python module for easy, cross-platform colored output to the terminal."""

from __future__ import print_function

import atexit
import colorise.formatter
from colorise.attributes import Attr
import itertools
import os
import platform
import sys

_PY2 = sys.version_info[0] < 3
_DEBUG_MODE = False
_SYSTEM_OS = platform.system().lower()

__author__ = 'Alexander Asp Bock'
__version__ = '1.0.0'
__license__ = 'MIT'
__all__ = [
    'can_redefine_colors',
    'redefine_colors',
    'color_names',
    'num_colors',
    'set_num_colors',
    'set_color',
    'cprint',
    'fprint',
    'highlight'
]


if _DEBUG_MODE:
    sys.stderr.write('Python {0}'.format(sys.version))

    import struct

    def _32or64bit():
        """Determine if the OS is using a 32- or 64-bit architecture."""
        return 8 * struct.calcsize('P')


# Determine which platform-specific color manager to import
if _SYSTEM_OS.startswith('win'):
    from colorise.win import\
        reset_color,\
        set_color as _set_color,\
        redefine_colors as _redefine_colors,\
        num_colors as _num_colors,\
        set_color as _set_color

    from colorise.win.win32_functions import\
        can_redefine_colors as _can_redefine_colors,\
        restore_console_modes

    # Ensure that the console mode set before colorise was loaded is restored
    atexit.register(restore_console_modes)

    if _DEBUG_MODE:
        print('{0} {1} ({2}-bit)'.format(platform.system(),
                                         platform.release(),
                                         _32or64bit()))
else:
    from colorise.nix import\
        reset_color,\
        set_color as _set_color,\
        redefine_colors as _redefine_colors,\
        num_colors as _num_colors,\
        set_color as _set_color\

    from colorise.nix.cluts import\
        can_redefine_colors as _can_redefine_colors

    if _DEBUG_MODE:
        dist = platform.linux_distribution()

        print('{0}, {1}, {2} ({3}-bit)'.format(dist + _32or64bit()))

# User-defined color count
__NUM_COLORS__ = 0


def num_colors():
    """Return the number of colors supported by the terminal."""
    if __NUM_COLORS__ > 0:
        # Return a user-defined color count
        return __NUM_COLORS__

    return _num_colors()


def set_num_colors(color_count):
    """Set the number of colors available instead of autodetecting it.

    This is primarily useful for testing and debugging.

    """
    color_counts = [8, 16, 88, 256, 2**24]

    if color_count not in color_counts:
        raise ValueError('Invalid color count, expected any of {0}'
                         .format(', '.join(str(cc) for cc in color_counts)))

    global __NUM_COLORS__
    __NUM_COLORS__ = color_count


def can_redefine_colors():
    """Return True if the terminal supports redefinition of colors.

    Only returns True for Windows 7/Vista and beyond as of now.

    """
    return _can_redefine_colors()


def redefine_colors(color_map, file=sys.stdout):
    """Redefine colors using a color map of indices and RGB tuples."""
    _redefine_colors(color_map, file)


def color_names():
    """Return a list of supported color names."""
    return [
        'black',
        'red',
        'green',
        'yellow',
        'blue',
        'purple',
        'magenta',
        'cyan',
        'gray',
        'grey',
        'lightgrey',
        'lightgray',
        'lightred',
        'lightgreen',
        'lightyellow',
        'lightblue',
        'lightpurple',
        'lightcyan',
        'white',
    ]


def set_color(fg=None, bg=None, attributes=[], file=sys.stdout):
    """Set the current colors.

    If no arguments are given, sets default colors.

    """
    _set_color(fg, bg, attributes, file)


def cprint(string, fg=None, bg=None, attributes=[], end=os.linesep,
           file=sys.stdout, enabled=True):
    """Print a string to a target stream with colors and attributes.

    The fg and bg keywords specify foreground- and background colors while
    attributes is a list of desired attributes. The remaining two keyword
    arguments are the same as Python's built-in print function.

    Colors and attribtues are reset before the function returns.

    """
    if not enabled:
        file.write(string)
        file.write(end)
        file.flush()
    else:
        set_color(fg, bg, attributes, file)
        file.write(string)
        file.flush()  # Flush before resetting colors
        reset_color(file)

        # Make sure to print the end keyword after resetting so the next line
        # is not affected by a newline or similar
        file.write(end)
        file.flush()  # Flush before resetting colors


# Global color formatter instance
_color_formatter = colorise.formatter.ColorFormatter(set_color, reset_color)


def fprint(fmt, autoreset=False, end=os.linesep, file=sys.stdout,
           enabled=True):
    """Print a string with color formatting.

    The autoreset keyword controls if colors and attributes are reset before
    each new color format. For example:

    >>> colorise.fprint('{fg=blue}Hi {bg=red}world', autoreset=False)

    would print 'Hi' in blue foreground colors and 'world' in blue foreground
    colors AND a red background color, whereas:

    >>> colorise.fprint('{fg=blue}Hi {bg=red}world', autoreset=True)

    would print 'Hi' in blue foreground colors but 'world' only with a red
    background color since colors are reset when '{bg=red}' is encountered.

    The remaining two keyword arguments are the same as Python's built-in print
    function.

    Colors and attribtues are reset before the function returns.

    """
    _color_formatter.autoreset = autoreset
    _color_formatter.file = file
    _color_formatter.enabled = enabled
    _color_formatter.format(fmt)

    if enabled:
        file.flush()  # Flush before resetting colors
        reset_color(file)

    # Make sure to print the end keyword after resetting so the next line is
    # not affected by a newline or similar
    file.write(end)


def highlight(string, indices, fg=None, bg=None, attributes=[], end=os.linesep,
              file=sys.stdout, enabled=True):
    """Highlight characters using indices and print to a target stream.

    The indices argument is a list of indices (not necessarily sorted) for
    which to apply the colors and attributes. Indices that are out of bounds
    are ignored.

    fg and bg specify foreground- and background colors while attributes is a
    list of desired attributes. The remaining two keyword arguments are the
    same as Python's built-in print function.

    Colors and attribtues are reset before the function returns.

    """
    if not string or not indices or not (fg or bg or attributes)\
            or not enabled:
        file.write(string + end)
        return

    idx = 0

    # Group consecutive indices, e.g. [0, 2, 3, 5, 6] -> [(0), (2, 3), (5, 6)]
    # NOTE: The lambda syntax is necessary to support both Python 2 and 3
    groups = itertools.groupby(enumerate(sorted(indices)), lambda x: x[0]-x[1])

    for _, group in groups:
        # Get the starting and ending indices of the group
        group = list(group)
        start_idx, end_idx = group[0][1], group[-1][1]+1

        # Write anything up until the start index of the current group
        file.write(string[idx:start_idx])
        file.flush()

        set_color(fg, bg, attributes, file)

        # Write the range of characters specified by the group
        file.write(string[start_idx:end_idx])
        file.flush()

        reset_color(file)

        # Set current index to end of group
        idx = end_idx

    # Write anything that is left to write
    if idx < len(string):
        file.write(string[idx:])

    file.write(end)


# Ensure colors and attributes return to normal when colorise is quit
if sys.stdout.isatty():
    atexit.register(reset_color)
