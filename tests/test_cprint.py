#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the cprint function."""

import colorise
import pytest
import os
import sys


def test_valid_cprint():
    colorise.cprint('Hello', fg='red')
    colorise.cprint('Hello', fg=201)
    colorise.cprint('Hello', fg='#a696ff')
    colorise.cprint('Hello', fg='0xa696ff')
    colorise.cprint('Hello', fg='hls(0.6919;0.7940;1.0)')
    colorise.cprint('Hello', fg='hsv(249;41;100)')
    colorise.cprint('Hello', fg='rgb(167;151;255)')

    colorise.cprint('Hello', bg='red')
    colorise.cprint('Hello', bg=201)
    colorise.cprint('Hello', bg='#a696ff')
    colorise.cprint('Hello', bg='0xa696ff')
    colorise.cprint('Hello', bg='hls(0.6919;0.7940;1.0)')
    colorise.cprint('Hello', bg='hsv(249;41;100)')
    colorise.cprint('Hello', bg='rgb(167;151;255)')

    colorise.cprint('Hello', fg='red', bg='red')
    colorise.cprint('Hello', fg=201, bg=201)
    colorise.cprint('Hello', fg='#a696ff', bg='#a696ff')
    colorise.cprint('Hello', fg='0xa696ff', bg='0xa696ff')
    colorise.cprint('Hello', fg='hls(0.6919;0.7940;1.0)',
                    bg='hls(0.6919;0.7940;1.0)')
    colorise.cprint('Hello', fg='hsv(249;41;100)', bg='hsv(249;41;100)')
    colorise.cprint('Hello', fg='rgb(167;151;255)', bg='rgb(167;151;255)')


def test_invalid_cprint():
    kwargs = [
        {'fg': 'unknown'},
        {'fg': 256},
        {'bg': '#a69ff'},
        {'bg': '0xa69ff'},
        {'fg': 'hls(0.6919,0.7940;1.0='},
        {'bg': 'hsv(249;41;-100)'},
        {'fg': 'rgb(167;xxx;255)'},
    ]

    for kwarg in kwargs:
        with pytest.raises(ValueError):
            colorise.cprint('Hello', **kwarg)


@pytest.mark.skip_on_windows
def test_valid_named_cprint_output(test_stdout):
    tests = zip(
        ['red', 'red', None],
        [None, 'blue', 'blue'],
        [
            '\x1b[0m\x1b[31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[31m\x1b[44mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[44mHello\x1b[0m' + os.linesep
        ]
    )

    for fg, bg, expected in tests:
        test_stdout(colorise.cprint, expected, 'Hello', fg=fg, bg=bg)


@pytest.mark.require_colors(256)
def test_valid_256_index_cprint_output(test_stdout):
    expected = '\x1b[0m\x1b[38;5;201mHello\x1b[0m' + os.linesep
    test_stdout(colorise.cprint, expected, 'Hello', fg=201)


@pytest.mark.require_colors(256**3)
def test_valid_truecolor_cprint_output(test_stdout):
    tests = [
        (
            {'fg': '0xa696ff'},
            '\x1b[0m\x1b[38;2;166;150;255mHello\x1b[0m' + os.linesep
        ),
        (
            {'fg': 'hls(0.6919;0.7940;1.0)'},
            '\x1b[0m\x1b[38;2;166;150;255mHello\x1b[0m' + os.linesep
        ),
        (
            {'fg': 'hsv(249;41;100)'},
            '\x1b[0m\x1b[38;2;166;150;255mHello\x1b[0m' + os.linesep
        ),
        (
            {'fg': 'rgb(167;151;255)'},
            '\x1b[0m\x1b[38;2;167;151;255mHello\x1b[0m' + os.linesep
        ),
    ]

    for kwargs, expected in tests:
        test_stdout(colorise.cprint, expected, 'Hello', **kwargs)


@pytest.mark.skip_on_windows
def test_cprint_disabled(test_stdout):
    test_stdout(
        colorise.cprint,
        '\x1b[0mHello' + os.linesep,
        'Hello',
        fg='red',
        enabled=False
    )


@pytest.mark.skip_on_windows
def test_cprint_proper_reset(redirect_stdout):
    with redirect_stdout() as stdout:
        colorise.set_color(fg='red')
        colorise.cprint('Hello', bg='blue', file=sys.stdout)

        assert stdout.value == '\x1b[0m\x1b[44mHello\x1b[0m' + os.linesep
