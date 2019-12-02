#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test redefinition of colors."""

import colorise
import pytest


@pytest.mark.skip_on_windows
def test_redefine_colors_error():
    with pytest.raises(colorise.error.NotSupportedError):
        colorise.redefine_colors({})
