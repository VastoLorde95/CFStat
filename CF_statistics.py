from bs4 import BeautifulSoup
import requests

from datetime import datetime
from tabulate import tabulate

start_year = 2014
end_year = 2016

def getSubmissions(user, page_mx, print_flag = Flag):
 base_url = 'http://codeforces.com/submissions/' + user + '/page/'
 page_no = 1
 submissions = []

 while page_no <= page_mx:
  try:
   r = requests.get(base_url + str(page_no))
  except:
   print 'Something went wrong'
   break

  data = r.text
  soup = BeautifulSoup(data, 'lxml')
 
  tablerows = soup.find_all('tr')
  for tr in tablerows:
   if tr.get("data-submission-id") == None: continue
  
   row_data =  tr.find_all('td')
  
   day   = row_data[1].string.strip()
   problem_url = row_data[3].a.get('href')
   verdict  = row_data[5].span.get('submissionverdict')

   date_object = datetime.strptime(day, '%Y-%m-%d %H:%M:%S')
  
   submissions.append((date_object, problem_url, verdict))
   
  page_no += 1

 if print_flag: 
  print 'Fetched', page_no-1, 'pages'
  print 'You have made', len(submissions), 'submissions'

  for row in submissions:
   print row[0], row[1], row[2]
 
 return submissions
  
def getWeeklyStatistics(submissions, aggregate = False):
 weeks = {}
 for j in xrange(start_year, end_year+1):
  for i in xrange(1,54):
   weeks[(i,j)] = {'OK': 0,
       'WRONG_ANSWER': 0,
       'CHALLENGED' : 0, 
       'TIME_LIMIT_EXCEEDED' : 0,
       'MEMORY_LIMIT_EXCEEDED' : 0,
       'COMPILATION_ERROR' : 0,
       'RUNTIME_ERROR' : 0,
       'SKIPPED' : 0,
       }
 
 mnw, mxw = 54, 0
 mny, mxy = end_year, start_year
 
 
 for row in submissions:
  yr   = row[0].isocalendar()[0]
  weekno  = row[0].isocalendar()[1]
  weekday = row[0].isocalendar()[2]
  
  mnw, mxw = min(mnw, weekno), max(mxw, weekno)
  mny, mxy = min(mny, yr), max(mxy, yr)

  try:
   weeks[(weekno,yr)][row[2]] += 1
  except:
   print 'KEYERROR', row[2]
   

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
  aggr = {'OK': 0,
    'WRONG_ANSWER': 0,
    'CHALLENGED' : 0, 
    'TIME_LIMIT_EXCEEDED' : 0,
    'MEMORY_LIMIT_EXCEEDED' : 0,
    'COMPILATION_ERROR' : 0,
    'RUNTIME_ERROR' : 0,
    'SKIPPED' : 0,
    }
  
  total = len(submissions) * 1.0
  for j in xrange(mny, mxy+1):
   for i in xrange(mnw, mxw+1):
    for key in weeks[(i,j)]:
     try:
      aggr[key] += weeks[(i,j)][key]
     except:
      print 'KEYERROR', key
 
  print    
  print 'Your overall performance: submissions made:', total
  print
  table = []
  for key in aggr:
   table.append([key, aggr[key], str(100 * aggr[key] / total) + '%'])
  print tabulate(table, headers = ["Verdict", "Count", "%"])
  print

def compareUsers(user1, submission1, user2, submission2):
 return

s = getSubmissions('VastoLorde95', 53, False)
