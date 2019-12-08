#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the highlight function."""

import colorise
from io import StringIO
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
    colors = [
        'unknown',
        256,
        '#a69ff',
        '0xa69ff',
        'hls(0.6919,0.7940;1.0=',
        'hsv(249;41;-100)',
        'rgb(167;xxx;255)'
    ]

    for color in colors:
        with pytest.raises(ValueError):
            colorise.highlight(text, indices, fg=color)


@pytest.mark.skip_on_windows
def test_highlight_named_output():
    sio = StringIO()
    result = '\x1b[0m\x1b[31mH\x1b[0me\x1b[31ml\x1b[0ml\x1b[31mo\x1b[0m'\
        + os.linesep

    with pytest.redirect_stdout(sio):
        colorise.highlight('Hello', [0, 2, 4], fg='red', file=sys.stdout)
        assert sio.getvalue() == result

    sio = StringIO()
    result = '\x1b[0m\x1b[41mH\x1b[0me\x1b[41ml\x1b[0ml\x1b[41mo\x1b[0m'\
        + os.linesep

    with pytest.redirect_stdout(sio):
        colorise.highlight('Hello', [0, 2, 4], bg='red', file=sys.stdout)
        assert sio.getvalue() == result


@pytest.mark.skip_on_windows
@pytest.mark.require_colors(256)
def test_highlight_256_index_output():
    sio = StringIO()
    result = '\x1b[0m\x1b[38;5;201mH\x1b[0me\x1b[38;5;201m'\
             'l\x1b[0ml\x1b[38;5;201mo\x1b[0m' + os.linesep

    with pytest.redirect_stdout(sio):
        colorise.highlight('Hello', [0, 2, 4], fg=201, file=sys.stdout)
        assert sio.getvalue() == result

    sio = StringIO()
    result = '\x1b[0m\x1b[48;5;201mH\x1b[0me\x1b[48;5;201m'\
             'l\x1b[0ml\x1b[48;5;201mo\x1b[0m' + os.linesep

    with pytest.redirect_stdout(sio):
        colorise.highlight('Hello', [0, 2, 4], bg=201, file=sys.stdout)
        assert sio.getvalue() == result


@pytest.mark.skip_on_windows
@pytest.mark.require_colors(256**3)
def test_highlight_truecolor_output():
    text = 'Hello'
    indices = [0, 2, 4]
    kwargs = [
        {'fg': '0xa696ff'},
        {'fg': 'hls(0.6919;0.7940;1.0)'},
        {'fg': 'hsv(249;41;100)'},
        {'fg': 'rgb(166;150;255)'},
    ]
    result = '\x1b[0m\x1b[38;2;166;150;255mH\x1b[0me\x1b[38;2;166;150;255m'\
             'l\x1b[0ml\x1b[38;2;166;150;255mo\x1b[0m' + os.linesep

    for kwarg in kwargs:
        sio = StringIO()

        with pytest.redirect_stdout(sio):
            colorise.highlight(text, indices, file=sys.stdout, **kwarg)
            assert sio.getvalue() == result


@pytest.mark.skip_on_windows
def test_highlight_disabled():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.highlight('Hello', [0, 2, 4], fg='red', file=sys.stdout,
                           enabled=False)
        assert sio.getvalue() == 'Hello' + os.linesep


@pytest.mark.skip_on_windows
def test_highlight_proper_reset():
    sio = StringIO()
    expected_result = '\x1b[0mH\x1b[44mel\x1b[0ml\x1b[44mo\x1b[0m' + os.linesep

    with pytest.redirect_stdout(sio):
        colorise.set_color(fg='red')
        colorise.highlight('Hello', [1, 2, 4], bg='blue', file=sys.stdout)
        assert sio.getvalue() == expected_result
