#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Demonstration of the various ways of coloring text."""

from __future__ import print_function

__date__ = "2014-05-17"  # YYYY-MM-DD

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
    colorise.set_color()

    # Use colorise.cprint
    colorise.cprint(humpty[1], 'green')

    # Use color formatting
    colorise.fprint("<fg=purple:{}>", humpty[2])

    # Alternatively, you can use colorise.formatcolor
    colorise.fprint(colorise.formatcolor(humpty[3], 'cyan'))

    print()
    randindices = random.sample(range(len(humpty[3])), 12)

    # You can also highlight different parts of a string...
    colorise.highlight(humpty[random.randint(0, 3)], 'white', 'darkyellow',
                       randindices)

    # ...or use colorise.formatbyindex
    colorise.fprint(colorise.formatbyindex(humpty[random.randint(0, 3)],
                                           'darkgreen', 'yellow', randindices))
