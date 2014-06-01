#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup
import threading
import json
import logging
import stackoverflow as so
import os

logging.basicConfig(filename='root.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

def open(url):
  return urllib2.urlopen(url).read()

URL = 'http://stackoverflow.com'
USE_THREADS = False 

if __name__ == '__main__':
    url = '{}/users?tab=reputation&filter=quarter'.format(URL)
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

        
