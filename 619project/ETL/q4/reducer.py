#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

formerKey = None
formerHashtag = None

key = None
hashtag = None
htInfo = None

popularity = 0
firstId = None
firstIndex = None

for line in sys.stdin:
    line = line.strip()
    if line == '': continue
    words = line.split('\t')
    if len(words) < 4: continue
    key = words[0]
    hashtag = words[1]
    tid = words[2]
    index = words[3]
    
    if key == formerKey:
        if hashtag == formerHashtag:
            popularity += 1
            htInfo = htInfo + ',' + tid
        else:
            print key + '\t' + str(popularity) + '\t' + firstId + '\t' + firstIndex + '\t' + htInfo + ';'
            formerHashtag = hashtag
            firstId = tid
            firstIndex = index
            htInfo = hashtag + ':' + tid
            popularity = 1
    else:
        if formerKey != None:
            print formerKey + '\t' + str(popularity) + '\t' + firstId + '\t' + firstIndex + '\t' + htInfo + ';'
        formerKey = key
        formerHashtag = hashtag
        firstId = tid
        firstIndex = index
        htInfo = hashtag + ':' + tid
        popularity = 1

print key + '\t' + str(popularity) + '\t' + firstId + '\t' + firstIndex + '\t' + htInfo + ';'



