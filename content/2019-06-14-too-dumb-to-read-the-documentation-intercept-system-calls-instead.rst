===================================================================
Too dumb to read the documentation? Intercept system calls instead!
===================================================================
:slug: too-dumb-to-read-the-documentation-intercept-system-calls-instead
:date: 2019-06-14 22:04
:tags: unix, debugging
:author: capu
:summary: Join me in this brainfarting journey

-------
Context
-------
Let's start this one off with a screenshot:

.. image:: {static}/too-dumb-to-read-the-documentation-intercept-system-calls-instead/time_spent_learning_a_language.png
  :alt: a pie-chart captioned "Time spent when learning a new programming language" in which a minuscule portion is "Actually learning the language" and the overwhelming remainder is "Customizing vim to become the perfect IDE for the specific language"

Although I am tempted to say vIm Is NoT aN IdE, and rant about how you need little more than a good Language Server filling your omnifunc and an updated tags file to edit proficiently, it can totally be a man-hour black hole even just to get the two aforementioned things to work, as we'll soon see.

So, the journey begins with me spending more time writing solidity at work, when I was navigating a smart contract's code (I'll use `truffle's metacoin`_ for this example) and opened `vim-tagbar`_ expecting to see a summary of its functions, variables, etcetera:

.. image:: {static}/too-dumb-to-read-the-documentation-intercept-system-calls-instead/tagbar_not_working.png
  :alt: a screenshot of vim with vim-tagbar open, but the tagbar is empty

And it was empty! On a clearly non-empty contract!

If you are not familiar with the aforementioned plugin, it's really simple: when invoking a command, it opens a vertical split with the definitions of the current file. |br|
For example, here is the plugin working correctly on an example Java file:

.. image:: {static}/too-dumb-to-read-the-documentation-intercept-system-calls-instead/tagbar_java_example.png
  :alt: a screenshot of vim with tagbar open and working on an example Java class

It even lists the fields in categories and with UML-like signs so you can know what is private, protected or public! And of course this listing is foldable with vim's default keybinidings (see ``:help folding``).

How vim-tagbar and ctags work
------------------------------
A 'tag' is a way of indexing definitions (variables, functions, classes...) in source code so it can very easily be looked up, since this is a rather usual requirement when developing.

There are programs like `ctags`_ which can create this kind of index for a file, or an entire directory, and usually store them in a file called ``tags``, which is then queried when using the go-to-definition functionality of an editor. |br|
You probably have used it (or some substitute) yourself! In most editors the go-to-definition is used by holding ``CTRL`` and clicking the desired name, whilst in vim this is achieved by ``<C-]>``, that is, holding down ``CTRL`` and pressing ``]``.

The difference with tagbar is, instead of using the ``tags`` file to find where something is defined, the definitions of a particular file are listed.
Since the ``tags`` file is sorted by the definition names, and not the files they are defined in, it's faster to run ``ctags`` over the current file than it is to read the already generated file and filter only the definitions of the current file (and this is less fragile since it doesn't depend on the tags file being up to date, or even on it existing at all)

------------
The problem
------------

After checking that the tagbar was being displayed correctly for many other languages, it was evident that the problem was specific to solidity source code. |br|
And it kind of makes sense, since it's a rather new language. But this showed the problem was not in the plugin itself.

After some duckduckgo-ing, I found Someone On The Internet  who wrote `some regexes`_ which could be used to extend ctags (nice!) and add support for solidity, alongside with some settings for vim-tagbar so it can differentiate between events, classes, methods, etcetera.

These regexes should be added into one of ctags' configuration files ``~/.ctags``, and then they'd be used by the program to parse the source files searching for functions, identifiers and the like.

I created the file, try to open the tagbar again, and... it was empty.

Running ctags on the file produced an empty (well, not empty, but only comments) tags file:

.. code-block:: text

    [~/tmp/metacoin-box, master, 60s]: ctags contracts/MetaCoin.sol
    [~/tmp/metacoin-box, master+1]: cat tags
    !_TAG_FILE_FORMAT       2       /extended format; --format=1 will not append ;" to lines/
    !_TAG_FILE_SORTED       1       /0=unsorted, 1=sorted, 2=foldcase/
    !_TAG_OUTPUT_MODE       u-ctags /u-ctags or e-ctags/
    !_TAG_PROGRAM_AUTHOR    Universal Ctags Team    //
    !_TAG_PROGRAM_NAME      Universal Ctags /Derived from Exuberant Ctags/
    !_TAG_PROGRAM_URL       https://ctags.io/       /official site/
    !_TAG_PROGRAM_VERSION   0.0.0   /248cffc9/

...but if I manually told it to read options from the aforementined file, it generated the tags as expected:

.. code-block:: text

    [~/tmp/metacoin-box, 1, master+1]: ctags  --options=${HOME}/.ctags contracts/MetaCoin.sol
    [~/tmp/metacoin-box, master+1]: cat tags
    !_TAG_FILE_FORMAT       2       /extended format; --format=1 will not append ;" to lines/
    !_TAG_FILE_SORTED       1       /0=unsorted, 1=sorted, 2=foldcase/
    !_TAG_OUTPUT_MODE       u-ctags /u-ctags or e-ctags/
    !_TAG_PROGRAM_AUTHOR    Universal Ctags Team    //
    !_TAG_PROGRAM_NAME      Universal Ctags /Derived from Exuberant Ctags/
    !_TAG_PROGRAM_URL       https://ctags.io/       /official site/
    !_TAG_PROGRAM_VERSION   0.0.0   /248cffc9/
    MetaCoin        contracts/MetaCoin.sol  10;"    c
    Transfer        contracts/MetaCoin.sol  13;"    e
    balances (address=>uint)        contracts/MetaCoin.sol  11;"    m
    getBalance      contracts/MetaCoin.sol  31;"    f
    getBalanceInEth contracts/MetaCoin.sol  27;"    f
    sendCoin        contracts/MetaCoin.sol  19;"    f

So the problem seems to be that my version of ctags doesn't use the same configuration files as the version used by shuangjj (the regexes' author).

Just as a sanity check, I tried to configure the plugin so it called ctags with the ``--options`` flag.
The `ctags configuration for solidity`_ consisted of two parts:

One labeled ``vim ~/.ctags``:

.. code-block:: text

    --langdef=Solidity
    --langmap=Solidity:.sol
    --regex-Solidity=/^contract[ \t]+([a-zA-Z0-9_]+)/\1/c,contract/
    --regex-Solidity=/[ \t]*function[ \t]+([a-zA-Z0-9_]+)/\1/f,function/
    --regex-Solidity=/[ \t]*event[ \t]+([a-zA-Z0-9_]+)/\1/e,event/
    --regex-Solidity=/[ \t]*(struct[ \t]+[a-zA-Z0-9_]+)([ \t]*\{)/\1/v,variable/
    --regex-Solidity=/[ \t]*(enum[ \t]+[a-zA-Z0-9_]+)([ \t]*\{)/\1/v,variable/
    --regex-Solidity=/[ \t]*mapping[ \t]+\(([a-zA-Z0-9_]+)[ \t]*=>[ \t]*([a-zA-Z0-9_]+)\)[ \t]+([a-zA-Z0-9_]+)/\3 (\1=>\2)/m,mapping/

And other labeled ``vim ~/.vimrc``:

.. code-block:: text

    let g:tagbar_type_solidity = {
        \ 'ctagstype': 'solidity',
        \ 'kinds' : [
            \ 'c:contracts',
            \ 'e:events',
            \ 'f:functions',
            \ 'm:mappings',
            \ 'v:varialbes',
        \ ]
    \ }

The first one is the proper regexes for extending ctags, and the latter are the configurations for vim-tagbar to understand what ctags generates.

I added a few lines to the latter to also instruct the plugin to pass some arguments to ctags.

.. code-block:: vimscript

    let g:tagbar_type_solidity = {
        \ 'ctagstype': 'solidity',
        \ 'ctagsargs': '-f - --options=/home/capu/.ctags',
        \ 'kinds' : [
            \ 'c:contracts',
            \ 'e:events',
            \ 'f:functions',
            \ 'm:mappings',
            \ 'v:varialbes',
        \ ]
    \ }

``\ 'ctagsargs': '-f - --options=/home/capu/.ctags',``: sets the arguments for ctags. ``-f -`` makes ctags output to stdout, which is necessary for the plugin to work.

...And it worked!:

.. image:: {static}/too-dumb-to-read-the-documentation-intercept-system-calls-instead/tagbar_working.png
  :alt: tagbar working for the solidity file

But this is not a *good* solution. The Right Thing To Do™ is to find what files does my version of ctags read for configurations and move them there, so for the rest of the journey, this last addition to the ``.vimrc`` is not present.

--------------
The brainfart
--------------
To find out where my version of ctags reads configurations, I could've read the README or the man page, both of which clearly explain what are the differences between universal-ctags (what I use) and exhuberant ctags (its predecessor which is probably what shuangjj uses), and which files it sources.
But I searched on the intertubes instead, and ended up reading an `outdated issue`_, which suggested that universal-ctags reads the ``~/.u-ctags/`` directory for settings files.

But after moving the file there, it still didn't work. In the moment I had two options:

- Reading the source code for universal-ctags and figure out which files are opened

- Intercept the system calls for opening files when ctags runs, hoping to see the path where it tries to open them.

The latter seemed more interesting, and so I tried, filtering for `open` syscalls only, because I figured it would produce a lot of output:

.. code-block:: text

    [~/tmp/metacoin-box, master+1]: strace -e trace=open ctags contracts/Migrations.sol                                    <<<
    --- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=30777, si_uid=1001, si_status=0, si_utime=0, si_stime=0} ---
    +++ exited with 0 +++

So it seems there are no ``open`` syscalls? Let's try again without any filters:

.. code-block:: text

    [~/tmp/metacoin-box, master+1]: strace ctags contracts/Migrations.sol                                              <<<
    execve("/usr/local/bin/ctags", ["ctags", "contracts/Migrations.sol"], 0x7ffc0172bd38 /* 77 vars */) = 0
    brk(NULL)                               = 0x1cf5000
    access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
    ...
    openat(AT_FDCWD, "/home/capurro/.ctags.d", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = -1 ENOENT (No such file or directory)
    openat(AT_FDCWD, ".ctags.d", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = -1 ENOENT (No such file or directory)
    openat(AT_FDCWD, "ctags.d", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = -1 ENOENT (No such file or directory)
    ...
    rt_sigaction(SIGQUIT, {sa_handler=SIG_DFL, sa_mask=[], sa_flags=SA_RESTORER, sa_restorer=0x7f1437aa3100}, NULL, 8) = 0
    rt_sigprocmask(SIG_SETMASK, [], NULL, 8) = 0
    --- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=31710, si_uid=1001, si_status=0, si_utime=0, si_stime=0} ---
    exit_group(0)                           = ?
    +++ exited with 0 +++

After some manual filtering, I found the executable uses ``openat`` instead of ``open``, and tries to open ``/home/capurro/.ctags.d``. So I moved the configurations file to ``~/.ctags.d/main.ctags``. And it worked!

.. code-block:: text

    [~/tmp/metacoin-box, master+2]: ctags -f - contracts/MetaCoin.sol
    MetaCoin        contracts/MetaCoin.sol  10;"    c
    Transfer        contracts/MetaCoin.sol  13;"    e
    balances (address=>uint)        contracts/MetaCoin.sol  11;"    m
    getBalance      contracts/MetaCoin.sol  31;"    f
    getBalanceInEth contracts/MetaCoin.sol  27;"    f
    sendCoin        contracts/MetaCoin.sol  19;"

.. _truffle's metacoin: https://www.trufflesuite.com/boxes/metacoin
.. _vim-tagbar: https://github.com/majutsushi/tagbar
.. _some regexes: `ctags configuration for solidity`_
.. _ctags configuration for solidity: https://gist.github.com/shuangjj/ae816cacffce3a27e256de7c21312c50
.. _ctags: https://en.wikipedia.org/wiki/Ctags
.. _outdated issue: https://github.com/universal-ctags/ctags/pull/1519#issuecomment-319998393
