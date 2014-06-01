#!/usr/bin/python

import sys
import json
import calendar
from datetime import datetime

def main():
    DATE_2000 = 946684800
    percent = 7.5
    filename = sys.argv[1]
    f = open(filename, 'r')
    json_data = json.load(f)
    answerer = json_data['answerer']
    print json.dumps(answerer, indent=4)
    ar0 = answerer["total_score"]
    norm = 0
    num = 0
    questions = json_data['questions']
    questions = sorted(questions, key=lambda question: question['datetime'])
    for question in questions:
        if not question['datetime']:
            continue
        dt = datetime.strptime(question["datetime"], '%Y-%m-%dT%H:%M:%S')
        t = (calendar.timegm(dt.utctimetuple()) - DATE_2000) / 3600 / 24
        qr = question["questioner_reputation"]
        qs = question["question_score"]
        as0 = question["answer_score"]
        interest = pow(1+percent/100, t)
        interest = t
        norm += interest
        num += (qr + qs + as0)/(num/norm + 1.0)*interest
        
        print t, qr, qs, ar0, as0, num, norm
        #print json.dumps(question, indent=4)
        
    print num/norm
if __name__ == '__main__':
    main()
