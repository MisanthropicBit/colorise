Tutorial
========

In addition to this tutorial, you can find examples in the `examples
<https://github.com/MisanthropicBit/colorise/tree/master/examples>`_ folder.

**Table of Contents:**

1. `Basic Usage <#basic-usage>`__
2. `colorise.cprint <#colorise-cprint>`__
3. `colorise.fprint <#colorise-fprint>`__
4. `colorise.highlight <#colorise-highlight>`__
5. `Attributes <#attributes>`__
6. `Disabling Colors <#disabling-colors>`__
7. `More Colors! <#more-colors>`__
8. `Redefining Colors <#redefining-colors>`__

Basic Usage
-----------

You may be interested to know how many colors your terminal can represent,
which you can check using :py:func:`colorise.num_colors` which tries its best
to guess the number of colors supported.

>>> import colorise
>>> colorise.num_colors()
256

Returned values may be 8, 16, 88, 256 and 16,777,216 (or 256^3 i.e. 24-bit
true-color). You can also run the `color_test.py script
<https://github.com/MisanthropicBit/colorise/blob/master/color_test.py>`__
which prints all the capabilities of your console. To set the current color,
you can use the :py:func:`colorise.set_color` function.  For example,

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">set_color</span><span class="p">(</span><span class="n">fg</span><span class="o">=</span><span class="s1">&#39;red&#39;</span><span class="p">)</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="nb">print</span><span class="p">(</span><span class="s1">&#39;Hello&#39;</span><span class="p">)</span>
   <span style="color:red;">Hello</span></pre>
      </div>
   </div>

would set the current foreground color to red while

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">set_color</span><span class="p">(</span><span class="n">fg</span><span class="o">=</span><span class="s1">&#39;red&#39;</span><span class="p">,</span> <span class="n">bg</span><span class="o">=</span><span class="s1">&#39;green&#39;</span><span class="p">)</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="nb">print</span><span class="p">(</span><span class="s1">&#39;Hello&#39;</span><span class="p">)</span>
   <span style="color:red;background:green;">Hello</span></pre>
      </div>
   </div>

would set the current foreground color to red and the background color to
green. Supported color names can be queried via :py:func:`colorise.color_names`.

>>> colorise.color_names()
['black', 'red', 'green', 'yellow', 'blue', 'purple', 'magenta', 'cyan', 'gray', 'grey', 'lightgrey', 'lightgray', 'lightred', 'lightgreen', 'lightyellow', 'lightblue', 'lightpurple', 'lightcyan', 'white']

Use :py:func:`colorise.reset_color` to reset colors to their defaults.

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">set_color</span><span class="p">(</span><span class="n">fg</span><span class="o">=</span><span class="s1">&#39;red&#39;</span><span class="p">)</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="nb">print</span><span class="p">(</span><span class="s1">&#39;Hello&#39;</span><span class="p">)</span>
   <span style="color:red;">Hello</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">reset_color</span><span class="p">(</span><span class="p">)</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="nb">print</span><span class="p">(</span><span class="s1">&#39;Hello&#39;</span><span class="p">)</span>
   <span>Hello</span></pre>
      </div>
   </div>

:py:func:`colorise.cprint`
--------------------------

To print colored text, you can use the :py:func:`colorise.cprint` function.

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">cprint</span><span class="p">(</span><span class="s1">&#39;This has blue text and a green background&#39;</span><span class="p">,</span> <span class="n">fg</span><span class="o">=</span><span class="s1">&#39;blue&#39;</span><span class="p">,</span> <span class="n">bg</span><span class="o">=</span><span class="s1">&#39;green&#39;</span><span class="p">)</span>
   <span style="color:blue;background:green;">This has blue text and a green background</span></pre>
      </div>
   </div>

:py:func:`colorise.fprint`
--------------------------

The :py:func:`colorise.fprint` function provides more control than
:py:func:`colorise.cprint` by letting you specify colors akin to Python 3's
`string formatting <https://docs.python.org/3.7/library/stdtypes.html#str.format>`_.

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">fprint</span><span class="p">(</span><span class="s1">&#39;{fg=blue,bg=green}This has blue text and a green background&#39;</span><span class="p">)</span>
   <span style="color:blue;background:green;">This has blue text and a green background</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">fprint</span><span class="p">(</span><span class="s1">&#39;{fg=blue,bg=green}This has a green background and blue foreground but{fg=red} changes to red&#39;</span><span class="p">)</span>
   <span style="color:blue;background:green;">This has a green background and blue foreground but</span><span style="color:red;"> changes to red</span></pre>
      </div>
   </div>

The :py:func:`colorise.fprint` function provides the `autoreset` keyword
argument to control if colors should be reset when a new color format is
encountered. It is ``True`` by default.

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">fprint</span><span class="p">(</span><span class="s1">&#39;{fg=blue,bg=green}This has a green background and blue foreground but {fg=red}changes to red&#39;</span><span class="p">,</span> <span class="n">autoreset</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
   <span style="color:blue;background:green;">This has a green background and blue foreground but <span style="color:red;">changes to red</span></span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">fprint</span><span class="p">(</span><span class="s1">&#39;{fg=blue,bg=green}This has a green background and blue foreground but {fg=red}changes to red&#39;</span><span class="p">,</span> <span class="n">autoreset</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
   <span style="color:blue;background:green;">This has a green background and blue foreground but</span><span style="color:red;background:none;"> changes to red</span></pre>
      </div>
   </div>

Notice in the second example that both fore- and background colors are reset.
It would correspond to the following example where we explicitly reset all
colors and attributes with ``{reset}`` before setting the foreground color to
red.

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">fprint</span><span class="p">(</span><span class="s1">&#39;{fg=blue,bg=green}This has a green background and blue foreground but</span><span class="si">{reset}</span> <span class="s1">{fg=red}changes to red&#39;</span><span class="p">,</span> <span class="n">autoreset</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
   <span style="color:blue;background:green;">This has a green background and blue foreground but</span><span style="color:red;background:none;"> changes to red</span></pre>
      </div>
   </div>

:py:func:`colorise.highlight`
-----------------------------

The :py:func:`colorise.highlight` function can be used to highlight ranges of
characters within a string.

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">highlight</span><span class="p">(</span><span class="s1">&#39;This is a highlighted string&#39;</span><span class="p">,</span> <span class="n">fg</span><span class="o">=</span><span class="s1">&#39;red&#39;</span><span class="p">,</span> <span class="n">indices</span><span class="o">=</span><span class="p">[</span><span class="mi">0</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">10</span><span class="p">,</span> <span class="mi">13</span><span class="p">,</span> <span class="mi">15</span><span class="p">,</span> <span class="mi">16</span><span class="p">,</span> <span class="mi">17</span><span class="p">,</span> <span class="mi">22</span><span class="p">,</span> <span class="mi">26</span><span class="p">,</span> <span class="mi">27</span><span class="p">])</span>
   <span style="color:red;">T</span>hi<span style="color:red;">s</span> <span style="color:red;">i</span>s a <span style="color:red;">h</span>ig<span style="color:red;">h</span>l<span style="color:red;">igh</span>ted <span style="color:red;">s</span>tri<span style="color:red;">ng</span></pre>
      </div>
   </div>

Attributes
----------

Text attributes are supported via the :py:class:`colorise.attributes.Attr` class.

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span> <span class="nn">colorise</span> <span class="k">import</span> <span class="n">Attr</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">cprint</span><span class="p">(</span><span class="s1">&#39;Hello&#39;</span><span class="p">,</span> <span class="n">fg</span><span class="o">=</span><span class="s1">&#39;yellow&#39;</span><span class="p">,</span> <span class="n">bg</span><span class="o">=</span><span class="s1">&#39;purple&#39;</span><span class="p">,</span> <span class="n">attributes</span><span class="o">=</span><span class="p">[</span><span class="n">Attr</span><span class="o">.</span><span class="n">Italic</span><span class="p">])</span>
   <span style="color:yellow;background:purple;font-style:italic;">Hello</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">cprint</span><span class="p">(</span><span class="s1">&#39;Hello&#39;</span><span class="p">,</span> <span class="n">fg</span><span class="o">=</span><span class="s1">&#39;yellow&#39;</span><span class="p">,</span> <span class="n">bg</span><span class="o">=</span><span class="s1">&#39;purple&#39;</span><span class="p">,</span> <span class="n">attributes</span><span class="o">=</span><span class="p">[</span><span class="n">Attr</span><span class="o">.</span><span class="n">Underline</span><span class="p">])</span>
   <span style="color:yellow;background:purple;"><u>Hello</u></span></pre>
      </div>
   </div>

As for :py:func:`colorise.fprint`, you can specify the attributes directly in the format string.

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">fprint</span><span class="p">(</span><span class="s1">&#39;{fg=red,bg=green,italic}Hello&#39;</span><span class="p">)</span>
   <span style="color:red;background:cyan;font-style:italic;">Hello</span>
   <span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">fprint</span><span class="p">(</span><span class="s1">&#39;Hello </span><span class="si">{bold}</span><span class="s1">Hello&#39;</span><span class="p">)</span>
   <span>Hello</span> <span style="font-weight:bold;">Hello</span></pre>
      </div>
   </div>

Disabling Colors
----------------

It is sometimes useful to disable colors, for example in an application where
colored output is controlled by a configuration file. The
:py:func:`colorise.cprint`, :py:func:`colorise.fprint` and
:py:func:`colorise.highlight` functions all support the ``enabled`` keyword
argument for this purpose. Colors are enabled by default.

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">cprint</span><span class="p">(</span><span class="s1">&#39;Enabled!&#39;</span><span class="p">,</span> <span class="n">fg</span><span class="o">=</span><span class="s1">&#39;red&#39;</span><span class="p">,</span> <span class="n">enabled</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
   <span style="color:red;">Enabled!</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">cprint</span><span class="p">(</span><span class="s1">&#39;Disabled!&#39;</span><span class="p">,</span> <span class="n">fg</span><span class="o">=</span><span class="s1">&#39;red&#39;</span><span class="p">,</span> <span class="n">enabled</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
   <span>Disabled!</span></pre>
      </div>
   </div>

More Colors!
------------

Besides named colors, you can also specify colors via color table index, RGB,
hex, `HLS and HSV <https://en.wikipedia.org/wiki/HSL_and_HSV>`__. Color indices
index into color tables commonly supported by different platforms.

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">cprint</span><span class="p">(</span><span class="s1">&#39;Via color indices&#39;</span><span class="p">,</span> <span class="n">fg</span><span class="o">=</span><span class="mi">198</span><span class="p">)</span>
   <span style="color:#ff0087">Via color indices</span>
   <span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">cprint</span><span class="p">(</span><span class="s1">&#39;Via hex&#39;</span><span class="p">,</span> <span class="n">fg</span><span class="o">=</span><span class="s1">&#39;#43fff3&#39;</span><span class="p">,</span> <span class="n">bg</span><span class="o">=</span><span class="s1">&#39;0xd60c74&#39;</span><span class="p">)</span>
   <span style="color:#43fff3;background:#d60c74;">Via hex</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">fprint</span><span class="p">(</span><span class="s1">&#39;{fg=rgb(255;0;135)}Via RGB&#39;</span><span class="p">)</span>
   <span style="color:rgb(255,0,135);">Via hex</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">cprint</span><span class="p">(</span><span class="s1">&#39;Via HSV&#39;</span><span class="p">,</span> <span class="n">bg</span><span class="o">=</span><span class="s1">&#39;hsv(250;84;82)&#39;</span><span class="p">)</span>
   <span style="background:rgb(42,0,255);">Via HSV</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">fprint</span><span class="p">(</span><span class="s1">&#39;{bg=hls(0.11;0.412;0.762)}Via HLS&#39;</span><span class="p">)</span>
   <span style="background:rgb(185,96,25);">Via HLS</span></pre>
      </div>
   </div>

.. note::

   Even if your terminal does not support 88/256 index color tables or true-color,
   colorise will attempt to approximate the color by finding the closest one
   (via linear distance) and use that. For example, Windows usually supports only
   16 colors but using ``colorise.cprint('Hello', fg='rgb(240;240;0)')`` on such a
   system will still give you a yellow color (assuming standard Windows console
   colors). Also see the sprites in the :doc:`screenshots` section.

Redefining Colors
-----------------

Some platforms allow you to redefine the standard colors but currently you can
only redefine colors on Windows. As an example, let us redefine 'green' (color
index 2).

.. raw:: html

   <div class="highlight-default notranslate">
      <div class="highlight">
         <pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">cprint</span><span class="p">(</span><span class="s1">&#39;This should be green&#39;</span><span class="p">,</span> <span class="n">fg</span><span class="o">=</span><span class="s1">&#39;green&#39;</span><span class="p">)</span>
   <span style="color:green;">This should be green</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">redefine_colors</span><span class="p">({</span><span class="mi">2</span><span class="p">:</span> <span class="p">(</span><span class="mi">255</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">255</span><span class="p">)})</span>
   <span class="gp">&gt;&gt;&gt; </span><span class="n">colorise</span><span class="o">.</span><span class="n">cprint</span><span class="p">(</span><span class="s1">&#39;This should be green&#39;</span><span class="p">,</span> <span class="n">fg</span><span class="o">=</span><span class="s1">&#39;green&#39;</span><span class="p">)</span>
   <span style="color:magenta;">This should be green</span></pre>
      </div>
   </div>

:py:func:`colorise.redefine_colors` takes a dictionary of colortable indices as
keys and RGB tuples as values. Here, we redefine the entry in the colortable at
the color index for green (2) to be magenta instead. This change persists until
the color is redefined again or colorise is quit.

.. note::

   Redefining colors does not currently work with `ConEmu <https://conemu.github.io/>`__ or on Mac and Linux systems.
