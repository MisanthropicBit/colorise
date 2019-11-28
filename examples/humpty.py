#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demonstration of the various ways of coloring text."""

from __future__ import print_function

import random
import colorise


if __name__ == '__main__':
    humpty = ["Humpty Dumpty sat on the wall",
              "Humpty Dumpty had a great fall",
              "All the king's horses and all the king's men",
              "Couldn't put Humpty together again"]

    # Set colors manually
    colorise.set_color('red')
    print(humpty[0])
    colorise.reset_color()

    # Use colorise.cprint
    colorise.cprint(humpty[1], 'green')

    # Use color formatting
    colorise.fprint('{{fg=purple}}{0}'.format(humpty[2]))

    randindices = random.sample(range(len(humpty[3])), 12)

    # You can also highlight different parts of a string...
    colorise.highlight(humpty[3], fg='yellow', bg='red', indices=randindices)
