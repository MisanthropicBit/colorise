#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pytest configuration file."""

import colorise
import platform
import pytest
import sys
from contextlib import redirect_stdout

def pytest_configure(config):  # noqa
    pytest.redirect_stdout = redirect_stdout

    config.addinivalue_line(
        'markers',
        'skip_on_windows: skip test when on windows'
    )

    config.addinivalue_line(
        'markers',
        'skip_on_nix: skip test on nix systems'
    )

    config.addinivalue_line(
        'markers',
        'require_colors(count): run test only if a specific number of colors '
        'are supported'
    )


_PLATFORM = platform.system().lower()


def pytest_runtest_setup(item):  # noqa
    for mark in item.iter_markers():
        if mark.name == 'skip_on_windows':
            if _PLATFORM.startswith('win'):
                pytest.skip('Cannot check for color escape sequences '
                            'on Windows')
        elif mark.name == 'skip_on_nix':
            if not _PLATFORM.startswith('win'):
                pytest.skip('Test skipped on nix systems')
        elif mark.name == 'require_colors':
            if colorise.num_colors() < mark.args[0]:
                pytest.skip('Test only relevant for terminals with {0} colors'
                            .format(mark.args[0]))
