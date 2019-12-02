#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Linux/Mac color functions."""

import colorise.error
import colorise.nix.cluts
from colorise.attributes import Attr
from colorise.cluts import get_color
from colorise.terminal import terminal_name
import io
import os
import sys


def num_colors():
    """Attempt to get the number of colors supported by the terminal."""
    # iTerm supports true-color from version 3 onward, earlier versions
    # supported 256 colors
    if terminal_name() == 'iTerm.app':
        version = os.environ.get('TERM_PROGRAM_VERSION', '')

        if version and int(version.split('.')[0]) > 2:
            return 2**24
        else:
            return 256

    # If all else fails, use curses
    import curses
    color_count = 0

    try:
        curses.setupterm()
        color_count = curses.tigetnum('colors')
    except curses.error:
        pass
    except io.UnsupportedOperation:
        pass

    if color_count <= 0:
        # Failed to get color count from curses, default to 16 colors
        return 16

    return color_count


def to_ansi(*codes):
    """Convert a set of ANSI codes into a valid ANSI escape sequence."""
    if not codes:
        return ''

    return colorise.nix.cluts._COLOR_ESCAPE_CODE +\
        '{0}m'.format(';'.join(str(c) for c in codes))


def attributes_to_codes(attributes):
    """Convert a set of attributes to ANSI escape codes."""
    return [int(attr.value) for attr in attributes]


def reset_color(file=sys.stdout):
    """Reset all colors and attributes."""
    file.write(to_ansi(Attr.Reset.value))


def set_color(fg=None, bg=None, attributes=[], file=sys.stdout):
    """Set color and attributes of the terminal.

    'fg' and 'bg' specify foreground- and background colors while 'attributes'
    is a list of desired attributes. The 'file' keyword specifies the target
    output stream.

    """
    codes = []

    if attributes:
        codes.append(to_ansi(*attributes_to_codes(attributes)))

    if Attr.Reset not in attributes:
        color_count = num_colors()

        for colorspec, isbg in ((fg, False), (bg, True)):
            if colorspec:
                prefix, color = get_color(colorspec, color_count,
                                          colorise.nix.cluts, isbg)
                codes.append(prefix.format(color))

    if codes:
        file.write(''.join(codes))


def redefine_colors(color_map, file=sys.stdout):
    """Redefine the base console colors with a new mapping."""
    raise colorise.error.NotSupportedError('Cannot redefine colors on nix '
                                           'systems')
