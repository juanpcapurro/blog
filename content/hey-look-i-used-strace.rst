=======================================
Hey look! I used strace for something!
=======================================
:date: 2019-06-14 22:04
:category: unix
:author: capu
:status: draft
:summary: I'm really happy to have found a situation where knowing what a system call is was useful for something.

-------
Context
-------
Let's start this one off with a screenshot:

.. image:: {static}/imgs/time_spent_learning_a_language.png
  :alt: a pie-chart captioned "Time spent when learning a new programming language" in which a minuscule portion is "Actually learning the language" and the overwhelming remainder is "Customizing vim to become the perfect IDE for the specific language"

Although I am tempted to say vIm Is NoT aN IdE, and rant about how you need little more than a good Language Server filling your omnifunc and an updated tags file to edit proficiently, it can totally be a hour black hole even just to get the two aforementioned things to work.

So, the journey begins with me spending more time writing solidity at work, when I was navigating a smart contract's code (I'll use `truffle's metacoin`_ for this example) and opened `vim-tagbar`_ expecting to see a summary of its functions, variables, etcetera:

.. image:: {static}/imgs/tagbar_not_working.png
  :alt: a screenshot of vim with vim-tagbar open, but the tagbar is empty

And it was empty! On a clearly non-empty contract!

For those of you who are not familiar with the aforementioned plugin, it's really simple: when invoking a command, it opens a vertical split with the definitions of the current file. |br|
For example, here is the plugin working correctly on an example Java file:

.. image:: {static}/imgs/tagbar_java_example.png
  :alt: a screenshot of vim with tagbar open and working on an example Java class

It even lists the fields in categories and with UML-like signs so you can know what is private, protected or public! And of course this listing is foldable and hitting enter on any of the


How vim-tagbar and ctags work
------------------------------
A 'tag' is a way of indexing definitions (variables, functions, classes...) in source code so it can very easily be looked up, since this is a rather usual requirement when developing.

There are programs like `ctags`_ which can create this kind of index for a file, or an entire directory, and usually store them in a file called ``tags``, which is then queried when using the go-to-definition functionality of an editor. |br|
You probably have used it (or some :strike:`more bloated` substitute) yourself! In most editors the go-to-definition is used by holding ``CTRL`` and clicking the desired name, whilst in Vi/Vim/neovim this is achieved by ``<C-]>``, that is, holding down ``CTRL`` and pressing ``]``.

The difference with tagbar is, instead of using the ``tags`` file to find where something is defined, the definitions of a particular file are listed.
Since the ``tags`` file is sorted by the definition names, and not the files they are defined in, it's faster to run ``ctags`` over the current file than it is to read the already generated file and filter only the definitions of the current file (and this is less fragile since it doesn't depend on the tags file being up to date, or even on it existing at all)

------------
The problem
------------

After checking that the tagbar is being displayed correctly for many other languages, it was evident that the problem was specific to solidity source code. |br| 
And it kind of makes sense, since it's a rather new language. But this shows the problem is not in the plugin itself.

After some duckduckgo-ing

.. _truffle's metacoin: https://www.trufflesuite.com/boxes/metacoin
.. _vim-tagbar: https://github.com/majutsushi/tagbar
.. _ctags: https://en.wikipedia.org/wiki/Ctags
