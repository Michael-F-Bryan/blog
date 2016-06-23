#!/usr/bin/env python3

AUTHOR = 'Michael F Bryan'
SITENAME = "Michael's Website"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Australia/Perth'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Categories', '/categories.html'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
        ('github', 'https://github.com/Michael-F-Bryan'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Define the theme
THEME = './theme'

# Plugins
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["tag_cloud"]
