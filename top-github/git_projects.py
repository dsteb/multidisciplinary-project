#!/usr/bin/python

import os
import json
import urllib2
import shutil

GITHUB_AUTH_TOKEN = 'bc883c945fc317d8af7fc8f886d665fe1cc7f819'

def get_all_repositories():

	REPOSITORY_FILENAME = 'repositories.json'
	users_file = open('github-users-stats.json')

	last_user = None
	if os.path.isfile(REPOSITORY_FILENAME):
		repos_file = open(REPOSITORY_FILENAME, 'r+')
		tmp = open(REPOSITORY_FILENAME + '.tmp', 'w+')
		i = 0

		for line in repos_file:
			line = line.replace('][', ',')
			if i != 0 and line[0] == ']':
				continue
			elif i != 0 and line[0] == '[':
				line = ',' + line[1:]
			i += 1
			tmp.write(line)
		tmp.write(']')
		repos_file.close()
		tmp.close()
		os.remove(REPOSITORY_FILENAME)
		shutil.copyfile(REPOSITORY_FILENAME + '.tmp', REPOSITORY_FILENAME)
		repos_file = open(REPOSITORY_FILENAME, 'r+')
		repos = json.load(repos_file)
		last_user = repos[len(repos) - 1]['owner']['login']
	else:
		repos_file = open(REPOSITORY_FILENAME, 'a+')

	top_users = json.load(users_file)
	i = 0
	l = len(top_users)
	start = False
	for user in top_users:
		i += 1
		if not start:
			if last_user == user['login']:
				start = True
			print last_user, user['login'], 'skip...'
			continue
		else:
			url = 'https://api.github.com/users/{}/repos?per_page=100&access_token={}'.format(user['login'], GITHUB_AUTH_TOKEN)
			data = json.loads(urllib2.urlopen(url).read())
			repos_file.write(json.dumps(data, indent=4))
			print "{0:.2f}%".format(i * 100. / l)
			
get_all_repositories()