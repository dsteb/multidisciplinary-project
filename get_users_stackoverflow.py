#!/usr/bin/python
"""
	Program Developed for the course: MultiDisciplinary Project

	The program get as a argument a String that corresponds to the username that 
	we want to looking for into StackOverflow. As a result we have a list formed
	by a tuple {user, id, total_score} which matched with the given String.

	@author: Ferran B.
"""

import urllib2
import re
import json
import sys
from bs4 import BeautifulSoup

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
    text = getPageSourceCode(generateURL(username))
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

def get_answers_page(user, number):
    return 'http://stackoverflow.com/users/{}/{}?tab=answers&page={}'.format(user['id'], user['user'], number)

def parse_answer_url(url):
    HTTP_STACKOVERFLOW = 'http://stackoverflow.com'
    text = getPageSourceCode(url)
    soup = BeautifulSoup(text)
    accepted = soup.find_all('div', {'class': 'answered-accepted'})
    urls = []
    for div in accepted:
        rem = 'window.location.href='
        url = div['onclick']
        url = url[len(rem) + 1:]
        url = HTTP_STACKOVERFLOW + url[:-1]
        urls.append(url)
        parse_question_score(url)
    return urls

def parse_question_score(url):
    text = getPageSourceCode(url)
    soup = BeautifulSoup(text)
    votes = soup.find_all('span', {'class', 'vote-count-post'})
    if len(votes) < 2:
        return {'question': 0, 'answer': 0}
    print int(votes[0].contents[0]), int(votes[1].contents[0])

if __name__ == '__main__':
    username = sys.argv[1]
    json_data = searchUser(username)
    user = json_data[0]
    answer_url = get_answers_page(user, 1)
    parse_answer_url(answer_url)
    # use dumps for pretty printing    
    print json.dumps(json_data, indent=4)
