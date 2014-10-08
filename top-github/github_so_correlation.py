#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
import json
import codecs
import urllib2
import urllib
import httplib2
import contextlib
import re, urlparse
import os

def get_page(url):
	text = ''
	with contextlib.closing(urllib.urlopen(url)) as opened:
		text = opened.read()
	return text

def username_format(username):
	formatted = username.replace(' ', '+').encode('UTF-8')
	return formatted

def parse_user_details(text):
	soup = BeautifulSoup(text)
	divs = soup.findAll('div', {'class': 'user-details'})
	so_users = []
	for div in divs:
		user_url = div.a['href']
		username = div.a.get_text()
		so_users.append((user_url, username))
	soup.decompose()
	return so_users


users_file = codecs.open('github-users-stats.json', encoding='utf-8')
data = json.load(users_file)
unique = 0
ambiguous = 0
i = -1

users = []
for user in data:
	i += 1
	result_file = 'git-so/{}'.format(user['login'])
	if os.path.isfile(result_file):
		continue
	url = 'http://stackoverflow.com/users?&search={}'.format(user['login'])
	print url,
	text = get_page(url)
	so_users = parse_user_details(text)
	
	if len(so_users) == 0:
		url = 'http://stackoverflow.com/users?&search={}'.format(username_format(user['name']))
		print url,
		text = get_page(url)
		so_users = parse_user_details(text)
		
	
	print '{0:.2f}%'.format(i * 100. / len(data))
	result = {
		'login': user['login'],
		'username': user['name'],
		'so_users': so_users
	}
	users.append(result)
	output = open(result_file, 'w+')
	output.write(json.dumps(result, indent=4))
	output.close()

# print 'All: {}; Unique: {}; Ambiguous: {}'.format(len(data), unique, ambiguous)

print 'Success'