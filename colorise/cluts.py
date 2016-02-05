#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note:
# All look-up tables presented here are entirely based on internet research, as
# it is impossible to ensure complete cross-platform support across all kinds
# of terminals. Therefore, there is no guarantee that any of these tables will
# be accurate.
#
# If you have suggestions, please do not hesitate to contact me :)

import operator
import colorise

try:
    import curses
except ImportError:
    pass


###############################################################################
# Windows color setup
###############################################################################

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
###############################################################################

# System base colors that are assumed to be present for 8 color terminals
_NIX_SYSTEM_COLORS = {
    0: (0x00, 0x00, 0x00), 1: (0x80, 0x00, 0x00), 2: (0x00, 0x80, 0x00),
    3: (0x80, 0x80, 0x00), 4: (0x00, 0x00, 0x80), 5: (0x80, 0x00, 0x80),
    6: (0x00, 0x80, 0x80), 7: (0xc0, 0xc0, 0xc0), 8: (0x80, 0x80, 0x80),
    9: (0xff, 0x00, 0x00), 10: (0x00, 0xff, 0x00), 11: (0xff, 0xff, 0x00),
    12: (0x00, 0x00, 0xff), 13: (0xff, 0x00, 0xff), 14: (0x00, 0xff, 0xff),
    15: (0xff, 0xff, 0xff)
}

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


def color_difference(a, b):
    """Return the scalar difference between two colors."""
    return sum(abs(i - j) for i, j in zip(a, b))


###############################################################################
# Global color query function setup depending on OS
###############################################################################
if 'windows' in colorise._SYSTEM_OS:
    import ctypes
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
    def get_num_colors():
        """Get the number of colors supported by the terminal."""
        # TODO: Do a check to avoid reinitialisation?
        curses.setupterm()
        return curses.tigetnum("colors")

    def get_approx_color(r, g, b):
        """Return an approximate color based on the terminal's capabilities."""
        colors = get_num_colors()

        if colors == 256:
            clut = _XTERM_CLUT_256
        elif colors == 88:
            clut = _XTERM_CLUT_88
        else:
            clut = _NIX_SYSTEM_COLORS

        j = min(enumerate([color_difference((r, g, b), clut[i])
                           for i in range(len(clut))]),
                key=operator.itemgetter(1))[0]

        return j, clut[j]
