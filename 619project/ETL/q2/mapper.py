#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.strip()
    if line == '': continue
    words = line.split('\t')
    if len(words) < 5: continue
    print line
