#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test all Python 3 formatting examples without colors.

These tests ensure that colorise produces the visually same result as
str.format() would, with and without color format specifications.

See the documentation at:
https://docs.python.org/3.8/library/string.html#formatexamples.

"""

import colorise
import datetime
from io import StringIO
import pytest
import os
import sys

class Point:  # noqa
    def __init__(self, x, y):  # noqa
        self.x, self.y = x, y

    def test_without_colors(self):  # noqa
        assert_colored_output(
            colorise.fprint,
            'Point(4, 2)',
            'Point({self.x}, {self.y})',
            self=self
        )

    def test_with_colors(self):  # noqa
        assert_colored_output(
            colorise.fprint,
            'Point(\x1b[1m4\x1b[0m, \x1b[0m\x1b[5m\x1b[41m2\x1b[0m)',
            'Point({self.x:intense}, {self.y:blink;bg=red})',
            self=self
        )

    def __str__(self):  # noqa
        return 'Point({self.x}, {self.y})'.format(self=self)


def assert_colored_output(func, expected, fmt, *args, **kwargs):
    """Call func to get colored output and compare it to an expected result."""
    sio = StringIO()

    with pytest.redirect_stdout(sio):
        func(fmt, *args, **kwargs, file=sys.stdout)
        assert sio.getvalue() == '\x1b[0m' + expected + '\x1b[0m' + os.linesep


def test_fprint_python_formatting_examples_positions_no_color():
    """Test all Python 3 formatting examples without colors."""
    assert_colored_output(
        colorise.fprint,
        'a, b, c',
        '{0}, {1}, {2}',
        'a', 'b', 'c'
    )

    assert_colored_output(
        colorise.fprint,
        'a, b, c',
        '{}, {}, {}',
        'a', 'b', 'c'
    )

    assert_colored_output(
        colorise.fprint,
        'c, b, a',
        '{2}, {1}, {0}',
        'a', 'b', 'c'
    )

    assert_colored_output(
        colorise.fprint,
        'c, b, a',
        '{2}, {1}, {0}',
        *'abc'
    )

    assert_colored_output(
        colorise.fprint,
        'abracadabra',
        '{0}{1}{0}',
        'abra',
        'cad'
    )


def test_fprint_python_formatting_examples_keyword_arguments_no_color():
    assert_colored_output(
        colorise.fprint,
        'Coordinates: 37.24N, -115.81W',
        'Coordinates: {latitude}, {longitude}',
        latitude='37.24N',
        longitude='-115.81W'
    )

    coord = {'latitude': '37.24N', 'longitude': '-115.81W'}

    assert_colored_output(
        colorise.fprint,
        'Coordinates: 37.24N, -115.81W',
        'Coordinates: {latitude}, {longitude}',
        **coord,
    )


def test_fprint_python_formatting_examples_attributes_no_color():
    c = 3 - 5j

    assert_colored_output(
        colorise.fprint,
        'The complex number (3-5j) is formed from the real part 3.0 and the '
        'imaginary part -5.0.',
        'The complex number {0} is formed from the real part '
        '{0.real} and the imaginary part {0.imag}.',
        c,
    )

    point = Point(4, 2)
    point.test_without_colors()


def test_fprint_python_formatting_examples_indexing_no_color():
    coord = (3, 5)

    assert_colored_output(
        colorise.fprint,
        'X: 3;  Y: 5',
        'X: {0[0]};  Y: {0[1]}',
        coord
    )


def test_fprint_python_formatting_examples_repr_str_no_color():
    assert_colored_output(
        colorise.fprint,
        "repr() shows quotes: 'test1'; str() doesn't: test2",
        "repr() shows quotes: {!r}; str() doesn't: {!s}",
        'test1',
        'test2'
    )


def test_fprint_python_formatting_examples_alignments_no_color():
    assert_colored_output(
        colorise.fprint,
        'left aligned                  ',
        '{:<30}',
        'left aligned'
    )

    assert_colored_output(
        colorise.fprint,
        '                 right aligned',
        '{:>30}',
        'right aligned'
    )

    assert_colored_output(
        colorise.fprint,
        '           centered           ',
        '{:^30}',
        'centered'
    )

    assert_colored_output(
        colorise.fprint,
        '***********centered***********',
        '{:*^30}',
        'centered'
    )


def test_fprint_python_formatting_examples_floating_point_signs_no_color():
    assert_colored_output(
        colorise.fprint,
        '+3.140000; -3.140000',
        '{:+f}; {:+f}',
        3.14,
        -3.14
    )

    assert_colored_output(
        colorise.fprint,
        ' 3.140000; -3.140000',
        '{: f}; {: f}',
        3.14,
        -3.14
    )

    assert_colored_output(
        colorise.fprint,
        '3.140000; -3.140000',
        '{:-f}; {:-f}',
        3.14,
        -3.14
    )


def test_fprint_python_formatting_examples_conversions_no_color():
    assert_colored_output(
        colorise.fprint,
        'int: 42;  hex: 2a;  oct: 52;  bin: 101010',
        'int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}',
        42
    )


def test_fprint_python_formatting_examples_thousand_separator_no_color():
    assert_colored_output(
        colorise.fprint,
        '1,234,567,890',
        '{:,}',
        1234567890
    )


def test_fprint_python_formatting_examples_percentages_no_color():
    points = 19
    total = 22

    assert_colored_output(
        colorise.fprint,
        'Correct answers: 86.36%',
        'Correct answers: {:.2%}',
        points/total
    )


def test_fprint_python_formatting_examples_datetimes_no_color():
    dt = datetime.datetime(2010, 7, 4, 12, 15, 58)

    assert_colored_output(
        colorise.fprint,
        '2010-07-04;12:15:58',
        '{:%Y-%m-%d;%H:%M:%S}',
        dt
    )


def test_fprint_python_formatting_examples_nested_no_color():
    tests = zip(
        '<^>',
        ['left', 'center', 'right'],
        ['left<<<<<<<<<<<<', '^^^^^center^^^^^', '>>>>>>>>>>>right']
    )

    for align, text, expected in tests:
        assert_colored_output(
            colorise.fprint,
            expected,
            '{0:{fill}{align}16}',
            text,
            fill=align,
            align=align
        )


def test_fprint_python_formatting_examples_hex_no_color():
    octets = [192, 168, 0, 1]

    assert_colored_output(
        colorise.fprint,
        'C0A80001',
        '{:02X}{:02X}{:02X}{:02X}',
        *octets
    )

    # width = 5
    # i = 0
    # expected_results = [
    #     '    5'
    #     '    5'
    #     '    5'
    #     '  101'
    #     '    6'
    #     '    6'
    #     '    6'
    #     '  110'
    #     '    7'
    #     '    7'
    #     '    7'
    #     '  111'
    #     '    8'
    #     '    8'
    #     '   10'
    #     ' 1000'
    #     '    9'
    #     '    9'
    #     '   11'
    #     ' 1001'
    #     '   10'
    #     '    A'
    #     '   12'
    #     ' 1010'
    #     '   11'
    #     '    B'
    #     '   13'
    #     ' 1011'
    # ]

    # for num in range(5, 12):
    #     for base in 'dXob':
    #         expected = expected_results[i]
    #         i += 1

    #         assert_colored_output(
    #             colorise.fprint,
    #             expected,
    #             '{0:{width}{base}}',
    #             num,
    #             base=base,
    #             width=width,
    #             end=' '
    #         )


def test_fprint_python_formatting_examples_positions_color():
    assert_colored_output(
        colorise.fprint,
        '\x1b[31ma\x1b[0m, \x1b[0m\x1b[34m\x1b[42mb\x1b[0m, '
        '\x1b[0m\x1b[1mc\x1b[0m',
        '{0:fg=red}, {1:bg=green;fg=blue}, {2:bold}',
        'a', 'b', 'c'
    )

    assert_colored_output(
        colorise.fprint,
        '\x1b[35ma\x1b[0m, \x1b[0m\x1b[34m\x1b[42mb\x1b[0m, '
        '\x1b[0m\x1b[3mc\x1b[0m',
        '{:fg=purple}, {:bg=green;fg=blue}, {:italic}',
        'a', 'b', 'c'
    )

    assert_colored_output(
        colorise.fprint,
        '\x1b[1m\x1b[35mc\x1b[0m, \x1b[0m\x1b[45mb\x1b[0m, '
        '\x1b[0m\x1b[2ma\x1b[0m',
        '{2:fg=purple;bold}, {1:bg=magenta}, {0:faint}',
        'a', 'b', 'c'
    )

    assert_colored_output(
        colorise.fprint,
        '\x1b[7mc\x1b[0m, \x1b[0m\x1b[36mb\x1b[0m, '
        '\x1b[0m\x1b[35m\x1b[42ma\x1b[0m',
        '{2:reverse}, {1:fg=cyan}, {0:bg=green;fg=purple}',
        *'abc'
    )

    assert_colored_output(
        colorise.fprint,
        '\x1b[31mabra\x1b[0m\x1b[1mcadabra',
        '{fg=red}{0}{bold}{1}{0}',
        'abra',
        'cad'
    )

    assert_colored_output(
        colorise.fprint,
        '\x1b[31mabra\x1b[1mcadabra',
        '{fg=red}{0}{bold}{1}{0}',
        'abra',
        'cad',
        autoreset=False
    )


def test_fprint_python_formatting_examples_keyword_arguments_color():
    assert_colored_output(
        colorise.fprint,
        '\x1b[1mCoordinates:\x1b[0m \x1b[0m\x1b[34m37.24N\x1b[0m, '
        '\x1b[0m\x1b[32m-115.81W\x1b[0m',
        '{bold}Coordinates:{reset} {latitude:fg=blue}, {longitude:fg=green}',
        latitude='37.24N', longitude='-115.81W'
    )

    coord = {'latitude': '37.24N', 'longitude': '-115.81W'}

    assert_colored_output(
        colorise.fprint,
        '\x1b[1mCoordinates:\x1b[0m \x1b[0m\x1b[34m37.24N\x1b[0m, '
        '\x1b[0m\x1b[32m-115.81W\x1b[0m',
        '{bold}Coordinates:{reset} {latitude:fg=blue}, {longitude:fg=green}',
        **coord
    )


def test_fprint_python_formatting_examples_attributes_color():
    c = 3 - 5j

    assert_colored_output(
        colorise.fprint,
        'The complex number \x1b[1m(3-5j)\x1b[0m is formed from the '
        'real part \x1b[0m\x1b[1m\x1b[31m3.0\x1b[0m and the imaginary part '
        '\x1b[0m\x1b[91m-5.0\x1b[0m.',
        'The complex number {0:bold} is formed from the real part '
        '{0.real:fg=red;bold} and the imaginary part {0.imag:fg=lightred}.',
        c
    )

    point = Point(4, 2)
    point.test_with_colors()


def test_fprint_python_formatting_examples_indexing_color():
    coord = (3, 5)

    assert_colored_output(
        colorise.fprint,
        'X: \x1b[1;4m\x1b[35m3\x1b[0m;  \x1b[0m\x1b[31mY: 5',
        'X: {0[0]:fg=purple;bold;underline};  {fg=red}Y: {0[1]}',
        coord
    )


def test_fprint_python_formatting_examples_repr_str_color():
    assert_colored_output(
        colorise.fprint,
        "repr() shows quotes: \x1b[31m'test1'\x1b[0m; "
        "str\x1b[0m\x1b[32m() doesn\'t: \x1b[0m\x1b[1m\x1b[33mtest2\x1b[0m",
        "repr() shows quotes: {!r:fg=red}; str{fg=green}() "
        "doesn't: {!s:fg=yellow;bold}",
        'test1',
        'test2'
    )


def test_fprint_python_formatting_examples_alignments_color():
    assert_colored_output(
        colorise.fprint,
        '\x1b[91mleft aligned                  \x1b[0m',
        '{:fg=lightred;<30}',
        'left aligned'
    )

    assert_colored_output(
        colorise.fprint,
        '\x1b[102m                 right aligned\x1b[0m',
        '{:>30;bg=lightgreen}',
        'right aligned'
    )

    assert_colored_output(
        colorise.fprint,
        '\x1b[103m           centered           \x1b[0m',
        '{:bg=lightyellow;^30}',
        'centered'
    )

    assert_colored_output(
        colorise.fprint,
        '\x1b[95m\x1b[41m***********centered***********\x1b[0m',
        '{:*^30;fg=lightpurple;bg=red}',
        'centered'
    )


def test_fprint_python_formatting_examples_floating_point_signs_color():
    assert_colored_output(
        colorise.fprint,
        '\x1b[31m\x1b[0m\x1b[1m\x1b[42m+3.140000\x1b[0m; '
        '\x1b[0m\x1b[34m-3.140000\x1b[0m',
        '{fg=red}{:+f;bg=green;bold}; {:+f;fg=blue}',
        3.14,
        -3.14
    )

    assert_colored_output(
        colorise.fprint,
        '\x1b[31m\x1b[0m\x1b[1m\x1b[42m 3.140000\x1b[0m; '
        '\x1b[0m\x1b[34m-3.140000\x1b[0m',
        '{fg=red}{: f;bg=green;bold}; {: f;fg=blue}',
        3.14,
        -3.14
    )

    colorise.fprint('{fg=red}{:+f;bg=green;bold}; {:+f;fg=blue}', 3.14, -3.14,
                    autoreset=False)
    colorise.fprint('{bold}{: f}; {:fg=red; f}', 3.14, -3.14)
    colorise.fprint('{bold}{:-f}; {:fg=red;-f}', 3.14, -3.14, autoreset=False)
    assert_colored_output(
        colorise.fprint,
        '\x1b[31m\x1b[0m\x1b[1m\x1b[42m3.140000\x1b[0m; '
        '\x1b[0m\x1b[34m-3.140000\x1b[0m',
        '{fg=red}{:-f;bg=green;bold}; {:-f;fg=blue}',
        3.14,
        -3.14
    )


def test_fprint_python_formatting_examples_conversions_color():
    assert_colored_output(
        colorise.fprint,
        'int: \x1b[36m42\x1b[0m;  hex: 0x2a;  oct: 0o52;  bin: 0b101010',
        'int: {0:d;fg=cyan};  hex: {0:#x};  oct: {0:#o};  bin: {0:#b}',
        42
    )

    assert_colored_output(
        colorise.fprint,
        '\x1b[36mint: \x1b[33m42;  hex: \x1b[45m0x2a;  oct\x1b[44m: 0o52;  '
        'bin: 0b101010',
        '{fg=cyan}int: {0:d;fg=yellow};  hex: {0:#x;bg=purple};  '
        'oct{bg=blue}: {0:#o};  bin: {0:#b}',
        42,
        autoreset=False
    )


def test_fprint_python_formatting_examples_thousand_separator_color():
    assert_colored_output(
        colorise.fprint,
        '\x1b[1;5m\x1b[36m1,234,567,890\x1b[0m',
        '{:,;fg=cyan;bold;blink}',
        1234567890
    )


def test_fprint_python_formatting_examples_percentages_color():
    points = 19
    total = 22

    assert_colored_output(
        colorise.fprint,
        'Correct answers: \x1b[31m\x1b[42m86.36%\x1b[0m',
        'Correct answers: {:fg=red;.2%;bg=green}',
        points/total
    )


def test_fprint_python_formatting_examples_datetimes_color():
    dt = datetime.datetime(2010, 7, 4, 12, 15, 58)

    assert_colored_output(
        colorise.fprint,
        '\x1b[1;3m\x1b[34m2010-07-04;12:15:58\x1b[0m',
        '{:fg=blue;intense;italic;%Y-%m-%d;%H:%M:%S}',
        dt
    )


def test_fprint_python_formatting_examples_nested_color():
    # tests = zip(
    #     '<^>',
    #     ['left', 'center', 'right'],
    #     ['red', 'green', 'blue'],
    #     [
    #         '\x1b[1m\x1b31mleft<<<<<<<<<<<<\x1b[0m',
    #         '\x1b[1m\x1b32m^^^^^center^^^^^\x1b[0m',
    #         '\x1b[1m\x1b34m>>>>>>>>>>>right\x1b[0m'
    #     ]
    # )

    # for align, text, color, expected in tests:
    #     assert_colored_output(
    #         colorise.fprint,
    #         expected,
    #         '{0:bold;{fill}{align}16;fg={color}}',
    #         text,
    #         fill=align,
    #         align=align,
    #         color=color
    #     )
    pass


def test_fprint_python_formatting_examples_hex_color():
    octets = [192, 168, 0, 1]

    assert_colored_output(
        colorise.fprint,
        '\x1b[1m\x1b[31mC0\x1b[34mA8\x1b[33m00\x1b[32m01',
        '{bold}{:fg=red;02X}{:fg=blue;02X}{:fg=yellow;02X}{:02X;fg=green}',
        *octets,
        autoreset=False
    )

    # colorise.fprint('{fg=red}text {0:bg=green} text', 'text')
    # colorise.fprint('{fg=red}text {0:bg=green} text', 'text', autoreset=False)
