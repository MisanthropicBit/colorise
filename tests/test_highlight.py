#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the highlight function."""

import colorise
from io import StringIO
import pytest
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
    result = '\x1b[31mH\x1b[0me\x1b[31ml\x1b[0ml\x1b[31mo\x1b[0m\n'

    with pytest.redirect_stdout(sio):
        colorise.highlight('Hello', [0, 2, 4], fg='red', file=sys.stdout)
        assert sio.getvalue() == result


@pytest.mark.skip_on_windows
@pytest.mark.require_colors(256)
def test_highlight_256_index_output():
    sio = StringIO()
    result = '\x1b[38;5;201mH\x1b[0me\x1b[38;5;201m'\
             'l\x1b[0ml\x1b[38;5;201mo\x1b[0m\n'

    with pytest.redirect_stdout(sio):
        colorise.highlight('Hello', [0, 2, 4], fg=201, file=sys.stdout)
        assert sio.getvalue() == result


@pytest.mark.skip_on_windows
@pytest.mark.require_colors(256**3)
def test_highlight_truecolor_output():
    text = 'Hello'
    indices = [0, 2, 4]

    result = '\x1b[38;2;166;150;255mH\x1b[0me\x1b[38;2;166;150;255m'\
             'l\x1b[0ml\x1b[38;2;166;150;255mo\x1b[0m\n'

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.highlight(text, indices, fg='0xa696ff', file=sys.stdout)
        assert sio.getvalue() == result

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.highlight(text, indices, fg='hls(0.6919;0.7940;1.0)',
                           file=sys.stdout)
        assert sio.getvalue() == result

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.highlight('Hello', [0, 2, 4], fg='hsv(249;41;100)',
                           file=sys.stdout)
        assert sio.getvalue() == result

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.highlight('Hello', [0, 2, 4], fg='rgb(167;151;255)',
                           file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;2;167;151;255mH\x1b[0me'\
                                 '\x1b[38;2;167;151;255m'\
                                 'l\x1b[0ml\x1b[38;2;167;151;255mo\x1b[0m\n'


@pytest.mark.skip_on_windows
def test_highlight_disabled():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.highlight('Hello', [0, 2, 4], file=sys.stdout, enabled=False)
        assert sio.getvalue() == 'Hello\n'
