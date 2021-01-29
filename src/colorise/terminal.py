#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Terminal functions."""

import os


def terminal_name() -> str:
    """Return the name of the terminal."""
    return os.environ.get('TERM_PROGRAM', '')
