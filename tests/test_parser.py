#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""py.test file for testing the ColorFormatParser class."""

__date__ = "2014-06-11"  # YYYY-MM-DD

import pytest
from colorise.ColorFormatParser import ColorFormatParser, ColorSyntaxError


class TestColorFormatParser(object):

    """Test color formatting."""

    def test_formats(self):
        parser = ColorFormatParser()

        # Test cases which should not fail
        ok_tests = ["Some text <fg=darkred:and color>",
                    "<fg=red:Searching> for '{item}'",
                    "<fg=red:Searching for <bg=blue:'{item}'> in database...>",
                    "T<fg=green:he> ch<fg=green:ang>es are h<fg=green:i>ghli<f"
                    "g=green:g>hted",
                    "\<This should \:not be parsed\>",
                    "This has no color, but <fg=yellow:this is yellow>, and "
                    "back to no color",
                    "<fg=yellow:This is yellow :3>",
                    "<fg=darkblue:>",  # This is still valid
                    "Just some text"]

        ok_tests_results = [(('Some text ', (None, None)),
                             ('and color', ('darkred', None))),
                            (('Searching', ('red', None)),
                             (" for '{item}'", (None, None))),
                            (('Searching for ', ('red', None)),
                             ("'{item}'", ('red', 'blue')),
                             (' in database...', ('red', None))),
                            (('T', (None, None)),
                             ('he', ('green', None)),
                             (' ch', (None, None)),
                             ('ang', ('green', None)),
                             ('es are h', (None, None)),
                             ('i', ('green', None)),
                             ('ghli', (None, None)),
                             ('g', ('green', None)),
                             ('hted', (None, None))),
                            (('<This should :not be parsed>', (None, None)),),
                            (('This has no color, but ', (None, None)),
                             ('this is yellow', ('yellow', None)),
                             (', and back to no color', (None, None))),
                            (('This is yellow :3', ('yellow', None)),),
                            (()),
                            (('Just some text', (None, None)),)]

        for test, result in zip(ok_tests, ok_tests_results):
            assert tuple(parser.parse(test)) == result

        # Test cases which should fail
        fail_tests = ["fg=red:fail>",  # Missing start token
                      "<fg=redfail>",  # Missing format token
                      "<fg=red:fail",  # Missing stop token
                      "<fg=red:I forgot to '<' escape>",  # Forgot to escape
                                                          # '<'
                      "<fg=red:I forgot to '<' escape>"]  # Same, but with '>'

        for test in fail_tests:
            with pytest.raises(ColorSyntaxError):
                list(parser.parse(test))
