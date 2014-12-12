#!/usr/bin/python
import sys
import json

for line in sys.stdin:
    line = line.strip()
    if line == '': continue
    data = json.loads(line)
    retweeted_id = 0
    photo_num = 0
    tweet_id = data['id']
    if 'retweeted_status' in data:
        retweeted_id = data['retweeted_status']['user']['id']
    if 'media' in data['entities']:
        for media in data['entities']['media']:
            if media['type'] == 'photo': photo_num += 1
    user_id = data['user']['id']
    print str(tweet_id) + '\t' + str(user_id) + '\t' + str(retweeted_id) + '\t' + str(photo_num)
