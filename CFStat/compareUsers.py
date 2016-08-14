#!/usr/bin/python

from getSubmissions import *
from datetime import datetime
from tabulate import tabulate
from global_params import *

'''
Using the first mx1 submissions of user1 and first mx2 pages of user2, this function prints a list of all problems solved by user1 but not by user2
'''
def compareUsers(user1, mx1, user2, mx2):
    submission1 = getSubmissions(user1, mx1)
    submission2 = getSubmissions(user2, mx2)
    
    solvedProblems1 = set()
    solvedProblems2 = set()
    
    for row in submission1:
        if row[2] == 'OK': solvedProblems1.add(row[1])
    for row in submission2:
        if row[2] == 'OK': solvedProblems2.add(row[1])
    
    diff = solvedProblems1.difference(solvedProblems2)
    
    lst = [key for key in diff]
    lst.sort()
    
    print user1, "Solved", len(solvedProblems1), "problems"
    print user2, "Solved", len(solvedProblems2), "problems"
    
    print 'The problems solved by', user1, 'but not by', user2, 'are:'
    for key in lst:
        print key
