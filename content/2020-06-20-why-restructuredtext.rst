=====================
Why reStructuredText?
=====================
:slug: why-restructuredtext
:date: 2020-06-20
:tags: tech, programming
:author: capu
:summary: Content warning: extensibility

I'll be honest with you, I don't have all that much experience with the Python way of doing things, and I'm fairly new at this reStructuredText thing, but when writing my `previous blog post`_ I had an issue that made me understand why `Eric Holscher <https://www.ericholscher.com/>`_ loves it `so much <https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/>`_.

The problem
===========
In my `previous blog post`_ I had to add a video to explain how I used Inkscape to split a big svg files into pieces small enough to be printed by a regular printer.

Recording the video was easy enough with OBS and good ol' low quality expectations, but pelican (and reStructuredText for that matter) doesn't have a native way of showing videos.

A markdown evangelist would say "But that's not an issue in markdown! you just write HTML inline!"... and they would be kind of right. It'd work.

But every time I want to add another video (yes, zero times so far, I'll admit that), I'd have to copy-paste the same HTML snippet, and this means:

- If I make some change to how I display videos later, I'd have to re-do the changes in every previous instance
- Having the ``<video>`` alongside the rest of the document tag mixes *what* I want to show with *how* I want to show it. For reStructuredText this is decoupled.

The solution
============
Extend reStructuredText so it can show videos!

I started by looking at what the documentation said about videos, and it linked to `an old snippet <https://gist.github.com/dbrgn/2922648>`_.

Then, I figured I could turn it into a plugin by adding something similar to the plugin directory, and having a ``register()`` function in a file named ``__init__.py``.

.. code-block:: python

    """
        ReST directive for embedding selfhosted videos
    """
    from __future__ import absolute_import
    from docutils import nodes
    from docutils.parsers.rst import Directive, directives

    class Video(Directive):
        has_content = False
        html = '<video controls muted>  <source src="%(src)s" type="video/webm">  </video>'
        required_arguments = 1
        optional_arguments = 0
        final_argument_whitespace = False

        def run(self):
            self.options['src'] = directives.uri(self.arguments[0])
            return [nodes.raw('', self.html % self.options, format='html')]

    def register():
        directives.register_directive('video', Video)

I don't actually know what ``node.raw()`` does, for example, but so far it didn't seem necessary 🙃.

This enables me to create my own reStructuredText directive! I currently have no need for extra parameters, but in the future I could make it configurable.

Also, here's `the actual commit <https://github.com/juanpcapurro/blog/commit/e7c8c95a3d2dac9fd14cdb698534728cc78752c1>`_ where I implemented this changes.

...I should probably add a link to download the file if the browser doesn't support video. Perhaps for the next time I add one.

.. _previous blog post: {filename}/2020-05-02-i-made-another-hip-pack.rst
