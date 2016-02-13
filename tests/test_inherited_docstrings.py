#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for testing the colorise's testable public functions."""

import colorise
import colorise.base_color_manager
import colorise.nix.manager
import colorise.win.manager
import inspect


def test_nix_colormanager_docstrings():
    bm = colorise.base_color_manager.BaseColorManager()
    cm = colorise.nix.manager.ColorManager()

    for m in inspect.get_members(bm, predicate=inspect.ismethod):
        assert(getattr(bm, m[0]).__doc__ == getattr(cm, m[0]).__doc__)


def test_win_colormanager_docstrings():
    bm = colorise.base_color_manager.BaseColorManager()
    cm = colorise.win.manager.ColorManager()

    for m in inspect.get_members(bm, predicate=inspect.ismethod):
        assert(getattr(bm, m[0]).__doc__ == getattr(cm, m[0]).__doc__)
