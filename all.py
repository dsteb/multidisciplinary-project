#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup
import threading
import json
import logging
import mylogging
import stackoverflow as so
import os
import sys


def open(url):
  return urllib2.urlopen(url).read()

URL = 'http://stackoverflow.com'
USE_THREADS = False 

if __name__ == '__main__':
    page = int(sys.argv[1])
    while True:
        url = '{}/users?tab=reputation&filter=all&page={}'.format(URL, page)
        print url
        text = open(url)
        soup = BeautifulSoup(text)
        user_info_blocks = soup.find_all(class_='user-info')
        for user_info in user_info_blocks:
            try:
                details = user_info.find(class_='user-details')
                url = '{}/{}'.format(URL, details.a['href'])
                username = details.a['href'].split('/')[-1]
                if os.path.isfile('stackoverflow/{}.json'.format(username)):
                    logging.info('Skip ' + username)
                    continue
                if USE_THREADS:
                    logging.info('creating thread for url: {}'.format(url))
                    t = threading.Thread(target=so.process_user, args=(url,))
                    t.start()
                else: 
                    logging.info(url)
                    so.process_user(url)
            except Exception as e:
                logging.error(e)
        page += 10

