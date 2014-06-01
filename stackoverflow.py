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
import threading

# Auxiliar functions

def read_page(page):
    response = urllib2.urlopen(page)
    return response.read()

"""

Structure of the parse text:

# 1. user_id_1 		2. user_name_1

# 4. user_id_2 		5. user_name_2

"""
# Main Function

def user_data(username, id=None):
    username = urllib.quote(username)
    url = 'http://stackoverflow.com/users?tab=reputation/users/filter&search={}&filter=all&tab=reputation'.format(username)
    text = read_page(url)
    text = BeautifulSoup(text)
    divs = text.find_all('div', {'class': 'user-details'})
    user_data = None
    for div in divs:
        a = div.find('a')
        username = a.contents[0]
        found_id = int(a['href'].split('/')[2])
        span = div.find('span', {'class': 'reputation-score'})
        del_string = 'reputation score '
        total_score = span['title'][len(del_string):]
        if total_score == '':
            total_score = span.contents[0].replace(',', '')
        if id is not None:
            if id == found_id:
                return {
                    'user': username,
                    'id': found_id,
                    'total_score': int(total_score)
                }   
        else:            
            return {
                'user': username, 
                'id': found_id,
                'total_score': int(total_score)
            }
    return None

def get_answers_page(user, number):
    username = urllib.quote(user['user'])
    return 'http://stackoverflow.com/users/{0}/{1}?tab=answers&page={2}'.format(user['id'], username, number)

def parse_answer_url(url):
    HTTP_STACKOVERFLOW = 'http://stackoverflow.com'
    text = read_page(url)
    soup = BeautifulSoup(text)
    accepted = soup.find_all('div', {'class': 'answered-accepted'})
    urls = []
    for div in accepted:
        rem = 'window.location.href='
        url = div['onclick']
        url = url[len(rem) + 1:]
        url = HTTP_STACKOVERFLOW + url[:-1]
        urls.append(url)
    return urls

def parse_question_score(url):
    EMPTY = {'question_score': 0, 'answer_score': 0, 'datetime': '', 'questioner_reputation': 0}
    text = read_page(url)
    soup = BeautifulSoup(text)
    votes = soup.find_all('span', {'class': 'vote-count-post'})
    td_owner = soup.find('td', {'class': 'owner'})
    if td_owner is None:
        return EMPTY
    details = td_owner.find('div', {'class', 'user-details'})
    time = td_owner.find('div', {'class', 'user-action-time'}).span['title']
    dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%SZ')
   
    if details.a is None:
        return EMPTY
    splits = details.a['href'].split('/')
    id = int(splits[-2])
    questioner = user_data(details.a.contents[0], id)
    if len(votes) < 2 or questioner is None:
        return EMPTY
    return {
        'questioner_id': id,
        'question_score': int(votes[0].contents[0]),
        'questioner_reputation': questioner['total_score'],
        'answer_score': int(votes[1].contents[0]),
        'datetime': dt.strftime('%Y-%m-%dT%H:%M:%S')
    }	


lock = threading.Lock()
def process_page(urls, questions):
    for url in urls:
        print '  {}'.format(url)
        parsed_question = parse_question_score(url)
        lock.acquire()
        questions.append(parsed_question)
        lock.release()
    
def process_user(username):
    user = user_data(username)
    result = {}
    result['answerer'] = user
    result['questions'] = []
    page = 1
    threads = []
    while True:
        answer_url = get_answers_page(user, page)
        urls = parse_answer_url(answer_url)
        if len(urls) > 0:
            print "Thread {} started for page {}".format(len(threads), page)
            t = threading.Thread(target=process_page, args=(urls, result['questions']))
            t.start()
            threads.append(t)
        else:
            break
        page += 1
     
    for t in threads:
        t.join()
    # use dumps for pretty printing
    f = open('stackoverflow/{}.json'.format(username), 'w')
    f.write(json.dumps(result, indent=4))
    f.close()


if __name__ == '__main__':
    process_user(sys.argv[1]) 
