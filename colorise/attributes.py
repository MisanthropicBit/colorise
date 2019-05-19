#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Attributes supported by colorise.

Depending on your terminal's capabilities, some of these attributes may have no
effect.

"""

import platform

try:
    from enum import Enum  # Python 3
except ImportError:
    from enum34 import Enum  # Python 2

_SYSTEM_OS = platform.system().lower()


class Attr(Enum):

    """Console attributes.

    Each attribute's value is defined via its ANSI escape code.

    """

    Reset = 0
    Bold = 1
    Intense = 1  # Alias from Windows terminology
    Faint = 2
    Italic = 3
    Underline = 4
    Blink = 5
    Reverse = 7


if 'windows' in _SYSTEM_OS:
    import colorise.win.cluts

    def to_codes(attributes):
        """Convert a set of attributes to Windows character attributes."""
        codes = [colorise.win.cluts.attributes().get(attr, None)[1]
                 for attr in attributes]

        return filter(None, codes)
else:
    def to_codes(attributes):
        """Convert a set of attributes to ANSI escape codes."""
        return [int(attr.value) for attr in attributes]


def attribute_from_name(attribute):
    """Return an attribute object from its name.

    E.g. 'bold' -> Attr.Bold

    """
    return Attr[attribute.title()]


def attribute_names():
    """Return a set of all attribute names."""
    return set(attr.name.lower() for attr in Attr)
