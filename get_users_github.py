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

# Auxiliar functions

GITHUB_URL = 'https://github.com'

def read_page(page):
    response = urllib2.urlopen(page)
    return response.read()

def process_user(username):
    url = '{}/search?q={}&type=Users'.format(GITHUB_URL, username)
    text = read_page(url)
    soup = BeautifulSoup(text)
    user_info = soup.find(class_='user-list-info')
    a = user_info.find('a')
    username = a['href'][1:]
    commits = process_days(username)
    return {'username': username, 'commits': commits}

def process_days(username):
    url = '{}/users/{}/contributions_calendar_data'.format(GITHUB_URL, username)
    days = read_page(url)
    days = json.loads(days)
    results = []
    for day in days:
        if day[1] != 0:
            dt = day[0].replace('/', '-')
            results.extend(parse_day(username, dt))
    return results

def parse_day(username, day):
    print day
    url = '{}/{}?tab=contributions&from={}'.format(GITHUB_URL, username, day)
    text = read_page(url)
    soup = BeautifulSoup(text)
    header = soup.find(class_='conversation-list-heading')
    results = []
    if header.get_text().find('commits') != -1:
        ul = soup.find(class_='simple-conversation-list')
        for a in ul.find_all('a'):
            results.extend(parse_repository(a['href']))
    return results

CACHE = Set()

def parse_repository(url):
    if url in CACHE:
        return []
    CACHE.add(url)
    url = GITHUB_URL + url
    text = read_page(url)
    soup = BeautifulSoup(text)
    commits = soup.find_all(class_='gobutton')
    results = []
    for a in commits:
        data = parse_commit(a['href'])
        results.append(data)
    return results

def parse_commit(url):
    print url
    url = GITHUB_URL + url
    text = read_page(url)
    soup = BeautifulSoup(text)
    toc = soup.find(id='toc')
    strong = toc.find('strong').find_next('strong')
    loc = strong.get_text().split(' ')[0]
    loc.replace(',', '')
    loc = int(loc)
    utc = soup.find('time')['datetime']
    utc = utc[:-6] # ignore timezone
    return {'commit': url, 'utc': utc, 'loc': loc}

if __name__ == '__main__':
    username = 'n43jl'
    result = process_user(username)
    f = open(username, 'w')
    f.write(json.dumps(result))
    f.close() 
    # use dumps for pretty printing    
