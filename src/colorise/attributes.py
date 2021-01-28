#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Attributes supported by colorise.

Depending on your terminal's capabilities, some of these attributes may have no
effect.

"""

from enum import Enum


class Attr(Enum):
    """Console attributes.

    Each attribute's value is defined via its ANSI escape code.

    """

    Reset = 0
    Bold = 1
    Intense = 1  # Alias for Bold from Windows terminology
    Faint = 2
    Italic = 3
    Underline = 4
    Blink = 5
    Reverse = 7

    @classmethod
    def from_name(cls, attribute):
        """Return an attribute object from its name.

        E.g. 'bold' -> Attr.Bold

        """
        return cls[attribute.title()]

    @classmethod
    def names(cls):
        """Return a set of all attribute names."""
        return set(attr.name.lower() for attr in cls)

    @classmethod
    def names_with_aliases(cls):
        """Return a set of all attribute names with aliases."""
        return set(attr.lower() for attr in cls.__members__)
