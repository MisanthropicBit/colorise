#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the fprint function."""

import colorise
from io import StringIO
import pytest
import sys



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


@pytest.mark.skip_on_windows
def test_valid_named_fprint_output():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint('{fg=red}Hello', file=sys.stdout)
        assert sio.getvalue() == '\x1b[31mHello\x1b[0m\n'


@pytest.mark.skip_on_windows
@pytest.mark.require_colors(256)
def test_valid_256_index_fprint_output():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint('{fg=201}Hello', file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;5;201mHello\x1b[0m\n'


@pytest.mark.skip_on_windows
@pytest.mark.require_colors(256**3)
def test_valid_truecolor_fprint_output():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint('{fg=0xa696ff}Hello', file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;2;166;150;255mHello\x1b[0m\n'

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint('{fg=hls(0.6919;0.7940;1.0)}Hello', file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;2;166;150;255mHello\x1b[0m\n'

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint('{fg=hsv(249;41;100)}Hello', file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;2;166;150;255mHello\x1b[0m\n'

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint('{fg=rgb(167;151;255)}Hello', file=sys.stdout)
        assert sio.getvalue() == '\x1b[38;2;167;151;255mHello\x1b[0m\n'


@pytest.mark.skip_on_windows
def test_fprint_disabled():
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint('{fg=red}Hello', file=sys.stdout, enabled=False)
        assert sio.getvalue() == 'Hello\n'


@pytest.mark.skip_on_windows
def test_fprint_autoreset():
    text = '{fg=red}Hello {bg=blue}world!'
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint(text, file=sys.stdout, autoreset=False)
        assert sio.getvalue() == '\x1b[31mHello \x1b[44mworld!\x1b[0m\n'

    sio = StringIO()

    with pytest.redirect_stdout(sio):
        colorise.fprint(text, file=sys.stdout, autoreset=True)
        assert sio.getvalue() == '\x1b[0m\x1b[31mHello '\
                                 '\x1b[0m\x1b[44mworld!\x1b[0m\n'
