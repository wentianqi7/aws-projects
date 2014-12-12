import sys
import os
import re

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

# find the most popular English article title from [filename]
def find_pop_en(filename):
    total_line = 0
    total_request = 0
    filtered_line = 0
    # key = title, value = number of access
    dict = {}

    f = open(filename, 'rU')

    # iterate the file line by line
    for line in f:
        result = line.strip().split(' ')
        prefix = result[0]
        title = result[1]
        num_access = int(result[2])

        total_line += 1
        total_request += num_access

        # save the validated title in the dictionary
        if prefix == 'en' and checkValid(title):
            dict[title] = num_access

    f.close()

    # sort the dictionary and print out the sorted result
    for key in sorted(dict, key = dict.get, reverse = True):
        print key, dict[key]
        if filtered_line == 0: max_key = key
        filtered_line += 1

    # print the result
    print 'totle line = %d\ntotle request = %d\nline after filter = %d' % (total_line, total_request, filtered_line)
    print 'the most popular article is: %s\nits view is: %d' % (max_key, dict[max_key])


# main routine
def main():
    args = sys.argv[1:]

    # input filename as argument
    if not args:
        print 'usage: filename'
        sys.exit(1)

    filename = args[0]
    find_pop_en(filename)


if __name__ == '__main__':
    main()
