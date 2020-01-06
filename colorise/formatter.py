#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ColorFormatter class for colorise.fprint.

This class extends the string.Formatter class.

"""

import string
from colorise.attributes import Attr


class ColorFormatter(string.Formatter):

    """Class for formatting strings containing color syntax.

    As opposed to an ordinary derived string.Formatter, this one does not
    construct and return a formatted string but immediately outputs the
    formatted string. This is necessary to support Windows consoles that cannot
    interpret ANSI escape sequences since they have no way of embedding colors
    into strings but instead set colors through an API call.

    """

    def __init__(self, set_color_func, reset_func):
        """Initialise the color formatter.

        Two OS-dependent functions are passed in for setting and resetting the
        color.

        """
        super().__init__()

        self._autoreset = False
        self._file = None
        self._enabled = True
        self._set_color_func = set_color_func
        self._reset_func = reset_func
        self._attribute_names = Attr.names_with_aliases()

    @property
    def autoreset(self):
        """If True, automatically reset before each color format field."""
        return self._autoreset

    @autoreset.setter
    def autoreset(self, value):
        self._autoreset = value

    @property
    def file(self):
        """The target output handle of the formatter."""
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    @property
    def enabled(self):
        """Whether colors are enabled or not."""
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    def parse(self, format_string):
        """Parse a format string and generate tokens."""
        # Flush any remaining stuff before resetting colors
        self.file.flush()
        self._reset_func(self.file)

        first_format = True
        tokens = super().parse(format_string)

        for literal_text, field_name, format_spec, conversion in tokens:
            fg, fg_attrs, bg, bg_attrs = self._parse_color_format(field_name)

            if fg or fg_attrs or bg or bg_attrs:
                # Emit any literal text
                yield literal_text, None, None, None

                # Automatically reset colors and attributes if enabled and if
                # it is not the first format we encounter
                if self.autoreset and not first_format:
                    self._reset_func(self.file)

                # Set colors and attributes
                if self.enabled:
                    self._set_color_func(fg, bg, fg_attrs + bg_attrs,
                                         self.file)
            else:
                # Yield tokens as normal
                yield literal_text, field_name, format_spec, conversion

            first_format = False

    def _parse_color_format(self, colors):
        """Parse and extract the color format from a format field."""
        result = [None, [], None, []]

        if not colors:
            return result

        is_fg = False

        for color in colors.split(','):
            color = color.strip()

            if color.startswith('fg='):
                # Foreground color
                result[0] = color[3:]
                is_fg = True
            elif color.startswith('bg='):
                # Background color
                result[2] = color[3:]
                is_fg = False
            elif color in self._attribute_names:
                # This is an attribute
                result[1 if is_fg else 3].append(Attr.from_name(color))
            else:
                raise ValueError("Unknown color format or attribute '{0}'"
                                 .format(color))

        return result

    def vformat(self, format_string, args, kwargs):
        """Hijack the internals of string.Formatter.vformat.

        Copied (almost) verbatim from the Python 3.7 source code but does not
        return a formatted string.

        """
        used_args = set()
        self._vformat(format_string, args, kwargs, used_args)
        self.check_unused_args(used_args, args, kwargs)

    def _vformat(self, format_string, args, kwargs, used_args,
                 auto_arg_index=0):
        """Hijack the internals of string.Formatter._vformat.

        Copied (almost) verbatim from the Python 3.7 source code but does not
        return a formatted string. The only major changes is that the result
        list normally returned by _vformat is gone and has been replaced with
        direct writes to a stream. Furthermore, nested formats have been
        removed.

        This is extremely brittle if the source ever changes and thus not
        always guaranteed to work. A better work-around is needed.

        """
        tokens = self.parse(format_string)

        for literal_text, field_name, format_spec, conversion in tokens:
            # Output the literal text
            if literal_text:
                self.file.write(literal_text)
                self.file.flush()

            # If there's a field, output it
            if field_name is not None:
                # This is some markup, find the object and do the formatting.
                # Handle arg indexing when empty field_names are given
                if field_name == '':
                    if auto_arg_index is False:
                        raise ValueError('cannot switch from manual field '
                                         'specification to automatic field '
                                         'numbering')
                    field_name = str(auto_arg_index)
                    auto_arg_index += 1
                elif field_name.isdigit():
                    if auto_arg_index:
                        raise ValueError('cannot switch from manual field '
                                         'specification to automatic field '
                                         'numbering')
                    # Disable auto arg incrementing, if it gets used later on,
                    # then an exception will be raised
                    auto_arg_index = False

                # Given the field_name, find the object it references and the
                # argument it came from
                obj, arg_used = self.get_field(field_name, args, kwargs)
                used_args.add(arg_used)

                # Do any conversion on the resulting object
                obj = self.convert_field(obj, conversion)

                # Format the object and append to the result
                self.file.write(self.format_field(obj, format_spec))
