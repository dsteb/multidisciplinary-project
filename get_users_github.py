#!/usr/bin/python
"""
	Program Developed for the course: MultiDisciplinary Project

	The program get as a argument a String that corresponds to the username that 
	we want to looking for into GitHub. As a result we have a list formed
	by a tuple {name, url} which matched with the given String.

	@author: Ferran B.
"""

import urllib2
import re
import json

# Auxiliar functions

GITHUB_URL = 'https://github.com/'

def generateURL(username):
    return 'https://github.com/search?q=' + username + '&ref=cmdform&type=Users'

def getPageSourceCode(page):
    response = urllib2.urlopen(page)
    return response.read()

def searchUser(username):
    text = getPageSourceCode(generateURL(username))
    matches = re.findall('<a href="/(\D+)" class="gravatar">', text)
    final_list = []
    for match in matches:
        final_list.append({
            'user': match,
            'url': GITHUB_URL + match
        })
    return final_list

if __name__ == '__main__':
    username = 'slurm'
    json_data = searchUser(username)
    # use dumps for pretty printing    
    print json.dumps(json_data, indent=4)
