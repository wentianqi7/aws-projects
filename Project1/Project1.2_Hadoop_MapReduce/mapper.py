#!/usr/bin/python

import sys
import os

# special strings that page title should not start with
special_prefixes = ['Media', 'Special', 'Talk', 'User', 'User_talk', 'Project', 'Project_talk', 'File', 'File_talk', 'Mediawiki', 'Mediawiki_talk', 'Template', 'Template_talk', 'Help', 'Help_talk', 'Category', 'Category_talk', 'Portal', 'Wikipedia', 'Wikipedia_talk']

# image file extensions that should be excluded
special_extensions = ['.jpg', '.gif', '.png', '.JPG', '.GIF', '.PNG', '.txt', '.ico']

# boilerplate articles that should be excluded
special_titles = ['404_error/', 'Main_Page', 'Hypertext_Transfer_Protocol', 'Favicon.ico', 'Search']


# filter out invalid page titles
# return true if the title is valid
def checkValid(title):
    # check if the title if start with special strings
    for special_prefix in special_prefixes:
        if title.startswith(special_prefix): return False

    # check if the title start with uppercase chars
    if title[0].islower(): return False

    # check if the results refer to image files
    for special_extension in special_extensions:
        if title[-4:] == special_extension: return False

    # check if the tile is boilerplate article
    for special_title in special_titles:
        if title == special_title: return False

    return True


filename = os.environ["map_input_file"]
file_info = filename.split('-')
date = file_info[-2];

# main routine
for line in sys.stdin:
    line = line.strip()
    words = line.split(' ')
    if len(words) < 3: continue
    prefix = words[0]
    title = words[1]
    num_views = words[2]

    if prefix == 'en' and checkValid(title):
        print '%s\t%s' % (title, date+'-'+num_views)

