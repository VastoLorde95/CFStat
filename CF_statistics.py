from bs4 import BeautifulSoup
import requests
from datetime import datetime
from tabulate import tabulate

''' Start Code '''

start_year = 2014
end_year   = 2016

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
        
def getWeeklyStatistics(user, mx, aggregate = False):
    submissions = getSubmissions(user, mx)
    weeks = {}
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
        
            table = []
            for key in weeks[(i,j)]:
                table.append([key, weeks[(i,j)][key], str(100 * weeks[(i,j)][key] / total) + '%'])
            
            print 'Week', i, j
            print
            print tabulate(table, headers = ["Verdict", "Count", "%"])
            print
            
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


'''
    Make changes below
'''
if __name__ == '__main__':
    #getSubmissions('VastoLorde95', 1, True)
    #getWeeklyStatistics('VastoLorde95', 1, True)
    #compareUsers('VastoLorde95', 55, 'tourist', 28, False)



