#!/usr/bin/python

import sys

sumall = 0.
n = 0
max_value = -1
for row in iter(sys.stdin.readline, ''):
	value = int(row)
	if value > 0:
		if value > max_value:
			max_value = value
		if sumall > 9340280:
			print sumall
		n += 1
		sumall += value
print n, sumall / n, max_value