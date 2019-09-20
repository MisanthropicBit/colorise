#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Small script for testing your terminal's capabilities."""

import colorise
from colorise.attributes import Attr
import os
import platform


def print_stats_and_env():
    """Print statistics and relevant environment variables."""
    color_count = colorise.num_colors()
    color_count_name = 'true-color' if color_count == 2**24 else color_count

    stats = [
            ('Color count',  color_count_name),
            ('TERM',         os.environ.get('TERM', 'N/A')),
            ('TERM_PROGRAM', os.environ.get('TERM_PROGRAM', 'N/A')),
            ('COLORTERM',    os.environ.get('COLORTERM', 'N/A')),
            ('COLORFGBG',    os.environ.get('COLORFGBG', 'N/A')),
        ]

    system = platform.system().lower()
    shellvar = 'ComSpec' if system.startswith('win') else 'SHELL'
    stats.insert(1, (shellvar, os.environ.get(shellvar, 'N/A')))

    for name, value in stats:
        print(('{0:<15}{1:>25}').format(name, value))


def print_system_colors(char):
    """Print the system colors."""
    print('System colors:')

    for i, name in enumerate(colorise.color_names()):
        if name in ('grey', 'magenta'):
            continue  # Skip aliases

        colorise.cprint(char, bg=name, end='')

        if i == 8:
            print()

    print()


def print_256_indices(char):
    """Print the 256 color indices."""
    print('256 color indices:')

    k = 0

    for j in range(36):
        for i in range(6):
            color_idx = k + 16 + i * 36
            aligned_idx = str(color_idx).ljust(3)
            colorise.fprint('{0} {{bg={1}}}{2}'
                            .format(aligned_idx, color_idx, char), end=' ')

        k += 1
        print()

    print()
    print('Grayscale:')

    for i in range(232, 256):
        colorise.fprint('{0} {{bg={1}}}{2}'
                        .format(i, i, char), end=' ')

        if (i - 232 + 1) % 6 == 0:
            print()


def print_attributes():
    """Print all text attributes."""
    print('Attributes:')

    for attr in Attr:
        if attr == attr.Reset:
            continue

        colorise.cprint(attr.name, attributes=[attr], end=' ')

    print()


if __name__ == "__main__":
    colorise.cprint('colorise v{0}'.format(colorise.__version__),
                    fg='white', attributes=[Attr.Bold])
    print()
    char = '   '

    print_stats_and_env()
    print()
    print_system_colors(char)

    if colorise.num_colors() >= 256:
        print()
        print_256_indices(char)

    print()
    print_attributes()
