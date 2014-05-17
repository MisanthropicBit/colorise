# -*- coding: utf-8 -*-

"""ColorFormatParser class which parses color formatted strings."""

__date__ = '2014-05-08'  # YYYY-MM-DD

import re
import itertools
import colorise.compat


class ColorSyntaxError(SyntaxError):

    """Thrown when incorrectly formatted color syntax is encountered."""

    pass


class ColorFormatParser(object):

    """Parses color formatted strings."""

    _START_TOKEN = '<'
    _FMT_TOKEN = ':'
    _STOP_TOKEN = '>'
    _COLOR_DELIM = ','
    _ESCAPE = '\\'

    def __init__(self):
        """Initialize the parser."""
        tstr = "".join([self._START_TOKEN, self._FMT_TOKEN, self._STOP_TOKEN])
        s = r"(({0}+)?([{1}]))".format(re.escape(self._ESCAPE), tstr)
        self._pattern = re.compile(s)

    def tokenize(self, string):
        """Tokenize a string and return an iterator over its tokens."""
        pos, buf, lm = -1, '', -1
        it = colorise.compat.ifilter(None, self._pattern.finditer(string))
        t = colorise.compat.next(it)

        # Check if we need to yield any starting text
        if t.start() > 0:
            yield string[:t.start()]
            pos = t.start()

        it = itertools.chain([t], it)

        for m in it:
            start = m.start()
            e, s = m.group(2) or '', m.group(3)
            escaped = e.count(self._ESCAPE) % 2 != 0

            if escaped:
                buf += string[pos:m.end(2)-1] + s
            else:
                buf += string[pos:m.start(3)]

                if buf:
                    yield buf
                    buf = ''

                if lm == start:
                    yield ''

                yield s
                lm = m.end()

            pos = m.end()

        if buf:
            yield buf

        if pos < len(string):
            yield string[pos:]

    def parse(self, format_string):
        """Parse color syntax from a formatted string."""
        txt, state = '', 0
        colorstack = [(None, None)]
        itokens = self.tokenize(format_string)

        for token in itokens:
            if token == self._START_TOKEN:
                if txt:
                    yield txt, colorstack[-1]
                    txt = ''

                state += 1
                colors = self.extract_syntax(colorise.compat.next(itokens))
                colorstack.append(tuple(b or a
                                        for a, b in zip(colorstack[-1],
                                                        colors)))
            elif token == self._FMT_TOKEN:
                if state == 0:
                    raise ColorSyntaxError("Missing '{0}'"
                                           .format(self._START_TOKEN))

                if state % 2 != 0:
                    state += 1
                else:
                    txt += token
            elif token == self._STOP_TOKEN:
                if state < 2:
                    raise ColorSyntaxError("Missing '{0}' or '{1}'"
                                           .format(self._STOP_TOKEN,
                                                   self._FMT_TOKEN))

                if txt:
                    yield txt, colorstack[-1]
                    txt = ''

                state -= 2
                colorstack.pop()
            else:
                txt += token

        if state != 0:
            raise ColorSyntaxError("Invalid color format")

        if txt:
            yield txt, colorstack[-1]

    def extract_syntax(self, syntax):
        """Parse and extract color/markup syntax from a format string."""
        tokens = syntax.split(self._COLOR_DELIM)
        r = [None, None]

        for token in tokens:
            for i, e in enumerate(('fg=', 'bg=')):
                if token.startswith(e):
                    r[i] = token[3:]

            if r == [None, None]:
                raise ColorSyntaxError("Unexpected color syntax '{0}'"
                                       .format(token))

        return tuple(r)
