#!/usr/bin/python

import csv
import sys

users = {}
with open('users.csv') as input_file:	
	reader = csv.reader(input_file, delimiter='	')
	for row in reader:
		users[row[0]] = row[1]
	input_file.close()

writer = csv.writer(sys.stdout, delimiter='	')
for row in csv.reader(iter(sys.stdin.readline, ''), delimiter='	'):
	answer_id = int(row[0])
	question_user_id = row[1]
	question_score = row[2]
	answer_user_id = row[3]
	answer_score = row[4]
	answer_date = row[5]
	question_user_reputation = users.get(question_user_id, 0)
	answer_user_reputation = users.get(answer_user_id, 0)
	result = [answer_user_id, answer_id, question_user_id, question_user_reputation, question_score, answer_user_reputation, answer_score, answer_date]
	writer.writerow(result)