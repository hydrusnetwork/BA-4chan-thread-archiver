BA 4chan API Thread Archiver
===============

This script archive all images, thumbnails, JSON, and converted HTML of a 4chan thread, using the [4chan API](https://github.com/4chan/4chan-API). The script will continue until the thread 404s or the connection is lost.

Part of the JSON-based-chanarchiver by Lawrence Wu, built 2012/04/04

This script:

* Downloads all images and/or thumbnails in a certain thread.
* Downloads a JSON dump of thread comments using the 4chan API.
* Downloads the HTML page
* Converts links in HTML to use the downloaded images
* Keeps downloading until 404 (with a user-set delay)

* Forked from [Socketub's 4chandownloader.](https://github.com/socketubs/4chandownloader)

Usage
============

    Usage:
      4chandownloader <url> [--path=<string>] [--delay=<int>] [--nothumbs] [--thumbsonly]
      4chandownloader -h | --help
      4chandownloader -v | --version

    Options:
      --nothumbs          Don't download thumbnails
      --thumbsonly        Download thumbnails, no images
      --delay=<int>       Delay between thread checks [default: 20]
      -h --help           Show help
      -v --version        Show version

Modifications to original
============

This script has almost fully diverged from the original, and 

* Based on py4chan
* Downloads HTML dump of thread
* New --thumbsonly option to download thumbnails and no images
* Code modularization
* More comments in code

Wishlist
=========

* Turn the functions into an independent class
* Download CSS and convert HTML to use them
* Prompt user for metadata information.
* Define the `.chan.zip` format for 4chan thread archive transfer
* Create a PyQt GUI

Installation
============

    pip install 4chandownloader
    4chandownloader http://boards.4chan.org/b/res/423861837 4chanarchives --delay 5 --thumbs