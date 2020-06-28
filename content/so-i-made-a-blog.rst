=======================
So I have a blog now
=======================
:date: 2019-06-12 22:04
:tags: capu-tries-tech
:author: capu
:summary: Today is the day I begin my journey towards my life goal of being an internet personality in my second language.


----
Why?
----
It all started when, at work, I realized that it was very time consuming to individually tell everyone about each of the {clever,ugly} hacks that I was low key proud of.

Now I can also individually and inefficiently bug everyone to death with the fact that I have a javascript-less, tracking-less, nearly-content-less blog.

----
How?
----
This blog is made in `pelican`_.
Initially I tried to fork the `/dev/random theme`_ , but ended up just modifying the default 'simple' theme.

I really liked the look and feel (not to mention the content, of course) of `alephsecurity`_'s website, so I :strike:`kind of stole half of their css` took great inspiration from it. |br|
Also I'm trying to learn reStructuredText after `Eric Holscher's post`_ convinced me to dip my toes into this whole 'extensible language that actually has a standard' thing.

There are many features of Pelican left unused and probably breaking the site(this site has only one author and probably'll never use categories, for example), but it doesn't seem to add much bloat and solves the publish by RSS / compile rst / don't break all the links all the time issues so I'm pretty happy with it for now ✨.

If you want to use any part of this work, its source code is available over at `my github`_ under a BSD 3-clause license. |br|
If you can't stop yourself from aligning some markup or telling me how to spell things, of course I'll accept your pull request. |br|
If you instead want to argue or flirt with me, `my twitter`_ might be a better way.

As-I-write-this update 1:
-------------------------
While very hyped up for using some of the extensibility of reStructuredText, I found out Pelican has no built-in way of sharing :strike:`those thingies that star with ..` role definitions across content files (or I haven't found it), so I ended up using `a global includes plugin`_ that had no activity since since 2017 (boooo) but I managed to get working with only minor patching (yeeeey)

I have `forked`_ the aforementioned plugin and I'll try to contribute the really modest fixes back to the original project, if only to get a reply from the author telling me that I lack a configuration variable or something.

As-I-write-this update 2:
-------------------------
RSS feeds work out of the box, but they consist of only the title and summary for each article, and there's really no reason to force anyone to visit my site to read an article when they could easily consume it in the comfort of their reader, even without an internet connection.

As-I-write-this update 3:
-------------------------
TIL RSS was not meant to contain a full article (after all, it was meant for *syndication*, not distribution) and `Pelican 3.7 release notes`_ say that including a whole article in the ``<summary>`` tag might break some readers. 

So instead of modifying this behaviour I'll provide both RSS and Atom feeds. If you want to see the whole article in your reader, use the Atom feed (It'll be the only one visually linked anyway).

Update 4:
---------
Fuck Atom. It tries to do syndication and distribution, RSS is just simpler and if you want to have the whole article in your reader, use a reader with offline support.
Also, I don't fully understand what readers do when I update an article and I want to minimize the chances of someone reading outdated articles.

If you were following me via Atom: I love you. Thanks for following me.
But I broke your reader. Use the new RSS url at the bottom of this page.

.. _/dev/random theme: https://github.com/22decembre/dev-random3
.. _alephsecurity: https://alephsecurity.com/
.. _Eric Holscher's post: https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/
.. _pelican: https://docs.getpelican.com/en/stable/index.html
.. _a global includes plugin: https://github.com/mhoff/pelican-global-rst-include
.. _forked: https://github.com/juanpcapurro/pelican-global-rst-include
.. _Pelican 3.7 release notes: https://blog.getpelican.com/pelican-3.7-released.html
