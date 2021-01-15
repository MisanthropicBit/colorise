#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Windows API functions."""

import ctypes
from ctypes import wintypes, WinError
import os
import sys
from colorise.win.winhandle import WinHandle

# Create a separate WinDLL instance since the one from ctypes.windll.kernel32
# can be manipulated by other code that also imports it
#
# See
# https://stackoverflow.com/questions/34040123/ctypes-cannot-import-windll#comment55835311_34040124
kernel32 = ctypes.WinDLL('kernel32', use_errno=True, use_last_error=True)

# Handle IDs for stdout and stderr
_STDOUT_HANDLE_ID = -11
_STDERR_HANDLE_ID = -12

# Console modes for console virtual terminal sequences
DISABLE_NEWLINE_AUTO_RETURN = 0x0008
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

ERROR_INVALID_HANDLE = 6


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
kernel32.GetConsoleScreenBufferInfo.argtypes =\
    [wintypes.HANDLE, ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFO)]
kernel32.GetConsoleScreenBufferInfo.restype = wintypes.BOOL
kernel32.GetStdHandle.argtypes = [wintypes.DWORD]
kernel32.GetStdHandle.restype = wintypes.HANDLE
kernel32.GetConsoleMode.argtypes = [wintypes.HANDLE, LPDWORD]
kernel32.GetConsoleMode.restype = wintypes.BOOL
kernel32.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
kernel32.SetConsoleMode.restype = wintypes.BOOL
kernel32.GetLastError.argtypes = []
kernel32.GetLastError.restype = wintypes.DWORD
kernel32.SetLastError.argtypes = [wintypes.DWORD]
kernel32.SetLastError.restype = None  # void
kernel32.FormatMessageW.argtypes = [wintypes.DWORD,
                                           wintypes.LPCVOID,
                                           wintypes.DWORD,
                                           wintypes.DWORD,
                                           wintypes.LPWSTR,
                                           wintypes.DWORD,
                                           wintypes.LPVOID]
kernel32.FormatMessageW.restype = wintypes.DWORD
kernel32.LocalFree.argtypes = [wintypes.HLOCAL]
kernel32.LocalFree.restype = wintypes.HLOCAL
kernel32.SetConsoleTextAttribute.argtypes = [wintypes.HANDLE,
                                                    wintypes.WORD]
kernel32.SetConsoleTextAttribute.restype = wintypes.BOOL

if kernel32.SetConsoleScreenBufferInfoEx is not None:
    # We can query RGB values of console colors on Windows
    kernel32.GetConsoleScreenBufferInfoEx.argtypes =\
        [wintypes.HANDLE, ctypes.POINTER(CONSOLE_SCREEN_BUFFER_INFOEX)]
    kernel32.GetConsoleScreenBufferInfoEx.restype = wintypes.BOOL


def isatty(handle):
    """Check if a handle is a valid console handle.

    For example, if a handle is redirected to a file, it is not a valid console
    handle and all win32 console API calls will fail.

    """
    if not handle or not handle.valid:
        return False

    console_mode = wintypes.DWORD(0)

    # We use GetConsoleMode here but it could be any function that expects a
    # valid console handle
    retval = kernel32.GetConsoleMode(handle.value, ctypes.byref(console_mode))

    if retval == 0:
        errno = ctypes.get_last_error()

        if errno == ERROR_INVALID_HANDLE:
            return False
        else:
            # Another error happened
            raise WinError()
    else:
        return True


def can_redefine_colors(file):
    """Return whether the terminal allows redefinition of colors."""
    handle = get_win_handle(WinHandle.from_sys_handle(file))

    return kernel32.SetConsoleScreenBufferInfoEx is not None and isatty(handle)


def create_std_handle(handle_id):
    """Create a Windows standard handle from an identifier."""
    handle = kernel32.GetStdHandle(handle_id)

    if handle == WinHandle.INVALID:
        raise WinError()

    csbi = CONSOLE_SCREEN_BUFFER_INFO()

    retval = kernel32.GetConsoleScreenBufferInfo(
        handle,
        ctypes.byref(csbi),
    )
    win_handle = None

    if retval == 0:
        errno = ctypes.get_last_error()

        if errno == ERROR_INVALID_HANDLE:
            # Return a special non-console handle
            win_handle = WinHandle.get_nonconsole_handle(handle_id)
        else:
            raise WinError()
    else:
        win_handle = WinHandle(handle)

        # Set defaults color values
        # TODO: Do these need to be reread when colors are redefined?
        win_handle.default_fg = csbi.wAttributes & 0xf
        win_handle.default_bg = (csbi.wAttributes >> 4) & 0xf

    # Set the color for the handle
    win_handle.fg = win_handle.default_fg
    win_handle.bg = win_handle.default_bg

    return win_handle


# Create handles for stdout and stderr
# _STDOUT_HANDLE = create_std_handle(_STDOUT_HANDLE_ID)
# _STDERR_HANDLE = create_std_handle(_STDERR_HANDLE_ID)


def get_win_handle(target):
    """Return the Windows handle corresponding to a Python handle."""
    if WinHandle.validate(target):
        # We create a new handle each time since the old handle may have been
        # invalidated by a redirection
        return create_std_handle(target)

    raise ValueError("Invalid handle identifier '{0}'".format(target))


def get_windows_clut():
    """Query and return the internal Windows color look-up table."""
    # On Windows Vista and beyond you can query the current colors in the
    # color table. On older platforms, use the default color table
    csbiex = CONSOLE_SCREEN_BUFFER_INFOEX()
    csbiex.cbSize = ctypes.sizeof(CONSOLE_SCREEN_BUFFER_INFOEX)

    if kernel32.GetConsoleScreenBufferInfoEx(
                get_win_handle(WinHandle.STDOUT).value,
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
    if not handle or not handle.valid:
        raise ValueError('Invalid handle')

    if not isatty(handle):
        return False

    console_mode = wintypes.DWORD(0)

    if kernel32.GetConsoleMode(handle.value, ctypes.byref(console_mode)) == 0:
        raise WinError()

    handle.console_mode = console_mode

    target_mode = wintypes.DWORD(console_mode.value |
                                 ENABLE_VIRTUAL_TERMINAL_PROCESSING |
                                 DISABLE_NEWLINE_AUTO_RETURN)

    # First attempt to set console mode to interpret ANSI escape codes and
    # disable immediately jumping to the next console line
    if kernel32.SetConsoleMode(handle.value, target_mode) == 0:
        # If that fails, try just setting the mode for ANSI escape codes
        target_mode = wintypes.DWORD(console_mode.value |
                                     ENABLE_VIRTUAL_TERMINAL_PROCESSING)

        if kernel32.SetConsoleMode(handle.value, target_mode) == 0:
            return None

    # Return the original console mode so we can restore it later
    return console_mode


def restore_console_mode(handle, restore_mode):
    """Restore the console mode for a handle to its original mode."""
    if not handle or handle == WinHandle.INVALID:
        raise ValueError('Invalid handle')

    if not kernel32.SetConsoleMode(handle.value, restore_mode):
        raise WinError()


def restore_console_modes():
    """Restore console modes for stdout and stderr to their original mode."""
    if can_interpret_ansi(sys.stdout):
        stdout = get_win_handle(WinHandle.STDOUT)
        restore_console_mode(stdout, stdout.console_mode)

    if can_interpret_ansi(sys.stderr):
        stderr = get_win_handle(WinHandle.STDERR)
        restore_console_mode(stderr, stderr.console_mode)


def can_interpret_ansi(file):
    """Return True if the Windows console can interpret ANSI escape codes."""
    # NOTE: Not sure if sys.stdout and sys.stderr are synced with the handles
    # returned by GetStdHandle so we use existing windows functions to tell if
    # the handles are valid console handles
    handle = get_win_handle(WinHandle.from_sys_handle(file))
    handle_isatty = isatty(handle)

    if not handle_isatty:
        return False

    if os.environ.get('ConEmuANSI', '') == 'ON':
        return True

    return enable_virtual_terminal_processing(handle)


def set_console_text_attribute(handle, flags):
    """Set the console's text attributes."""
    if not handle or handle == WinHandle.INVALID:
        raise ValueError('Invalid handle')

    if kernel32.SetConsoleTextAttribute(handle.value,
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
    if not can_redefine_colors(file):
        raise RuntimeError('Cannot redefine colors on this system')

    if not all(0 <= c < 16 for c in color_map):
        raise RuntimeError('New color map must contain indices in range 0-15')

    # Create a new CONSOLE_SCREEN_BUFFER_INFOEX structure based on the given
    # color map
    csbiex = CONSOLE_SCREEN_BUFFER_INFOEX()

    # We must set the size of the structure before using it
    csbiex.cbSize = ctypes.sizeof(CONSOLE_SCREEN_BUFFER_INFOEX)

    win_handle = get_win_handle(WinHandle.from_sys_handle(file))

    # Get console color info
    if kernel32.GetConsoleScreenBufferInfoEx(
                win_handle.value,
                ctypes.byref(csbiex)
            ) == 0:
        raise WinError()

    # Redefine colortable
    for idx in color_map:
        csbiex.ColorTable[idx] = encode_rgb_tuple(color_map[idx])

    # Set the new colors
    if kernel32.SetConsoleScreenBufferInfoEx(win_handle.value, csbiex) == 0:
        raise WinError()
