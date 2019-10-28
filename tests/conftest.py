#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pytest configuration file."""

import colorise
import platform
import pytest
import sys


try:
    from contextlib import redirect_stdout
except ImportError:
    class redirect_stdout():
        """Non-reentrant version of contextlib's redirect_stdout."""

        def __init__(self, new_target, stream='stdout'):  # noqa
            self._new_target = new_target
            self._stream = stream
            self._old_target = None

        def __enter__(self):  # noqa
            self._old_target = getattr(sys, self._stream)
            setattr(sys, self._stream, self._new_target)

            return self._new_target

        def __exit__(self, exctype, excinst, exctb):  # noqa
            setattr(sys, self._stream, self._old_target)


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
