#!/usr/bin/env python
# coding: utf-8

# The Hydrus Network developer screwed around with this April 2013
# Part of the JSON-based-chanarchiver by Lawrence Wu, 2012/04/04
# Originally from https://github.com/socketubs/4chandownloader
# Rewritten to save in seperate images folder, download plain HTML, modularization, comments, and code cleanup

#
# Initial release Nov. 5, 2009
# v6 release Jan. 20, 2009
# http://cal.freeshell.org
#
# Refactor, update and Python package
# by Socketubs (http://socketubs.net/)
# 09-08-12
#

import os
import time
import json
import re
import errno
import requests
import py4chan

# Links to 4chan URLs (with regex!)
FOURCHAN_API_URL = 'https://api.4chan.org/%s/res/%s.json' # board, thread
FOURCHAN_IMAGES_URL = 'https://images.4chan.org/%s/src/%s' # board, image
FOURCHAN_THUMBS_URL = 'https://thumbs.4chan.org/%s/thumb/%s' # board, thumb
FOURCHAN_BOARDS_URL = 'http://boards.4chan.org/%s/res/%s' # board, thread

# folder names for image and thumbnails
_IMAGE_DIR_NAME = "img"
_THUMB_DIR_NAME = "thumb"
_DEFAULT_FOLDER = "4chan-saved-threads"

_DUMP_COMPLETE_STRING = "Dump complete. To resume dumping the same thread,\nrun this script again."

class Archiver():
    
    def __init__( self, log_callback ):
        
        self._log_callback = self._log_callback
        
    
    # Recursively create paths if they don't exist 
    # replace with `os.makedirs(path,exist_ok=True)` in python3
    def _make_sure_path_exists(path):
        try:
        os.makedirs(path)
        except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    # Download any file using requests
    def _download_file(fname, dst_folder, file_url, self._log_callback):
        # Destination of downloaded file
        file_dst = os.path.join(dst_folder, fname)
        
        # If the file doesn't exist, download it
        if not os.path.exists(file_dst):
        self._log_callback('%s downloading...' % fname)
        i = requests.get(file_url)
        if i.status_code == 404:
            self._log_callback(' | Failed, try later (%s)' % file_url)
        else:
            open(file_dst, 'w').write(i.content)
        else:
        self._log_callback('%s already downloaded' % fname)

    # File in place regex function originally scripted by steveha on StackOverflow: 
    # http://stackoverflow.com/questions/1597649/replace-strings-in-files-by-python
    # Notice: `\1` notation could be interpreted by python as `\x01`! Escape it with a second backslash: `\\1`  
    def _file_replace(fname, pat, s_after):
        # first, see if the pattern is even in the file.
        with open(fname) as f:
        if not any(re.search(pat, line) for line in f):
            return # pattern does not occur in file so we are done.

        # pattern is in the file, so perform replace operation.
        with open(fname) as f:
        out_fname = fname + ".tmp"
        out = open(out_fname, "w")
        for line in f:
            out.write(re.sub(pat, s_after, line))
        out.close()
        os.rename(out_fname, fname)

    # Dumps thread in raw HTML format to `<thread-id>.html`
    def _dump_html(dst_dir, board, thread):
        fourchan_images_regex = re.compile("http://images.4chan.org/\w+/src/")
        fourchan_thumbs_regex = re.compile("http://\d+.thumbs.4chan.org/\w+/thumb/")
        html_filename = "%s.html" % thread
        html_url = FOURCHAN_BOARDS_URL % (board, thread)
        _download_file(html_filename, dst_dir, html_url)
        
        # Convert all links in HTML dump to use locally downloaded files
        html_path = os.path.join(dst_dir, html_filename)
        _file_replace(html_path, '"//', '"http://')
        _file_replace(html_path, fourchan_images_regex, _IMAGE_DIR_NAME + "/")
        _file_replace(html_path, fourchan_thumbs_regex, _THUMB_DIR_NAME + "/")
        
        # (future) Download a local copy of all CSS files, and convert HTML links to use them (we need to use beautifulsoup to get links...)
        #_file_replace(html_path, "http://static.4chan.org/css/(\w+.\d+).css", "css/\\1.css")

    # Grab thread JSON from 4chan API
    def _dump_json(dst_dir, board, thread):
        json_filename = "%s.json" % thread
        json_path = os.path.join(dst_dir, json_filename)
        
        json_thread = requests.get(FOURCHAN_API_URL % (board, thread))
        json.dump(json_thread.json, open(json_path, 'w'), sort_keys=True, indent=2, separators=(',', ': '))
          
    # Get all external links quoted in comments
    def _list_external_links(curr_thread, dst_dir, self._log_callback):
        # The Ultimate URL Regex
        # http://stackoverflow.com/questions/520031/whats-the-cleanest-way-to-extract-urls-from-a-string-using-python
        linkregex = re.compile(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.‌​][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(‌​([^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""", re.DOTALL)

        # File to store list of all external links quoted in comments (overwrite upon each loop iteration)
        linklist_dst = os.path.join(dst_dir, "external_links.txt")
        linklist_file = open(linklist_dst, "w")

        for reply in curr_thread.replies:
          if not linkregex.search(reply.Comment):
          continue
          else:
          # We need to get rid of all <wbr> tags before parsing
          cleaned_com = re.sub(r'\<wbr\>', '', reply.Comment)
          linklist = re.findall(linkregex, cleaned_com)
          for item in linklist:
              self._log_callback("Found link to external site, saving in %s:\n%s\n" % (linklist_dst, item[0]))
              linklist_file.write(item[0])	# re.findall creates tuple
              linklist_file.write('\n')	# subdivide with newlines

        # Close linklist file after loop
        linklist_file.close()

    # Download images, thumbs, and gather links to external urls
    def _get_files(dst_dir, curr_thread, nothumbs, thumbsonly):

        # Create and set destination folders
        dst_images_dir = os.path.join(dst_dir, _IMAGE_DIR_NAME)
        _make_sure_path_exists(dst_images_dir)
        dst_thumbs_dir = os.path.join(dst_dir, _THUMB_DIR_NAME)
        _make_sure_path_exists(dst_thumbs_dir)
        
        # regex for obtaining filenames
        fourchan_images_regex = re.compile("http://images.4chan.org/\w+/src/")
        fourchan_thumbs_regex = re.compile("http://\d+.thumbs.4chan.org/\w+/thumb/")
        
        if (thumbsonly == False):
          # Dump all images within a thread from 4chan
          for image_url in curr_thread.Files():
        image_name = re.sub(fourchan_images_regex, '', image_url)
        _download_file(image_name, dst_images_dir, image_url)

        if thumbsonly or (nothumbs == False):
          # Dump all thumbnails within a thread from 4chan
          for thumb_url in curr_thread.Thumbs():
        thumb_name = re.sub(fourchan_thumbs_regex, '', thumb_url)
        _download_file(thumb_name, dst_thumbs_dir, thumb_url)

    def Archive( thread, board, path, nothumbs, thumbsonly, delay ):
        
        # Set a default path if none is given
        if (path == None):
          path = os.path.join(os.getcwd() + os.path.sep + _DEFAULT_FOLDER)

        # Initiate py4chan object
        curr_board = py4chan.Board(board)
        curr_thread = curr_board.getThread(int(thread))

        # Switch to tell first run
        firstIteration = True

        # try/except to handle Ctrl-C
        try:
          while 1:
          # don't run this code the first time
          if (firstIteration == False):
              # Wait to execute code again
              self._log_callback("Waiting %s seconds before retrying (Type Ctrl-C to stop)\n" % delay)
              time.sleep(int(delay))
              
              if curr_thread.is_404:
            self._log_callback("[Thread 404'ed or Connection Lost]")
            break
              
              # Update thread and check if new replies have appeared
              newReplies = curr_thread.update()
              if (newReplies == 0):
            continue
              else:
            self._log_callback("%s new replies found!" % newReplies)
          else:
              self._log_callback(' :: Board: %s' % board)
              self._log_callback(' :: Thread: %s' % thread)
              
              # Create paths if they don't exist
              dst_dir = os.path.join(path, board, thread)
              _make_sure_path_exists(dst_dir)
              self._log_callback(' :: Folder: %s' % dst_dir)
              
              # Download images and thumbs 
              _get_files(dst_dir, curr_thread, nothumbs, thumbsonly)
              
              # Get all external links quoted in comments
              _list_external_links(curr_thread, dst_dir)

              # Dumps thread in raw HTML format to `<thread-id>.html`
              _dump_html(dst_dir, board, thread)
              
              # Dumps thread in JSON format to `<thread-id>.json` file, pretty printed
              _dump_json(dst_dir, board, thread)
              
              # first iteration is complete
              firstIteration = False
            
        except KeyboardInterrupt:
          self._log_callback("\n")
          self._log_callback(_DUMP_COMPLETE_STRING)
          raise SystemExit(0)
        
        self._log_callback(_DUMP_COMPLETE_STRING)
