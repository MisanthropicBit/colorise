#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test attributes."""

import colorise
from colorise.attributes import Attr
from io import StringIO
import pytest
import os
import sys


@pytest.fixture
def expected_results():
    return zip(Attr, [
            '\x1b[0m\x1b[0mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[1;31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[2;31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[3;31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[4;31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[5;31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[7;31mHello\x1b[0m' + os.linesep,
        ])


def test_attributes():
    colorise.cprint('Hello',                       attributes=[Attr.Bold])
    colorise.cprint('Hello', fg='red',             attributes=[Attr.Bold])
    colorise.cprint('Hello',            bg='blue', attributes=[Attr.Bold])
    colorise.cprint('Hello', fg='red',  bg='blue', attributes=[Attr.Bold])

    colorise.fprint('{bold}Hello')
    colorise.fprint('{fg=red;bold}Hello')
    colorise.fprint('{bg=blue;bold}Hello')
    colorise.fprint('{fg=red;bg=blue;bold}Hello')


def test_invalid_attributes():
    with pytest.raises(KeyError):
        colorise.fprint('{overlined}Hello')

    with pytest.raises(KeyError):
        colorise.fprint('{fg=red;overlined}Hello')

    with pytest.raises(KeyError):
        colorise.fprint('{bg=blue;overlined}Hello')

    with pytest.raises(KeyError):
        colorise.fprint('{fg=red;bg=blue;overlined}Hello')


@pytest.mark.skip_on_windows
def test_attribute_cprint_output(expected_results):
    for attribute, result in expected_results:
        sio = StringIO()

        with pytest.redirect_stdout(sio):
            colorise.cprint('Hello', fg='red', attributes=[attribute],
                            file=sys.stdout)
            assert sio.getvalue() == result


@pytest.mark.skip_on_windows
def test_attribute_fprint_output(expected_results):
    for attribute, result in expected_results:
        sio = StringIO()

        with pytest.redirect_stdout(sio):
            colorise.fprint('{{fg=red;{0}}}Hello'
                            .format(attribute.name.lower()),
                            file=sys.stdout)
            assert sio.getvalue() == result
