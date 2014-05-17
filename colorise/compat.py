# -*- coding: utf-8 -*-

"""Defines a small set of Python 2/3 compatibility functions and imports."""

__date__ = '2014-05-17'  # YYYY-MM-DD

import colorise
import itertools


if colorise._PY2:
    import types
    ClassType = types.ClassType
    ifilter = itertools.ifilter

    def iteritems(d):
        """Return an iterator over the key-value pairs of a dictionary."""
        return d.iteritems()
else:
    ClassType = type
    ifilter = filter

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
