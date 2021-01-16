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
from colorise.win.winhandle import WinHandle
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
    build = sys.getwindowsversion().build

    # Windows 10 build 14931 has support for 24-bit colors
    if release == '10' and build >= 14931:
        return 2**24

    # We check both output streams here because we want to determine color
    # capabilities in general so this should return 2**24 if stdout is
    # redirected but stderr is not. If both are redirected, the output stream
    # does not interpreat ANSI escape sequences
    if can_interpret_ansi(sys.stdout) or can_interpret_ansi(sys.stderr):
        return 2**24

    # Supported colors in Windows are pre-determined. Though you can update the
    # colors in the color table on Vista and beyond, this also changes all
    # colors of text already in the console window
    return 16


def reset_color(file=sys.stdout):
    """Reset all colors and attributes."""
    if num_colors() > 16 and can_interpret_ansi(file):
        colorise.nix.color_functions.reset_color(file)
    else:
        handle = get_win_handle(WinHandle.from_sys_handle(file))

        if handle.is_console_handle:
            # Do not call the console api when output target is not a tty since
            # calls that expect it to be a valid console handle will fail
            set_console_text_attribute(
                handle,
                handle.default_fg | handle.default_bg,
            )


def or_bit_flags(*bit_flags):
    """Bitwise OR together a list of bitflags into a single flag."""
    return functools.reduce(operator.or_, bit_flags)


def set_color(fg=None, bg=None, attributes=None, file=sys.stdout):
    """Set color and attributes in the terminal."""
    if num_colors() > 16 and can_interpret_ansi(file):
        colorise.nix.color_functions.set_color(
            fg, bg, attributes, file, num_colors_func=num_colors,
        )
    else:
        if fg or bg or attributes:
            if Attr.Reset not in attributes:
                handle = get_win_handle(WinHandle.from_sys_handle(file))
                color_count = num_colors()
                codes = []

                for idx, color in enumerate([fg, bg]):
                    isbg = idx == 1

                    if color:
                        codes.extend(get_color(
                            color,
                            color_count,
                            colorise.win.cluts,
                            isbg,
                            attributes,
                        ))
                    else:
                        codes.append(
                            handle.default_bg if isbg else handle.default_fg,
                        )

                if handle.is_console_handle:
                    # Combine attributes and color codes into a single bitflag
                    # if the handle is a valid console handle (a tty) since
                    # win32 calls that expect it to be a valid console handle
                    # will fail otherwise. We still call get_color above
                    # because we want to inform users about incorrect color
                    # formats even if the output is a pipe or a call in a
                    # subprocess
                    flags = or_bit_flags(*codes)
                    set_console_text_attribute(handle, flags)
            else:
                reset_color(file)


def redefine_colors(color_map, file=sys.stdout):
    """Redefine the base console colors with a new mapping."""
    _redefine_colors(color_map, file)
