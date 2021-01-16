#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the highlight function."""

import colorise
import pytest
import os
import sys


def test_highlight():
    text = 'Hello'
    indices = [0, 2, 4]

    colorise.highlight(text, indices, fg='red')
    colorise.highlight(text, indices, fg=201)
    colorise.highlight(text, indices, fg='#a696ff')
    colorise.highlight(text, indices, fg='0xa696ff')
    colorise.highlight(text, indices, fg='hls(0.6919;0.7940;1.0)')
    colorise.highlight(text, indices, fg='hsv(249;41;100)')
    colorise.highlight(text, indices, fg='rgb(167;151;255)')

    colorise.highlight(text, indices, bg='red')
    colorise.highlight(text, indices, bg=201)
    colorise.highlight(text, indices, bg='#a696ff')
    colorise.highlight(text, indices, bg='0xa696ff')
    colorise.highlight(text, indices, bg='hls(0.6919;0.7940;1.0)')
    colorise.highlight(text, indices, bg='hsv(249;41;100)')
    colorise.highlight(text, indices, bg='rgb(167;151;255)')


def test_invalid_highlight():
    text = 'Hello'
    indices = [0, 2, 4]
    invalid_colors = [
        ('unknown', r"^Unknown color name 'unknown'$"),
        (256, r"^Color index must be in range 0-255 inclusive$"),
        (300, r"^Color index must be in range 0-255 inclusive$"),
        ('#a69ff', r"^Unknown or invalid color format '#a69ff'$"),
        ('0xa69ff', r"^Unknown or invalid color format '0xa69ff'$"),
        (
            'hls(0.6923,0.7960;1.0=',
            r"^Unknown or invalid color format 'hls\(0.6923,0.7960;1.0='$",
        ),
        (
            'hsv(249;41;-100)',
            r"^Unknown or invalid color format 'hsv\(249;41;-100\)'$",
        ),
        (
            'rgb(167;xxx;255)',
            r"^Unknown or invalid color format 'rgb\(167;xxx;255\)'$",
        ),
    ]

    for color, error_message in invalid_colors:
        with pytest.raises(ValueError, match=error_message):
            colorise.highlight(text, indices, fg=color)


@pytest.mark.skip_on_windows
def test_highlight_named_output(test_stdout):
    test_stdout(
        colorise.highlight,
        '\x1b[0m\x1b[31mH\x1b[0me\x1b[31ml\x1b[0ml\x1b[31mo\x1b[0m!'
        + os.linesep,
        'Hello!',
        [0, 2, 4],
        fg='red',
    )

    test_stdout(
        colorise.highlight,
        '\x1b[0m\x1b[41mH\x1b[0me\x1b[41ml\x1b[0ml\x1b[41mo\x1b[0m!'
        + os.linesep,
        'Hello!',
        [0, 2, 4],
        bg='red',
    )


@pytest.mark.require_colors(256)
@pytest.mark.skip_on_windows
def test_highlight_256_index_output(test_stdout):
    test_stdout(
        colorise.highlight,
        '\x1b[0m\x1b[38;5;201mH\x1b[0me\x1b[38;5;201m'
        'l\x1b[0ml\x1b[38;5;201mo\x1b[0m' + os.linesep,
        'Hello',
        [0, 2, 4],
        fg=201,
    )

    test_stdout(
        colorise.highlight,
        '\x1b[0m\x1b[48;5;201mH\x1b[0me\x1b[48;5;201m'
        'l\x1b[0ml\x1b[48;5;201mo\x1b[0m' + os.linesep,
        'Hello',
        [0, 2, 4],
        bg=201,
    )


@pytest.mark.require_colors(256**3)
@pytest.mark.skip_on_windows
def test_highlight_truecolor_output(test_stdout):
    text = 'Hello'
    indices = [0, 2, 4]
    kwargs = [
        {'fg': '0xa696ff'},
        {'fg': 'hls(0.6919;0.7940;1.0)'},
        {'fg': 'hsv(249;41;100)'},
        {'fg': 'rgb(166;150;255)'},
    ]
    expected = '\x1b[0m\x1b[38;2;166;150;255mH\x1b[0me\x1b[38;2;166;150;255m'\
        'l\x1b[0ml\x1b[38;2;166;150;255mo\x1b[0m' + os.linesep

    for kwarg in kwargs:
        test_stdout(colorise.highlight, expected, text, indices, **kwarg)


@pytest.mark.skip_on_windows
def test_highlight_disabled(test_stdout):
    test_stdout(
        colorise.highlight,
        'Hello' + os.linesep,
        'Hello',
        [0, 2, 4],
        fg='red',
        enabled=False
    )


@pytest.mark.skip_on_windows
def test_highlight_proper_reset(redirect_stdout):
    expected = '\x1b[0mH\x1b[44mel\x1b[0ml\x1b[44mo\x1b[0m' + os.linesep

    with redirect_stdout() as stdout:
        colorise.set_color(fg='red')
        colorise.highlight('Hello', [1, 2, 4], bg='blue', file=sys.stdout)

        assert stdout.value == expected
