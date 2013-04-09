BA 4chan API Thread Archiver
===============

This script archives all images, thumbnails, JSON, and converted HTML of a 4chan thread, using the `4chan API <https://github.com/4chan/4chan-API>`_. The script will continue until the thread 404s or the connection is lost.

Part of the JSON-based-chanarchiver by Lawrence Wu, built 2012/04/04

This script:

* Downloads all images and/or thumbnails in a certain thread.
* Downloads a JSON dump of thread comments using the 4chan API.
* Downloads the HTML page
* Converts links in HTML to use the downloaded images
* Keeps downloading until 404 (with a user-set delay)

* Forked from Socketub's `4chan-thread-archiver. <https://github.com/socketubs/4chan-thread-archiver>`_

By default, the script saves to the folder ``4chan-saved-threads`` in the current working directory.

Usage
============

::

    Usage:
      4chan-thread-archiver <url> [--path=<string>] [--delay=<int>] [--nothumbs] [--thumbsonly]
      4chan-thread-archiver -h | --help
      4chan-thread-archiver -v | --version

    Options:
      --nothumbs          Don't download thumbnails
      --thumbsonly        Download thumbnails, no images
      --delay=<int>       Delay between thread checks [default: 20]
      -h --help           Show help
      -v --version        Show version

Installation
============

Install Python on your computer. On Linux, Python is almost always preinstalled; however, you will also have to install the program ``pip`` from the repositories.

::

    easy_install pip
    pip install BA-4chan-thread-archiver
    
Example
=======

::

    4chan-thread-archiver http://boards.4chan.org/b/res/423861837 --path=saved-threads --delay 5 --thumbsonly

Modifications to original
============

This script has changed considerably from the original it was forked from. Here is a list of additions:

* Based on `py4chan <https://github.com/e000/py-4chan>`_
* Downloads HTML dump of thread
* New --thumbsonly option to download thumbnails and no images
* Code modularization
* More comments in code

More info and a full journal can be found in ``log.md``.

Wishlist
=========

* Turn the functions into an independent class
* Download CSS and convert HTML to use them
* Prompt user for metadata information.
* Define the ``.chan.zip`` format for 4chan thread archive transfer
* Create a PyQt GUI