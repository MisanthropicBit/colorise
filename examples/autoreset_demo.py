#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstration of colorise's autoreset future when exceptions are thrown."""

import colorise


if __name__ == '__main__':
    # Set the current color
    colorise.set_color('blue')

    # Should be printed in blue
    print("Chapter 1: The Zen of Python")

    try:
        # Even though this statement will fail, colors will be reset
        colorise.fprint("{fg=???}I can wait to be in color!")
    except ValueError:
        pass
