#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test writing to stdout and stderr."""

import os
import sys

import pytest

import colorise


def test_stdout_stderr(redirect):
    with redirect('stdout') as stdout:
        colorise.cprint('Hello', fg='red', file=sys.stderr)

        assert stdout.value == ''

    with redirect('stderr') as stderr:
        colorise.cprint('Hello', fg='red', file=sys.stdout)

        assert stderr.value == ''

    with redirect('stdout') as stdout:
        with redirect('stderr') as stderr:
            colorise.cprint('Hello', fg='red', file=sys.stdout)
            colorise.cprint('World', fg='blue', file=sys.stderr)

            assert stdout.value == '\x1b[0m\x1b[31mHello\x1b[0m' + os.linesep
            assert stderr.value == '\x1b[0m\x1b[34mWorld\x1b[0m' + os.linesep


def test_stdin():
    with pytest.raises(AttributeError, match=r"no attribute 'flush'"):
        colorise.cprint('Hello', fg='red', file=sys.stdin)
