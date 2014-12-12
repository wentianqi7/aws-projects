#!/usr/bin/python

import sys

hashinfo = None
former = None

for line in sys.stdin:
	line = line.strip()
	words = line.split('\t')
	if len(words) < 3: continue
	ltime = words[0]
	rank = words[1]
	hashtag = words[2]
	if ltime == former:
		hashinfo += '*'+hashtag
	else:
		if former != None: print former+'\t'+hashinfo
		former = ltime
		hashinfo = hashtag

print former+'\t'+hashinfo
