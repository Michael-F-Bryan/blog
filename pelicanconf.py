#!/usr/bin/env python3

AUTHOR = 'Michael F Bryan'
SITENAME = "Michael's Website"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Australia/Perth'

DEFAULT_LANG = 'en'
TYPOGRIFY = True
MD_EXTENSIONS = ["codehilite(css_class=highlight)", "extra", "toc"]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

TAGS_URL = 'tags.html'
CATEGORIES_URL = 'categories.html'

ARTICLE_PATHS = ['blog']

# Sidebar stuff
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = True

# Blogroll
LINKS = [
        ('Python.org', 'http://python.org/'),
        ('Jinja2', 'http://jinja.pocoo.org/'),
]

# Social widget
SOCIAL = [
        ('github', 'https://github.com/Michael-F-Bryan')
]

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Define the theme
THEME = './theme'

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['tag_cloud', 'gzip_cache']

# Tag-Cloud plugin configuration
TAG_CLOUD_BADGE = True
TAG_CLOUD_MAX_ITEMS = 8
TAG_CLOUD_SORTING = 'random'
DISPLAY_TAGS_INLINE = False
