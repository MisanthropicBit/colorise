Changelog
=========

.. 'new' is for new, planned modifications
.. 'fix' is for bugfixes
.. 'feature' is for features added via pull requests
.. 'refactor' is for code refactors
.. 'docs' is for anything related to documentation

.. raw:: html

    <style> .new      { color:#329932 } </style>
    <style> .fix      { color:#e50000 } </style>
    <style> .feature  { color:#a64ca6 } </style>
    <style> .refactor { color:#ffa500 } </style>
    <style> .docs     { color:#0376ee } </style>

.. role:: new
.. role:: fix
.. role:: feature
.. role:: refactor
.. role:: docs

Version numbers follow `Semantic Versioning <https://semver.org/>`__ (i.e. <major>.<minor>.<patch>).

1.0.0
-----

2019-11-28

.. warning::

   Major update with breaking changes.

- [:new:`new`] Support for 88/256 colortable indices, and RGB, `HSV/HLS
  <https://en.wikipedia.org/wiki/HSL_and_HSV>`__ and hexadecimal color formats.
- [:new:`new`] Support for virtual terminal processing on Windows.
- [:new:`new`] Changed parser to use Python's str.format syntax, e.g. ``<fg=red>`` becomes
  ``{fg=red}``. Removed ColorManager classes since no state needs to be stored,
  replaced by a ColorFormatter class.
- [:new:`new`] Better detection of terminal color capabilities.
- [:new:`new`] If an unsupported color format is specified which the terminal does not
  support it (e.g. an RGB color in a 16 color terminal), colorise will
  automatically find color on your system that matches the desired color (via
  linear distance).
- [:refactor:`refactor`] Reworked entire library.
- [:refactor:`refactor`] Removed formatcolor and formatbyindex functions.
- [:docs:`docs`] Online documentation and updated comments.

`0.1.4 <https://github.com/MisanthropicBit/colorise/tree/bd00f84c5b7723732e942f25714df0c0f00bd19f>`__
-----------------------------------------------------------------------------------------------------

2014-06-11

- [:fix:`Fix`] Fixed a bug on nix platforms that caused background colors to break.

`0.1.3 <https://github.com/MisanthropicBit/colorise/tree/6f795e40ee7fe5fa3089e975d59b8434a5f87f75>`__
-----------------------------------------------------------------------------------------------------

2014-06-02

- [:fix:`Fix`] Fixed a bug where passing a string without any color formatting would print
  the empty string.

`0.1.2 <https://github.com/MisanthropicBit/colorise/tree/efee35dd90542e19532828d447ab18970f29f126>`__
-----------------------------------------------------------------------------------------------------

2014-05-31

- [:fix:`Fix`] Fixed a bug in ``nix/ColorManager.py`` which caused ``set_color`` to
  malfunction.

`0.1.1 <https://github.com/MisanthropicBit/colorise/tree/6b2b3ca0eb1f83fc6be823a7195e8b6f78cc0a98>`__
-----------------------------------------------------------------------------------------------------

2014-05-24

- [:fix:`Fix`] Fixed a bug where putting a ``:`` or escaped ``>`` or ``<`` just before or
  after some color formatted text would raise a ``ColorSyntaxError``.

`0.1.0 <https://github.com/MisanthropicBit/colorise/tree/00f58d7fd4cf8df5b16bb450cfee9de978d6278d>`__ 
-----------------------------------------------------------------------------------------------------

2014-05-14

- Initial version.
