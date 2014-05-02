
"""
	Program Developed for the course: MultiDisciplinary Project

	The program get as a argument a String that corresponds to the username that 
	we want to looking for into StackOverflow. As a result we have a list formed
	by a tuple [user_name, user_id] which matched with the given String.

	@author: Ferran B.
"""

import urllib2
import re

# Auxiliar functions

def generateURL(username):
	return 'http://stackoverflow.com/users?tab=reputation/users/filter&search='+username+'&filter=week&tab=reputation'

def getPageSourceCode(page):
	response = urllib2.urlopen(page)
	return response.read()

"""

Structure of the parse text:

# 1. user_id_1 		2. user_name_1

# 4. user_id_2 		5. user_name_2

"""

# aaaakbbbb

def parse(text, part1, part2):
	li = re.split(part1, text)
	another = re.split(part2, li[1])
	return another[0]

# Main Function

def searchUsername(username):
	text = getPageSourceCode(generateURL('slurm'))
	lis = re.split('<a href="/users/(\d+)/(\D+)"><div>',text)
	final_list = []
	for i in range(1, len(lis), 3):
		# ll = re.split('total reputation: (/d+)',lis[i+2])
		#print lis[i+2]
		total_score = re.search('total reputation: (\d+)', lis[i+2]).group(1)
		final_list.append ({'user':lis[i+1], 'id':lis[i], 'total_score': total_score})
		#print ll[1]

	return final_list

"""

TEST SAMPLE

"""

# Name of the user we want to search
user_search = 'slurms'

print searchUsername(user_search)
