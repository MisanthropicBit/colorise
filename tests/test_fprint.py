#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the fprint function."""

import colorise
from io import StringIO
import pytest
import os
import sys


def test_valid_fprint():
    colorise.fprint('Hello {fg=red}world')
    colorise.fprint('Hello {fg=201}world')
    colorise.fprint('Hello {fg=#a696ff}world')
    colorise.fprint('Hello {fg=0xa696ff}world')
    colorise.fprint('Hello {fg=hls(0.6923;0.7960;1.0)}world')
    colorise.fprint('Hello {fg=hsv(249;41;100)}world')
    colorise.fprint('Hello {fg=rgb(167;151;255)}world')

    colorise.fprint('Hello {bg=red}world')
    colorise.fprint('Hello {bg=201}world')
    colorise.fprint('Hello {bg=#a696ff}world')
    colorise.fprint('Hello {bg=0xa696ff}world')
    colorise.fprint('Hello {bg=hls(0.6923;0.7960;1.0)}world')
    colorise.fprint('Hello {bg=hsv(249;41;100)}world')
    colorise.fprint('Hello {bg=rgb(167;151;255)}world')

    colorise.fprint('Hello {fg=red ,bg=red}world')
    colorise.fprint('Hello { fg=201,bg=201}world')
    colorise.fprint('Hello {bg=#a696ff,bg=#a696ff }world')
    colorise.fprint('Hello {fg=0xa696ff,bg=0xa696ff}world')
    colorise.fprint('Hello {fg=hls(0.6923;0.7960;1.0),'
                    'bg=hls(0.6923;0.7960;1.0)}world')
    colorise.fprint('Hello {fg=hsv(249;41;100),bg=hsv(249;41;100)}world')
    colorise.fprint('Hello {fg=rgb(167;151;255),bg=rgb(167;151;255)}world')


def test_invalid_fprint():
    kwargs = [
        'unknown',
        '300',
        '#a69ff',
        '0xa69ff',
        'hls(0.6923,0.7960;1.0=',
        'hsv(249;41;-100)',
        'rgb(167;xxx;255)',
    ]

    for kwarg in kwargs:
        with pytest.raises(ValueError):
            colorise.fprint('{fg=' + kwarg + '}Hello')

        with pytest.raises(ValueError):
            colorise.fprint('{bg=' + kwarg + '}Hello')


@pytest.mark.skip_on_windows
def test_valid_named_fprint_output():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint('{fg=red}Hello', file=sys.stdout)
        assert sio.getvalue() == '\x1b[0m\x1b[31mHello\x1b[0m' + os.linesep


@pytest.mark.require_colors(256)
def test_valid_256_index_fprint_output():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint('{fg=201}Hello', file=sys.stdout)
        assert sio.getvalue() == '\x1b[0m\x1b[38;5;201mHello\x1b[0m'\
            + os.linesep


@pytest.mark.require_colors(256**3)
def test_valid_truecolor_fprint_output():
    tests = [
        ('fg=0xa696ff',
         '\x1b[0m\x1b[38;2;166;150;255mHello\x1b[0m' + os.linesep),
        ('fg=0xa696ff',
         '\x1b[0m\x1b[38;2;166;150;255mHello\x1b[0m' + os.linesep),
        ('fg=hsv(249;41;100)',
         '\x1b[0m\x1b[38;2;166;150;255mHello\x1b[0m' + os.linesep),
        ('fg=rgb(167;151;255)',
         '\x1b[0m\x1b[38;2;167;151;255mHello\x1b[0m' + os.linesep),
    ]

    for color, expected_result in tests:
        sio = StringIO()

        with pytest.redirect_stdout(sio):
            colorise.fprint('{' + color + '}Hello', file=sys.stdout)
            assert sio.getvalue() == expected_result


@pytest.mark.skip_on_windows
def test_fprint_disabled():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint('{fg=red}Hello', file=sys.stdout, enabled=False)
        assert sio.getvalue() == '\x1b[0mHello' + os.linesep


@pytest.mark.skip_on_windows
def test_fprint_proper_reset():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.set_color(fg='red')
        colorise.fprint('Hel{bg=blue}lo', file=sys.stdout)
        assert sio.getvalue() == '\x1b[0mHel\x1b[44mlo\x1b[0m' + os.linesep


@pytest.mark.skip_on_windows
def test_fprint_autoreset():
    text = '{fg=red}Hello {bg=blue}world!'
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint(text, file=sys.stdout, autoreset=False)
        assert sio.getvalue() ==\
            '\x1b[0m\x1b[31mHello \x1b[44mworld!\x1b[0m' + os.linesep

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint(text, file=sys.stdout, autoreset=True)
        assert sio.getvalue() ==\
            '\x1b[0m\x1b[31mHello \x1b[0m\x1b[44mworld!\x1b[0m' + os.linesep
