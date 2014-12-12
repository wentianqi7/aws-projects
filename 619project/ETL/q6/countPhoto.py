#!/usr/bin/python

import sys

fid = None
fcount = 0

for line in sys.stdin:
	line = line.strip()
	words = line.split('\t')
	if len(words) < 2: continue
	userid = words[0]
	photo_count = int(words[1])
	if fid == userid: fcount += photo_count
	else:
		if fid != None and fcount > 0:
			print fid + '\t' + str(fcount)
		fid = userid
		fcount = photo_count

if fcount > 0:
	print fid + '\t' + str(fcount)
