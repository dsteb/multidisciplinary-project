#!/usr/bin/python

import sys
import json

def main():
    filename = sys.argv[1]
    f = open(filename, 'r')
    json_data = json.load(f)
    answerer = json_data['answerer']
    print json.dumps(answerer, indent=4)
    for question in json_data['questions']:
        print json.dumps(question, indent=4)
        

if __name__ == '__main__':
    main()
