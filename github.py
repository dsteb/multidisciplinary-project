#!/usr/bin/python
"""
	Program Developed for the course: MultiDisciplinary Project

	The program get as a argument a String that corresponds to the username that 
	we want to looking for into GitHub. As a result we have a list formed
	by a tuple {name, url} which matched with the given String.

	@author: Ferran B.
"""
import urllib
import urllib2
import time
from time import mktime
import datetime as dtpackage
from datetime import datetime
import re
import json
from sets import Set
from bs4 import BeautifulSoup
import sys
import os
from concurrent import futures
from futures import ThreadPoolExecutor
import contextlib
import codecs

# Auxiliar functions

THREADS = 10
GITHUB_URL = 'https://github.com'

def read_page(page):
    text = ''
    print page
    with contextlib.closing(urllib2.urlopen(page)) as response:
        text = response.read()
    return text

def get_user(username):
    url = u'{}/search?q={}&type=Users'.format(GITHUB_URL, username)
    text = read_page(url)
    soup = BeautifulSoup(text)
    user_info = soup.find(class_='user-list-info')
    if not user_info:
        soup.decompose()
        return {'username': username, 'commits': []}
    a = user_info.find('a')
    username = a['href'][1:]
    soup.decompose()
    commits = process_days(username)
    if username in CACHE:
        del CACHE[username]
    return {'username': username, 'commits': commits}

def process_days(username):
    url = u'{}/users/{}/contributions_calendar_data'.format(GITHUB_URL, username)
    days = read_page(url)
    days = json.loads(days)
    results = []
    for day in days:
        if day[1] != 0:
            dt = day[0].replace('/', '-')
            results.extend(parse_day(username, dt))
    return results

def parse_day(username, day):
    print u"{}: day={}".format(username, day)
    url = u'{}/{}?tab=contributions&from={}'.format(GITHUB_URL, username, day)
    text = read_page(url)
    soup = BeautifulSoup(text)
    header = soup.find(class_='conversation-list-heading')
    urls = []
    if header.get_text().find('commits') != -1:
        ul = soup.find(class_='simple-conversation-list')
        for a in ul.find_all('a'):
            urls.append(a['href'])
    soup.decompose()
    results = []
    for url in urls:
        results.extend(parse_repository(username, url))
    return results

CACHE = {}

def parse_repository(username, url):
    user_cache = CACHE.get(username)
    if not user_cache:
        user_cache = Set()
        CACHE[username] = user_cache
    if url in user_cache:
        return []
    user_cache.add(url)
    url = GITHUB_URL + url
    text = read_page(url)
    soup = BeautifulSoup(text)
    commits = soup.find_all(class_='gobutton')
    urls = []
    for a in commits:
        urls.append(a['href'])
    soup.decompose()
    results = []
    for url in urls:
        data = parse_commit(username, url)
        results.append(data)
    return results

def parse_commit(username, url):
    print u"{}: {}".format(username, url)
    url = GITHUB_URL + url
    text = read_page(url)
    soup = BeautifulSoup(text)
    toc = soup.find(id='toc')
    strong = toc.find('strong').find_next('strong')
    loc = strong.get_text().split(' ')[0]
    loc = loc.replace(',', '')
    loc = int(loc)
    utc = soup.find('time')['datetime']
    utc = utc[:-6] # ignore timezone
    soup.decompose()
    return {'commit': url, 'utc': utc, 'loc': loc}

def process_user(username): 
    print u'creating thread for user: {}'.format(username)
    result = get_user(username)
    f = open('github/{}.json'.format(username), 'w')
    f.write(json.dumps(result, indent=4))
    f.close()

if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=THREADS)
    for subdirs, dirs, files in os.walk('stackoverflow/'):
        for filename in files:
            username = filename[:-5]
            if os.path.isfile('github/{}'.format(filename)):
                print u"skip {}".format(username)
            else:
                f = codecs.open('stackoverflow/{}'.format(filename), 'r', 'utf-8')
                data = json.load(f)
                f.close()
                username = data['answerer']['name'].replace(' ', '+')
                print u"put in thread pool user '{}'".format(username)
                # executor.submit(process_user, username)
                process_user(username)
    executor.shutdown(wait=True)
