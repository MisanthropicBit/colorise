#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple function that illustrates how to use colorise.highlight."""

import colorise
from colorise.attributes import Attr


def cprint_missing(ls1, ls2, color, attributes):
    """Print a padding placeholder for strings of different lengths."""
    if ls2 > ls1:
        colorise.cprint('_' * (ls2-ls1), fg=color, attributes=attributes)
    else:
        print()


def colordiff(s1, s2, color):
    """Highlight the characters in s2 that differ from those in s1."""
    ls1, ls2 = len(s1), len(s2)
    diff_indices = [i for i, (a, b) in enumerate(zip(s1, s2)) if a != b]

    print(s1, end='')
    cprint_missing(ls1, ls2, color, [Attr.Bold])

    colorise.highlight(s2, indices=diff_indices, attributes=[Attr.Bold],
                       fg=color, end='')

    cprint_missing(ls1, ls2, color, [Attr.Bold])


if __name__ == '__main__':
    colordiff('Highlight the differences',
              'Hightight tke sifferenc',
              'red')

    print()

    colordiff('I wonder if these strings are any different?',
              'A wonder iF thzse xxxings are xxy different???',
              'red')
