#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Class for Windows handles."""

import sys
from ctypes import wintypes


class WinHandle:
    """Represents a Windows stream handle."""

    STDOUT = -11
    STDERR = -12
    INVALID = wintypes.HANDLE(-1).value

    def __init__(self, handle):
        """Initialise the Windows handle."""
        self._handle = handle
        self._fg = -1
        self._bg = -1
        self._default_fg = -1
        self._default_bg = -1
        self._console_mode = 0
        self._is_console_handle = False

    @classmethod
    def validate(cls, handle):
        """Check if a handle is valid to colorise."""
        return handle in (cls.STDOUT, cls.STDERR)

    @classmethod
    def from_sys_handle(cls, syshandle):
        """Return the handle identifier for a python handle."""
        if syshandle is sys.stdout:
            return cls.STDOUT
        elif syshandle is sys.stderr:
            return cls.STDERR
        else:
            return cls.INVALID

    @classmethod
    def get_nonconsole_handle(cls, handle):
        """Get a handle that works for non-console output streams."""
        nonconsole_handle = cls(handle)

        nonconsole_handle.fg = 0
        nonconsole_handle.bg = 0
        nonconsole_handle.default_fg = 0
        nonconsole_handle.default_bg = 0
        nonconsole_handle.is_console_handle = 0

        return nonconsole_handle

    @property
    def valid(self):
        """True if the handle is valid, False otherwise."""
        return self._handle != WinHandle.INVALID

    @property
    def value(self):
        """Return the internal Windows handle value."""
        return self._handle

    @property
    def is_console_handle(self):
        """If the handle is a valid console handle."""
        return self._is_console_handle

    @is_console_handle.setter
    def is_console_handle(self, value):
        self._is_console_handle = value

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
