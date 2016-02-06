# -*- coding: utf-8 -*-

"""Base class for platform specific color managers."""

import sys


class BaseColorManager(object):

    """Base class for platform-specific color managers."""

    def __init__(self):
        """Initialize the color manager."""
        pass

    def _onerror(self):
        """Handle platform-specific errors."""
        raise NotImplementedError

    def set_defaults(self, target=sys.stdout):
        """Set the default colors."""
        pass

    def get_defaults(self, target=sys.stdout):
        """Return a tuple of default foreground and background color."""
        raise NotImplementedError

    def get_supported(self):
        """Return the names of all supported colors."""
        raise NotImplementedError

    def set_color(self, fg=None, bg=None, intensify=False, target=sys.stdout):
        """Set foreground- and background colors and intensity."""
        raise NotImplementedError
