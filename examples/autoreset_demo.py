#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstration of colorise's autoreset future when exceptions are thrown."""

from __future__ import print_function

__date__ = "2014-05-21"  # YYYY-MM-DD

import colorise


if __name__ == '__main__':
    # Set the current color
    colorise.set_color('darkblue')

    # Should be printed in dark blue
    print("Chapter 1: The Zen of Python")

    # Even though this statement will fail, colors will be reset
    colorise.fprint("<fg=???:I can wait to be in color!>")
