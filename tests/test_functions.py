# -*- coding: utf-8 -*-

"""py.test file for testing the colorise's testable public functions."""

__date__ = "2014-05-17"  # YYYY-MM-DD

import sys
sys.path.append('.')
import colorise


formattests = [({'bg': 'yellow'},
                "Yellow like the sun!",
                "<bg=yellow:Yellow like the sun!>"),
               ({'fg': 'red', 'bg': 'darkgreen'},
                "This should be formatted with red foreground and darkgreen "
                "background",
                "<fg=red,bg=darkgreen:This should be formatted "
                "with red foreground and darkgreen background>")]


iformattests = [({'fg': 'blue', 'bg': 'cyan',
                  'indices': [29, 4, 27, 5, 17, 31, 10, 11, 19, 26]},
                 "Format me in pretty colors, please",
                 "Form<fg=blue,bg=cyan:at> me <fg=blue,bg=cyan:in> "
                 "pret<fg=blue,bg=cyan:t>y<fg=blue,bg=cyan: >colors<fg=blue,"
                 "bg=cyan:, >p<fg=blue,bg=cyan:l>e<fg=blue,bg=cyan:a>se"),
                ({'bg': 'purple', 'indices': [0, 12, 6, 4, 7]},
                 "What indices?",
                 "<bg=purple:W>hat<bg=purple: >i"
                 "<bg=purple:nd>ices<bg=purple:?>")]


def test_formatting():
    """Test formatting."""
    for formattest in formattests:
        assert colorise.formatcolor(formattest[1],
                                    **formattest[0]) == formattest[2]


def test_formattingbyindex():
    """Test formatting by index."""
    for iformattest in iformattests:
        assert colorise.formatbyindex(iformattest[1],
                                      **iformattest[0]) == iformattest[2]
