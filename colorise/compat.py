# -*- coding: utf-8 -*-

"""Defines a small set of Python 2/3 compatibility functions and imports."""

__date__ = '2014-05-08'  # YYYY-MM-DD

import sys
import colorise


if colorise._PY2:
    import types
    ClassType = types.ClassType

    def iteritems(d):
        """Return an iterator over the key-value pairs of a dictionary."""
        return d.iteritems()
else:
    ClassType = type

    def iteritems(d):
        """Return an iterator over the key-value pairs of a dictionary."""
        return d.items()


try:
    next = next
except NameError:
    # Define a next function for Python < 2.6
    def _next(it):
        return it.next()

    next = _next
