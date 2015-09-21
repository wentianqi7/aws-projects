#!/usr/bin/python
import sys
import os
import json
import re

for line in sys.stdin:

	line = line.strip()
	if line == '': continue

	data = json.loads(line)

	if 'retweeted_status' in data:
                userId =  data["user"]["id"]
                reId = data["retweeted_status"]["user"]["id"]
		print str(userId) + '\t' + str(reId)

 		

