#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

former = None
rank = 1

for line in sys.stdin:
    line = line.strip()
    if line == '': continue
    words = line.split('\t')
    key = words[0]
    hashtag = words[4]
    if key == former:
        rank += 1
    else:
        rank = 1
        former = key

    print key + '\t' + str(rank) + '\t' + hashtag
