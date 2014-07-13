#!/usr/bin/python

import csv
import sys
import calendar
from datetime import datetime

LAST_ID = 3600000
DATE_2000 = 946684800

'''
	Calculate dindex for user considering his all answers.
	Answers is array of dictionary elements.
	Dictionary element contains:
		questioner_id
		questioner_reputation
		question_score
		answerer_id
		answerer_reputation
		answer_score
		days_diff
'''
def dindex(user_answers):
	### HERE YOUR OWN d-index implementation
	max_value = 0
	k = 1000.
	for answer in user_answers:
		score = answer['answer_score']
		dt = answer['days_diff']
		value = k * score / dt
		if value > max_value:
			max_value = value
	return max_value

answers = []
previous_user = -1

writer = csv.writer(sys.stdout, delimiter='	')
for row in csv.reader(iter(sys.stdin.readline, ''), delimiter='	'):

	created = row[7].split('.')[0]
	created = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S')
	# days since Y2k
	created = (calendar.timegm(created.utctimetuple()) - DATE_2000) / 3600 / 24 
	answer = {
		'questioner_id': int(row[2]),
		'questioner_reputation': int(row[3]),
		'question_score': int(row[4]),
		'answerer_id': int(row[0]),
		'answerer_reputation': int(row[5]),
		'answer_score': int(row[6]),
		'days_diff': created
	}
	if answer['answerer_id'] != previous_user:
		writer.writerow([previous_user, dindex(answers)])
		previous_user = answer['answerer_id']
		answers = []

	answers.append(answer)	

writer.writerow([previous_user, dindex(answers)])
