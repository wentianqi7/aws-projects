import sys

for line in sys.stdin:
	line = line.strip()
	words = line.split('\t')
	if len(words) < 4: continue
	tweet_id = words[0]
	user_id = words[1]
	tweeted_id = words[2]
	print words[2] + '\t' + words[1]
