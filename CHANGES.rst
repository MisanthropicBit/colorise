Version log
===========

0.1.0
-----
- Initial version

0.1.1
-----
- Fixed a bug where putting a ``:`` or escaped ``>`` or ``<`` just before or after some color formatted text would raise a ``ColorSyntaxError``

0.1.2
-----
- Fixed a bug in ``nix/ColorManager.py`` which caused ``set_color`` to malfunction

0.1.3
-----
- Fixed a bug where passing a string without any color formatting would print the empty string
