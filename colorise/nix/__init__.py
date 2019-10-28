#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Linux/Mac color functions."""

from colorise.attributes import Attr, to_codes
import colorise.nix.cluts
import sys


def to_ansi(*codes):
    """Convert a set of ANSI codes into a valid ANSI escape sequence."""
    if not codes:
        return ''

    return '\033[{0}m'.format(';'.join(str(c) for c in codes))


def reset(file=sys.stdout):
    """Reset all colors and attributes."""
    file.write(to_ansi(Attr.Reset.value))


def set_color(fg=None, bg=None, attributes=[], file=sys.stdout):
    """Set color and attributes of the terminal.

    'fg' and 'bg' specify foreground- and background colors while 'attributes'
    is a list of desired attributes. The 'file' keyword specifies the target
    output stream.

    """
    codes = []

    if attributes:
        codes.append(to_ansi(*to_codes(attributes)))

    if Attr.Reset not in attributes:
        if fg:
            fg_prefix, fg_color = colorise.cluts.get_color(fg, False)
            codes.append(fg_prefix.format(fg_color))

        if bg:
            bg_prefix, bg_color = colorise.cluts.get_color(bg, True)
            codes.append(bg_prefix.format(bg_color))

    if codes:
        file.write(''.join(codes))


def redefine_colors(color_map, file=sys.stdout):
    """Redefine the base console colors with a new mapping."""
    # Cannot currently redefine colors on nix systems
    pass
