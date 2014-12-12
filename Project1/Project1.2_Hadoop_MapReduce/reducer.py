#!/usr/bin/python

import sys

current_title = None
title = None
date = None
current_month_count = 0
date_view = {}

for line in sys.stdin:
    line = line.strip()
    if line == '': continue
    # line: title+'\t'+date-count
    title, info = line.split('\t')
    date_and_count = info.split('-')
    date = date_and_count[0]
    count = int(date_and_count[1])

    if current_title == title:
        current_month_count += count
        if date in date_view:
            date_view[date] += count
        else: date_view[date] = count
    else:
        # print previous title info if views greater than 100000
        if current_title and current_month_count > 100000:
            date_info = ''
            for key in sorted(date_view.keys()):
                if date_info != '': date_info += '\t'
                date_info += '%s:%s' % (key, str(date_view[key]))

            print '%s\t%s\t%s' % (str(current_month_count), current_title, date_info)

        # reset info for new title
        current_month_count = count
        current_title = title
        date_view.clear()
        date_view[date] = count

# check the last line
if current_title == title and current_month_count > 100000:
    date_info = ''
    for key in sorted(date_view.keys()):
        if date_info != '': date_info += '\t'
        date_info += '%s:%s' % (key, str(date_view[key]))

    print '%s\t%s\t%s' % (str(current_month_count), current_title, date_info)

