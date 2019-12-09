#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Class for Windows handles."""


class WinHandle:
    """Represents a Windows stream handle."""

    def __init__(self, handle):
        """Initialise the Windows handle."""
        self._handle = handle
        self._console_mode = 0
        self._fg = -1
        self._bg = -1
        self._default_fg = -1
        self._default_bg = -1

    @property
    def handle(self):
        """Return the internal Windows handle."""
        return self._handle

    @property
    def fg(self):
        """Return the current foreground color set for the handle."""
        return self._fg

    @fg.setter
    def fg(self, value):
        self._fg = value

    @property
    def bg(self):
        """Return the current background color set for the handle."""
        return self._bg

    @bg.setter
    def bg(self, value):
        self._bg = value

    @property
    def default_fg(self):
        """Return the default foreground color set for the handle."""
        return self._default_fg

    @default_fg.setter
    def default_fg(self, value):
        self._default_fg = value

    @property
    def default_bg(self):
        """Return the default background color set for the handle."""
        return self._default_bg

    @default_bg.setter
    def default_bg(self, value):
        self._default_bg = value

    @property
    def console_mode(self):
        """Return the current console mode for the handle."""
        return self._console_mode

    @console_mode.setter
    def console_mode(self, value):
        self._console_mode = value

    def __str__(self):
        return "{0}({1}, {2})".format(self.__class__.__name__,
                                      self.fg, self.bg)
