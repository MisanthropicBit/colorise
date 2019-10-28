#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the cprint function."""

import colorise
import pytest
import sys

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


def test_valid_cprint():
    colorise.cprint('Hello', fg='red')
    colorise.cprint('Hello', fg=201)
    colorise.cprint('Hello', fg='#a696ff')
    colorise.cprint('Hello', fg='0xa696ff')
    colorise.cprint('Hello', fg='hls(0.6919;0.7940;1.0)')
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
        colorise.cprint('Hello', fg='hls(0.6919,0.7940;1.0=')

    with pytest.raises(ValueError):
        colorise.cprint('Hello', bg='hsv(249;41;-100)')

    with pytest.raises(ValueError):
        colorise.cprint('Hello', fg='rgb(167;xxx;255)')


@pytest.mark.skip_on_windows
def test_valid_named_cprint_output():
    tests = zip(
            ['red', 'red', None],
            [None, 'blue', 'blue'],
            [
                '\x1b[31mHello\x1b[0m\n',
                '\x1b[31m\x1b[44mHello\x1b[0m\n',
                '\x1b[44mHello\x1b[0m\n'
            ]
        )

    for fg, bg, result in tests:
        sio = StringIO()

        with pytest.redirect_stdout(sio):
            colorise.cprint('Hello', fg=fg, bg=bg, file=sys.stdout)
            assert sio.getvalue() == result


@pytest.mark.skip_on_windows
@pytest.mark.require_colors(256)
def test_valid_256_index_cprint_output():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.cprint('Hello', 201, file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;5;201mHello\x1b[0m\n'


@pytest.mark.skip_on_windows
@pytest.mark.require_colors(256**3)
def test_valid_truecolor_cprint_output():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.cprint('Hello', fg='0xa696ff', file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;2;166;150;255mHello\x1b[0m\n'

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.cprint('Hello', fg='hls(0.6919;0.7940;1.0)', file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;2;166;150;255mHello\x1b[0m\n'

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.cprint('Hello', fg='hsv(249;41;100)', file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;2;166;150;255mHello\x1b[0m\n'

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.cprint('Hello', fg='rgb(167;151;255)', file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;2;167;151;255mHello\x1b[0m\n'


@pytest.mark.skip_on_windows
def test_cprint_disabled():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.cprint('Hello', fg='red', file=sys.stdout, enabled=False)
        assert sio.getvalue() == 'Hello\n'
