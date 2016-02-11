#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Output the color capabilities of the terminal and run tests."""

from __future__ import print_function
import colorise


if __name__ == '__main__':
    print("Number of supported colors:", colorise.get_num_colors())
    print("Can redefine colors       :", colorise.can_redefine_colors())

    colorise.set_color(fg='red')
    print("This should be red")

    colorise.set_color(bg='yellow')
    print("This should be red with a yellow background")

    colorise.set_color(fg='green', bg='magenta')
    print("This should be green with a magenta/purple background")
