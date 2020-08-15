==========================
I didn't brick my GPS yet!
==========================
:date: 2020-08-13
:tags: capu-tries-tech, cycling
:author: capu
:status: draft
:summary: Let's see if I can make this thing tell me where to go

recap
=====

let's try this new gpsbabel version
===================================
Cloned 

cmake -> apt-file -> apt-get

cmake is not reccommended but it was the one which gave error messages that I could understand and do something about
 
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

.. code-block:: text

    [~/src/gpsbabel, master+3, 115s]: apt-file search libusb.h

.. code-block:: text

    [~/src/gpsbabel, master+3, 115s]: apt-file search libusb.h
    apcupsd-doc: /usr/share/doc/apcupsd/examples/libusb.h
    libusb-1.0-0-dev: /usr/include/libusb-1.0/libusb.h
    lirc-doc: /usr/share/doc/lirc/lirc.org/html/atilibusb.html
    lirc-doc: /usr/share/doc/lirc/lirc.org/html/srm7500atilibusb.html
    mrpt-doc: /usr/share/doc/mrpt-doc/html/dep-libusb.html

gpsbabel works!

.. code-block:: text

    [~/src/gpsbabel, master+3]: ./gpsbabel --version
    GPSBabel Version 1.7.0.  https://www.gpsbabel.org

let's see what happens if i convert a fit file into a fit file. i hope it'll write it as a course

.. code-block:: text

    [~/tmp/garmin, 130]: file A8D02107.FIT
    A8D02107.FIT: FIT Map data, unit id 65536, serial 3919222549, Thu Aug 13 00:21:08 2020, manufacturer 1 (garmin), product 2238, type 4 (Activity)
    [~/tmp/garmin]: gpsbabel -i garmin_fit -f A8D02107.FIT -o garmin_fit -F fit2fit.fit                      Format does not support writing.
    [~/tmp/garmin, 1]: ~/src/gpsbabel/gpsbabel -i garmin_fit  
    [~/tmp/garmin, 130]: file A8D02107.FIT
    A8D02107.FIT: FIT Map data, unit id 65536, serial 3919222549, Thu Aug 13 00:21:08 2020, manufacturer 1 (garmin), product 2238, type 4 (Activity)
    [~/tmp/garmin]: gpsbabel -i garmin_fit -f A8D02107.FIT -o garmin_fit -F fit2fit.fit                      Format does not support writing.
    [~/tmp/garmin, 1]: ~/src/gpsbabel/gpsbabel -i garmin_fit -f A8D02107.FIT -o garmin_fit -F fit2fit.fit
    [~/tmp/garmin]: file fit2fit.fit
    fit2fit.fit: FIT Map data, unit id 520094213, serial 17041168, Sun Dec 31 02:41:36 1989, manufacturer 19, product 64779, type 2 (Settings)

WHAT THE FUCK? how did it get turned into settings?


[~/tmp/garmin, 130]: file A8D02107.FIT
A8D02107.FIT: FIT Map data, unit id 65536, serial 3919222549, Thu Aug 13 00:21:08 2020, manufacturer 1 (garmin), product 2238, type 4 (Activity)
[~/tmp/garmin]: gpsbabel -i garmin_fit -f A8D02107.FIT -o garmin_fit -F fit2fit.fit                      Format does not support writing.
[~/tmp/garmin, 1]: ~/src/gpsbabel/gpsbabel -i garmin_fit -f A8D02107.FIT -o garmin_fit -F fit2fit.fit
[~/tmp/garmin]: file fit2fit.fit
fit2fit.fit: FIT Map data, unit id 520094213, serial 17041168, Sun Dec 31 02:41:36 1989, manufacturer 19, product 64779, type 2 (Settings)
[~/tmp/garmin]: diff fit2fit.fit A8D02107.FIT
Binary files fit2fit.fit and A8D02107.FIT differ

[~/tmp/garmin, 1]: ~/src/gpsbabel/gpsbabel -i gpx -f A8D02107-track.gpx -o garmin_fit -F fit2gpx2fit.fit
[~/tmp/garmin]: file fit2gpx2fit.fit
fit2gpx2fit.fit: FIT Map data, unit id 520094213, serial 17041168, Sun Dec 31 02:41:36 1989, manufacturer 19, product 64779, type 2 (Settings)
[~/tmp/garmin]: ~/src/gpsbabel/gpsbabel -i gpx -f ~/syncthing/tracks/rec/2020-08-09_22-21_Sun.gpx -o garmin_fit -F gpx2fit.fit
[~/tmp/garmin]: file gpx2fit.fit
gpx2fit.fit: FIT Map data, unit id 520094213, serial 17041168, Sun Dec 31 02:41:36 1989, manufacturer 19, product 64779, type 2 (Settings)


now let's try to send this all to the device and hope it's not parsed as settings, 'cause I don't expect the device to handle it properly

[~/tmp/garmin, 4s]: sudo cp fit2fit.fit fit2gpx2fit.fit gpx2fit.fit /media/capu/garmin/GARMIN/NEWFILES
[~/tmp/garmin]: sudo umount /media/capu/garmin
[~/tmp/garmin]: sudo mount /dev/sdc /media/capu/garmin
[~/tmp/garmin, 3s]: cd /media/capu/garmin/GARMIN
[/media/capu/garmin/GARMIN]: tree .
.
├── ACTIVITY
│   └── A8D02107.FIT
├── COURSES
│   ├── A8DI4331.FIT
│   └── A8DI4332.FIT
├── DEBUG
├── DEVICE.FIT
├── GarminDevice.xml


images of the device recognizing course 1 and course 2, but it didn't correctly parse the gpx2fit.fit file

i guess i'll have to read what gromit1811 said about 'fit files don't suscribe to our track-route-waypoint-model'

> Note that routes are not handled, so they should be transformed to tracks first before converting to FIT. Also, track segments are not supported, so all segments in a track get concatenated and written as a single continuous track without gaps

can i turn a gpx file from a route into a track with gpsbabel?

it seems so, I'll delete the rte from the converted file and see what happens
