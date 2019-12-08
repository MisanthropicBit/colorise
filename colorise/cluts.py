#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main color look-up table (CLUT) functions.

All look-up tables presented here are entirely based on research and the
author's own knowledge as it is impossible to ensure complete cross-platform
support across all kinds of terminals. Therefore, there is no guarantee that
any of these tables will be accurate.

If you have corrections or suggestions, please submit an issue.

"""

from colorise.color_tools import hls_to_rgb, hsv_to_rgb
import re

_DELIMITER = ';'
_RGB_RE = re.compile(r'^(rgb)?\((\d{1,3}' +
                     _DELIMITER +
                     r'\s*\d{1,3}' +
                     _DELIMITER +
                     r'\s*\d{1,3})\)$')
_HEX_RE = re.compile(r'^(0x|#)?(([0-9a-fA-F]{2}){3})$')
_HSV_RE = re.compile(r'^(hsv)\((\d+' +
                     _DELIMITER +
                     r'\s*\d+' +
                     _DELIMITER +
                     r'\s*\d+)\)$')
_HLS_RE = re.compile(r'^(hls)\((\d+(\.\d+)?' +
                     _DELIMITER +
                     r'\s*\d+(\.\d+)?' +
                     _DELIMITER +
                     r'\s*\d+(\.\d+)?)\)$')

# Supported formats of colorise. The order matters!
_FORMATS = [
    (_RGB_RE.match, 'rgb'),
    (str.isdigit,   'index'),
    (str.isalpha,   'name'),
    (_HEX_RE.match, 'hex'),
    (_HLS_RE.match, 'hls'),
    (_HSV_RE.match, 'hsv')
]


def match_color_formats(value):
    """Return the color format of the first format to match the given value."""
    for matcher, name in _FORMATS:
        m = matcher(str(value))

        if m:
            return m, name

    return None, None


def get_color(value, color_count, cluts, bg=False, attributes=[]):
    """Return the color given by a color format."""
    match, colorspace = match_color_formats(value)

    if colorspace == 'name':
        # Color was given as text, e.g. 'red'
        return cluts.color_from_name(value, color_count, bg, attributes)
    elif colorspace == 'index':
        # Color is a 8, 16, 88 or 256 color index
        return cluts.color_from_index(int(value), color_count, bg, attributes)
    elif colorspace == 'hex':
        value = match.group(2)
        rgb = [int(value[i:i+2], 16) for i in range(0, 6, 2)]
    elif colorspace == 'hsv':
        rgb = hsv_to_rgb(*[float(c) for c in match.group(2).split(_DELIMITER)])
    elif colorspace == 'hls':
        rgb = hls_to_rgb(*[float(c) for c in match.group(2).split(_DELIMITER)])
    elif colorspace == 'rgb':
        rgb = [int(c.strip()) for c in match.group(2).split(_DELIMITER)]
    else:
        raise ValueError("Unknown color format '{0}'".format(value))

    return cluts.get_rgb_color(color_count, bg, rgb, attributes)
