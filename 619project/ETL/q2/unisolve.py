#!/usr/bin/python
# -- coding: utf-8 --

import sys
import re

f = open('q2','w')
for line in sys.stdin:
    	line = line.strip()
    	if line == '': continue
	fields =  line.split('\t')
	if len(fields) < 5: continue
	tweet_id = fields[0]
	user_id = fields[1]
	time = fields[2]
	text = fields[3].strip()
	score = fields[4].strip()

	utf_text = text.decode('unicode-escape','ignore')	
	enc_text = utf_text.encode('utf8')
       
	if len(time)<19: time=time[0:5]+'0'+time[5:18]
    	
        f.write(user_id + '\t' + time + '\t' + tweet_id + ':' + str(score) + ':' + enc_text + '\n')

f.close()

