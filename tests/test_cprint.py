#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""."""

import colorise
import pytest


def test_valid_cprint():
    colorise.cprint('Hello', fg='red')
    colorise.cprint('Hello', fg=201)
    colorise.cprint('Hello', fg='#a696ff')
    colorise.cprint('Hello', fg='0xa696ff')
    colorise.cprint('Hello', fg='hls(0.6923;0.7960;1.0)')
    colorise.cprint('Hello', fg='hsv(249;41;100)')
    colorise.cprint('Hello', fg='rgb(167;151;255)')


def test_invalid_cprint():
    with pytest.raises(ValueError):
        colorise.cprint('Hello', fg='unknown')

    with pytest.raises(ValueError):
        colorise.cprint('Hello', fg=256)

    with pytest.raises(ValueError):
        colorise.cprint('Hello', bg='#a69ff')

    with pytest.raises(ValueError):
        colorise.cprint('Hello', bg='0xa69ff')

    with pytest.raises(ValueError):
        colorise.cprint('Hello', fg='hls(0.6923,0.7960;1.0=')

    with pytest.raises(ValueError):
        colorise.cprint('Hello', bg='hsv(249;41;-100)')

    with pytest.raises(ValueError):
        colorise.cprint('Hello', fg='rgb(167;xxx;255)')
