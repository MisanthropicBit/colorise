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
            '\x1b[0m\x1b[1m\x1b[31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[2m\x1b[31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[3m\x1b[31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[4m\x1b[31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[5m\x1b[31mHello\x1b[0m' + os.linesep,
            '\x1b[0m\x1b[7m\x1b[31mHello\x1b[0m' + os.linesep,
        ])


def test_attributes():
    colorise.cprint('Hello',                       attributes=[Attr.Bold])
    colorise.cprint('Hello', fg='red',             attributes=[Attr.Bold])
    colorise.cprint('Hello',            bg='blue', attributes=[Attr.Bold])
    colorise.cprint('Hello', fg='red',  bg='blue', attributes=[Attr.Bold])

    colorise.fprint('{bold}Hello')
    colorise.fprint('{fg=red,bold}Hello')
    colorise.fprint('{bg=blue,bold}Hello')
    colorise.fprint('{fg=red,bg=blue,bold}Hello')


def test_attribute_names():
    names = frozenset([
        'reset',
        'bold',
        'faint',
        'italic',
        'underline',
        'blink',
        'reverse'
    ])

    assert Attr.names() == names


def test_attribute_aliases():
    colorise.cprint('Hello',                       attributes=[Attr.Intense])
    colorise.cprint('Hello', fg='red',             attributes=[Attr.Intense])
    colorise.cprint('Hello',            bg='blue', attributes=[Attr.Intense])
    colorise.cprint('Hello', fg='red',  bg='blue', attributes=[Attr.Intense])

    colorise.fprint('{intense}Hello')
    colorise.fprint('{fg=red,intense}Hello')
    colorise.fprint('{bg=blue,intense}Hello')
    colorise.fprint('{fg=red,bg=blue,intense}Hello')


def test_invalid_attributes():
    with pytest.raises(ValueError):
        colorise.fprint('{overlined}Hello')

    with pytest.raises(ValueError):
        colorise.fprint('{fg=red,overlined}Hello')

    with pytest.raises(ValueError):
        colorise.fprint('{bg=blue,overlined}Hello')

    with pytest.raises(ValueError):
        colorise.fprint('{fg=red,bg=blue,overlined}Hello')


@pytest.mark.skip_on_windows
def test_attribute_cprint_output(test_stdout, expected_results):
    for attribute, expected in expected_results:
        test_stdout(
            colorise.cprint,
            expected,
            'Hello',
            fg='red',
            attributes=[attribute],
        )


@pytest.mark.skip_on_windows
def test_attribute_fprint_output(test_stdout, expected_results):
    for attribute, expected in expected_results:
        test_stdout(
            colorise.fprint,
            expected,
            '{{fg=red,{0}}}Hello'.format(attribute.name.lower())
        )
