import sys

score1 = {}
score2 = {}
score3 = {}
score_total = {}

frid = None
fuid = None

for line in sys.stdin:
	line = line.strip()
	words = line.split('\t')
	if len(words) < 2: continue
	rid = str(words[0])
	uid = str(words[1])
	if uid in score1: score1[uid] += 1
	else: score1[uid] = 1
	if uid in score_total: score_total[uid] += 1
	else: score_total[uid] = 1

	if rid in score2: score2[rid] += 3
	elif rid != '0': score2[rid] = 3
	if rid in score_total: score_total[rid] += 3
	elif rid != '0': score_total[rid] = 3

	if rid == frid:
		if uid != fuid:
			score3[rid] += 10
			score_total[rid] += 10
	elif rid != '0':
		score3[rid] = 10
		if rid in score_total: score_total[rid] += 10
		else: score_total[rid] = 10
		frid = rid
		fuid = uid

for key in sorted(score_total.keys()):
	temp_score1 = 0
	temp_score2 = 0
	temp_score3 = 0
	if key in score1: temp_score1 = score1[key]
	if key in score2: temp_score2 = score2[key]
	if key in score3: temp_score3 = score3[key]
	print key + '\t' + str(score_total[key]) + '\t' + str(temp_score1) + '\t' + str(temp_score2) + '\t' + str(temp_score3) 
