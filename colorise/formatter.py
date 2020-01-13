#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ColorFormatter class for colorise.fprint.

This class extends the string.Formatter class.

"""

import re
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
        self._first_color_spec = False
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
    def first_color_spec(self):
        """Whether it is the first time a color specification is found."""
        return self._first_color_spec

    @first_color_spec.setter
    def first_color_spec(self, value):
        self._first_color_spec = value

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
        first_format = True
        tokens = super(ColorFormatter, self).parse(format_string)

        for literal_text, field_name, format_spec, conversion in tokens:
            # print('1', [literal_text, field_name, format_spec, conversion])
            color_spec, real_field_name, real_format_spec =\
                self._extract_color_format(field_name, format_spec)

            # print(f'2 "{color_spec}", "{real_field_name}", "{real_format_spec}"')
            # print(f'lit: {literal_text}')

            if any(spec for spec in color_spec):
                fg, fg_attrs, bg, bg_attrs = color_spec

                # Emit any literal text that should not be colored
                if literal_text:
                    yield literal_text, None, '', None

                if self.enabled:
                    # Automatically reset colors and attributes if enabled and
                    # if it is not the first format we encounter
                    if self.autoreset and not first_format:
                        self._reset_func(self.file)

                    # Set colors and attributes
                    self._set_color_func(fg, bg, fg_attrs + bg_attrs,
                                         self.file)

                yield '', real_field_name, real_format_spec, conversion
            else:
                # Yield tokens as normal
                yield literal_text, real_field_name, real_format_spec,\
                    conversion

            first_format = False

    def _set_color(self, fg, fg_attrs, bg, bg_attrs):
        """Set the current color."""
        if self.enabled and (fg or fg_attrs or bg or bg_attrs):
            attrs = fg_attrs + bg_attrs

            # Automatically reset colors and attributes if autoreset is set,
            # it is not the first color format we encounter and the attributes
            # are not just resetting colors
            if self.autoreset and not self.first_color_spec\
                    and attrs != [Attr.Reset]:
                self._reset_func(self.file)

            # Set colors and attributes
            self._set_color_func(fg, bg, attrs, self.file)

            self.first_color_spec = False

    def _extract_color_spec(self, color_spec, colors, default_value):
        """Extract the color specification from a format specification."""
        is_fg = False
        real_spec = []
        result = colors
        # print(f'Extracting {color_spec}')

        if color_spec is None:
            return colors, default_value

        for color in color_spec.split(';'):
            stripped_color = color.strip()

            if re.match('[fb]g=', stripped_color):
                index = 0 if stripped_color[0] == 'f' else 2

                if result[index]:
                    raise ValueError('Duplicate {0}ground color format'
                                     .format('back' if index > 0 else 'fore'))

                result[index] = stripped_color[3:]
                is_fg = index == 0
            elif stripped_color in self._attribute_names:
                # This is an attribute
                attr = Attr.from_name(stripped_color)
                result[1 if is_fg else 3].append(attr)
            else:
                # print(color)
                real_spec.append(color)
                # real_spec = color

        # print(f'Result: {result, ";".join(real_spec)}')
        return result, ';'.join(real_spec) if real_spec else default_value

    def _is_valid_color_spec(self, color_spec):
        """Return True if the color specification is valid."""
        return any(spec for spec in color_spec)

    def _extract_color_format(self, field_name, format_spec):
        """Parse and extract the color format from a format field."""
        colors = [None, [], None, []]
        real_field_name, real_format_spec = '', ''

        if not colors:
            return colors, None, ''

        # print(field_name, format_spec)

        colors, real_field_name =\
            self._extract_color_spec(field_name, colors, None)
        # print('4', field_name, real_field_name)
        colors, real_format_spec =\
            self._extract_color_spec(format_spec, colors, '')
        # print(colors)

        # print(colors, real_field_name, real_format_spec)
        return colors, real_field_name, real_format_spec

    def vformat(self, format_string, args, kwargs):
        """Hijack the internals of string.Formatter.vformat.

        Copied (almost) verbatim from the Python 3.7 source code but does not
        return a formatted string.

        """
        # Flush any remaining stuff before resetting colors
        self.file.flush()
        self._reset_func(self.file)
        self.first_color_spec = True

        used_args = set()
        _, _ = self._vformat(format_string, args, kwargs, used_args, 2)
        self.check_unused_args(used_args, args, kwargs)

    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth,
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
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')

        tokens = super().parse(format_string)

        # Keep the results around is necessary to support nested format
        # specification like string.format
        result = []

        for literal_text, field_name, format_spec, conversion in tokens:
            # print(3, [literal_text, field_name, format_spec, conversion])
            # Output the literal text
            if literal_text:
                result.append(literal_text)

                if recursion_depth == 2:
                    self.file.write(literal_text)
                    self.file.flush()

            # Extract any color spec from the field name and the real field
            # name itself
            color_spec = [None, [], None, []]
            color_spec, field_name =\
                self._extract_color_spec(field_name, color_spec, None)

            self._set_color(*color_spec)

            # print('field_name: ', field_name)
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
                    # print(field_name, auto_arg_index)
                    if auto_arg_index:
                        raise ValueError('cannot switch from manual field '
                                         'specification to automatic field '
                                         'numbering')
                    # Disable auto arg incrementing, if it gets used later on,
                    # then an exception will be raised
                    auto_arg_index = False

                # Given the field_name, find the object it references and the
                # argument it came from
                # print(field_name,args)
                obj, arg_used = self.get_field(field_name, args, kwargs)
                # print('acb', obj, arg_used, format_spec)
                used_args.add(arg_used)

                # Do any conversion on the resulting object
                obj = self.convert_field(obj, conversion)

                # print(f'1: "{format_spec}"')
                format_spec, auto_arg_index = self._vformat(
                    format_spec, args, kwargs,
                    used_args, recursion_depth-1,
                    auto_arg_index=auto_arg_index)
                # print(f'2: "{format_spec}"')
                # print(f'"{result}"')

                # Extract any color specification from the format specification
                color_spec, format_spec =\
                    self._extract_color_spec(format_spec, color_spec, '')

                valid_color_spec = self._is_valid_color_spec(color_spec)

                # if valid_color_spec and self.autoreset:
                #     # Reset colors before outputting a formatted field if a
                #     # color specification was present
                #     self._reset_func(self.file)

                self._set_color(*color_spec)

                # Format the object and append to the result
                formatted_field = self.format_field(obj, format_spec)
                # print(f'"{formatted_field}"')
                result.append(formatted_field)

                if recursion_depth == 2:
                    # Only output the field if we are at the top of the
                    # recursive call stack, otherwise we would output any
                    # nested format specifications
                    self.file.write(formatted_field)

                    if valid_color_spec and self.autoreset:
                        # Reset colors after outputting a formatted field if a
                        # color specification was present since colors should
                        # only apply to the formatted field and nothing else
                        self._reset_func(self.file)

        return ''.join(result), auto_arg_index
