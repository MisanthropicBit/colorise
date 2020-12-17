#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the fprint function."""

import colorise
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


def test_duplicate_color_spec():
    with pytest.raises(ValueError, match='foreground'):
        colorise.fprint('Hello {fg=red,fg=red}world')

    with pytest.raises(ValueError, match='background'):
        colorise.fprint('Hello {bg=red,bg=red}world')


@pytest.mark.skip_on_windows
def test_valid_named_fprint_output(test_stdout):
    test_stdout(
        colorise.fprint,
        '\x1b[0m\x1b[31mHello\x1b[0m' + os.linesep,
        '{fg=red}Hello',
    )


@pytest.mark.require_colors(256)
def test_valid_256_index_fprint_output(test_stdout):
    test_stdout(
        colorise.fprint,
        '\x1b[0m\x1b[38;5;201mHello\x1b[0m' + os.linesep,
        '{fg=201}Hello',
    )


@pytest.mark.require_colors(256**3)
def test_valid_truecolor_fprint_output(test_stdout):
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

    for color, expected in tests:
        test_stdout(colorise.fprint, expected, '{' + color + '}Hello')


@pytest.mark.skip_on_windows
def test_fprint_disabled(test_stdout):
    test_stdout(
        colorise.fprint,
        '\x1b[0mHello' + os.linesep,
        '{fg=red}Hello',
        enabled=False,
    )


@pytest.mark.skip_on_windows
def test_fprint_proper_reset(redirect_stdout):
    with redirect_stdout() as stdout:
        colorise.set_color(fg='red')
        colorise.fprint('Hel{bg=blue}lo', file=sys.stdout)
        assert stdout.value == '\x1b[0mHel\x1b[44mlo\x1b[0m' + os.linesep


@pytest.mark.skip_on_windows
def test_fprint_autoreset(test_stdout):
    text = '{fg=red}Hello {bg=blue}world!'

    test_stdout(
        colorise.fprint,
        '\x1b[0m\x1b[31mHello \x1b[44mworld!\x1b[0m' + os.linesep,
        text,
        autoreset=False,
    )

    test_stdout(
        colorise.fprint,
        '\x1b[0m\x1b[31mHello \x1b[0m\x1b[44mworld!\x1b[0m' + os.linesep,
        text,
        autoreset=True,
    )
