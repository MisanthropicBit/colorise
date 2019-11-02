#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Windows color functions."""

import colorise.cluts
import colorise.win.cluts
from colorise.win.win32_functions import get_win_handle,\
    set_console_text_attribute
from colorise.win.win32_functions import redefine_colors as _redefine_colors
import operator
import sys

try:
    import functools
    reduce = functools.reduce
except ImportError:
    pass


def reset_color(file=sys.stdout):
    """Reset all colors and attributes."""
    handle = get_win_handle(file)
    set_color(handle.default_fg, handle.default_bg, file=file)


def or_bit_flags(*bit_flags):
    """Bitwise OR together a list of bitflags into a single flag."""
    return reduce(operator.or_, bit_flags)


def set_color(fg=None, bg=None, attributes=[], file=sys.stdout):
    """Set color and attributes in the terminal."""
    if fg or bg or attributes:
        if colorise.win.cluts.num_colors() > 16 and\
                colorise.win.cluts.can_interpret_ansi():
            # Extended terminal capabilities for interpreting ANSI escape
            # codes, delegate to nix color function
            colorise.nix.set_color(fg, bg, attributes, file)
        else:
            # Ordinary terminal capabilities, use Windows API
            attr_codes = colorise.attributes.to_codes(attributes)
            color_codes = [colorise.cluts.get_color(fg, False),
                           colorise.cluts.get_color(bg, True)]

            # Combine character attributes and color codes into a single
            # bitwise OR'ed bitflag
            flags = or_bit_flags(*(list(attr_codes) + color_codes))

            set_console_text_attribute(get_win_handle(file), flags)


def redefine_colors(color_map, file=sys.stdout):
    """Redefine the base console colors with a new mapping."""
    _redefine_colors(color_map, file)
