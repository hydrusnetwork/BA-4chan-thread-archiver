## (FUTURE) Save to current working directory if a path is not given. Use `os.cwd()`

## Setting HTML to local folders

Originally, my plan was to automatically generate HTML from the JSON downloaded. However, perhaps the easier way was to download the HTML that 4chan already generated, and convert it to use the images the script already downloaded.

To do so, these find and replace functions converted absolute links to relative links to the downloaded images.

* `"//` -> `"http://`
* `http://images.4chan.org/\w/src/` -> `img/`
* `http://\d.thumbs.4chan.org/\w/thumb/` -> `thumb/`

### The function

To perform the regex, I needed a suitable function. Rather than reinvent the wheel, I borrowed code from StackOverflow.

    # Regex function originally by steveha on StackOverflow: 
    # http://stackoverflow.com/questions/1597649/replace-strings-in-files-by-python
    import re
    import os
    def file_replace(fname, pat, s_after):
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

## The Regex Expressions

This is the test file I created to work with the regex, known as `testfile.html`

    <html>"//images.4chan.org/k/src/4238749327.img"</html>
    <a="//9.thumbs.4chan.org/k/thumb/"<test>
    <"//static.4chan.org/css/jfoajweaf.478.css">
    <"//static.4chan.org/css/yuiyiiu.283.css">

So we can now use our regex.

    html_path = "testfile.html"
    file_replace(html_path, '"//', "http://")
    file_replace(html_path, "http://images.4chan.org/\w/src/", "img/")
    file_replace(html_path, "http://\d.thumbs.4chan.org/\w/thumb/", "thumb/")

## Downloading and linking to a local copy of the CSS

CSS can just stay linked to 4chan, but 4chan tends to change the CSS all the time, so it's a good idea to use a local snapshot for best compatiblity.

In the HTML of threads, they have some weird CSS number in addition, for some reason... It seems to be consistent, so we should have a copy locally.

Convert link to plain file path:

`http://static.4chan.org/css/(\w+).\d+.css` -> `css/\1.css`

### (FUTURE) Downloading a local copy of the CSS

We need to grab the names of all those css files, and use them to save a copy of the stylesheets locally under `css/`.

I used [this tutorial](http://palewi.re/posts/2008/04/05/python-recipe-open-a-file-read-through-it-print-each-line-matching-a-search-term/) to understand how to grab all matching lines.

* Use beautifulsoup to find links with `<link href=>` tag

#### Function to find text in file

    # Return lines matching a regex, code by Ben Welsh
    # http://palewi.re/posts/2008/04/05/python-recipe-open-a-file-read-through-it-print-each-line-matching-a-search-term/
    # Notice: `\1` notation could be interpreted by python as `\x01`! Escape it with a second backslash: `\\1`
    def file_find(fname, pat)
	f = open(fname, "r")

	for line in f:
	    if re.match(pat, line):
		print line,

### Regex for linking to a local copy of the CSS

The below regex used a `\1` replace, but it was giving me problems in python. Apparently, since this character was in a string literal, python converted the `\1` to a `\x01` character before it got to the regex replace function. The recommended way to send this raw string was to use `r"\1"`. However, since the function added an extra layer of abstraction,  there was no way to use that.

After hours of searching, the solution was to escape the `\1` with a backslash, resulting in `\\1`. When the string finally reached the replace function, it would be interpreted as `\1`.

    file_replace(html_path, "http://static.4chan.org/css/(\w+).\d+.css", "css/\\1.css")
    
## (FUTURE) Metadata file

The metadata file would be in JSON or YAML format, and contain information about the thread useful to a reader.

The script could prompt the user to add a title or quick description

## (FUTURE) Abstracted Interface and PyQt GUI

Something like the Chandler.

We would have to convert all the functions into a class, with a GUI and CLI interface script.

## (FUTURE) chan.zip file format

For ease of transmission, this script should give the ability to transfer in `.chan.zip` format. All this does is zip up the folder, just like an `.epub`. This will provide a universal archive format for transferring information between archives, or between anons on 4chan, which may happen a lot.

## (FUTURE) Implement useful functions from other CSS/JS mods

* Expand image in the current HTML
* SauceNao and TinEye