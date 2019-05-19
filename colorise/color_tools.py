#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for converting and comparing colors."""

import colorsys
import math
import operator


def hls_to_rgb(h, l, s):
    """Convert HLS (hue, lightness, saturation) values to RGB."""
    return tuple(int(math.ceil(c * 255.))
                 for c in colorsys.hls_to_rgb(h, l, s))


def hsv_to_rgb(h, s, v):
    """Convert HSV (hue, saturation, value) values to RGB."""
    return tuple(int(c * 255.)
                 for c in colorsys.hsv_to_rgb(h/360., s/100., v/100.))


def color_difference(rgb1, rgb2):
    """Return the sums of component differences between two colors."""
    return sum(abs(i - j) for i, j in zip(rgb1, rgb2))


def color_distance(rgb1, rgb2):
    """Compute the Euclidian distance between two colors."""
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2

    return math.sqrt((r2 - r1)**2 + (g2 - g1)**2 + (b2 - b1)**2)


def closest_color(rgb, clut):
    """Return the CLUT index of the closest RGB color to a given RGB tuple."""
    # Generate a list of tuples of CLUT indices and the color difference value
    indexed_diffs = ((idx, color_difference(rgb, clut[idx])) for idx in clut)

    return min(indexed_diffs, key=operator.itemgetter(1))[0]
