#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Output the color capabilities of the terminal and run tests."""

from __future__ import print_function
import colorise
import sys


if __name__ == '__main__':
    # NOTE: We use sys.stdout.write so the newline will not be included and the
    # colors will not spill onto the next line
    print("Running color capability test...")
    print("Number of supported colors:", colorise.get_num_colors())
    print("Can redefine colors       :", colorise.can_redefine_colors())

    # Colors by name
    colorise.set_color(fg='red')
    print("This should be red")

    colorise.set_color(bg='yellow')
    sys.stdout.write("This should be red with a yellow background")
    colorise.set_color()
    print()

    colorise.set_color(fg='green', bg='magenta')
    sys.stdout.write("This should be green with a magenta/purple background")
    colorise.set_color()
    print()

    # Colors by index
    colorise.set_color(fg=201)
    print("This should be purplish")

    colorise.set_color(bg=20)
    sys.stdout.write("This should have a blueish background")
    colorise.set_color()
    print()

    colorise.set_color(fg=227, bg=47)
    sys.stdout.write("This should be yellowish with a greenish background")
    colorise.set_color()
    print()

    # Colors by RGB/hex
    colorise.set_color(fg=(102, 255, 255))
    print("This should be cyanish")

    colorise.set_color(fg='0x0080ff')
    print("This should be blueish")

    # Colors by HSV
    colorise.set_color(bg=colorise.cluts.hsv_to_rgb(215, 100, 72.5))
    sys.stdout.write("This should have a blueish background")
    colorise.set_color()
    print()

    colorise.set_color(fg='green', bg='hsv(78, 26, 55)')
    sys.stdout.write("This should be greenish with a ? background")
    colorise.set_color()
    print()

    # Colors by HLS
    colorise.set_color(bg=colorise.cluts.hls_to_rgb(0, 0.48, 0.69))
    sys.stdout.write("This should be redish")
    colorise.set_color()
    print()

    colorise.set_color(fg='hls(0, 0, 0)', bg='white')
    sys.stdout.write("This should be brownish with a white background")
    colorise.set_color()
    print()

    print("Restored defaults...")
    print("End of test...")
