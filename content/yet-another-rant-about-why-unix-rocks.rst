==============================================
Where we're going, we don't need StackOverflow
==============================================
:date: 2020-09-12
:tags: capu-tries-tech, debugging, unix
:author: capu
:summary: Googling error messages is nice, but what if the apocalypse comes and you only have an offline debian repository and some paracord?

A few days ago, `when trying to get gpsbabel to write FIT files <{filename}/i-bought-a-gps.rst>`_ I had to build gpsbabel from sources to make use of a feature implemented only recently, 

While CMake was not the 'preferred way' of building the project, I used it because it was the method which gave error messages that I could understand and do something about. [1]_

CMake, for those of you who don't know, is a cross-platform build system which when run, generates Makefiles to build for a particular platform.

So, after creating said makefiles, I ran ``make`` and it didnt' build, of course.
 
.. code-block:: text

    [~/src/gpsbabel, 130, master+3, 25s]: make -j 3
    [ 94% ] Building CXX object CMakeFiles/gpsbabel.dir/jeeps/gpslibusb.cc.o
    /home/capu/src/gpsbabel/jeeps/gpslibusb.cc:43:14: fatal error: libusb-1.0/libusb.h: No such file or directory
    #    include <libusb-1.0/libusb.h>
    ^~~~~~~~~~~~~~~~~~~~~
    compilation terminated.
    make[2]: *** [CMakeFiles/gpsbabel.dir/build.make:2598: CMakeFiles/gpsbabel.dir/jeeps/gpslibusb.cc.o] Error 1
    make[2]: *** Waiting for unfinished jobs....
    make[1]: *** [CMakeFiles/Makefile2:73: CMakeFiles/gpsbabel.dir/all] Error 2
    make: *** [Makefile:84: all] Error 2

The compiler [2]_ tries to find a header file in the system files (includes with ``<`` reference OS-wide dependencies and includes with double quotes reference the source tree), and can't find it.

The solution to that is to have said file in my system. And in most unix environments, files are added to critical system paths via *packages*. Not installers, and especially not downloading them from some forum and copying them manually.

And the software responsible for adding, removing and searching packages is called a *package manager*.

I use Debian, and its package manager is ``apt``. You might've used in Ubuntu or other Debian-based distro mainly to install programs, for example with ``apt-get install package``

``apt``, however, has many more features than simply installing packages. ``apt-file``, in particular was useful for my problem, because it lets you search for 'what package(s) provide X file':

.. code-block:: text

    [~/src/gpsbabel, master+3, 115s]: apt-file search libusb.h
    apcupsd-doc: /usr/share/doc/apcupsd/examples/libusb.h
    libusb-1.0-0-dev: /usr/include/libusb-1.0/libusb.h
    lirc-doc: /usr/share/doc/lirc/lirc.org/html/atilibusb.html
    lirc-doc: /usr/share/doc/lirc/lirc.org/html/srm7500atilibusb.html
    mrpt-doc: /usr/share/doc/mrpt-doc/html/dep-libusb.html

... and of course it's a substring search and it matched a lot of html files. If that was a problem I could've used the ``--regexp`` flag with some pattern like ``\/libusb.h$``, but with that few results it was easy to see that I should install ``libusb-1.0-0-dev``.

After doing this for a few more packages:

.. code-block:: text

    [~/src/gpsbabel, master+3]: ./gpsbabel --version
    GPSBabel Version 1.7.0.  https://www.gpsbabel.org

I got gpsbabel to build!

What I like about unix-like systems is how everything is designed so you can (and are encouraged to) fix your problems on your own, without needing a Senior Libusb Enterprise Expert to figure out how the thing can fail and documenting it for you, the helpless user.

Once you know what a package manager is supposed to do, it's fairly easy to search the man pages to find out how to accomplish a particular task. And this knowledge transfers to other package managers, too! on Arch-based distros ``pacman -Fs`` does the same thing [3]_, for example.


.. [1] yes, I'm taking CMake's side on this one, sorry.

.. [2] aCtUalLy, InClUdEs aRe HaNdLeD bY tHe pRePrOcEsSor.

.. [3] I find pacman way easier to use than apt. The various one-letter flags might seem cryptic from afar, but with zsh's completion it's a really good experience to write a query interactively
