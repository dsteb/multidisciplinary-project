#!/usr/bin/python

def get_string(line, template):
	result = line.split(template)
	if len(result) is not 1:
		return result[1].split('"')[0]
	return ''

def get_int(line, template):
	s = get_string(line, template).strip()
	return int(s) if s else 0 