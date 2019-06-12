#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'capu'
SITENAME = "capu's blog"
SITEURL = 'http://localhost:8000'
SITESUBTITLE = 'ahre se hacia el hacker'

PATH = 'content'

TIMEZONE = 'America/Argentina/Buenos_Aires'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
SOCIAL = ( ('github', 'http://github.com/juanpcapurro'),
         ('twitter', 'http://twitter.com/cuddle_lord') )

# Social widget
# LINKS = (('You can add links in your config file', '#'), ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'themes/capu'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelican-global-rst-include']

# idk, this seems to be relative to the context directory
RST_GLOBAL_INCLUDES =['../globals/globals.rst']
