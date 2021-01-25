#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test approximation of RGB colors."""

import os

import pytest

import colorise


@pytest.mark.skip_on_windows
def test_rgb_approximation(test_stdout, monkeypatch):
    # Mock 8 system colors
    import curses
    monkeypatch.setattr(curses, 'setupterm', lambda fd=None: fd)
    monkeypatch.setattr(curses, 'tigetnum', lambda _: 8)
    monkeypatch.setenv('COLORTERM', '')
    monkeypatch.setenv('TERM_PROGRAM', '')
    monkeypatch.setenv('TERM_PROGRAM_VERSION', '')

    expected = '\x1b[0m\x1b[31mHello\x1b[0m' + os.linesep
    test_stdout(colorise.cprint, expected, 'Hello', fg='rgb(255;0;0)')

    # Mock 16 system colors
    monkeypatch.setattr(curses, 'tigetnum', lambda _: 16)

    expected = '\x1b[0m\x1b[31mHello\x1b[0m' + os.linesep
    test_stdout(colorise.cprint, expected, 'Hello', fg='rgb(255;0;0)')

    # Mock 88 colors
    monkeypatch.setattr(curses, 'tigetnum', lambda _: 88)

    expected = '\x1b[0m\x1b[38;5;64mHello\x1b[0m' + os.linesep
    test_stdout(colorise.cprint, expected, 'Hello', fg='rgb(255;0;0)')

    # Mock 256 colors
    monkeypatch.setattr(curses, 'tigetnum', lambda _: 256)

    expected = '\x1b[0m\x1b[38;5;196mHello\x1b[0m' + os.linesep
    test_stdout(colorise.cprint, expected, 'Hello', fg='rgb(255;0;0)')

    # Mock true-color
    monkeypatch.setenv('COLORTERM', 'truecolor')

    expected = '\x1b[0m\x1b[38;2;255;0;0mHello\x1b[0m' + os.linesep
    test_stdout(colorise.cprint, expected, 'Hello', fg='rgb(255;0;0)')
