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
import re

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
_TRUE_COLOR_RE = re.compile('^true[ -_]?color$')

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
_COLOR_PREFIX_TRUE_COLOR = _COLOR_ESCAPE_CODE + '38;2;{0}m'


###############################################################################
# Color look-up tables
###############################################################################
# User-defined color count (always ignored on Windows as it only ever
# has 16 colors)
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
_windows_logical_names = ['black', 'darkblue', 'darkgreen', 'darkcyan',
                          'darkred', 'magenta', 'yellow', 'white', 'gray',
                          'blue', 'green', 'cyan', 'red', 'purple', 'yellow',
                          'white']

# Mapping from colors in _WINDOWS_CLUT to logical color names
# (see set_windows_clut below)
_WINDOWS_LOGICAL_NAMES = {}


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
    mapped = itertools.imap(lambda f, cs: (f(value), cs), _FORMATS)

    return next(((v, colorspace) for m, colorspace in mapped if v), None)

###############################################################################
# Global OS-dependent setup and color functions
###############################################################################
if 'windows' in colorise._SYSTEM_OS:
    from ctypes import windll, wintypes

    _WIN_CAN_GET_COLORS =\
        windll.kernel32.SetConsoleScreenBufferInfoEx is not None

    if _WIN_CAN_GET_COLORS:
        # Struct defined in 'wincon.h'
        class CONSOLE_SCREEN_BUFFER_INFO_EX(ctypes.Structure):
            _fields_ = [('cbSize', wintypes.ULONG),
                        ('dwSize', wintypes._COORD),
                        ('dwCursorPosition', wintypes._COORD),
                        ('wAttributes', ctypes.c_ushort),
                        ('srWindow', wintypes._SMALL_RECT),
                        ('dwMaximumWindowSize', wintypes._COORD),
                        ('wPopupAttributes', wintypes.WORD),
                        ('bFullscreenSupported', wintypes.BOOL),
                        ('ColorTable', wintypes.COLORREF * 16)]

        # Set correct parameter types and return type for 64-bit Windows
        windll.kernel32.GetConsoleScreenBufferInfoEx.argtypes =\
            [wintypes.HANDLE, ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFO_EX)]
        windll.kernel32.GetConsoleScreenBufferInfo.restype = wintypes.BOOL

    def set_windows_clut():
        """Set the internal Windows color look-up table."""
        if _WIN_CAN_GET_COLORS:
            # Windows Vista and beyond you can query the current colors in the
            # color table. On older platforms, use the default color table
            csbiex = CONSOLE_SCREEN_BUFFER_INFO_EX()
            windll.kernel32.GetConsoleScreenBufferInfoEx(self._handle,
                                                         ctypes.byref(csbiex))

            # Update according to the currently set colors
            for i in range(16):
                _WINDOWS_CLUT[i] =\
                    (windll.kernel32.GetRValue(csbiex.ColorTable[i]),
                     windll.kernel32.GetGValue(csbiex.ColorTable[i]),
                     windll.kernel32.GetBValue(csbiex.ColorTable[i]))

        # Create a mapping from windows colors to their logical names
        for color, name in zip(_WINDOWS_CLUT.values(),
                               _windows_logical_names):
            _WINDOWS_LOGICAL_NAMES[color] = name

    def get_num_colors():
        """Get the number of colors supported by the terminal."""
        # Supported colors in Windows are pre-determined. Though you can update
        # the colors in the color table on Vista and beyond, this also changes
        # all colors of text already in the console window
        return 16

    def get_approx_color(r, g, b):
        """Return an approximate color based on the terminal's capabilities."""
        j = min(enumerate([color_difference((r, g, b), clut_color)
                           for _, clut_color in _WINDOWS_CLUT]),
                key=operator.itemgetter(1))[0]

        return j, _WINDOWS_CLUT[j]

    def set_logical_color(r, g, b):
        """Set a logical color name to a specific color on Windows.

        This changes all text in the console that already uses this logical
        name. E.g. if 'red' is mapped to the color red and this function
        changes it to another color, all text in red will be rendered with this
        new color, even though it may already have been written to the console.

        """
        pass
else:
    def set_num_colors(color_count):
        """Set the number of colors available instead of autodetecting it."""
        color_counts = frozenset([16, 88, 256, 2**24])
        color_names = frozenset(['true-color'])

        if color_count not in color_counts and not\
                _TRUE_COLOR_RE.match(color_count):
            raise ValueError("Invalid color count, use {0} or {1}"
                             .format(", ".join(map(str, color_counts)),
                                     ", ".join(color_names)))

        # TODO: Find an alternative to globals
        global __NUM_COLORS__
        __NUM_COLORS__ = 2**24 if color_count == 'true-color' else\
            color_count

    # NOTE: Can use TERM_PROGRAM/TERM_PROGRAM_VERSION to detect terminals
    def get_num_colors():
        """Get the number of colors supported by the terminal."""
        if __NUM_COLORS__ > 0:
            return __NUM_COLORS__

        # TODO: Do a check to avoid reinitialisation?
        curses.setupterm()
        return curses.tigetnum("colors")

    def closest_color(rgb, clut):
        """Return the key and value of closest RGB color in the given table."""
        key, value = min([(idx, color_difference(rgb, clut[idx]))
                          for idx in clut],
                         key=operator.itemgetter(1))

        return key, value

    def get_color_from_name(name, isbg):
        """Return the color value and color count for a given color name."""
        if name not in _NIX_SYSTEM_COLOR_NAMES:
            raise ValueError("Unknown color name '{0}'".format(name))

        colors = get_num_colors()

        if colors > 256:
            # True-color
            return _COLOR_PREFIX_TRUE_COLOR,\
                ';'.join(
                    map(str,
                        _NIX_SYSTEM_COLORS[_NIX_SYSTEM_COLOR_NAMES[name]]))
        else:
            # We fall back on 16 color codes to maintain consistency
            return _COLOR_PREFIX_16,\
                _NIX_SYSTEM_COLOR_NAMES[name] + 30 + 10 * int(isbg)

    def get_color_from_index(idx, isbg):
        """Return the color value and color count for a given color index."""
        idx = int(idx)

        if idx < 0 or idx > 256:
            raise ValueError("Color index must be in range [0-256]")

        colors = get_num_colors()

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

    def get_color(value, isbg):
        """Return an approximate color based on the terminal's capabilities."""
        match, colorspace = match_color_formats(value)

        if colorspace == 'name':
            # The color was given as text, e.g. 'red'
            return get_color_from_name(value, isbg)
        elif colorspace == 'index':
            return get_color_from_index(value, isbg)
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

        colors = get_num_colors()

        if colors > 256:
            return _COLOR_PREFIX_TRUE_COLOR, ";".join(map(str, [r, g, b]))
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

    def color_code(color, isbg):
        """Return the appropriate color code for a given color format."""
        if not color:
            return '', None

        # colorspace = get_color_format(color)
        prefix, value = get_color(color, isbg)

        return prefix, value
