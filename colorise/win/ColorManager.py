# -*- coding: utf-8 -*-

"""A Windows-specific console color manager class."""

import ctypes
from ctypes import windll, wintypes
import colorise
import colorise.decorators
from colorise.BaseColorManager import BaseColorManager

__date__ = '2014-05-12'  # YYYY-MM-DD


# Struct defined in wincon.h
class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [('dwSize', wintypes._COORD),
                ('dwCursorPosition', wintypes._COORD),
                ('wAttributes', ctypes.c_ushort),
                ('srWindow', wintypes._SMALL_RECT),
                ('dwMaximumWindowSize', wintypes._COORD)]


class WinHandle(object):

    """Represents a colored Windows stream handle."""

    def __init__(self, handle):
        self.handle = handle
        self.fg = 0
        self.bg = 0

    @property
    def wincolor(self):
        return self.fg | (self.bg << 4)

    @property
    def color(self):
        return (self.fg, self.bg, None)

    def __str__(self):
        return "{}, {}: {}".format(self.fg, self.bg, self.color)


@colorise.decorators.inherit_docstrings
class ColorManager(BaseColorManager):

    """Windows-specific console color manager class."""

    def __init__(self):
        # Fore- and background colors (wincon.h)
        self.fg_colors = dict(zip(['black', 'darkblue', 'darkgreen',
                                   'darkcyan', 'darkred', 'darkmagenta',
                                   'darkyellow', 'default'],
                                  range(8)))
        self.fg_colors.update(zip(['blue', 'green', 'cyan', 'red',
                                   'magenta', 'yellow', 'white'],
                                  range(9, 16)))

        # Support multiple spellings and color name aliases
        self.fg_colors['grey'] = 8
        self.fg_colors['gray'] = 8
        self.fg_colors['purple'] = 13
        self.fg_colors['darkpurple'] = 5
        self.fg_inv = dict(v: k for k, v in self.fg_colors.items())

        # Background colors (Also in wincon.h)
        self.bg_colors = self.fg_colors.copy()  # Swallow copy
        self.bg_inv = self.fg_inv.copy()

        # Handles 64-bit Python interpreters
        windll.kernel32.GetConsoleScreenBufferInfo.argtypes =\
            [wintypes.HANDLE,
             ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFO)]

        # Get handles (defined in winbase.h)
        INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
        self._handle = WinHandle(windll.kernel32.GetStdHandle(-11))

        if self._handle.handle == INVALID_HANDLE_VALUE:
            self._onerror(INVALID_HANDLE_VALUE)

        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        retval = windll.kernel32.GetConsoleScreenBufferInfo(
            self._handle.handle,
            ctypes.byref(csbi))

        if retval == 0:
            self._onerror(retval)

        # Set defaults color values
        self.default_fg = self.fg_inv[csbi.wAttributes & 0xf]
        self.default_bg = self.bg_inv[(csbi.wAttributes >> 4) & 0xf]

        # Set the color for the handle
        self._handle.fg = csbi.wAttributes & 0xf
        self._handle.bg = (csbi.wAttributes >> 4) & 0xf

    def _onerror(self, errorcode=None):
        errid = windll.kernel32.GetLastError()

        if errid == 0:
            LANG_NEUTRAL = 0x0
            SUBLANG_NEUTRAL = 0x0
            LANG_ENGLISH = 0x9
            SUBLANG_ENGLISH_US = 0x1
            # SYS_FLAG is a combination of:
            # FORMAT_MESSAGE_ALLOCATE_BUFFER,
            # FORMAT_MESSAGE_IGNORE_INSERTS and
            # FORMAT_MESSAGE_FROM_SYSTEM
            SYS_FLAG = 0x1300
            bufptr = wintypes.LPWSTR()

            # Format as english
            chars = windll.kernel32.FormatMessageW(SYS_FLAG, None, errid,
                                                   (LANG_ENGLISH & 0xff) |
                                                   (SUBLANG_ENGLISH_US & 0xff)
                                                   << 16,
                                                   ctypes.byref(bufptr),
                                                   0,
                                                   None)

            # If that fails, format in system neutral language
            if chars == 0:
                chars = windll.kernel32.FormatMessageW(SYS_FLAG, None, errid,
                                                       (LANG_NEUTRAL & 0xff) |
                                                       (SUBLANG_NEUTRAL & 0xff)
                                                       << 16,
                                                       ctypes.byref(bufptr),
                                                       0,
                                                       None)

            # Free the message buffer
            msg = bufptr.value[:chars]
            windll.kernel32.LocalFree(bufptr)

            if errorcode is None:
                raise OSError(msg)
            else:
                raise OSError(errorcode, msg)

    def set_defaults(self):
        self.set_color(self.default_fg,
                       self.default_bg)

    def get_defaults(self):
        return (self.default_fg, self.default_bg)

    def get_supported(self):
        return (list(self.fg_colors.keys()), list(self.bg_colors.keys()))

    def set_color(self, fg=None, bg=None):
        if fg:
            if fg not in self.fg_colors:
                raise ValueError("Unknown color '{}'".format(fg))

            self._handle.fg = self.fg_colors[fg]
        else:
            self._handle.fg = self.fg_colors[self.default_fg]

        if bg:
            if bg not in self.bg_colors:
                raise ValueError("Unknown color '{}'".format(bg))

            self._handle.bg = self.bg_colors[bg]
        else:
            self._handle.bg = self.bg_colors[self.default_bg]

        windll.kernel32.SetConsoleTextAttribute(self._handle.handle,
                                                self._handle.wincolor)
