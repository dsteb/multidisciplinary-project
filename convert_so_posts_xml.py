#!/usr/bin/python

import csv
from mdp_util import get_int, get_string

answers = {}
LAST_ID = 23452377
with open('Posts.xml') as input_file:
# with open('test.txt') as input_file:
	with open('answers.csv', 'w') as csv_file:
		writer = csv.writer(csv_file, delimiter='	')
		for line in input_file:
			id = get_int(line, 'Id="')
			answer_id = get_int(line, 'AcceptedAnswerId="')
			question_data = answers.get(id)
			if answer_id or question_data:
				score = get_int(line, 'Score="')
				user_id = get_int(line, 'OwnerUserId="')
				if question_data is not None:
					# is answer
					del answers[id]
					creation_date = get_string(line, 'CreationDate="')
					row = [id, question_data[0], question_data[1], user_id, score, creation_date]
					writer.writerow(row)
				else:
					# is question
					answers[answer_id] = [user_id, score]
			if id:
				print 'id: {0}; {1:.2f}%'.format(id, 100 * float(id)/ LAST_ID)
		csv_file.close()
	input_file.close()