#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Demonstrates how colorise's color format syntax can be endlessly nested."""

import colorise
import random


if __name__ == '__main__':
    # colorise's color format syntax can be nested as much as you want
    colors = ['black', 'darkblue', 'darkgreen', 'darkcyan', 'darkred',
              'darkmagenta', 'darkyellow', 'grey', 'blue', 'green', 'cyan',
              'red', 'magenta', 'yellow']

    s = '<{0}={3}:An example <{1}={4}:of a <{2}={5}:nested> color> syntax' +\
        'string>'

    colorise.fprint(s.format(*([random.choice(['fg', 'bg']) for _ in range(3)]
                             + random.sample(colors, 3))))
