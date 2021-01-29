#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for converting and comparing colors."""

import colorsys
import math
import operator
from typing import Tuple

Rgb = Tuple[int, int, int]

def hls_to_rgb(
    hue: float,
    lightness: float,
    saturation: float
) -> Tuple[int, ...]:
    """Convert HLS (hue, lightness, saturation) values to RGB."""
    return tuple(int(math.ceil(c * 255.))
                 for c in colorsys.hls_to_rgb(hue, lightness, saturation))


def hsv_to_rgb(hue: float, saturation: float, value: float) -> Tuple[int, ...]:
    """Convert HSV (hue, saturation, value) values to RGB."""
    return tuple(
        int(c * 255.) for c in colorsys.hsv_to_rgb(
            hue / 360.,
            saturation / 100.,
            value / 100.
        )
    )


def color_difference(rgb1: Rgb, rgb2: Rgb) -> int:
    """Return the sums of component differences between two colors."""
    return sum(abs(i - j) for i, j in zip(rgb1, rgb2))


def closest_color(rgb: Rgb, clut) -> Tuple[int, int]:
    """Return the CLUT index of the closest RGB color to a given RGB tuple."""
    # Generate a list of tuples of CLUT indices and the color difference value
    indexed_diffs = ((idx, color_difference(rgb, clut[idx])) for idx in clut)

    return min(indexed_diffs, key=operator.itemgetter(1))[0]
