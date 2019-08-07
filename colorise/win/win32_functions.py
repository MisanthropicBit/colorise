#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Windows API functions."""

import colorise
import ctypes
from ctypes import windll, wintypes
import sys


# Invalid handle type for error checking
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

# Handle IDs for stdout and stderr
_STDOUT_HANDLE_ID = -11
_STDERR_HANDLE_ID = -12

# Console modes for console virtual terminal sequences
DISABLE_NEWLINE_AUTO_RETURN = 0x0008
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004


# Struct defined in wincon.h
class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [('dwSize',              wintypes._COORD),
                ('dwCursorPosition',    wintypes._COORD),
                ('wAttributes',         ctypes.c_ushort),
                ('srWindow',            wintypes._SMALL_RECT),
                ('dwMaximumWindowSize', wintypes._COORD)]


# Struct defined in wincon.h
class CONSOLE_SCREEN_BUFFER_INFOEX(ctypes.Structure):
    _fields_ = [('cbSize',               wintypes.ULONG),
                ('dwSize',               wintypes._COORD),
                ('dwCursorPosition',     wintypes._COORD),
                ('wAttributes',          ctypes.c_ushort),
                ('srWindow',             wintypes._SMALL_RECT),
                ('dwMaximumWindowSize',  wintypes._COORD),
                ('wPopupAttributes',     wintypes.WORD),
                ('bFullscreenSupported', wintypes.BOOL),
                ('ColorTable',           wintypes.COLORREF * 16)]

if not hasattr(wintypes, 'LPDWORD'):
    LPDWORD = wintypes.POINTER(wintypes.DWORD)
else:
    LPDWORD = wintypes.LPDWORD

# Set argument and return types for Windows API calls
windll.kernel32.GetConsoleScreenBufferInfo.argtypes =\
    [wintypes.HANDLE, ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFO)]
windll.kernel32.GetConsoleScreenBufferInfo.restype = wintypes.BOOL
windll.kernel32.GetStdHandle.argtypes = [wintypes.DWORD]
windll.kernel32.GetStdHandle.restype = wintypes.HANDLE
windll.kernel32.GetConsoleMode.argtypes = [wintypes.HANDLE, LPDWORD]
windll.kernel32.GetConsoleMode.restype = wintypes.BOOL
windll.kernel32.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
windll.kernel32.SetConsoleMode.restype = wintypes.BOOL
windll.kernel32.GetLastError.argtypes = []
windll.kernel32.GetLastError.restype = wintypes.DWORD
windll.kernel32.FormatMessageW.argtypes = [wintypes.DWORD,
                                           wintypes.LPCVOID,
                                           wintypes.DWORD,
                                           wintypes.DWORD,
                                           wintypes.LPWSTR,
                                           wintypes.DWORD,
                                           wintypes.LPVOID]
windll.kernel32.FormatMessageW.restype = wintypes.DWORD
windll.kernel32.LocalFree.argtypes = [wintypes.HLOCAL]
windll.kernel32.LocalFree.restype = wintypes.HLOCAL
windll.kernel32.SetConsoleTextAttribute.argtypes = [wintypes.HANDLE,
                                                    wintypes.WORD]
windll.kernel32.SetConsoleTextAttribute.restype = wintypes.BOOL


def can_redefine_colors():
    """Return whether the terminal allows redefinition of colors."""
    return windll.kernel32.SetConsoleScreenBufferInfoEx is not None


if can_redefine_colors():
    # We can query RGB values of console colors on Windows
    windll.kernel32.GetConsoleScreenBufferInfoEx.argtypes =\
        [wintypes.HANDLE, ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFOEX)]
    windll.kernel32.GetConsoleScreenBufferInfoEx.restype = wintypes.BOOL


class WinHandle(object):

    """Represents a Windows stream handle."""

    def __init__(self, handle):
        """Initialise the Windows handle."""
        self._handle = handle
        self.fg = 0
        self.bg = 0

    @property
    def handle(self):
        """Return the internal Windows handle."""
        return self._handle

    @property
    def fg(self):
        """Return the current foreground color set for the handle."""
        return self._fg

    @fg.setter
    def fg(self, value):
        self._fg = value

    @property
    def bg(self):
        """Return the current background color set for the handle."""
        return self._bg

    @bg.setter
    def bg(self, value):
        self._bg = value

    @property
    def default_fg(self):
        """Return the default foreground color set for the handle."""
        return self._default_fg

    @default_fg.setter
    def default_fg(self, value):
        self._default_fg = value

    @property
    def default_bg(self):
        """Return the default background color set for the handle."""
        return self._default_bg

    @default_bg.setter
    def default_bg(self, value):
        self._default_bg = value

    def __str__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__,
                                      self.fg, self.bg)


def raise_win_error(error_code=None):
    """Format and raise a Windows specific error."""
    err_id = windll.kernel32.GetLastError()

    if err_id == 0:
        LANG_NEUTRAL = 0x0
        SUBLANG_NEUTRAL = 0x0
        LANG_ENGLISH = 0x9
        SUBLANG_ENGLISH_US = 0x1

        # SYS_FLAG is a combination of:
        # FORMAT_MESSAGE_ALLOCATE_BUFFER, FORMAT_MESSAGE_IGNORE_INSERTS and
        # FORMAT_MESSAGE_FROM_SYSTEM
        SYS_FLAG = 0x1300

        bufptr = wintypes.LPWSTR()

        # Format as english
        chars = windll.kernel32.FormatMessageW(
                SYS_FLAG,
                None,
                err_id,
                (LANG_ENGLISH & 0xff) | (SUBLANG_ENGLISH_US & 0xff) << 16,
                ctypes.byref(bufptr),
                0,
                None
            )

        # If english formatting fails, format in system neutral language
        if chars == 0:
            chars = windll.kernel32.FormatMessageW(
                    SYS_FLAG,
                    None,
                    err_id,
                    (LANG_NEUTRAL & 0xff) | (SUBLANG_NEUTRAL & 0xff) << 16,
                    ctypes.byref(bufptr),
                    0,
                    None
                )

        # Free the message buffer
        msg = bufptr.value[:chars]
        windll.kernel32.LocalFree(bufptr)

        if error_code:
            raise WindowsError(error_code, msg)
        else:
            raise WindowsError(msg)


def create_std_handle(handle_id):
    """Create a Windows standard handle from an identifier."""
    win_handle = WinHandle(windll.kernel32.GetStdHandle(handle_id))

    if win_handle == INVALID_HANDLE_VALUE:
        colorise.win.cluts.raise_win_error(INVALID_HANDLE_VALUE)

    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    retval = windll.kernel32.GetConsoleScreenBufferInfo(
            win_handle.handle,
            ctypes.byref(csbi)
        )

    if retval == 0:
        colorise.win.cluts.raise_win_error(retval)

    # Set defaults color values
    # TODO: Do these need to be reread when colors are redefined?
    win_handle.default_fg = csbi.wAttributes & 0xf
    win_handle.default_bg = (csbi.wAttributes >> 4) & 0xf

    # Set the color for the handle
    win_handle.fg = win_handle.default_fg
    win_handle.bg = win_handle.default_bg

    return win_handle


# Create handles for stdout and stderr
_STDOUT_HANDLE = create_std_handle(-11)
_STDERR_HANDLE = create_std_handle(-12)


def get_win_handle(target):
    """Return the Windows handle corresponding to a Python handle."""
    if target is sys.stdout:
        return _STDOUT_HANDLE
    elif target is sys.stderr:
        return _STDERR_HANDLE

    raise ValueError('Only stdout and stderr supported')


def set_windows_clut():
    """Set the internal Windows color look-up table."""
    if can_redefine_colors():
        # On Windows Vista and beyond you can query the current colors in the
        # color table. On older platforms, use the default color table
        csbiex = CONSOLE_SCREEN_BUFFER_INFOEX()

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


def enable_virtual_terminal_processing(handle):
    """Enable Windows processing of ANSI escape sequences."""
    if not handle or handle == INVALID_HANDLE_VALUE:
        raise ValueError('Invalid handle')

    console_mode = wintypes.DWORD(0)

    if not windll.kernel32.GetConsoleMode(handle.handle,
                                          ctypes.byref(console_mode)):
        raise_win_error()

    target_mode = wintypes.DWORD(console_mode.value |
                                 ENABLE_VIRTUAL_TERMINAL_PROCESSING |
                                 DISABLE_NEWLINE_AUTO_RETURN)

    # First attempt to set console mode to interpret ANSI escape codes and
    # disable immediately jumping to the next console line
    if not windll.kernel32.SetConsoleMode(handle.handle, target_mode):
        # If that fails, try just setting the mode for ANSI escape codes
        target_mode = wintypes.DWORD(console_mode.value |
                                     ENABLE_VIRTUAL_TERMINAL_PROCESSING)

        if not windll.kernel32.SetConsoleMode(handle.handle, target_mode):
            return None

    # Return the original console mode so we can restore it later
    return console_mode


def restore_console_mode(handle, restore_mode):
    """Restore the console mode for a handle to its original mode."""
    if not handle or handle == INVALID_HANDLE_VALUE:
        raise ValueError('Invalid handle')

    if not windll.kernel32.SetConsoleMode(handle.handle, restore_mode):
        raise_win_error()


_WIN_CAN_INTERPRET_ANSI_CODES =\
    enable_virtual_terminal_processing(_STDOUT_HANDLE) is not None


def can_interpret_ansi():
    """Return True if the Windows console can interpret ANSI escape codes."""
    return _WIN_CAN_INTERPRET_ANSI_CODES


def set_console_text_attribute(handle, flags):
    """Set the console's text attributes."""
    if not handle or handle == INVALID_HANDLE_VALUE:
        raise ValueError('Invalid handle')

    if not windll.kernel32.SetConsoleTextAttribute(handle.handle,
                                                   wintypes.WORD(flags)):
        raise_win_error()


def encode_rgb_tuple(rgb):
    """Hexadecimally encode an rgb tuple as 0xbbggrr."""
    r, g, b = rgb

    return (b << 16) | (g << 8) | r


def redefine_colors(color_map, file=sys.stdout):
    """Redefine the base console colors with a new mapping.

    This only redefines the 8 colors in the console and changes all text in the
    console that already uses the logical names. E.g. if 'red' is mapped to the
    color red and this function changes it to another color, all text in 'red'
    will be rendered with this new color, even though it may already have been
    written to the console.

    """
    if not can_redefine_colors():
        raise RuntimeError('Cannot redefine colors on this system')

    if not all(c >= 0 and c < 16 for c in color_map):
        raise RuntimeError('New color map must contain indices in range 0-15')

    # Create a new CONSOLE_SCREEN_BUFFER_INFOEX structure based on the given
    # color map
    #
    # TODO: Check if allocation succeeds?
    csbiex = colorise.win.cluts.CONSOLE_SCREEN_BUFFER_INFOEX()

    win_handle = get_win_handle(file)

    # Get console color info
    windll.kernel32.GetConsoleScreenBufferInfoEx(
            win_handle,
            ctypes.byref(csbiex)
        )

    # Redefine colors
    for idx, color in color_map:
        csbiex.ColorTable[idx] = encode_rgb_tuple(color)

    # Set the new colors
    if not windll.kernel32.SetConsoleScreenBufferInfoEx(
                win_handle.handle, csbiex):
        raise_win_error()
