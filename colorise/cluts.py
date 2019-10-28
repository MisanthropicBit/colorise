#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main color look-up table (CLUT) functions.

All look-up tables presented here are entirely based on research and the
author's own knowledge as it is impossible to ensure complete cross-platform
support across all kinds of terminals. Therefore, there is no guarantee that
any of these tables will be accurate.

If you have corrections or suggestions, please submit an issue.

"""

from colorise.color_tools import hls_to_rgb, hsv_to_rgb, closest_color
import platform
import re

_SYSTEM_OS = platform.system().lower()

# OS-dependent imports
if 'windows' in _SYSTEM_OS:
    from colorise.win.cluts import num_colors as _num_colors

    from colorise.win.cluts import get_prefix,\
        get_clut,\
        color_from_name,\
        color_from_index
else:
    from colorise.nix.cluts import num_colors as _num_colors

    from colorise.nix.cluts import get_prefix,\
        get_clut,\
        color_from_name,\
        color_from_index

_INNER_DELIMITER = ';'
_RGB_RE = re.compile(r'^(rgb)?\((\d{1,3};\s*\d{1,3};\s*\d{1,3})\)$')
_HEX_RE = re.compile(r'^(0x|#)?(([0-9a-fA-F]{2}){3})$')
_HSV_RE = re.compile(r'^(hsv)\((\d+;\s*\d+;\s*\d+)\)$')
_HLS_RE = re.compile(r'^(hls)\((\d+(\.\d+)?;\s*\d+(\.\d+)?;\s*\d+(\.\d+)?)\)$')

# Supported formats of colorise. The order matters!
_FORMATS = [
    (_RGB_RE.match, 'rgb'),
    (str.isdigit,   'index'),
    (str.isalpha,   'name'),
    (_HEX_RE.match, 'hex'),
    (_HLS_RE.match, 'hls'),
    (_HSV_RE.match, 'hsv')
]

# User-defined color count
__NUM_COLORS__ = 0


def match_color_formats(value):
    """Return the color format of the first format to match the given value."""
    for matcher, name in _FORMATS:
        m = matcher(str(value))

        if m:
            return m, name

    return None, None


def num_colors():
    """Get the number of colors supported by the terminal."""
    if __NUM_COLORS__ > 0:
        # Return a user-defined color count
        return __NUM_COLORS__

    return _num_colors()


def set_num_colors(color_count):
    """Set the number of colors available instead of autodetecting it.

    This is primarily useful for testing and debugging.

    """
    color_counts = [8, 16, 88, 256, 2**24]

    if color_count not in color_counts:
        raise ValueError('Invalid color count, expected any of {0}'
                         .format(', '.join(str(cc) for cc in color_counts)))

    global __NUM_COLORS__
    __NUM_COLORS__ = color_count


def get_color(value, bg=False):
    """Return the color given by a color format."""
    if not value:
        return None, None  # TODO: Fix for Windows

    match, colorspace = match_color_formats(value)
    color_count = num_colors()

    if colorspace == 'name':
        # Color was given as text, e.g. 'red'
        return color_from_name(value, color_count, bg)
    elif colorspace == 'index':
        # Color is a 8, 16, 88 or 256 color index
        return color_from_index(int(value), color_count, bg)
    elif colorspace == 'hex':
        value = match.group(2)
        rgb = [int(value[i:i+2], 16) for i in range(0, 6, 2)]
    elif colorspace == 'hsv':
        rgb = hsv_to_rgb(*[float(c) for c in match.group(2).split(';')])
    elif colorspace == 'hls':
        rgb = hls_to_rgb(*[float(c) for c in match.group(2).split(';')])
    elif colorspace == 'rgb':
        rgb = [int(c.strip()) for c in match.group(2).split(';')]
    else:
        raise ValueError("Unknown color format '{0}'".format(value))

    prefix = get_prefix(color_count, bg)

    if color_count < 2**24:
        # No true-color capabilities and color was given as a true-color value,
        # approximate to closest color given current capabilities
        color_idx = closest_color(rgb, get_clut(color_count))

        if color_count <= 16:
            return prefix, color_idx + 10 * int(bg)
        else:
            return prefix, color_idx

    return prefix, ';'.join(str(c) for c in rgb)
