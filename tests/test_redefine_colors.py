#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test redefinition of colors."""

import sys

import pytest

import colorise


@pytest.mark.skip_on_windows
def test_redefine_colors_error():
    assert not colorise.can_redefine_colors(sys.stdout)
    assert not colorise.can_redefine_colors(sys.stderr)

    error_message = '^Cannot redefine colors on nix systems$'

    with pytest.raises(colorise.error.NotSupportedError, match=error_message):
        colorise.redefine_colors({})
