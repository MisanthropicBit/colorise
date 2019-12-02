#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Nix color look-up tables (CLUTs) and functions."""

from colorise.color_tools import closest_color
from colorise.terminal import terminal_name
import collections
import io
import os


_COLOR_ESCAPE_CODE = '\x1b['
_COLOR_PREFIX_16 = _COLOR_ESCAPE_CODE + '{0}m'
_COLOR_PREFIX_FG_88 = _COLOR_ESCAPE_CODE + '38;5;{0}m'
_COLOR_PREFIX_BG_88 = _COLOR_ESCAPE_CODE + '48;5;{0}m'
_COLOR_PREFIX_FG_256 = _COLOR_PREFIX_FG_88
_COLOR_PREFIX_BG_256 = _COLOR_PREFIX_BG_88
_COLOR_PREFIX_FG_TRUE_COLOR = _COLOR_ESCAPE_CODE + '38;2;{0}m'
_COLOR_PREFIX_BG_TRUE_COLOR = _COLOR_ESCAPE_CODE + '48;2;{0}m'

_prefix_map = {
        #       Foreground prefix            Background prefix
        8:     (_COLOR_PREFIX_16,            _COLOR_PREFIX_16),
        16:    (_COLOR_PREFIX_16,            _COLOR_PREFIX_16),
        88:    (_COLOR_PREFIX_FG_88,         _COLOR_PREFIX_BG_88),
        256:   (_COLOR_PREFIX_FG_256,        _COLOR_PREFIX_BG_256),
        2**24: (_COLOR_PREFIX_FG_TRUE_COLOR, _COLOR_PREFIX_BG_TRUE_COLOR)
    }

# System base colors that are assumed to be present for 8 color terminals
_NIX_SYSTEM_COLORS = {
    30: (0x00, 0x00, 0x00),  # black
    31: (0xff, 0x00, 0x00),  # red
    32: (0x00, 0xff, 0x00),  # green
    33: (0xff, 0xff, 0x00),  # yellow
    34: (0x00, 0x00, 0xff),  # blue
    35: (0xff, 0x00, 0xff),  # purple
    36: (0x00, 0xff, 0xff),  # cyan
    37: (0xff, 0xff, 0xff)   # white
}

# System color names as given by colorise
_NIX_SYSTEM_COLOR_NAMES = {
    'black':       30,
    'red':         31,
    'green':       32,
    'yellow':      33,
    'blue':        34,
    'purple':      35,
    'cyan':        36,
    'lightgray':   37,
    'gray':        90,
    'lightred':    91,
    'lightgreen':  92,
    'lightyellow': 93,
    'lightblue':   94,
    'lightpurple': 95,
    'lightcyan':   96,
    'white':       97,
}

# Alias for British english gray and alias for purple
_NIX_SYSTEM_COLOR_NAMES['grey'] = 90
_NIX_SYSTEM_COLOR_NAMES['lightgrey'] = 37
_NIX_SYSTEM_COLOR_NAMES['magenta'] = 35

# xterm 88-color look-up table (based on 88colres.h)
_XTERM_CLUT_88_STEPS = [0x00, 0x8b, 0xcd, 0xff]
_XTERM_CLUT_88_GRAYSCALE = [46, 92, 113, 139, 162, 185, 208, 231]
_XTERM_CLUT_88 = collections.OrderedDict(_NIX_SYSTEM_COLORS)

_XTERM_CLUT_88.update(zip(
        range(16, 88),
        [(r, g, b)
         for r in _XTERM_CLUT_88_STEPS
         for g in _XTERM_CLUT_88_STEPS
         for b in _XTERM_CLUT_88_STEPS])
    )

_XTERM_CLUT_88.update(zip(
        range(80, 89),
        [(g, g, g) for g in _XTERM_CLUT_88_GRAYSCALE])
    )

# xterm 256-color look-up table
_XTERM_CLUT_256_STEPS = [0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff]
_XTERM_CLUT_256_GRAYSCALE = [8 + 10 * i for i in range(24)]
_XTERM_CLUT_256 = collections.OrderedDict(_NIX_SYSTEM_COLORS)

_XTERM_CLUT_256.update(zip(
        range(16, 232),
        [(r, g, b)
         for r in _XTERM_CLUT_256_STEPS
         for g in _XTERM_CLUT_256_STEPS
         for b in _XTERM_CLUT_256_STEPS])
    )

_XTERM_CLUT_256.update(zip(
        range(232, 256),
        [(g, g, g) for g in _XTERM_CLUT_256_GRAYSCALE])
    )


def get_prefix(color_count, bg):
    """Get the color code prefix corresponding to the supported color count."""
    return _prefix_map[color_count][int(bg)]


def get_clut(color_count):
    """Return the appropriate color look-up table."""
    if terminal_name() == 'iTerm.app' and color_count == 88:
        # Uses the 256 color table for 88 color indices
        return _XTERM_CLUT_256

    return {
            8:   _NIX_SYSTEM_COLORS,
            16:  _NIX_SYSTEM_COLORS,
            88:  _XTERM_CLUT_88,
            256: _XTERM_CLUT_256,
        }[color_count]


def can_redefine_colors():
    """Return whether the terminal allows redefinition of colors."""
    return False


def color_from_name(name, color_count, bg, attributes):
    """Return the color value and color count for a given color name."""
    if name not in _NIX_SYSTEM_COLOR_NAMES:
        raise ValueError("Unknown color name '{0}'".format(name))

    # We just return the 16 color prefix and code. Assumes this can can be done
    # in terminals with more capabilities
    return _COLOR_PREFIX_16, _NIX_SYSTEM_COLOR_NAMES[name] + 10 * int(bg)


def color_from_index(idx, color_count, bg, attributes):
    """Return the color value and color count for a given color index."""
    if idx < 0 or idx > 255:
        raise ValueError('Color index must be in range 0-255 inclusive')

    if color_count > 88:
        # NOTE: Assume we can use 256 color prefixes if we have true-color
        return (_COLOR_PREFIX_BG_256 if bg else _COLOR_PREFIX_FG_256), idx
    elif color_count == 88:
        prefix = _COLOR_PREFIX_BG_88 if bg else _COLOR_PREFIX_FG_88

        if terminal_name() == 'iTerm.app':
            return prefix, idx

        if idx <= 88:
            return prefix, idx
        else:
            # Approximate > 88 color index with 256 color clut
            return prefix,\
                closest_color(_XTERM_CLUT_256[idx], _XTERM_CLUT_88)
    else:
        if idx <= 16:
            return _COLOR_PREFIX_16, idx + 10 * int(bg)
        else:
            # Approximate > 16 color index with 256 color clut
            key = closest_color(_XTERM_CLUT_256[idx], _NIX_SYSTEM_COLORS)

            return _COLOR_PREFIX_16, key + 10 * int(bg)


def get_rgb_color(color_count, bg, rgb, attributes):
    """Get the color for an RGB triple or approximate it if necessary."""
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
