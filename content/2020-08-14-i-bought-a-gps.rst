===============
I bought a GPS!
===============
:slug: i-bought-a-gps
:date: 2020-08-14
:tags: tech, cycling
:author: capu
:summary: Let's see if I brick it or get bored first

My second-hand Garmin Edge 20 just arrived. I bought it because the police and I don't seem to reach an agreement on what is a 'safe way'[1]_ of exercising during a pandemic, so I'd rather not be asked questions.

How to avoid being asked questions? By looking confident of where I'm going.

How to look confident of where I'm going? By either exploring new paths very slowly and actually knowing where I am and what turns to take all the time (which is hard), or by having a nifty little gadget which helps me follow a pre-planned route (which gives me an excuse to buy stuff).

But you know me, I'm not going to create an account on some cLoUd sErViCe to move some files around in MY device.
How hard can it be, right? I've already recorded some rides on my phone, and even wrote some KML files from python for a uni project.

How the thing works
===================
Thankfully when I connected the device it showed up as a regular storage device and I didn't have to fiddle with MTP or any of the other transfer protocols which I've been too lazy to learn to use properly.

It has a whopping 5.4MB of storage

.. code-block:: text

    [~]: df -h /dev/sdc
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sdc        5.4M  2.4M  3.0M  45% /media/capu/garmin

Most of which seems to be used by the previous owner's activities

Seeing how little space is used by everything else, there won't be much to be gained by deleting translations that I won't use.

.. code-block:: text

    [/media/capu/garmin/GARMIN]: du -sh *
    2.3M    ACTIVITY
    512     COURSES
    512     DEBUG
    512     DEVICE.FIT
    7.5K    GarminDevice.xml
    1.0K    NEWFILES
    1.0K    RECORDS
    512     REMOTESW
    1.0K    SETTINGS
    1.0K    SPORTS
    120K    TEXT
    1.0K    TOTALS

After backing up all the files to my drive, let's poke around a little.
What's that XML file about?

It seems the file defines a few datatypes. Let's see an example:

.. code-block:: xml

    <DataType>
      <Name>FIT_TYPE_2</Name>
      <File>
        <Specification>
          <Identifier>FIT</Identifier>
        </Specification>
        <Location>
          <Path>GARMIN/SETTINGS</Path>
          <FileExtension>FIT</FileExtension>
        </Location>
        <TransferDirection>OutputFromUnit</TransferDirection>
      </File>
      <File>
        <Specification>
          <Identifier>FIT</Identifier>
        </Specification>
        <Location>
          <Path>GARMIN/NEWFILES</Path>
          <FileExtension>FIT</FileExtension>
        </Location>
        <TransferDirection>InputToUnit</TransferDirection>
      </File>
    </DataType>

All datatypes have one or two ``File`` entries, which define where in the device's storage files of that datatype belong.

All ``InputToUnit`` belong in the ``NEWFILES`` directory. So unless I want to do something the device doesn't expect, I should be only writing files there.

It's more helpful to think about ``InputToUnit`` as 'import' locations and ``OutputFromUnit`` as 'export' locations

Some files are ``InputOutput``, those seem to be files the device would read to look up some information and are not meant to export or import anything.

- ``FIT_TYPE_2``: To describe the device's settings. This defines paths for importing and exporting (and I guess persisting. Or is persistence only done in ``InputOutput`` files?)
- ``FIT_TYPE_3``: I don't know. For SPORTS? I guess it'd have the definitions for converting road/mountain cycling data into calories or something like that.
- ``FIT_TYPE_4``: Activity format, output only.
- ``FIT_TYPE_29``: They seem to be to import/export the user's records. Input and output files are defined, strangely.
- ``ErrorShutdownReports``: They go in the DEBUG directory and have the txt extension, so I guess if I ever make the device crash at least I'll have some actually readable information.
- ``FITBinary``: They have ``InputOutput`` direction. I have no idea what this is, and given there's a file in the defined path, I was afraid of even reading it, but ``file`` seems to tell me it's a` `type 1 (Device)`` so I guess this defines the device itself, and that might be what the device reads when opening the 'software version' page.
- ``TranslatedText``: These might be fun to play with, it defines where the translation files are, and also are of the type ``InputOutput``
- ``FIT_TYPE_6``: Defines courses, with both input and output paths. I think I'll spend most of my time here.
- ``EphemerisT1``: I was completely lost at first with this, but it defines an ``InputOutput`` file which the device reads to get satellite constellation data to speed up the GPS fix (it should take a few seconds instead of 2-3 minutes). `Another blogger <https://www.kluenter.de/2014/03/23/garmin-ephemeris-files-and-linux.html>`_ wrote about how to get the appropriate files, but given they are useful for only 3-14 days I'll probably not bother with it.

... And then there are a bunch of references to files which seem to have been used to upgrade the device's software. I'm probably not going to be updating anything and the files are not there anymore, so I won't bother with it.

But what's a FIT file anyway?
=============================

The first thing I assumed about FIT files is they're a format for recording GPS tracks with some extra data(ie: from cadence/hearth rate sensors), which is binary instead of XML-based due to the storage restrictions of the devices that record them.

But after fiddling with the ``file`` command and seeing the many formats defined in the XML file, I knew they were more than just that, they seem to be Garmin's standard for nearly-arbitrary binary data storage and transfer.
It might as well mean "File. Isn't Text". Or "FIT Isn't Text", if you're into that sort of thing.

Let's try to get some documentation on the subject.

There's no RFC defining the format. Or any other kind of public document.

The closest thing I could find is the `FIT SDK <https://www.thisisant.com/resources/fit-sdk/>`_. It's behind a license agreement, which you can think of as a paywall that you pay for not with money but with your freedoms (?

And let me tell you, it doesn't seem approachable. For example, the introduction pdf instructs you to define a few things on some headers and then run a pre-compiled .exe to generate the code that'll let you work with FIT files.

The specification
-----------------
From what I understood of the documentation, there are several types of FIT files, defined as *profiles* in a spreadsheet bundled with the SDK, and this seems to be what ``file`` reports.

The profile along with some other details are written in the file's header, and the rest of the file is a list of *messages* with a final checksum.

The messages can be either a definition of a data message, or a data message, and it's not required for all the definitions to be at the beginning of a file.

The definitions map a *global* event id (2 bytes, part of the protocol) to a *local* event id (1 byte, local to the current file), and specifies how is the data stored (including if it's big or little endian, theoretically it could be possible to have some definitions be little endian and other big endian in the same (valid) file. I'm fairly skeptical of the value this configuration option can add)

To further complicate things, local message ids might be reassigned to different global message ids in the same file.

All the event ids are documented in the aforementioned spreadsheet, and boy there are a lot.

The problem
-----------
I couldn't find any information on what kind of messages a file should include for it to conform to a certain *profile*, or on what other conditions must a file fulfill to be a valid course, for example.

AFAICT there's no public documentation on what will particular devices accept as valid FIT files either, and it seems to be a recurring problem in the forums [2]_

Translation files
=================
It'd be fun to mess a little with the translations, since they're available as files in the device
However, I can't find a ``.LNG`` file standard.

Apparently they have a header which I can't completely figure out, but the rest of the files is zero-terminated-strings in some weird 8bit encoding (í seems to be `0xed` instead of the `0xc3 ad` of good ol' UTF-8)

It seems like Garmin only maintains one set of these files for the EDGE 20/25, since they have strings for some conditions which doesn't make sense in a device that can't connect to VARIA lights, for example.

How do I make this thing understand GPX?
========================================
The easiest thing I think will be to convert a GPX file to a FIT file of type 6

I believe It'll be best to use a file from an actual activity instead of one generated manually, since the gist of this thing is to follow courses which other people already biked through.

Now that I think about it, to use this thing my way without even creating a Garmin account and seeing its features the 'normal' way is borderline irresponsible.

Anyway, let's convert a ride that I recorded with my phone:

.. code-block:: text

    [~/tmp/garmin]: gpsbabel -i gpx -f ~/syncthing/tracks/rec/2020-08-09_22-21_Sun.gpx -o garmin_fit -F rerun.fit
    Format does not support writing.
    [~/tmp/garmin, 1]:

What?

The parameters are passed as specified in the manpage...

The documentation says... `Only reading is supported <https://www.gpsbabel.org/htmldoc-1.5.4/fmt_garmin_fit.html>`_?

When researching if I could use this device in a freedom-respecting way, I looked at some projects which *read* FIT files, and assumed writing wouldn't be an issue.

Let's see how can I walk around this:

The `sourcforge mailing list <https://sourceforge.net/p/gpsbabel/mailman/gpsbabel-misc/thread/1465413706645-12070.post%40n4.nabble.com/#msg35146152>`_ doesn't give me much hope.

Gpsbabel `moved to github <https://github.com/gpsbabel/gpsbabel>`_, perhaps there's something more recent there. Otherwise I'll have to look at that awful spreadsheet and see what I can implement myself...

Thankfully, that wasn't necessary. I'm proud to present to you `today's unsung hero of the internet <https://github.com/gpsbabel/gpsbabel/pull/395>`_. They go by the name gromit1811 and implemented FIT file writing in October 2019.

The last version of gpsbabel available on debian repos is 1.5.4, from eons ago. I guess I still have to compile the thing from source myself, since no one is hosting a PPA for it. [3]_

Midnight came before I could figure out if I should use Cmake or Qmake, how to get the required Qmake version or any of that. And with a new (odd-numbered) day came the right to exist in public roads to exercise.

So sorry gromit1811, I'll see if your patch serves my use case tomorrow. I'll go ride my bike.

.. [1] don't freak out, I ride alone, with a mask, and most of the time on nearly emtpy streets. But the *yuta* doesn't seem to approve of me going further than 500m from my place of residence, despite not being any actual regulation against it.

.. [2] https://www.thisisant.com/forum/viewthread/4275

.. [3] obligatory all of this wouldn't have happened on Arch, btw

