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
    process_days(username)    

def process_days(username):
    url = '{}/users/{}/contributions_calendar_data'.format(GITHUB_URL, username)
    days = read_page(url)
    days = json.loads(days)
    for day in days:
        if day[1] != 0:
            dt = day[0].replace('/', '-')
            parse_day(username, dt)

def parse_day(username, day):
    print day
    url = '{}/{}?tab=contributions&from={}'.format(GITHUB_URL, username, day)
    text = read_page(url)
    soup = BeautifulSoup(text)
    header = soup.find(class_='conversation-list-heading')
    if header.get_text().find('commits') != -1:
        ul = soup.find(class_='simple-conversation-list')
        for a in ul.find_all('a'):
            parse_repository(a['href'])

CACHE = Set()

def parse_repository(url):
    if url in CACHE:
        return
    print url
    CACHE.add(url)
    url = GITHUB_URL + url
    text = read_page(url)
    soup = BeautifulSoup(text)
    comits = soup.find_all(class_='gobutton')
    for a in comits:
        parse_comit(a['href'])

def parse_comit(url):
    print url
    url = GITHUB_URL + url
    text = read_page(url)
    soup = BeautifulSoup(text)
    toc = soup.find(id='toc')
    strong = toc.find('strong').find_next('strong')
    print int(strong.get_text().split(' ')[0])

if __name__ == '__main__':
    username = 'John+Resig'
    process_user(username)
    # use dumps for pretty printing    
