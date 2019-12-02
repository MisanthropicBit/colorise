#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Windows color functions."""

from colorise.attributes import Attr
from colorise.cluts import get_color
import colorise.nix.color_functions
from colorise.win.cluts import can_interpret_ansi
from colorise.win.win32_functions import\
    get_win_handle,\
    set_console_text_attribute,\
    redefine_colors as _redefine_colors
import functools
import operator
import os
import platform
import sys


def num_colors():
    """Get the number of colors supported by the terminal."""
    if os.environ.get('ConEmuANSI', '') == 'ON':
        # ANSI escapes sequences are interpreted. ConEmu console detected which
        # supports 24-bit colors, but can we detect this somehow?
        #
        # NOTE: ConEmu also supports more attributes than the normal Windows
        # console.
        return 256

    release = platform.win32_ver()[0]
    build = sys.getwindowsversion()[2]

    # Windows 10 build 14931 has support for 24-bit colors
    if release == '10' and build >= 14931:
        return 2**24

    if can_interpret_ansi():
        return 2**24

    # Supported colors in Windows are pre-determined. Though you can update the
    # colors in the color table on Vista and beyond, this also changes all
    # colors of text already in the console window
    return 16


if num_colors() > 16 and can_interpret_ansi():
    # Extended terminal capabilities for interpreting ANSI escape codes,
    # delegate to nix color functions

    def reset_color(file=sys.stdout):
        """Reset all colors and attributes."""
        colorise.nix.color_functions.reset_color(file)


    def set_color(fg=None, bg=None, attributes=[], file=sys.stdout):
        """Set color and attributes in the terminal."""
        colorise.nix.color_functions.set_color(fg, bg, attributes, file,
                                               num_colors_func=num_colors)
else:
    # Ordinary terminal capabilities, use Windows API

    def reset_color(file=sys.stdout):
        """Reset all colors and attributes."""
        handle = get_win_handle(file)
        set_console_text_attribute(handle,
                                   handle.default_fg | handle.default_bg)


    def or_bit_flags(*bit_flags):
        """Bitwise OR together a list of bitflags into a single flag."""
        return functools.reduce(operator.or_, bit_flags)

    def set_color(fg=None, bg=None, attributes=[], file=sys.stdout):
        """Set color and attributes in the terminal."""
        if fg or bg or attributes:
            if Attr.Reset not in attributes:
                handle = get_win_handle(file)
                color_count = num_colors()
                codes = []

                codes.extend(get_color(fg, color_count, colorise.win.cluts,
                                       False, attributes)
                            if fg else [handle.default_fg])
                codes.extend(get_color(bg, color_count, colorise.win.cluts,
                                       True, attributes)
                            if bg else [handle.default_bg])

                # Combine attributes and color codes into a single bitflag
                flags = or_bit_flags(*codes)
                set_console_text_attribute(handle, flags)
            else:
                reset_color(file)


def redefine_colors(color_map, file=sys.stdout):
    """Redefine the base console colors with a new mapping."""
    _redefine_colors(color_map, file)
