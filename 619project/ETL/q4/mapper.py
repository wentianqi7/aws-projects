#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

for line in sys.stdin:
    line = line.strip()
    if line == '': continue
    words = line.split('\t')
    if len(words) < 4: continue
    location = words[0]
    date = words[1]
    hashs = words[2]
    tid = words[3]
    key = location+'*'+date
    pairs = hashs.strip(';').split(';')
    for pair in pairs:
        results = pair.split(':')
        index = results[0]
        nums = index[1:-1].split(',')
        num = nums[0]       
        hashtag = results[1]
        print key+'\t'+hashtag+'\t'+tid+'\t'+num
