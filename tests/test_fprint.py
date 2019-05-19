#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""."""

import colorise
import pytest


def test_valid_formats():
    print(colorise.num_colors())
    colorise.fprint('{fg=red}Hello')
    colorise.fprint('{fg=201}Hello')
    colorise.fprint('{fg=#a696ff}Hello')
    colorise.fprint('{fg=0xa696ff}Hello')
    colorise.fprint('{fg=hls(0.6923;0.7960;1.0)}Hello')
    colorise.fprint('{fg=hsv(249;41;100)}Hello')
    colorise.fprint('{fg=rgb(167;151;255)}Hello')


def test_invalid_formats():

    with pytest.raises(ValueError):
        colorise.fprint('{fg=unknown}Hello')

    with pytest.raises(ValueError):
        colorise.fprint('{fg=300}Hello')

    with pytest.raises(ValueError):
        colorise.fprint('{fg=#a69ff}Hello')

    with pytest.raises(ValueError):
        colorise.fprint('{fg=0xa69ff}Hello')

    with pytest.raises(ValueError):
        colorise.fprint('{fg=hls(0.6923,0.7960;1.0=}Hello')

    with pytest.raises(ValueError):
        colorise.fprint('{fg=hsv(249;41;-100)}Hello')

    with pytest.raises(ValueError):
        colorise.fprint('{fg=rgb(167;xxx;255)}Hello')
