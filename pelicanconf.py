#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import random

JINJA_FILTERS = { 'pick_reccomendations': lambda array, article: random.sample([i for i in array if i.title != article.title], min(len(array), 3)) }

AUTHOR = 'capu'
SITENAME = "capu's blog"
SITEURL = 'http://localhost:8000'
SITESUBTITLE = 'I\'m probably over-engineering this'

PATH = 'content'
STATIC_PATHS = ['static']

TIMEZONE = 'America/Argentina/Buenos_Aires'

DEFAULT_LANG = 'en'

FEED_ALL_RSS = 'feeds/all.rss.xml'
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
SOCIAL = ( ('github', 'http://github.com/juanpcapurro'),
         ('twitter', 'http://twitter.com/cuddle_lord'),
         ('hire me', 'http://hire.capu.tech/') )

# Social widget
LINKS = (('website home', 'http://capu.tech'), ('hire me', 'http://hire.capu.tech/'))

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'themes/capu'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelican-global-rst-include','video']

# idk, this seems to be relative to the context directory
RST_GLOBAL_INCLUDES =['../globals/globals.rst']

STATIC_PATHS = ['extra/favicon.ico']
EXTRA_PATH_METADATA = {'extra/favicon.ico': {'path': 'favicon.ico'},}
