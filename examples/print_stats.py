#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Print statistics about the color capabilities of the terminal."""

from __future__ import print_function
import colorise

__date__ = "2016-02-06"  # YYYY-MM-DD


if __name__ == '__main__':
    print("Number of supported colors:", colorise.get_num_colors())
    print("Can redefine colors       :", colorise.can_redefine_colors())
