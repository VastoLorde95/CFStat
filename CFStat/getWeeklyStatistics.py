#!/usr/bin/python

from getSubmissions import *
from datetime import datetime
from tabulate import tabulate
from global_params import *

'''
Using the submissions list generated from the previous function, this generates a table for each week between start_year to end_year with statistics like % of WAs etc. Note: Week no is as per the ISO Calendar
'''
def getWeeklyStatistics(user, mx, aggregate = False):
    submissions = getSubmissions(user, mx)
    weeks = {}
    
    # Create a weekly statistics table for each week between start_year to end_year
    for j in xrange(start_year, end_year+1):
        for i in xrange(1,54):
            weeks[(i,j)] = {'OK':                     0,
                            'WRONG_ANSWER':           0,
                            'CHALLENGED' :            0, 
                            'TIME_LIMIT_EXCEEDED' :   0,
                            'MEMORY_LIMIT_EXCEEDED' : 0,
                            'COMPILATION_ERROR' :     0,
                            'RUNTIME_ERROR' :         0,
                            'SKIPPED' :               0,
                            }
    
    mnw, mxw, mny, mxy = 54, 0, end_year, start_year
    
    for row in submissions:
        yr         = row[0].isocalendar()[0]
        weekno     = row[0].isocalendar()[1]
        weekday    = row[0].isocalendar()[2]
        
        mnw, mxw = min(mnw, weekno), max(mxw, weekno)
        mny, mxy = min(mny, yr), max(mxy, yr)

        try:
            weeks[(weekno,yr)][row[2]] += 1
        except Exception as err:
            print 'KEYERROR', row[2]
            print err
            

    for j in xrange(mny, mxy+1):
        for i in xrange(mnw, mxw+1):
            total = 0
            for key in weeks[(i,j)]: total += weeks[(i,j)][key]
        
            if total == 0:
                print 'No submissions in week', i, j 
                continue
        
            # Compute Statistics for each week
            table = []
            for key in weeks[(i,j)]:
                table.append([key, weeks[(i,j)][key], str(100 * weeks[(i,j)][key] / total) + '%'])
            
            print 'Week', i, j
            print
            print tabulate(table, headers = ["Verdict", "Count", "%"])
            print
    
    # aggregate statistics is the table of your overall statistics on CF
    if aggregate:
        aggr = {'OK':                     0,
                'WRONG_ANSWER':           0,
                'CHALLENGED' :            0, 
                'TIME_LIMIT_EXCEEDED' :   0,
                'MEMORY_LIMIT_EXCEEDED' : 0,
                'COMPILATION_ERROR' :     0,
                'RUNTIME_ERROR' :         0,
                'SKIPPED' :               0,
                }
        
        total = len(submissions) * 1.0
        for j in xrange(mny, mxy+1):
            for i in xrange(mnw, mxw+1):
                for key in weeks[(i,j)]:
                    try:
                        aggr[key] += weeks[(i,j)][key]
                    except Exception as err:
                        print 'KEYERROR', key
                        print err
    
        print                
        print 'Your overall performance: submissions made:', total
        print
        
        table = []
        for key in aggr:
            table.append([key, aggr[key], str(100 * aggr[key] / total) + '%'])
        print tabulate(table, headers = ["Verdict", "Count", "%"])
        print
