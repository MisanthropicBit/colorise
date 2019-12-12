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
        if fg or bg:
            for i, [prefix, value] in [colorise.cluts.color_code(c, b)
                                       for c, b in zip([fg, bg],
                                                       [False, True])]:
                if value:
                    sys.stdout.write(prefix.format(value))
        else:
            self.set_defaults()
