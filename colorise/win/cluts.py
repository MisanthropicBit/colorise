#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Windows color look-up tables and functions."""

import colorise.nix.cluts
import colorise.color_tools
from colorise.attributes import Attr
from colorise.win.win32_functions import enable_virtual_terminal_processing,\
    can_interpret_ansi
import os
import platform
import sys


# Character attributes as defined in wincon.h
# We cannot get these through ctypes since they are #defines
_WIN_ATTRIBUTES = {
        Attr.Bold:      ('_FOREGROUND_INTENSITY',     0x0008),
        Attr.Intense:   ('_FOREGROUND_INTENSITY',     0x0008),  # Alias
        Attr.Reverse:   ('_COMMON_LVB_REVERSE_VIDEO', 0x4000),
        Attr.Underline: ('_COMMON_LVB_UNDERSCORE',    0x8000)

        # TODO: How do handle this when there is no ANSI escape sequence
        # equivalent?
        # ('_BACKGROUND_INTENSITY',     0x0080),
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
    9:  (0x00, 0x00, 0xff),  # Blue
    10: (0x00, 0xff, 0x00),  # Green
    11: (0x00, 0xff, 0xff),  # Cyan
    12: (0xff, 0x00, 0x00),  # Red
    13: (0xff, 0x00, 0xff),  # Purple
    14: (0xff, 0xff, 0x00),  # Yellow
    15: (0xff, 0xff, 0xff)   # White
}

# List of logical colors names on Windows (as defined by colorise)
_WINDOWS_LOGICAL_NAMES = {
    'black':       0,
    'red':         1,
    'green':       2,
    'yellow':      3,
    'magenta':     5,
    'blue':        4,
    'cyan':        6,
    'white':       7,
    'lightblack':  0 | _WIN_ATTRIBUTES[Attr.Bold][1],
    'lightred':    1 | _WIN_ATTRIBUTES[Attr.Bold][1],
    'lightgreen':  2 | _WIN_ATTRIBUTES[Attr.Bold][1],
    'lightyellow': 3 | _WIN_ATTRIBUTES[Attr.Bold][1],
    'lightblue':   4 | _WIN_ATTRIBUTES[Attr.Bold][1],
    'lightpurple': 5 | _WIN_ATTRIBUTES[Attr.Bold][1],
    'lightcyan':   6 | _WIN_ATTRIBUTES[Attr.Bold][1],
    'lightgray':   7 | _WIN_ATTRIBUTES[Attr.Bold][1],
}


def attributes():
    """Return a mapping of all Windows attributes."""
    return _WIN_ATTRIBUTES


def get_prefix(color_count, bg):
    """Get the color code prefix corresponding to the supported color count."""
    return ''


def get_clut(color_count):
    """Return the appropriate color look-up table."""
    return _WINDOWS_CLUT


def set_windows_clut():
    """Set the internal Windows color look-up table."""
    pass
    # if _WIN_CAN_SET_COLORS:
    #     # On Windows Vista and beyond you can query the current colors in the
    #     # color table. On older platforms, use the default color table
    #     csbiex = CONSOLE_SCREEN_BUFFER_INFOEX()
    #     windll.kernel32.GetConsoleScreenBufferInfoEx(
    #         colorise._color_manager._handle,
    #         ctypes.byref(csbiex)
    #     )

    #     # Update according to the currently set colors
    #     for i in range(16):
    #         _WINDOWS_CLUT[i] =\
    #             (windll.kernel32.GetRValue(csbiex.ColorTable[i]),
    #              windll.kernel32.GetGValue(csbiex.ColorTable[i]),
    #              windll.kernel32.GetBValue(csbiex.ColorTable[i]))

    # # Create a mapping from windows colors to their logical names
    # for color, name in zip(_WINDOWS_CLUT.values(),
    #                        _WINDOWS_LOGICAL_NAMES):
    #     _WINDOWS_LOGICAL_NAMES[color] = name


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

    if enable_virtual_terminal_processing():
        return 2**24

    # Supported colors in Windows are pre-determined. Though you can update the
    # colors in the color table on Vista and beyond, this also changes all
    # colors of text already in the console window
    return 16


def color_from_name(name, color_count, isbg):
    """Return the color value and color count for a given color name."""
    if name not in _WINDOWS_LOGICAL_NAMES:
        raise ValueError("Unknown color name '{0}'".format(name))

    return _WINDOWS_CLUT[_WINDOWS_LOGICAL_NAMES[name]]


def color_from_index(idx, color_count, bg):
    """Return the color value and color count for a given color index."""
    if can_interpret_ansi():
        # We can interpret ANSI escape sequences, delegate to nix
        return colorise.nix.cluts.color_from_index(idx, color_count, bg)

    if idx in get_clut(color_count):
        # Color index is an ordinary Windows logical color table index
        return idx

    if idx > 88:
        # 256 color index
        return colorise.color_tools.closest_color(
                colorise.nix.cluts._XTERM_CLUT_256[idx],
                _WINDOWS_CLUT
            )
    elif idx == 88:
        # 88 color index
        return colorise.color_tools.closest_color(
                colorise.nix.cluts._XTERM_CLUT_88[idx],
                _WINDOWS_CLUT
            )

    return colorise.color_tools.closest_color(_WINDOWS_CLUT)
