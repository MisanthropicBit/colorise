#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Output a 8-bit colored sprite of Mario."""

import colorise


def mario():
    width = 12
    height = 16

    # Source: https://github.com/BrianEnigma/NES_Sprite_Display
    yellow = '#e39d25'
    red = '#b13425'
    green = '#3a8400'
    green = '#6a6b04'

    mario_pixels = [
            [None,   None,   None,   red,    red,    red,    red,    red,
             None,   None,   None,   None],
            [None,   None,   red,    red,    red,    red,    red,    red,
             red,    red,    red,    None],
            [None,   None,   green,  green,  green,  yellow, yellow, green,
             yellow, None,   None,   None],
            [None,   green,  yellow, green,  yellow, yellow, yellow, green,
             yellow, yellow, yellow, None],
            [None,   green,  yellow, green,  green,  yellow, yellow, yellow,
             green,  yellow, yellow, yellow],
            [None,   green,  green,  yellow, yellow, yellow, yellow, green,
             green,  green,  green,  None],
            [None,   None,   None,   yellow, yellow, yellow, yellow, yellow,
             yellow, yellow, None,   None],
            [None,   None,   green,  green,  red,    green,  green,  green,
             None,   None,   None,   None],
            [None,   green,  green,  green,  red,    green,  green,  red,
             green,  green,  green,  None],
            [green,  green,  green,  green,  red,    red,    red,    red,
             green,  green,  green,  green],
            [yellow, yellow, green,  red,    yellow, red,    red,    yellow,
             red,    green,  yellow, yellow],
            [yellow, yellow, yellow, red,    red,    red,    red,    red,
             red,    yellow, yellow, yellow],
            [yellow, yellow, red,    red,    red,    None,   None,   red,
             red,    red,    yellow, yellow],
            [None,   None,   red,    red,    red,    None,   None,   red,
             red,    red,    None,   None],
            [None,   green,  green,  green,  None,   None,   None,   None,
             green,  green,  green,  None],
            [green,  green,  green,  green,  None,   None,   None,   None,
             green,  green,  green,  green],
        ]

    for y in range(0, height):
        for x in range(0, width):
            colorise.cprint('  ', bg=mario_pixels[y][x], end='')

        print()


if __name__ == "__main__":
    mario()
