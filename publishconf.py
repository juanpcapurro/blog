#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
# note to self: I disregarded the advice from the person that knowns what they are doing in the previous line,
# and used http://nginx.org/en/docs/http/ngx_http_sub_module.html to rewrite the urls in the https site
# this was done in order for the site to be available on both http and https
# future self, please note here how long it took for it to come back and kick me in the balls: 
SITEURL = 'http://blog.capu.tech'
COMMENTS_URL="https://blog.capu.tech"
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
