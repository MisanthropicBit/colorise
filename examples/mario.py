#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Output a 8-bit colored sprite of Mario."""

import colorise


def mario():
    """Print a mario sprite to stdout."""
    width = 12
    height = 16

    # Source: https://github.com/BrianEnigma/NES_Sprite_Display
    yellow = '#e39d25'
    red = '#b13425'
    green = '#6a6b04'
    color_table = [None, red, green, yellow]

    mario_pixels = [
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 2, 2, 2, 3, 3, 2, 3, 0, 0, 0],
        [0, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 0],
        [0, 2, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3],
        [0, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 0],
        [0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0],
        [0, 0, 2, 2, 1, 2, 2, 2, 0, 0, 0, 0],
        [0, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 0],
        [2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2],
        [3, 3, 2, 1, 3, 1, 1, 3, 1, 2, 3, 3],
        [3, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 3],
        [3, 3, 1, 1, 1, 0, 0, 1, 1, 1, 3, 3],
        [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 0],
        [2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2],
    ]

    for y in range(0, height):
        for x in range(0, width):
            colorise.cprint('  ', bg=color_table[mario_pixels[y][x]], end='')

        print()


if __name__ == "__main__":
    mario()
