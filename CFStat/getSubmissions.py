#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
from datetime import datetime

'''
Generates a list of all submissions from the first page_mx number of pages made by user and prints this list if print_flag = True. Your submissions will be pushed into a list of 3-tuples: time-stamp of submission, problem code and verdict
'''
def getSubmissions(user, page_mx, print_flag = False):
    base_url = 'http://codeforces.com/submissions/' + user + '/page/'
    page_no = 1
    submissions = []

    while page_no <= page_mx:
        try:
            r = requests.get(base_url + str(page_no))
        except Exception as err:
            print err
            break

        data = r.text
        soup = BeautifulSoup(data, 'lxml')
        
        # All submissions are in tablerows of HTML
        tablerows = soup.find_all('tr')
        for tr in tablerows:
            if tr.get("data-submission-id") == None: continue
        
            row_data =  tr.find_all('td')
        
            day         = row_data[1].string.strip()
            problem_url = row_data[3].a.get('href')
            verdict     = row_data[5].span.get('submissionverdict')

            date_object = datetime.strptime(day, '%Y-%m-%d %H:%M:%S')
        
            submissions.append((date_object, problem_url, verdict))
            
        page_no += 1

    if print_flag:    
        print 'Fetched', page_no-1, 'pages'
        print 'You have made', len(submissions), 'submissions'

        for row in submissions: print row[0], row[1], row[2]
    
    return submissions

