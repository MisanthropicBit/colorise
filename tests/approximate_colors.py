#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test color approximation on a given system."""

import colorise
import random
import string


def random_hex_color():
    """Return a random hex-string."""
    return '#' + ''.join(random.choices(string.hexdigits, k=6))


def random_rgb_color():
    """Return a random RGB tuple."""
    return tuple([random.randint(0, 255) for _ in range(3)])


def emulate(num_colors, color, idx, colors):
    """Emulate different color capabilities of the terminal."""
    system_color_name = 'true-color' if num_colors == 2**24 else num_colors

    # Start emulation from the terminal's current capabilities and downgrade
    # them in sequence to show what the same color would approximate to
    for i in range(idx, 0, -1):
        color_count = colors[i]
        colorise.set_num_colors(color_count)

        colorise.cprint('Emulating {0} colors on a {1} color system'
                        .format(color_count, system_color_name), fg=color)


if __name__ == '__main__':
    num_colors = colorise.num_colors()

    colors = [8, 16, 88, 256, 2**24]
    idx = colors.index(num_colors)

    print('>>> Emulating preset colors for debugging')

    for color in ['red', 201, '#ff0000', 'rgb(24,151,87)']:
        print("Emulating foreground color '{0}'".format(color))
        emulate(num_colors, color, idx, colors)
        print()

    # color_names = colorise.get_color_names()
    random_colors = [
            # random.choice(color_names),
            'yellow',
            random.randint(0, 255),
            random_hex_color(),
            random_rgb_color()
        ]

    print('>>> Emulating random colors')

    for color in random_colors:
        print("Emulating foreground color '{0}'".format(color))
        emulate(num_colors, color, idx, colors)
        print()
