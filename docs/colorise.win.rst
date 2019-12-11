colorise.win package
====================

Submodules
----------

colorise.win.cluts module
-------------------------

.. py:module:: colorise.win.cluts
   :platform: Windows

.. py:function:: get_clut(color_count)

   Return the appropriate color look-up table.

.. py:function:: to_codes(bg, color, attributes)

   Convert a set of attributes to Windows character attributes.

.. py:function:: color_from_name(name, color_count, bg, attributes)

   Return the color value and color count for a given color name.

.. py:function:: color_from_index(idx, color_count, bg, attributes)

   Return the color value and color count for a given color index.

.. py:function:: get_rgb_color(color_count, bg, rgb, attributes)

   Get the color for an RGB triple or approximate it if necessary.

colorise.win.color\_functions module
------------------------------------

.. py:module:: colorise.win.color_functions
   :platform: Windows

.. py:function:: num_colors()
   
   Get the number of colors supported by the terminal.

.. py:function:: reset_color(file=sys.stdout)

   Reset all colors and attributes.

.. py:function:: or_bit_flags(\*bit_flags)

   Bitwise OR together a list of bitflags into a single flag.

.. py:function:: set_color(fg=None, bg=None, attributes=[], file=sys.stdout)

   Set color and attributes in the terminal.

.. py:function:: redefine_colors(color_map, file=sys.stdout)

   Redefine the base console colors with a new mapping.

colorise.win.win32_functions module
------------------------------------

Windows API functions.

.. py:module:: colorise.win.win32_functions
   :platform: Windows

.. py:function:: can_redefine_colors()

   Return whether the terminal allows redefinition of colors.

.. py:function:: create_std_handle(handle_id)

   Create a Windows standard handle from an identifier.

.. py:function:: get_win_handle(target)

   Return the Windows handle corresponding to a Python handle.
   
.. py:function:: get_windows_clut()

   Query and return the internal Windows color look-up table.
   
.. py:function:: enable_virtual_terminal_processing(handle)

   Enable Windows processing of ANSI escape sequences.
   
.. py:function:: restore_console_mode(handle, restore_mode)

   Restore the console mode for a handle to its original mode.

.. py:function:: restore_console_modes()

   Restore console modes for stdout and stderr to their original mode.

.. py:function:: can_interpret_ansi()

   Return True if the Windows console can interpret ANSI escape codes.

.. py:function:: set_console_text_attribute(handle, flags)

   Set the console's text attributes.
   
.. py:function:: encode_rgb_tuple(rgb)

   Hexadecimally encode an rgb tuple as 0xbbggrr.

.. py:function:: redefine_colors(color_map, file=sys.stdout)

   Redefine the base console colors with a new mapping.

   This only redefines the 8 colors in the console and changes all text in the
   console that already uses the logical names. E.g. if 'red' is mapped to the
   color red and this function changes it to another color, all text in 'red'
   will be rendered with this new color, even though it may already have been
   written to the console.

colorise.win.winhandle module
------------------------------------

.. automodule:: colorise.win.winhandle
   :members:
   :undoc-members:
   :show-inheritance:
