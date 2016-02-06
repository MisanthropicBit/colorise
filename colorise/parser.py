# -*- coding: utf-8 -*-

"""ColorFormatParser class which parses color formatted strings."""

import re
import colorsys
import itertools
import colorise.cluts
import colorise.compat

__date__ = '2016-02-06'  # YYYY-MM-DD

# Add support for:
# colorise.fprint("<fg=(255,0,0): Red>")
# colorise.fprint("<fg=hls(255,0,0): Color>")
# colorise.fprint("<fg=hsv(255,0,0): Color>")
# colorise.fprint("<bg=#8032ab: Color>")


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

    # Regexes for color specifications
    _INDEX_RE = re.compile('^\d+$')
    _RGB_RE = re.compile('^rgb\((\d{1,3},\d{1,3},\d{1,3})\)$')
    _HEX_RE = re.compile('^(0x)?(([0-9a-fA-F]{2}){3})$')
    _HSV_RE = re.compile('^hsv\((\d+,\d+,\d+)\)$')
    _HLS_RE = re.compile('^hls\((\d+,\d+,\d+)\)$')

    # Simple conversion table
    _COLOR_CONVERSIONS = {
        'hls': colorsys.hls_to_rgb,
        'hsv': colorsys.hsv_to_rgb
    }

    def __init__(self):
        """Initialize the parser."""
        tstr = "".join([self._START_TOKEN, self._FMT_TOKEN, self._STOP_TOKEN])
        s = r"(({0}+)?([{1}]))".format(re.escape(self._ESCAPE), tstr)
        self._pattern = re.compile(s)

    def tokenize(self, string):
        """Tokenize a string and return an iterator over its tokens."""
        it = colorise.compat.ifilter(None, self._pattern.finditer(string))

        try:
            t = colorise.compat.next(it)
        except StopIteration:
            yield string, False
            return

        pos, buf, lm, escapeflag = -1, '', -1, False

        # Check if we need to yield any starting text
        if t.start() > 0:
            yield string[:t.start()], False
            pos = t.start()

        it = itertools.chain([t], it)

        for m in it:
            start = m.start()
            e, s = m.group(2) or '', m.group(3)
            escaped = e.count(self._ESCAPE) % 2 != 0

            if escaped:
                buf += string[pos:m.end(2)-1] + s
                escapeflag = True
            else:
                buf += string[pos:m.start(3)]

                if buf:
                    yield buf, escapeflag
                    buf = ''
                    escapeflag = False

                if lm == start:
                    yield '', False

                yield s, False
                lm = m.end()

            pos = m.end()

        if buf:
            yield buf, escapeflag
            escapeflag = False

        if pos < len(string):
            yield string[pos:], False

    def parse(self, format_string):
        """Parse color syntax from a formatted string."""
        txt, state = '', 0
        colorstack = [(None, None)]
        itokens = self.tokenize(format_string)

        for token, escaped in itokens:
            if token == self._START_TOKEN and not escaped:
                if txt:
                    yield txt, colorstack[-1]
                    txt = ''

                state += 1
                colors = self.extract_syntax(colorise.compat.next(itokens)[0])
                colorstack.append(tuple(b or a
                                        for a, b in zip(colorstack[-1],
                                                        colors)))
            elif token == self._FMT_TOKEN and not escaped:
                # if state == 0:
                #     raise ColorSyntaxError("Missing '{0}'"
                #                            .format(self._START_TOKEN))

                if state % 2 != 0:
                    state += 1
                else:
                    txt += token
            elif token == self._STOP_TOKEN and not escaped:
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

    def _to_rgb(self, fromspace, a, b, c):
        """Convert from one colorspace to RGB."""
        if fromspace == 'rgb':
            return a, b, c

        if fromspace not in self._COLOR_CONVERSIONS:
            raise ColorSyntaxError("Unsupported color space '{0}'"
                                   .format(fromspace))

        self._COLOR_CONVERSIONS[fromspace](a, b, c)

    def extract_syntax1(self, syntax):
        """Parse and extract color/markup syntax from a format string."""
        tokens = syntax.split(self._COLOR_DELIM)
        r = [None, None]

        for token in tokens:
            for i, e in enumerate('fg=', 'bg='):
                if token.startswith(e):
                    if r[i] is not None:
                        raise ColorSyntaxError("Multiple color definitions of"
                                               " {}".format(e[:-1]))

                    r[i] = token[3:]

        # Convert colors if necessary
        for i, color in enumerate(r):
            if color is not None:
                if color.isalpha():
                    r[i] = color
                elif self._INDEX_RE.match(color):
                    r[i] = int(color)

                m = self._HEX_RE()
                if self._HEX_RE.match(color):
                    r[i] = colorise.cluts.get_approx_color(
                        *[int(color[i:i+2], 16) for i in range(0, 6, 2)])
                    continue

                m = self._HSV_RE.match(color)
                if m:
                    r[i] = colorise.cluts.get_approx_color(
                        self._to_rgb('hsv', m.group(1).split(',')))
                    continue
                else:
                    m = self._HLS_RE.match(color)
                    if m:
                        r[i] = colorise.cluts.get_approx_color(
                            self._to_rgb('hls', m.group(1).split(',')))
                        continue

                raise ColorSyntaxError('Unrecognised color format: {}'
                                       .format(color))

        return tuple(r)
