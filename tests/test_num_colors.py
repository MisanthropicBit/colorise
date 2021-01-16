#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the num_colors function with mocked environments."""

import collections
import platform
import sys

import pytest

import colorise


@pytest.fixture
def mock_base_itermapp(monkeypatch):
    monkeypatch.setenv('COLORTERM', '')
    monkeypatch.setenv('TERM_PROGRAM', 'iTerm.app')


@pytest.mark.skip_on_windows
def test_num_colors_truecolor(monkeypatch):
    monkeypatch.setenv('COLORTERM', 'truecolor')
    assert colorise.num_colors() == 2**24


@pytest.mark.skip_on_windows
def test_num_colors_24bit(monkeypatch):
    monkeypatch.setenv('COLORTERM', '24bit')
    assert colorise.num_colors() == 2**24


@pytest.mark.skip_on_windows
def test_itermapp_256(mock_base_itermapp, monkeypatch):
    monkeypatch.setenv('TERM_PROGRAM_VERSION', '')

    assert colorise.num_colors() == 256


@pytest.mark.skip_on_windows
def test_itermapp_256_program_version(mock_base_itermapp, monkeypatch):
    monkeypatch.setenv('TERM_PROGRAM_VERSION', '2.1.5')

    assert colorise.num_colors() == 256


@pytest.mark.skip_on_windows
def test_itermapp_truecolor(mock_base_itermapp, monkeypatch):
    monkeypatch.setenv('TERM_PROGRAM_VERSION', '3.3.12')

    assert colorise.num_colors() == 2**24


@pytest.mark.skip_on_nix
def test_conemuansi(monkeypatch):
    monkeypatch.setenv('ConEmuANSI', 'ON')

    assert colorise.num_colors() == 256

    monkeypatch.setenv('ConEmuANSI', 'OFF')

    assert colorise.num_colors() != 256


@pytest.mark.skip_on_nix
def test_windows10_24bit(monkeypatch):
    def mocked_win32_ver():
        return ('10', '', '', '')

    getwindowsversion_tuple = collections.namedtuple(
        'getwindowsversion_tuple',
        ['build'],
    )

    def mocked_24bit_getwindowsversion():
        return getwindowsversion_tuple(14931)

    def mocked_not_24bit_getwindowsversion():
        return getwindowsversion_tuple(14930)

    monkeypatch.setattr(platform, 'win32_ver', mocked_win32_ver)
    monkeypatch.setattr(
        sys,
        'getwindowsversion',
        mocked_24bit_getwindowsversion
    )

    assert colorise.num_colors() == 256**3

    monkeypatch.setattr(platform, 'win32_ver', mocked_win32_ver)
    monkeypatch.setattr(
        sys,
        'getwindowsversion',
        mocked_not_24bit_getwindowsversion
    )

    assert colorise.num_colors() != 256**3
