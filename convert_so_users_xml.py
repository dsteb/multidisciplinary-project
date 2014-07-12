#!/usr/bin/python

import csv
from mdp_util import get_int, get_string

answers = {}
LAST_ID = 3600581
with open('Users.xml') as input_file:
# with open('users.xml') as input_file:
	with open('users.csv', 'w') as csv_file:
		writer = csv.writer(csv_file, delimiter='	')
		for line in input_file:
			id = get_int(line, 'Id="')
			reputation = get_int(line, 'Reputation="')
			writer.writerow([id, reputation])
			if id:
				print 'id: {0}; {1:.2f}%'.format(id, 100 * float(id)/ LAST_ID)
		csv_file.close()
	input_file.close()