4chan API Full Thread Archiver
===============

Feed the script a link to a 4chan thread, and it will download images, thumbnails, HTML of the thread, and the JSON of the thread for a full archive.

Part of the JSON-based-chanarchiver by Lawrence Wu, built 2012/04/04

This script:

* Downloads all images and/or thumbnails in a certain thread.
* Downloads a JSON dump of thread comments using the 4chan API.
* Downloads the HTML page
* (future) Converts links to use the downloaded images.
* (future) Prompts user for metadata information.

* Forked from _ Socketub's 4chandownloader. <https://github.com/socketubs/4chandownloader>_

Usage
============

::

    Usage:
      4chandownloader.py <url> <path> [--delay=<int>] [--thumbs] [--thumbsonly]
      4chandownloader.py -h | --help
      4chandownloader.py -v | --version

    Options:
      --thumbs            Download thumbnails
      --thumbsonly        Download thumbnails, no images
      --delay=<int>       Delay between thread checks [default: 20]
      -h --help           Show help
      -v --version        Show version

Modifications
============

* Downloads HTML dump of thread
* New --thumbsonly option to download thumbnails and no images
* More comments in code

Installation
============

::

    pip install 4chandownloader
    4chandownloader http://boards.4chan.org/b/res/423861837 4chanarchives --delay 5 --thumbs
