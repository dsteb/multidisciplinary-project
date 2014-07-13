#!/usr/bin/python

import csv
import sys

writer = csv.writer(sys.stdout, delimiter='	')
for row in csv.reader(iter(sys.stdin.readline, ''), delimiter='	'):
	writer.writerow([row[4]])