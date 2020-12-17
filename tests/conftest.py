#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pytest configuration file."""

import colorise
import contextlib
import io
import platform
import pytest
import sys


@pytest.fixture
def test_stdout(capsys):
    """Capture and test stdout against a call to a colorise function."""
    def _capture_output(func, expected_result, *args, **kwargs):
        # We point the colorise function to the newly captured sys.stdout
        func(*args, file=sys.stdout, **kwargs)
        stdout = capsys.readouterr().out
        assert stdout == expected_result

    return _capture_output


class RedirectedStdout():
    """Wrapper class around implementation of redirected stdout.

    This hides the implementation so it can be modified without having to
    change all tests.

    """

    def __init__(self, source):
        self._source = source

    @property
    def value(self):
        return self._source.getvalue()


@pytest.fixture
def redirect_stdout():
    """Return a context manager that captures stdout."""
    @contextlib.contextmanager
    def _redirected_stdout():
        sio = io.StringIO()

        with contextlib.redirect_stdout(sio):
            yield RedirectedStdout(sio)

    return _redirected_stdout


def pytest_configure(config):  # noqa
    pytest.redirect_stdout = contextlib.redirect_stdout

    config.addinivalue_line(
        'markers',
        'skip_on_windows: skip test on windows'
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
                pytest.skip('Test skipped on Windows systems')
        elif mark.name == 'skip_on_nix':
            if not _PLATFORM.startswith('win'):
                pytest.skip('Test skipped on nix systems')
        elif mark.name == 'require_colors':
            required_num_colors = mark.args[0]

            if colorise.num_colors() < mark.args[0]:
                msg = 'Test only relevant for terminals with {0}'

                if required_num_colors == 256**3:
                    color_name = 'true-color'
                else:
                    color_name = str(required_num_colors) + ' colors'

                pytest.skip(msg.format(color_name))
