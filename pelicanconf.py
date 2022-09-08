#!/usr/bin/env python3
from zlib import adler32

def deterministic_choice(sequence, choice_seed):
    return sequence[adler32(bytes(choice_seed, 'utf8')) % len(sequence)]

def deterministic_triple(sequence, choice_seed):
    result = []
    nonces = ['a', 'b','c','d','e','f','g','h']
    nonceIndex = 0
    while len(result) < min(len(sequence), 3):
        choice = deterministic_choice(sequence, choice_seed+nonces[nonceIndex])
        if choice not in result:
            result.append(choice)
        nonceIndex=nonceIndex+1
    return result


JINJA_FILTERS = { \
                 'pick_reccomendations': lambda array, article: deterministic_triple([i for i in array if i.title != article], article.title),\
                 'pick_subtitle': deterministic_choice\
                 }

AUTHOR = 'capu'
SITENAME = "capu's blog"
SITEURL = 'http://127.0.0.1:8000'
SITESUBTITLE = ['I\'m probably over-engineering this',\
                'You can\'t downvote me here',\
                'También en castellano, wachin',\
                'Tope (inferior) de gama',\
                'Brazing fast',\
                'Come surf Dunning-Kruger\'s crest with me',\
                'World\'s Okayest Programmer',\
                'We have nothing to lose but our OSDE 210',\
                'Alta paja agregar comentarios, mandame un mail',\
                'Cookie free! NGINX logs your IP, tho',
                'Looks just as good in w3m',\
                'Software is evil unless you can fork it',\
                'Content Warning: unsufferable hipsters',\
                'Hosted on the Other People\'s Computers ☁',\
                'Hack the planet! (it\'s a reference)',\
                'No backups. Can\'t restore. Don\'t want to either.']

PATH = 'content'

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
         ('hire me', 'http://hire.capu.tech/') )

# Social widget
LINKS = (('website home', 'http://capu.tech'), ('hire me', 'http://hire.capu.tech/'))

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'themes/capu'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelican-global-rst-include','video', 'plantuml']

# idk, this seems to be relative to the context directory
RST_GLOBAL_INCLUDES =['../globals/globals.rst']

STATIC_PATHS = ['static']
EXTRA_PATH_METADATA = {'static/favicon.ico': {'path': 'favicon.ico'},}
