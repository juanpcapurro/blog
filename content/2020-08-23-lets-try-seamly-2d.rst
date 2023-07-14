==================
Let's try Seamly2D
==================
:date: 2020-08-23
:tags: sewing, tech
:author: capu
:summary: Let's hope I don't end up in suckless repositories again
:featured_image: /lets-try-seamly-2d/tiled-pdf.png

Today I have a very basic sewing project: I want to make a bag to hold some spare bike parts, since the current solution doesn't seem to be holding up well:

.. image:: {static}/lets-try-seamly-2d/old-ziplock.jpg
  :alt: a large ziplock bag with a few handlebars inside

...And I remembered a few weeks ago I saw a `reddit post <https://old.reddit.com/r/myog/comments/gs08z4/made_a_video_tutorial_on_how_to_use_seamly2d_to/>`_ of someone making a tutorial for some open source pattern design software.

For context, so far I've been able to use freeCAD and Inkscape to design sewing patterns, you can read about my progress with that in a `previous blog post`_

After watching the video I had a few takeaways:

- This program should allow me to do the pattern and then add the seam allowances ✨.
- It should also be able to split the patterns into the size of paper that I'm able to print, instead of having to split the svg manually in inkscape (huge timesaver).
- It looks like the idea is to have patterns which take parameters so they can be scaled easily.
- It doesn't seem like it'll allow me to create 3d models from the patterns, but I guess I would have to be able to infer it from the name.
- If I have to use the mouse as much as this guy, I'm gonna have a bad time.
- It looks like there's `at least five other people <https://fashionfreedom.eu/team>`_ interested in having free software for developing clothing. That's a rabbit hole I'd love to fall into. It'd be better than the prepper subworld, for sure.

I had to add a PPA for installing it, but whatever.
Only the ``bionic`` ppa worked with debian buster, and I had to add the signer's key manually. Less than ideal, but I got it working.

After installing it, I tried to design this bag using the 'cut on fold' method I learned in the video.

The tool has three main modes of operation (views?), and kind of forces you into one particular (and in my opinion healthy) workflow:

- **Draw**: Where you draw the actual patterns. It has a few tools to help you do that, which are used to define straight lines and curves.
- **Details**: Where you turn those drawings into actual patterns, picking their external line and adding seam allowances on it. You can also define the label the pattern is going to have, listing what fabric it should be made of, if it should be cut on a fold, how many of it should be cut, et cetera.
- **Layout**: Where the detailed patterns are converted into a printable document.

It applies the principle of 'convention over configuration' to UX design, in a way.

Draw
----
The drawing interface doesn't feel as good as using freeCAD. It's just lines.

And for everything I drew I had to specify the dimensions in a floating dialog which only could be used with the mouse [1]_ , with no autocomplete for the variables.

.. image:: {static}/lets-try-seamly-2d/set-line-length.png
  :alt: screenshot of line creation modal in seamly2d

Oh, variables. That's a great feature.

For a set of patterns, 'increments' can be defined which act as a sort of variable which can then be referenced when defining lines.
Other lines can also be referenced, so 'I want a line as long as this other one' is something you can communicate to the program very easily.

As an example, I defined the following increments:

.. image:: {static}/lets-try-seamly-2d/finished-detail.png
  :alt: screenshot of variables modal in seamly2d

So I finished the dimensions of my glorified square, and moved on to the Details mode

Details
-------
Here you have to define a path following the already defined lines outlining a particular piece of the pattern.

It's possible to only use parts of a piece, for example I skipped the distinction between the channel for the string and the body of the bag (line from A1 to A7) and just followed the outer contour.

It's weird, but I don't see it bothering me in any way.

After that, the detail can be configured to have a label and seam allowances (which for this bag is pretty big since I'll try to do french seams).

Since I'm cutting this piece on a fold, I had to set the nodes from A3 to A5 to not have any seam allowance.

.. image:: {static}/lets-try-seamly-2d/finished-detail.png
  :alt: screenshot of detail view in seamly2d

Layout
------
Here you'll determine what size template you want to create, but I don't plan on printing the patterns with a large format printer, so I just chose whatever here. It's important for the template size to be bigger than the biggest pattern, of course.


.. image:: {static}/lets-try-seamly-2d/layout-dialog.png
    :alt: screenshot of the layout dialog, where large format paper to use is selected

.. image:: {static}/lets-try-seamly-2d/layout-view.png
    :alt: preview of the large format print

After that, it's possible to create a ✨tiled pdf✨ on whatever print size, which makes using Inkscape to split the pattern totally unnecessary.

.. image:: {static}/lets-try-seamly-2d/tiled-pdf.png
    :alt: screenshot of the tiled pdf

This approach, while orders of magnitude better than splitting the pattern manually, it's still far from ideal because it first lays out the pieces with some fancy paper-efficient algorithm for the large format, but then the tiling for home printer usage is done in the dumbest way possible and is prone to wasting paper.

I realized this project was too simple to bother printing patterns for it, since the exact dimensions don't matter and it's basically a big square, but for reference this 80x40cm bag takes 12 Legal pages to print.

But don't worry, there'll be more complicated projects soon which'll put this tool to good use.

Some thoughts
-------------

Seamly2d is pretty unstable [2]_ and doesn't have a polished UX, but even with those important shortcomings, it allowed me to work as fast, or perhaps even faster, than when using freeCAD.

This shows how a piece of software created with a particular use case in mind can make the user happier than a general-purpose, more mature alternative.

When developing a product in the future, Seamly2d will be what I'll aspire to in terms of how to best focus development effort.

.. image:: {static}/lets-try-seamly-2d/finished-bag.jpg
  :alt: a large cloth bag with a few handlebars inside

.. [1] I usually give a lot of shit to Electron apps, but I have to recognize, if it were a webapp, I could easily get the 'use tab to switch fields' to work, but if I were to fix it in this native app, I would have to research a little more about how QT does forms.

.. [2] The most distracting bug is sometimes the variables table wouldn't open for no apparent reason, and I had to restart the program to be able to open it. Console output didn't report any errors.

.. _previous blog post: {filename}/2020-05-02-i-made-another-hip-pack.rst
