#!/usr/bin/python

import sys
import re

for line in sys.stdin:
	line = line.strip()
	if line == '': continue
	fields = line.split('\t')
	print fields[0] + '\t' + fields[1]
