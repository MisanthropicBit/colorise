# Changes

## 1.0.0

**Major update**

- Reworked entire library
- Better documentation and comments
- Support for RGB, HSV, HLS and hexadecimal color formats
- Support for 88 and 256 color indices
- Support for virtual terminal processing on Windows
- Changed parser to use Python's str.format syntax, e.g. '<fg=red>' -> '{fg=red}''
- Removed formatcolor and formatbyindex functions
- Removed ColorManager classes since no state needs to be stored
- Better detection of color capabilities
- If e.g. a true-color color is specified and the terminal does not support it,
  colorise will automatically find the color on your system that most closely
  matches the desired color

## 0.1.4

- Fixed a bug on nix platforms that caused background colors to break

## 0.1.3

- Fixed a bug where passing a string without any color formatting would print
  the empty string

## 0.1.2

- Fixed a bug in ``nix/ColorManager.py`` which caused ``set_color`` to
  malfunction

## 0.1.1

- Fixed a bug where putting a ``:`` or escaped ``>`` or ``<`` just before or
  after some color formatted text would raise a ``ColorSyntaxError``

## 0.1.0

- Initial version
