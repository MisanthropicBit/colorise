#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Show how to use different colorspaces."""

import colorise


if __name__ == "__main__":
    colorise.cprint('Using color names', fg='red')
    colorise.cprint('Using color indices', fg=196)
    colorise.cprint("Using hex codes with '#'", fg='#27ee45')
    colorise.cprint("Using hex codes with '0x'", fg='0x27ee45')
    colorise.cprint('Using HLS', fg='hls(0.3; 0.2; 0.1)')
    colorise.cprint("Using HSV", fg='hsv(65; 23;90)')
    colorise.cprint('Using RGB', fg='rgb(57;95;200)')
