#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup

def open(url):
  return urllib2.urlopen(url).read()

if __name__ == '__main__':
    url = 'http://stackoverflow.com/users?tab=reputation&filter=quarter'
    text = open(url)
    soup = BeautifulSoup(text)
    user_info_blocks = soup.find_all(class_='user-info')
    for user_info in user_info_blocks:
        details = user_info.find(class_='user-details')
        span = details.span.contents
        location = ''
        if span: 
           location = span[0] 
        user = {
            'href': details.a['href'],
            'name': details.a.contents[0],
            'location': location
        
        }
        print user 
