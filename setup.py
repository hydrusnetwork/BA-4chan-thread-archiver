#!/usr/bin/env python
# coding: utf-8

import os
import sys

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist upload')
	sys.exit()

setup(
		name             = '4chandownloader',
		version          = '0.2',
		description      = '4chan thread downloader',
		long_description = open('README.rst').read(), 
		license          = open('LICENSE').read(),
		author           = 'Socketubs',
		author_email     = 'geoffrey@lehee.name',
		url              = 'https://github.com/Socketubs/4chandownloader',
		keywords         = '4chan downloader images',
		scripts          = ['4chandownloader'],
		install_requires = ['requests==0.14.0', 'docopt==0.5.0'],
		classifiers      = (
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7')
)
