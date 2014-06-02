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
import logging
from concurrent import futures
from futures import ThreadPoolExecutor
import mylogging

THREADS = 6
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


def process_page(urls, page):
    i = 0
    l = len(urls)
    questions = []
    for url in urls:
        i += 1
        logging.info('page {}: {}/{} {}'.format(page, i, l, url))
        parsed_question = parse_question_score(url)
        if parsed_question:
            questions.append(parsed_question)
    return questions
    
def process_user(url):
    try: 
        user = user_data(url)
        result = {}
        result['answerer'] = user
        result['questions'] = []
        page = 1
        executor = ThreadPoolExecutor(max_workers=THREADS)
        futures = []
        while True:
            answer_url = '{}?tab=answers&page={}'.format(url, page)
            urls = parse_answer_url(answer_url)
            if len(urls) > 0:
                logging.info('Adding page in thread pool: {}'.format(page))
                futures.append(executor.submit(process_page, urls, page))
            else:
                break
            page += 1
        
        for future in futures:
            result['questions'].extend(future.result())
        # use dumps for pretty printing
        username = url.split('/')[-1]
        f = open('stackoverflow/{}.json'.format(username), 'w')
        f.write(json.dumps(result, indent=4))
        f.close()
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    process_user(sys.argv[1])
