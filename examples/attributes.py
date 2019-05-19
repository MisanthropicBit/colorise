#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstration of the various ways of coloring text."""

from __future__ import print_function

import random
import colorise


if __name__ == '__main__':
    # Print in red and bold
    colorise.fprint("{fg=red,bold}", 100)
