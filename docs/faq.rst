FAQ
===

**Q: Why do I get different results on different platforms?**

Different platforms and terminals have support for different numbers of colors,
attributes and colortables, and colorise tries its best to provide uniform
results although platform differences makes this hard to do 100% correct.

For example, depending on your console/terminal color support, you may have
anything from 8-, 16-, 88-, 256-color support or even full-blown 24-bit colors
available. If you request a 24-bit color but only have 256 colors, colorise
will try its best to approximate the requested color according to the
available colortable for 256 colors.

**Q: I have custom colors set up in Windows, why are they not reflected in colorise?**

On `Windows Vista or Windows Server 2008
<https://docs.microsoft.com/en-us/windows/console/getconsolescreenbufferinfoex>`__,
colorise will read the current colortable and use that to lookup and
approximate colors so your custom console colors should be reflected. If you
are working on a Windows version before that, your custom colors will not be
properly reflected as colorise will have to assume a default colortable.

**Q: How come I can use more than 16 colors in Windows?**

`Some versions of Windows 10
<https://devblogs.microsoft.com/commandline/24-bit-color-in-the-windows-console/>`__
have 24-bit color support and can interpret `ANSI escape codes
<https://en.wikipedia.org/wiki/ANSI_escape_code>`__, the latter which is
commonly how colors are emitted on Mac and Linux systems.

.. _logical-color-table:

**Q: Why are the named colors on Windows incorrect?**

On Windows, named colors are actually indices into a color table and not actual
colors. Typing

>>> colorise.cprint('This should be yellow', fg='yellow')

will give you the color in the table correspoding to the 'yellow' index, not
necessarily the color yellow. This might be the case if you defined your own
colors. You can see the current colors by right-clicking the top bar of the
console and selecting 'Properties' then selecting the 'Colors' tab. You can
also set these programatically using :py:func:`colorise.redefine_colors`.

The same is true for other terminals on other platforms. For example,
`iTerm.app <https://iterm2.com/>`__ allows you to redefine the basic system
colors.

**Q: The blink and italic attributes do not appear to work in iTerm.app?**

This has to be enabled manually in the settings in `iTerm.app
<https://iterm2.com/>`__. Go into Preferences ­→ Profiles → Text and check the
boxes for "Blinking text" and "Italic text".

**Q: Can I use colorise in different threads?**

colorise is **not** thread-safe.

On nix systems, colorise emits `ANSI escape codes
<https://en.wikipedia.org/wiki/ANSI_escape_code>`__ to print colored output.
Internally, this happens in a way where multiple threads could potentially
interfere causing colors sequences to be intermingled, although it should be
possible to manually achieve this in a thread-safe manner.

On Windows systems that do *not* support `ANSI escape codes
<https://en.wikipedia.org/wiki/ANSI_escape_code>`__, multiple threads would
also interfere with each other. On Windows systems that *do* support ANSI
escape codes, it should still be possible to output colored text in a
thread-safe manner.

**Q: Why do the tests fail with 'The handle is invalid.' on Windows?**
**Q: Why does colorise not do colored output on Windows?**

Redirecting output or running colorise in a `subprocess
<https://docs.python.org/3/library/subprocess.html>`__ call means that the
Windows Console API will return a 'The handle is invalid.' error (errno 6)
since the output is no longer a valid console.

`tox <https://tox.readthedocs.io/en/latest/>`__ and `pytest
<https://docs.pytest.org/en/latest/contents.html>`__ `capture stdout and stderr
<https://docs.pytest.org/en/latest/capture.html>`__ which causes the above
mentioned error.

**Q: Was the colorise logo generated using colorise?**

Yes :)
