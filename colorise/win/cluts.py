#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Windows color look-up tables and functions."""

from colorise.attributes import Attr
from colorise.color_tools import closest_color
from colorise.win.win32_functions import can_interpret_ansi
import colorise.nix.cluts
import os
import platform
import sys

# Character attributes as defined in wincon.h
# We cannot get these through ctypes since they are #defines
_WIN_ATTRIBUTES = {
        Attr.Reset:     0x0000,
        Attr.Bold:      0x0008,
        Attr.Intense:   0x0008,  # Alias
        Attr.Faint:     0x0000,
        Attr.Italic:    0x0000,
        Attr.Underline: 0x8000,
        Attr.Blink:     0x0000,
        Attr.Reverse:   0x4000,
    }

# Windows 16-color (logical) look-up table
_WINDOWS_CLUT = {
    0:  (0x00, 0x00, 0x00),  # Black
    1:  (0x00, 0x00, 0x80),  # Red
    2:  (0x00, 0x80, 0x00),  # Green
    3:  (0x00, 0x80, 0x80),  # Yellow
    4:  (0x80, 0x00, 0x00),  # Magenta
    5:  (0x80, 0x00, 0x80),  # Blue
    6:  (0x80, 0x80, 0x00),  # Cyan
    7:  (0xff, 0xff, 0xff),  # White
    8:  (0x80, 0x80, 0x80),  # Gray/intensity
    # The remaining colors are sometimes referred to as the 'light' colors
    9:  (0x00, 0x00, 0xff),  # Light blue
    10: (0x00, 0xff, 0x00),  # Light green
    11: (0x00, 0xff, 0xff),  # Light cyan
    12: (0xff, 0x00, 0x00),  # Light red
    13: (0xff, 0x00, 0xff),  # Light purple
    14: (0xff, 0xff, 0x00),  # Light yellow
    15: (0xff, 0xff, 0xff)   # Light white
}

_FOREGROUND_RED = 0x0004
_FOREGROUND_GREEN = 0x0002
_FOREGROUND_BLUE = 0x0001
_FOREGROUND_INTENSITY = _WIN_ATTRIBUTES[Attr.Bold]

# List of logical colors names on Windows (as defined by colorise)
_WINDOWS_LOGICAL_NAMES = {
    'black':   0,
    'red':     _FOREGROUND_RED,
    'green':   _FOREGROUND_GREEN,
    'yellow':  _FOREGROUND_RED | _FOREGROUND_GREEN,
    'magenta': _FOREGROUND_RED | _FOREGROUND_BLUE,
    'purple':  _FOREGROUND_RED | _FOREGROUND_BLUE,
    'blue':    _FOREGROUND_BLUE,
    'cyan':    _FOREGROUND_GREEN | _FOREGROUND_BLUE,
    'white':   _FOREGROUND_RED | _FOREGROUND_GREEN | _FOREGROUND_BLUE,
}

for name in ['red', 'green', 'blue', 'yellow', 'purple', 'magenta', 'cyan']:
    _WINDOWS_LOGICAL_NAMES['light' + name] =\
        _WINDOWS_LOGICAL_NAMES[name] | _FOREGROUND_INTENSITY

_WINDOWS_LOGICAL_NAMES['gray'] = _WINDOWS_LOGICAL_NAMES['black'] |\
    _FOREGROUND_INTENSITY
_WINDOWS_LOGICAL_NAMES['grey'] = _WINDOWS_LOGICAL_NAMES['black'] |\
    _FOREGROUND_INTENSITY


def attributes():
    """Return a mapping of all Windows attributes."""
    return _WIN_ATTRIBUTES


def get_prefix(color_count, bg):
    """Get the color code prefix corresponding to the supported color count."""
    return ''


def get_clut(color_count):
    """Return the appropriate color look-up table."""
    return _WINDOWS_CLUT


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


def color_from_name(name, color_count, bg):
    """Return the color value and color count for a given color name."""
    if name not in _WINDOWS_LOGICAL_NAMES:
        raise ValueError("Unknown color name '{0}'".format(name))

    color = _WINDOWS_LOGICAL_NAMES[name]

    return color << 4 if bg else color


def color_from_index(idx, color_count, bg):
    """Return the color value and color count for a given color index."""
    if can_interpret_ansi():
        # We can interpret ANSI escape sequences, delegate to nix function
        return colorise.nix.cluts.color_from_index(idx, color_count, bg)

    if idx < 0 or idx > 255:
        raise ValueError('Color index must be in range 0-255 inclusive')

    if idx < 16:
        color = closest_color(
                colorise.nix.cluts._NIX_SYSTEM_COLORS,
                _WINDOWS_CLUT
            )
    elif idx < 88:
        # 88 color index
        color = closest_color(
                colorise.nix.cluts._XTERM_CLUT_88[idx],
                _WINDOWS_CLUT
            )
    elif idx < 256:
        # 256 color index
        color = closest_color(
                colorise.nix.cluts._XTERM_CLUT_256[idx],
                _WINDOWS_CLUT
            )

    return color << 4 if bg else color


def get_rgb_color(color_count, bg, rgb):
    """Get the color for an RGB triple or approximate it if necessary."""
    if color_count == 2**24:
        # We have true-color capabilities, delegate to nix function
        # approximate to closest color given current capabilities
        return colorise.nix.cluts.get_rgb_color(color_count, bg, rgb)

    # No true-color capabilities, approximate the rgb color
    idx = closest_color(rgb, get_clut(color_count))

    return idx << 4 if bg else idx
