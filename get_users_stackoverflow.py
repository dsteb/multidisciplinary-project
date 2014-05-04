#!/usr/bin/python
"""
	Program Developed for the course: MultiDisciplinary Project

	The program get as a argument a String that corresponds to the username that 
	we want to looking for into StackOverflow. As a result we have a list formed
	by a tuple [user_name, user_id] which matched with the given String.

	@author: Ferran B.
"""

import urllib2
import re
import json

# Auxiliar functions

def generateURL(username):
    return 'http://stackoverflow.com/users?tab=reputation/users/filter&search=' + username + '&filter=week&tab=reputation'

def getPageSourceCode(page):
    response = urllib2.urlopen(page)
    return response.read()

"""

Structure of the parse text:

# 1. user_id_1 		2. user_name_1

# 4. user_id_2 		5. user_name_2

"""
# Main Function

def searchUser(username):
    text = getPageSourceCode(generateURL('slurm'))
    matches = re.finditer('<a href="/users/(\d+)/(\D+)">\D*</a>', text)
    final_list = []
    for match in matches:
        subtext = text[match.start():]
        total_score = re.search('total reputation: (\d+)', subtext).group(1)
        final_list.append({
            'user': match.group(2), 
            'id': match.group(1),
            'total_score': total_score
        })
    return final_list

if __name__ == '__main__':
    username = 'slurm'
    json_data = searchUser(username)
    # use dumps for pretty printing    
    print json.dumps(json_data, indent=4)
