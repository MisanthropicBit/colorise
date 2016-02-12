# -*- coding: utf-8 -*-

"""A color manager class for Linux/Unix platforms."""

import sys
import colorise.compat
import colorise.decorators
from colorise.base_color_manager import BaseColorManager


@colorise.decorators.inherit_docstrings
class ColorManager(BaseColorManager):

    """Linux/Unix color manager class that uses ANSI escape sequences."""

    def __init__(self):
        colornames = ['black', 'red', 'green', 'yellow', 'blue', 'magenta',
                      'cyan', 'white']

        self.colors = dict()

        # Set up grayscale values
        self.colors['grey'] = 7
        self.colors[colornames[0]] = 30
        self.colors[colornames[-1]] = 37

        # Define ANSI color codes
        for i, name in enumerate(colornames[1:7], 31):
            self.colors[name] = i
            self.colors['dark'+name] = self.colors[name]

        # Set up color aliases
        self.colors['gray'] = self.colors['grey']
        self.colors['purple'] = self.colors['magenta']
        self.colors['darkpurple'] = self.colors['darkmagenta']

    def _to_ansi(self, *codes):
        """Convert a set of ANSI codes into a valid ANSI sequence."""
        return '\x1b[' + ';'.join(map(str, codes)) + 'm'

    def set_defaults(self):
        sys.stdout.write(self._to_ansi(22, 39, 49))

    def get_defaults(self):
        """Not implemented for ANSI sequences. Returns an empty list."""
        # Note: Throw instead?
        return []

    def get_supported(self):
        return ([fg for fg in self.colors.keys()],
                [bg for bg in self.colors.keys() if not bg.startswith('dark')])

    def set_color(self, fg=None, bg=None):
        codes = ['', '']

        # Move syntax extraction out here
        if fg or bg:
            for i, c in enumerate([fg, bg]):
                if c is not None and type(c) not in (int, tuple):
                    raise ValueError("Unknown color '{0}'".format(c))

                codes[i] = '' if c is None else str(30 * (i + 1) + c)

                if c > 7:
                    if c <= 256:
                        codes[i] = '{};5;{}'.format(38 * (i + 1), c)
                    else:
                        # RGB capability
                        if type(c) is tuple and len(c) != 3:
                            raise ValueError("RGB tuple must contain 3 "
                                             "elements")

                        # Note: Untested!
                        codes[i] = '{};2;{}'.format(38 * (i + 1),
                                                    ";".join(map(str, c)))

            sys.stdout.write(self._to_ansi(*codes))
        else:
            self.set_defaults()
