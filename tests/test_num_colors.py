#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the num_colors function with mocked environments."""

import colorise
import pytest


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
