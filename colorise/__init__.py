# -*- coding: utf-8 -*-

"""colorise v0.1.0.

A module for printing colored text to the console. Has support for
custom color format syntax and includes some useful utility functions.

"""

from __future__ import print_function

__author__ = 'Alexander Bock'
__version__ = '0.1.0'
__license__ = 'MIT'
__date__ = '2014-05-08'  # YYYY-MM-DD
__all__ = ['set_color', 'cprint', 'fprint', 'formatcolor', 'formatbyindex',
           'highlight']

import sys
import atexit
import platform
import operator
import itertools

_PY2 = sys.version_info[0] < 3
_DEBUG_MODE = False
_SYSTEM_OS = platform.system().lower()

from colorise.ColorFormatParser import ColorFormatParser


if _DEBUG_MODE:
    print("Python " + ".".join(map(str, sys.version_info[:3])))

    def _32or64bit():  # Note: The sys.maxsize tests only works for Python 2.6+
        """Determine if the OS is using a 32- or 64-bit architecture."""
        import struct
        return 8*struct.calcsize('P')


# Determine which platform-specific color manager to import
if _SYSTEM_OS.startswith('win'):
    from colorise.win.ColorManager import ColorManager

    if _DEBUG_MODE:
        print("{} {} ({}-bit)".format(platform.system(),
                                      platform.release(),
                                      _32or64bit()))
else:
    # Assume nix platform
    from colorise.nix.ColorManager import ColorManager

    if _DEBUG_MODE:
        if sys.version_info[:2] < (2, 6):
            dist = platform.dist()
        else:
            dist = platform.linux_distribution()

        print("Distribution details: {}, {}, {} ({}-bit)"
              .format(dist + (_32or64bit())))


# Global, "private" objects, don't use
_color_format_parser = ColorFormatParser()
_color_manager = ColorManager()


def set_color(fg=None, bg=None):
    """Set the current colors.

    If no arguments are given, sets default colors.

    """
    if fg or bg:
        _color_manager.set_color(fg, bg)
    else:
        _color_manager.set_defaults()


def cprint(string, fg=None, bg=None, end='\n', target=sys.stdout):
    """Print a colored string to the target handle.

    fg and bg specify foreground- and background colors, respectively. The
    remaining keyword arguments are the same as for Python's built-in print
    function. Colors are returned to their defaults before the function
    returns.

    """
    _color_manager.set_color(fg, bg)
    target.write(string + end)
    target.flush()  # Needed for Python 3.x
    _color_manager.set_defaults()


def fprint(fmt, *args, **kwargs):
    """Parse and print a colored and perhaps formatted string.

    The remaining keyword arguments are the same as for Python's built-in print
    function. Colors are returning to their defaults before the function
    returns.

    """
    if not fmt:
        return

    hascolor = False
    target = kwargs.get("target", sys.stdout)

    # Format the string before feeding it to the parser
    fmt = fmt.format(*args, **kwargs)

    for txt, markups in _color_format_parser.parse(fmt):
        if markups != (None, None):
            _color_manager.set_color(*markups)
            hascolor = True
        else:
            if hascolor:
                _color_manager.set_defaults()
                hascolor = False

        target.write(txt)
        target.flush()  # Needed for Python 3.x

    _color_manager.set_defaults()
    target.write(kwargs.get('end', '\n'))
    _color_manager.set_defaults()


def formatcolor(string, fg=None, bg=None):
    """Wrap color syntax around a string and return it.

    fg and bg specify foreground- and background colors, respectively.

    """
    if fg is bg is None:
        return string

    temp = (['fg='+fg] if fg else []) +\
           (['bg='+bg] if bg else [])
    fmt = _color_format_parser._COLOR_DELIM.join(temp)

    return _color_format_parser._START_TOKEN + fmt +\
        _color_format_parser._FMT_TOKEN + string +\
        _color_format_parser._STOP_TOKEN


def formatbyindex(string, fg=None, bg=None, indices=[]):
    """Wrap color syntax around characters using indices and return it.

    fg and bg specify foreground- and background colors, respectively.

    """
    if not string or not indices or (fg is bg is None):
        return string

    result, p = '', 0

    # The lambda syntax is necessary to support both Python 2 and 3
    for k, g in itertools.groupby(enumerate(sorted(indices)),
                                  lambda x: x[0]-x[1]):
        tmp = list(map(operator.itemgetter(1), g))
        s, e = tmp[0], tmp[-1]+1

        if s < len(string):
            result += string[p:s]
            result += formatcolor(string[s:e], fg, bg)
            p = e

    if p < len(string):
        result += string[p:]

    return result


def highlight(string, fg=None, bg=None, indices=[], end='\n',
              target=sys.stdout):
    """Highlight characters using indices and print it to the target handle.

    fg and bg specify foreground- and background colors, respectively. The
    remaining keyword arguments are the same as for Python's built-in print
    function.

    """
    if not string or not indices or (fg is bg is None):
        return

    p = 0

    # The lambda syntax is necessary to support both Python 2 and 3
    for k, g in itertools.groupby(enumerate(sorted(indices)),
                                  lambda x: x[0]-x[1]):
        tmp = list(map(operator.itemgetter(1), g))
        s, e = tmp[0], tmp[-1]+1
        target.write(string[p:s])
        target.flush()  # Needed for Python 3.x
        _color_manager.set_color(fg, bg)
        target.write(string[s:e])
        target.flush()  # Needed for Python 3.x
        _color_manager.set_defaults()
        p = e

    if p < len(string):
        target.write(string[p:])

    target.write(end)


def autoreset():
    """Call at module exit to revert colors back to normal."""
    set_color()


# Ensure colors return to normal when colorise is quit
atexit.register(autoreset)
