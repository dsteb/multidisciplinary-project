#!/usr/bin/python
"""
	Program Developed for the course: MultiDisciplinary Project

	@author: Ferran B.
"""

import urllib
import urllib2
import re
import json
import sys
from datetime import datetime
from bs4 import BeautifulSoup
import threading

USE_THREADS = True
STACKOVERFLOW_URL = 'http://stackoverflow.com'
# Auxiliar functions

def read_page(page):
    response = urllib2.urlopen(page)
    return response.read()

def user_data(url):
    soup = BeautifulSoup(read_page(url))
    reputation = int(soup.find(class_='reputation').a.contents[0].replace(',', ''))
    name = soup.find(id='user-displayname').contents[0]
    address_div= soup.find(class_='label adr').contents
    address = ''
    if address_div:
        address = address_div[0]
    return {
        'href': url,
        'name': name,
        'reputation': reputation,
        'address': address
    }

def parse_answer_url(url):
    text = read_page(url)
    soup = BeautifulSoup(text)
    accepted = soup.find_all('div', {'class': 'answered-accepted'})
    urls = []
    for div in accepted:
        rem = 'window.location.href='
        url = div['onclick']
        url = url[len(rem) + 1:]
        url = STACKOVERFLOW_URL + url[:-1]
        urls.append(url)
    return urls

def parse_question_score(url):
    text = read_page(url)
    soup = BeautifulSoup(text)
    votes = soup.find_all('span', {'class': 'vote-count-post'})
    td_owner = soup.find('td', {'class': 'owner'})
    if not td_owner:
        return
    details = td_owner.find('div', {'class', 'user-details'})
    time = td_owner.find('div', {'class', 'user-action-time'}).span['title']
    dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%SZ')
   
    if not details.a:
        return
    questioner = user_data('{}/{}'.format(STACKOVERFLOW_URL, details.a['href']))
    if len(votes) < 2 or not questioner:
        return
    return {
        'questioner': questioner,
        'question_votes': int(votes[0].contents[0]),
        'answer_votes': int(votes[1].contents[0]),
        'datetime': dt.strftime('%Y-%m-%dT%H:%M:%S')
    }	


lock = threading.Lock()
def process_page(urls, questions):
    for url in urls:
        print '  {}'.format(url)
        parsed_question = parse_question_score(url)
        if parsed_question:
            lock.acquire()
            questions.append(parsed_question)
            lock.release()
    
def process_user(url):
    user = user_data(url)
    result = {}
    result['answerer'] = user
    result['questions'] = []
    page = 1
    threads = []
    while True:
        answer_url = '{}?tab=answers&page={}'.format(url, page)
        urls = parse_answer_url(answer_url)
        if len(urls) > 0:
            if USE_THREADS:
                print "Thread {} started for page {}".format(len(threads), page)
                t = threading.Thread(target=process_page, args=(urls, result['questions']))
                t.start()
                threads.append(t)
            else:
                process_page(urls, result['questions'])
        else:
            break
        page += 1
     
    for t in threads:
        t.join()
    # use dumps for pretty printing
    username = url.split('/')[-1]
    f = open('stackoverflow/{}.json'.format(username), 'w')
    f.write(json.dumps(result, indent=4))
    f.close()


if __name__ == '__main__':
    process_user(sys.argv[1])
