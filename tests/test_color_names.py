#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test default color names."""

import colorise


def test_color_names():
    assert set(colorise.color_names()) == set([
        'black',
        'red',
        'green',
        'yellow',
        'blue',
        'purple',
        'magenta',
        'cyan',
        'gray',
        'grey',
        'lightgrey',
        'lightgray',
        'lightred',
        'lightgreen',
        'lightyellow',
        'lightblue',
        'lightpurple',
        'lightmagenta',
        'lightcyan',
        'white',
    ])
