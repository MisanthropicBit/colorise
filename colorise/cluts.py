#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note:
# All look-up tables presented here are entirely based on internet research, as
# it is impossible to ensure complete cross-platform support across all kinds
# of terminals. Therefore, there is no guarantee that any of these tables will
# be accurate.
#
# If you have suggestions, please do not hesitate to contact me :)

import colorise
import colorsys
import ctypes
import itertools
import operator
import os
import platform
import re
import sys

try:
    import curses
except ImportError:
    pass

_FLOAT_RE_FMT = r'\d+\.(\d+)?'
_RGB_RE = re.compile('^(rgb)?\((\d{1,3},\s*\d{1,3},\s*\d{1,3})\)$')
_HEX_RE = re.compile('^(0x|#)?(([0-9a-fA-F]{2}){3})$')
_HSV_RE = re.compile('^(hsv)\((\d+,\s*\d+,\s*\d+)\)$')
_HLS_RE = re.compile('^(hls)\(({0},\s*{1},\s*{2})\)$'.format(_FLOAT_RE_FMT,
                                                             _FLOAT_RE_FMT,
                                                             _FLOAT_RE_FMT))

# The order matters!
_FORMATS = [
    (_RGB_RE.match, 'rgb'),
    (str.isdigit,   'index'),
    (str.isalpha,   'name'),
    (_HEX_RE.match, 'hex'),
    (_HLS_RE.match, 'hls'),
    (_HSV_RE.match, 'hsv')
]

_COLOR_ESCAPE_CODE = '\033['
_COLOR_PREFIX_16 = _COLOR_ESCAPE_CODE + '{0}m'
_COLOR_PREFIX_88 = _COLOR_ESCAPE_CODE + '38;5;{0}m'
_COLOR_PREFIX_256 = _COLOR_PREFIX_88
_COLOR_PREFIX_FG_TRUE_COLOR = _COLOR_ESCAPE_CODE + '38;2;{0}m'
_COLOR_PREFIX_BG_TRUE_COLOR = _COLOR_ESCAPE_CODE + '48;2;{0}m'


###############################################################################
# Color look-up tables
###############################################################################
# User-defined color count (always ignored on Windows as it only ever
# has 16 colors)
class settings:
    __NUM_COLORS__ = 0

###############################################################################
# Windows color setup

# Windows 16-color (logical) look-up table
_WINDOWS_CLUT = {
    0: (0x00, 0x00, 0x00),  # Black
    1: (0x00, 0x00, 0x80),  # Dark blue (FOREGROUND_BLUE)
    2: (0x00, 0x80, 0x00),  # Dark green (FOREGROUND_GREEN)
    3: (0x00, 0x80, 0x80),  # Dark cyan (FOREGROUND_GREEN)
    4: (0x80, 0x00, 0x00),  # Dark red (FOREGROUND_RED)
    5: (0x80, 0x00, 0x80),  # Magenta
    6: (0x80, 0x80, 0x00),  # Yellow
    7: (0xff, 0xff, 0xff),  # White
    8: (0x80, 0x80, 0x80),  # Gray/intensity
    # The remaining colors are sometimes referred to as the 'light' colors
    9: (0x00, 0x00, 0xff),  # Blue
    10: (0x00, 0xff, 0x00),  # Green
    11: (0x00, 0xff, 0xff),  # Cyan
    12: (0xff, 0x00, 0x00),  # Red
    13: (0xff, 0x00, 0xff),  # Purple
    14: (0xff, 0xff, 0x00),  # Yellow
    15: (0xff, 0xff, 0xff)  # White
}

# List of logical colors names on Windows (as defined by colorise)
_WINDOWS_LOGICAL_NAMES = ['black', 'darkblue', 'darkgreen', 'darkcyan',
                          'darkred', 'magenta', 'yellow', 'white', 'gray',
                          'blue', 'green', 'cyan', 'red', 'purple', 'yellow',
                          'white']

# Mapping from colors in _WINDOWS_CLUT to logical color names
# (see set_windows_clut below)
# _WINDOWS_LOGICAL_NAMES = {}


###############################################################################
# Nix color setup

# System base colors that are assumed to be present for 8 color terminals
_NIX_SYSTEM_COLORS = {
    0: (0x00, 0x00, 0x00),   # black
    1: (0x80, 0x00, 0x00),   # dark red
    2: (0x00, 0x80, 0x00),   # dark green
    3: (0x80, 0x80, 0x00),   # dark yellow
    4: (0x00, 0x00, 0x80),   # dark blue
    5: (0x80, 0x00, 0x80),   # dark purple
    6: (0x00, 0x80, 0x80),   # dark cyan
    7: (0xc0, 0xc0, 0xc0),   # light gray
    8: (0x80, 0x80, 0x80),   # gray
    9: (0xff, 0x00, 0x00),   # red
    10: (0x00, 0xff, 0x00),  # green
    11: (0xff, 0xff, 0x00),  # yellow
    12: (0x00, 0x00, 0xff),  # blue
    13: (0xff, 0x00, 0xff),  # purple
    14: (0x00, 0xff, 0xff),  # cyan
    15: (0xff, 0xff, 0xff)   # white
}

_NIX_SYSTEM_COLOR_NAMES = {
    'black': 0,
    'darkred': 1,
    'darkgreen': 3,
    'darkyellow': 4,
    'darkblue': 5,
    'darkpurple': 6,
    'darkcyan': 7,
    'lightgray': 8,
    'red': 9,
    'green': 10,
    'yellow': 11,
    'blue': 12,
    'purple': 13,
    'cyan': 14,
    'white': 15
}

_NIX_SYSTEM_COLOR_NAMES['lightgrey'] = 8

# xterm 88-color look-up table (based on 88colres.h)
_XTERM_CLUT_88_STEPS = [0x00, 0x8b, 0xcd, 0xff]
_XTERM_CLUT_88 = dict(zip(range(16, 88),
                          [(r, g, b) for r in _XTERM_CLUT_88_STEPS
                           for g in _XTERM_CLUT_88_STEPS
                           for b in _XTERM_CLUT_88_STEPS]))
_XTERM_CLUT_88.update(_NIX_SYSTEM_COLORS)

# xterm 256-color look-up table
_XTERM_CLUT_256_STEPS = [0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff]
_XTERM_CLUT_256 = dict(zip(range(16, 233),
                           [(r, g, b) for r in _XTERM_CLUT_256_STEPS
                            for g in _XTERM_CLUT_256_STEPS
                            for b in _XTERM_CLUT_256_STEPS]))
_XTERM_CLUT_256.update(_NIX_SYSTEM_COLORS)

###############################################################################


def color_difference(a, b):
    """Return the scalar difference between two colors."""
    return sum(abs(i - j) for i, j in zip(a, b))


def hls_to_rgb(h, l, s):
    """Convert HLS values to RGB."""
    return tuple(int(c * 255.) for c in colorsys.hls_to_rgb(h, l, s))


def hsv_to_rgb(h, s, v):
    """Convert HSV values to RGB."""
    return tuple(int(c * 255.) for c in colorsys.hsv_to_rgb(h/360.,
                                                            s/100.,
                                                            v/100.))


def match_color_formats(value):
    """Return the color format of the first format to match the given value."""
    # Use lazy generators to return the first matching format
    mapped = itertools.imap(lambda t: (t[0](value), t[1]), _FORMATS)

    return next(((v, colorspace) for v, colorspace in mapped if v),
                (None, None))


def closest_color(rgb, clut):
    """Return the key and value of closest RGB color in the given table."""
    key, value = min([(idx, color_difference(rgb, clut[idx]))
                      for idx in clut],
                     key=operator.itemgetter(1))

    return key, value


def set_num_colors(color_count):
    """Set the number of colors available instead of autodetecting it."""
    color_counts = frozenset([16, 88, 256, 2**24])
    color_names = frozenset(['truecolor', 'true-color', 'true_color'])

    if color_count not in color_counts and color_count not in color_names:
        raise ValueError("Invalid color count, use {0} or {1}"
                         .format(", ".join(map(str, color_counts)),
                                 ", ".join(color_names)))

    settings.__NUM_COLORS__ = 2**24 if color_count == 'true-color' else\
        color_count

# ttp://stackoverflow.com/questions/4431703/python-resettable-instance-method-memoization-decorator
# class memoize(object):
    # """Resettable function decorator for memoizing return values."""
    # class _memoize(dict):
        # def __init__(self, f):
            # self.f = f

        # def __call__(self, *args):
            # return self[args]

        # def __missing__(self, key):
            # ret = self[key] = self.f(*key)
            # return ret

    # return _memoize(f)


###############################################################################
# Windows color functions
###############################################################################
def set_windows_clut():
    """Set the internal Windows color look-up table."""
    if _WIN_CAN_GET_COLORS:
        # Windows Vista and beyond you can query the current colors in the
        # color table. On older platforms, use the default color table
        csbiex = CONSOLE_SCREEN_BUFFER_INFO_EX()
        windll.kernel32.GetConsoleScreenBufferInfoEx(
            colorise._color_manager._handle,
            ctypes.byref(csbiex)
        )

        # Update according to the currently set colors
        for i in range(16):
            _WINDOWS_CLUT[i] =\
                (windll.kernel32.GetRValue(csbiex.ColorTable[i]),
                    windll.kernel32.GetGValue(csbiex.ColorTable[i]),
                    windll.kernel32.GetBValue(csbiex.ColorTable[i]))

    # Create a mapping from windows colors to their logical names
    for color, name in zip(_WINDOWS_CLUT.values(),
                           _WINDOWS_LOGICAL_NAMES):
        _WINDOWS_LOGICAL_NAMES[color] = name


def win_get_num_colors():
    """Get the number of colors supported by the terminal."""
    if 'ConEmuANSI' in os.environ:
        # ConEmu console detected. It also supports 24-bit colors, but can
        # we detect this somehow?
        if os.environ['ConEmuANSI'] == 'ON':
            # ANSI escapes code are interpreted
            return 256
        else:
            return 16

    release = platform.win32_ver()[0]
    build = sys.getwindowsversion()[2]

    # Windows 10 build 14931 has support for 24-bit colors
    if release == '10' and build >= 14931:
        settings.__NUM_COLORS__ = 2**24
        return settings.__NUM_COLORS__

    # Supported colors in Windows are pre-determined. Though you can update
    # the colors in the color table on Vista and beyond, this also changes
    # all colors of text already in the console window
    settings.__NUM_COLORS__ = 16

    return 16


def win_get_color_from_name(name, isbg):
    """Return the color value and color count for a given color name."""
    if name not in _WINDOWS_LOGICAL_NAMES:
        raise ValueError("Unknown color name '{0}'".format(name))

    colors = win_get_num_colors()

    if colors > 256:
        # True-color
        return (_COLOR_PREFIX_BG_TRUE_COLOR if isbg else
                _COLOR_PREFIX_FG_TRUE_COLOR),\
            ';'.join(
                map(str,
                    _NIX_SYSTEM_COLORS[_NIX_SYSTEM_COLOR_NAMES[name]]))
    else:
        # We fall back on 16 color codes to maintain consistency
        return _COLOR_PREFIX_16,\
            _NIX_SYSTEM_COLOR_NAMES[name] + 30 + 10 * int(isbg)


def win_get_color(value, isbg):
    """Return an approximate color based on the terminal's capabilities."""
    match, colorspace = match_color_formats(value)

    if colorspace == 'name':
        # The color was given as text, e.g. 'red'
        return win_get_color_from_name(value, isbg)
    elif colorspace == 'index':
        return nix_get_color_from_index(value, isbg)
    elif colorspace == 'hex':
        value = match.group(2)
        r, g, b = [int(value[i:i+2], 16) for i in range(0, 6, 2)]
    elif colorspace == 'hsv':
        r, g, b = hsv_to_rgb(*map(float, match.group(2).split(',')))
    elif colorspace == 'hls':
        r, g, b = hls_to_rgb(*map(float, match.group(2).split(',')))
    elif colorspace == 'rgb':
        r, g, b = match.group(2).split(',')
    else:
        raise ValueError("Unknown color format '{0}'".format(value))

    colors = nix_get_num_colors()

    if colors > 256:
        return (_COLOR_PREFIX_BG_TRUE_COLOR if isbg else
                _COLOR_PREFIX_FG_TRUE_COLOR), ";".join(map(str, [r, g, b]))
    if colors > 88:
        prefix = _COLOR_PREFIX_256
        clut = _XTERM_CLUT_256
    elif colors > 8:
        prefix = _COLOR_PREFIX_88
        clut = _XTERM_CLUT_88
    else:
        prefix = _COLOR_PREFIX_16
        clut = _NIX_SYSTEM_COLORS

    key, _ = closest_color([r, g, b], clut)

    return prefix, key


def win_color_code(color, isbg):
    """Return the appropriate color code for a given color format."""
    if not color:
        return '', None

    return '', None


def win_set_logical_color(r, g, b):
    """Set a logical color name to a specific color on Windows.

    This changes all text in the console that already uses this logical
    name. E.g. if 'red' is mapped to the color red and this function
    changes it to another color, all text in red will be rendered with this
    new color, even though it may already have been written to the console.

    """
    pass


###############################################################################
# Nix color functions
###############################################################################
# NOTE: Can use TERM_PROGRAM/TERM_PROGRAM_VERSION to detect terminals
def nix_get_num_colors():
    """Get the number of colors supported by the terminal."""
    if settings.__NUM_COLORS__ > 0:
        return settings.__NUM_COLORS__

    # iTerm supports true-color from version 3 onward, earlier versions
    # supported 256 colors
    if os.environ.get('TERM_PROGRAM', '') == 'iTerm.app':
        version = os.environ.get('TERM_PROGRAM_VERSION', '')

        if version and int(version.split('.')[0]) > 2:
            settings.__NUM_COLORS__ = 2**24
        else:
            settings.__NUM_COLORS__ = 256

        return settings.__NUM_COLORS__

    # If all else fails, use curses
    curses.setupterm()
    settings.__NUM_COLORS__ = curses.tigetnum("colors")

    return settings.__NUM_COLORS__


def nix_get_color_from_name(name, isbg):
    """Return the color value and color count for a given color name."""
    if name not in _NIX_SYSTEM_COLOR_NAMES:
        raise ValueError("Unknown color name '{0}'".format(name))

    colors = nix_get_num_colors()

    if colors > 256:
        # True-color
        return (_COLOR_PREFIX_BG_TRUE_COLOR if isbg else
                _COLOR_PREFIX_FG_TRUE_COLOR),\
            ';'.join(
                map(str,
                    _NIX_SYSTEM_COLORS[_NIX_SYSTEM_COLOR_NAMES[name]]))
    else:
        # We fall back on 16 color codes to maintain consistency
        return _COLOR_PREFIX_16,\
            _NIX_SYSTEM_COLOR_NAMES[name] + 30 + 10 * int(isbg)


def nix_get_color_from_index(idx, isbg):
    """Return the color value and color count for a given color index."""
    idx = int(idx)

    if idx < 0 or idx > 256:
        raise ValueError("Color index must be in range [0-256]")

    colors = nix_get_num_colors()

    if colors > 88:
        # 256-color and true-color
        return _COLOR_PREFIX_256, idx
    elif colors > 8:
        if idx > 88:
            key, _ = closest_color(_XTERM_CLUT_256[idx], _XTERM_CLUT_88)
            return _COLOR_PREFIX_88, key
    else:
        if idx > 16:
            key, _ = closest_color(_XTERM_CLUT_256[idx],
                                   _NIX_SYSTEM_COLORS)
            return _COLOR_PREFIX_16, key + 30 + 10 * int(isbg)


def nix_get_color(value, isbg):
    """Return an approximate color based on the terminal's capabilities."""
    match, colorspace = match_color_formats(value)

    if colorspace == 'name':
        # The color was given as text, e.g. 'red'
        return nix_get_color_from_name(value, isbg)
    elif colorspace == 'index':
        return nix_get_color_from_index(value, isbg)
    elif colorspace == 'hex':
        value = match.group(2)
        r, g, b = [int(value[i:i+2], 16) for i in range(0, 6, 2)]
    elif colorspace == 'hsv':
        r, g, b = hsv_to_rgb(*map(float, match.group(2).split(',')))
    elif colorspace == 'hls':
        r, g, b = hls_to_rgb(*map(float, match.group(2).split(',')))
    elif colorspace == 'rgb':
        r, g, b = match.group(2).split(',')
    else:
        raise ValueError("Unknown color format '{0}'".format(value))

    colors = nix_get_num_colors()

    if colors > 256:
        return (_COLOR_PREFIX_BG_TRUE_COLOR if isbg else
                _COLOR_PREFIX_FG_TRUE_COLOR), ";".join(map(str, [r, g, b]))
    if colors > 88:
        prefix = _COLOR_PREFIX_256
        clut = _XTERM_CLUT_256
    elif colors > 8:
        prefix = _COLOR_PREFIX_88
        clut = _XTERM_CLUT_88
    else:
        prefix = _COLOR_PREFIX_16
        clut = _NIX_SYSTEM_COLORS

    key, _ = closest_color([r, g, b], clut)

    return prefix, key


def nix_color_code(color, isbg):
    """Return the appropriate color code for a given color format."""
    if not color:
        return '', None

    if color == 'reset':
        _COLOR_PREFIX_16, 39 + 10 * int(isbg)

    prefix, value = nix_get_color(color, isbg)

    return prefix, value


###############################################################################
# OS-dependent setup and color functions
###############################################################################
if 'windows' in colorise._SYSTEM_OS:
    from ctypes import windll, wintypes

    _WIN_CAN_GET_COLORS =\
        windll.kernel32.SetConsoleScreenBufferInfoEx is not None

    if _WIN_CAN_GET_COLORS:
        # Struct defined in 'wincon.h'
        class CONSOLE_SCREEN_BUFFER_INFO_EX(ctypes.Structure):
            _fields_ = [('cbSize',               wintypes.ULONG),
                        ('dwSize',               wintypes._COORD),
                        ('dwCursorPosition',     wintypes._COORD),
                        ('wAttributes',          ctypes.c_ushort),
                        ('srWindow',             wintypes._SMALL_RECT),
                        ('dwMaximumWindowSize',  wintypes._COORD),
                        ('wPopupAttributes',     wintypes.WORD),
                        ('bFullscreenSupported', wintypes.BOOL),
                        ('ColorTable',           wintypes.COLORREF * 16)]

        # Set correct parameter types and return type for 64-bit Windows
        windll.kernel32.GetConsoleScreenBufferInfoEx.argtypes =\
            [wintypes.HANDLE, ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFO_EX)]
        windll.kernel32.GetConsoleScreenBufferInfo.restype = wintypes.BOOL

    get_num_colors = win_get_num_colors
    get_color = win_get_color
    color_code = win_color_code
else:
    get_num_colors = nix_get_num_colors
    get_color = nix_get_color
    color_code = nix_color_code
