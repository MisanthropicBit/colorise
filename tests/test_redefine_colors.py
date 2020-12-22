#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test redefinition of colors."""

import colorise
import pytest


@pytest.mark.skip_on_windows
def test_redefine_colors_error():
    assert not colorise.can_redefine_colors()

    error_message = '^Cannot redefine colors on nix systems$'

    with pytest.raises(colorise.error.NotSupportedError, match=error_message):
        colorise.redefine_colors({})
