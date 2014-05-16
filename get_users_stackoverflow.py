#!/usr/bin/python
"""
	Program Developed for the course: MultiDisciplinary Project

	The program get as a argument a String that corresponds to the username that 
	we want to looking for into StackOverflow. As a result we have a list formed
	by a tuple {user, id, total_score} which matched with the given String.

	@author: Ferran B.
"""

import urllib
import urllib2
import re
import json
import sys
import calendar
from datetime import datetime
from bs4 import BeautifulSoup

# Auxiliar functions

def generateURL(username):
    username = urllib.quote(username)
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

def searchUser(username, id=None):
    text = getPageSourceCode(generateURL(username))
    text = BeautifulSoup(text)
    divs = text.find_all('div', {'class': 'user-details'})
    final_list = []
    for div in divs:
        a = div.find('a')
        username = a.contents[0]
        found_id = a['href'].split('/')[2]
        total_score = div.find('span', {'class': 'reputation-score'}).contents[0]
#    matches = re.finditer('<a href="/users/(\d+)/(\.+)">.*</a>', text)
        final_list.append({
            'user': username, 
            'id': found_id,
            'total_score': total_score
        })
    return final_list

def get_answers_page(user, number):
    username = urllib.quote(user['user'])
    return 'http://stackoverflow.com/users/{0}/{1}?tab=answers&page={2}'.format(user['id'], username, number)

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
        print json.dumps(parse_question_score(url), indent=4)
    return urls

def parse_question_score(url):
    DATE_2000 = 946684800
    text = getPageSourceCode(url)
    soup = BeautifulSoup(text)
    votes = soup.find_all('span', {'class': 'vote-count-post'})
    td_owner = soup.find('td', {'class': 'owner'})
    details = td_owner.find('div', {'class', 'user-details'})
    time = td_owner.find('div', {'class', 'user-action-time'}).span['title']
    dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%SZ')
    ut = (calendar.timegm(dt.utctimetuple()) - DATE_2000) / 3600 / 24
    
    print ut, time
    splits = details.a['href'].split('/')
    id = int(splits[-2])
    questioner = searchUser(details.a.contents[0], id)[0]
    if len(votes) < 2:
        return {'question': 0, 'answer': 0}
    return {
        'question_score': int(votes[0].contents[0]),
        'questioner_reputation': questioner['total_score'],
        'answer_score': int(votes[1].contents[0])
    }	

if __name__ == '__main__':
    username = sys.argv[1]
    json_data = searchUser(username)
    user = json_data[0]
    i = 1
    while True:
        answer_url = get_answers_page(user, i)
        urls = parse_answer_url(answer_url)
        i = i + 1
        if len(urls) == 0:
            break;
    # use dumps for pretty printing    
    # print json.dumps(json_data, indent=4)
