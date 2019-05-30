# ``colorise`` FAQ

## Q: *Why do I not get the right RGB color?*

Depending on the console/terminal color support, you may have anything from 8-,
16-, 88-, 256-color support or even full-blown 24-bit RGB available.
``colorise`` will try its best to approximate a requested color according to
those available, but doing this 100% cross-platform is difficult. Stick to the
basic 8 colors if in doubt.

You can query ``num_colors`` to see if your terminal supports 256 color indices:

    if colorise.num_colors() >= 256:
        # Do 256-color index stuff here...

## Q: *I have custom colors set up in Windows, why are they not reflected in ``colorise``?*

Unfortunately, you can only query current console RGB colors in Windows on Vista
and beyond. If you are working a Windows version before that, there is no
reliable way to do so, and thus custom colors will not be properly reflected
when approximating colors.

## Q: *How come I can use 88 and 256 color indices in Windows?*

Actually, you can't, but ``colorise`` maps the index to its RGB color and uses
the result to approximate the requested color.

## Q: *Does ``colorise`` support 24-bit true-color?*

While some terminals do support true-color, there is no reliable way of
detecting it as of now (apart from hardcoding everything that can be changed in
the future), so ``colorise`` opts to **not** support true-color, but only the
256 color palette.
