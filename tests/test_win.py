#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import pytest


@pytest.mark.skip_on_nix
def test_win_raise_error():
    from colorise.win.win32_functions import raise_win_error

    with pytest.raises(WindowsError):
        raise_win_error()
