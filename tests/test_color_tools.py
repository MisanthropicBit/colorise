#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from colorise.color_tools import closest_color, color_difference
from colorise.nix.cluts import _NIX_SYSTEM_COLORS, _XTERM_CLUT_88, _XTERM_CLUT_256


@pytest.fixture
def test_colors():
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    forest = (50, 138, 45)
    orangish = (226, 140, 66)

    return red, green, blue, forest, orangish


def test_color_difference(test_colors):
    red, green, blue, forest, orangish = test_colors

    assert color_difference(red, green) == 255 * 2
    assert color_difference(red, blue) == 255 * 2
    assert color_difference(green, blue) == 255 * 2
    assert color_difference(forest, orangish) == 199


def test_closest_color_nix_system_colors(test_colors):
    red, green, blue, forest, orangish = test_colors

    assert closest_color(red, _NIX_SYSTEM_COLORS) == 31
    assert closest_color(green, _NIX_SYSTEM_COLORS) == 32
    assert closest_color(blue, _NIX_SYSTEM_COLORS) == 34
    assert closest_color(forest, _NIX_SYSTEM_COLORS) == 32
    assert closest_color(orangish, _NIX_SYSTEM_COLORS) == 33


def test_closest_color_xterm88(test_colors):
    red, green, blue, forest, orangish = test_colors

    assert closest_color(red, _XTERM_CLUT_88) == 64
    assert closest_color(green, _XTERM_CLUT_88) == 28
    assert closest_color(blue, _XTERM_CLUT_88) == 19
    assert closest_color(forest, _XTERM_CLUT_88) == 20
    assert closest_color(orangish, _XTERM_CLUT_88) == 52


def test_closest_color_xterm256(test_colors):
    red, green, blue, forest, orangish = test_colors

    assert closest_color(red, _XTERM_CLUT_256) == 196
    assert closest_color(green, _XTERM_CLUT_256) == 46
    assert closest_color(blue, _XTERM_CLUT_256) == 21
    assert closest_color(forest, _XTERM_CLUT_256) == 64
    assert closest_color(orangish, _XTERM_CLUT_256) == 173
