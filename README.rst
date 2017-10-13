ardu-acqua-visual
=================

Status
------

This project will probably never leave the status of:
Development - Alpha/Beta/Whatever

As I started this project, I installed python-virtual from
the debian apt repo (as I have both a debian-desktop and
a raspbian-develbox).
This is great for security, but not that great for
feature coverage...

Now I am starting to play around with IPython and Jupyter and
use vpython installed through pip - but still, for the arduino
project, I will probably use both tracks in parallel for some
time..


Dependencies, Requirements
--------------------------

 * Debian/Raspian

  - python-visual

 * Python 2

  - tested against: 2.7

  - see requrements.txt for further dependencies


Basic Idea
----------

Just for fun..

For the flussbad-berlin.de project we want to visualize the
sensor values in a very basic and inexpensive way. So I just
got a little 5" touchscreen for the raspberry pi, which is
connected to the arduino, which is collecting sensor data.
I then put
the whole stuff into an old wooden wine box...

This is just a first test to see whether the raspberry pi is
not getting too busy..


Outlook
-------

Really nice to have would be a vpython7 based collection
of objects, that could be loaded based on a JSON config
to visualize a certain sensor setup...

