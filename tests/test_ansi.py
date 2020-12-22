#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the cprint function."""

from colorise.nix.color_functions import to_ansi
import pytest


@pytest.mark.skip_on_windows
def test_ansi():
    assert to_ansi(34, '95') == '\x1b[34;95m'
    assert to_ansi(0) == '\x1b[0m'
    assert to_ansi() == ''
