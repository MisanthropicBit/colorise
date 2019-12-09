#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Windows API functions."""

import ctypes
from ctypes import windll, wintypes, WinError
import os
import sys
from colorise.win.winhandle import WinHandle


# Invalid handle type for error checking
INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

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
    LPDWORD = ctypes.POINTER(wintypes.DWORD)
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
windll.kernel32.SetLastError.argtypes = [wintypes.DWORD]
windll.kernel32.SetLastError.restype = None  # void
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


def create_std_handle(handle_id):
    """Create a Windows standard handle from an identifier."""
    win_handle = WinHandle(windll.kernel32.GetStdHandle(handle_id))

    if win_handle.handle == INVALID_HANDLE_VALUE:
        raise WinError()

    csbi = CONSOLE_SCREEN_BUFFER_INFO()

    if windll.kernel32.GetConsoleScreenBufferInfo(
                win_handle.handle,
                ctypes.byref(csbi)) == 0:
        raise WinError()

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


def get_windows_clut():
    """Query and return the internal Windows color look-up table."""
    # On Windows Vista and beyond you can query the current colors in the
    # color table. On older platforms, use the default color table
    csbiex = CONSOLE_SCREEN_BUFFER_INFOEX()
    csbiex.cbSize = ctypes.sizeof(CONSOLE_SCREEN_BUFFER_INFOEX)

    if windll.kernel32.GetConsoleScreenBufferInfoEx(
                get_win_handle(sys.stdout).handle,
                ctypes.byref(csbiex)
            ) == 0:
        raise WinError()

    clut = {}

    # Update according to the currently set colors
    for i in range(16):
        clut[i] =\
            (csbiex.ColorTable[i] & 0xff,
             (csbiex.ColorTable[i] >> 8) & 0xff,
             (csbiex.ColorTable[i] >> 16) & 0xff)

    return clut


def enable_virtual_terminal_processing(handle):
    """Enable Windows processing of ANSI escape sequences."""
    if not handle or handle == INVALID_HANDLE_VALUE:
        raise ValueError('Invalid handle')

    console_mode = wintypes.DWORD(0)

    if windll.kernel32.GetConsoleMode(handle.handle,
                                      ctypes.byref(console_mode)) == 0:
        raise WinError()

    handle.console_mode = console_mode

    target_mode = wintypes.DWORD(console_mode.value |
                                 ENABLE_VIRTUAL_TERMINAL_PROCESSING |
                                 DISABLE_NEWLINE_AUTO_RETURN)

    # First attempt to set console mode to interpret ANSI escape codes and
    # disable immediately jumping to the next console line
    if windll.kernel32.SetConsoleMode(handle.handle, target_mode) == 0:
        # If that fails, try just setting the mode for ANSI escape codes
        target_mode = wintypes.DWORD(console_mode.value |
                                     ENABLE_VIRTUAL_TERMINAL_PROCESSING)

        if windll.kernel32.SetConsoleMode(handle.handle, target_mode) == 0:
            return None

    # Return the original console mode so we can restore it later
    return console_mode


def restore_console_mode(handle, restore_mode):
    """Restore the console mode for a handle to its original mode."""
    if not handle or handle == INVALID_HANDLE_VALUE:
        raise ValueError('Invalid handle')

    if not windll.kernel32.SetConsoleMode(handle.handle, restore_mode):
        raise WinError()


def restore_console_modes():
    """Restore console modes for stdout and stderr to their original mode."""
    if can_interpret_ansi():
        stdout = get_win_handle(sys.stdout)
        stderr = get_win_handle(sys.stderr)
        restore_console_mode(stdout, stdout.console_mode)
        restore_console_mode(stderr, stderr.console_mode)


_WIN_CAN_INTERPRET_ANSI_CODES =\
    enable_virtual_terminal_processing(_STDOUT_HANDLE) is not None

enable_virtual_terminal_processing(_STDERR_HANDLE)


def can_interpret_ansi():
    """Return True if the Windows console can interpret ANSI escape codes."""
    if os.environ.get('ConEmuANSI', '') == 'ON':
        return True

    return _WIN_CAN_INTERPRET_ANSI_CODES


def set_console_text_attribute(handle, flags):
    """Set the console's text attributes."""
    if not handle or handle == INVALID_HANDLE_VALUE:
        raise ValueError('Invalid handle')

    if windll.kernel32.SetConsoleTextAttribute(handle.handle,
                                               wintypes.WORD(flags)) == 0:
        raise WinError()


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

    if not all(0 <= c < 16 for c in color_map):
        raise RuntimeError('New color map must contain indices in range 0-15')

    # Create a new CONSOLE_SCREEN_BUFFER_INFOEX structure based on the given
    # color map
    csbiex = CONSOLE_SCREEN_BUFFER_INFOEX()

    # We must set the size of the structure before using it
    csbiex.cbSize = ctypes.sizeof(CONSOLE_SCREEN_BUFFER_INFOEX)

    win_handle = get_win_handle(file)

    # Get console color info
    if windll.kernel32.GetConsoleScreenBufferInfoEx(
                win_handle.handle,
                ctypes.byref(csbiex)
            ) == 0:
        raise WinError()

    # Redefine colortable
    for idx in color_map:
        csbiex.ColorTable[idx] = encode_rgb_tuple(color_map[idx])

    # Set the new colors
    if windll.kernel32.SetConsoleScreenBufferInfoEx(
            win_handle.handle, csbiex) == 0:
        raise WinError()
