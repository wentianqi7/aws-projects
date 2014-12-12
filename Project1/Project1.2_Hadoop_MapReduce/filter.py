#!/usr/bin/env python

import sys

Films = ['The_Fault_in_Our_Stars_(film)', 'Guardians_of_the_Galaxy_(film)', 'Maleficent_(film)', 'Gravity_(film)', 'Her_(film)']

Celebrities = ['Ariana_Grande', 'Scarlett_Johansson', 'Dwayne_Johnson', 'Iggy_Azalea', 'Kurt_Russell']

Other_Special = ['Google', 'Amazon.com', 'Dawn_of_the_Planet_of_the_Apes']

total_line = 0
most_pop = None
max_view = 0
series_rank = {}

for line in sys.stdin:
    line = line.strip()
    if line == '': continue
    info = line.split('\t')
    if len(info) < 3: continue
    total_line = total_line + 1
    month_view = int(info[0])
    title = info[1]
    del info[0:2]

    if month_view > max_view:
        max_view = month_view
        most_pop = title

    for tv_series in TV_series:
        if title == tv_series: series_rank[title] = month_view

    for celebrity in Celebrities:
        if title == celebrity: print line

    for special_title in Other_Special:
        if title == special_title: print line

for key in sorted(series_rank, key = series_rank.get, reverse = True):
    print key, series_rank[key]

print 'totle line: ' + str(total_line)
print 'most popular title: %s\ttotal month view: %s' % (most_pop, str(max_view))
