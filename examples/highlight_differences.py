#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A simple function that illustrates how to use colorise.highlight."""

from __future__ import print_function

import colorise


def highlight_differences(s1, s2, color):
    """Highlight the characters in s2 that differ from those in s1."""
    ls1, ls2 = len(s1), len(s2)

    diff_indices = [i for i, (a, b) in enumerate(zip(s1, s2)) if a != b]

    print(s1)

    if ls2 > ls1:
        colorise.cprint('_' * (ls2-ls1), fg=color)
    else:
        print()

    colorise.highlight(s2, indices=diff_indices, fg=color, end='')

    if ls1 > ls2:
        colorise.cprint('_' * (ls1-ls2), fg=color)
    else:
        print()


if __name__ == '__main__':
    highlight_differences('Highlight the differences',
                          'Hightight tke sifferenc', 'red')

    print()

    highlight_differences('I wonder if these strings are any different?',
                          'A wonder iF thzse xxxings are xxy different???',
                          'red')
